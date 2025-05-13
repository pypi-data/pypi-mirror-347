"""
Core engine – Roo v1.9.8 (no Flask / no CLI)
Edits 2025-05-12:
  • quoted column names supported
  • negative numbers supported
Edits 2025-05-13:
  • GROUPSUM() support (per-row ratios)
"""

import re
import pandas as pd
from fractions import Fraction
from ortools.sat.python import cp_model

# ---------- regex patterns ----------
OBJ_RE   = re.compile(r'^(MAXIMIZE|MINIMIZE|SETVALUE)\s*:\s*(.+)$', re.I)
TOL_RE   = re.compile(r'^TOLERANCE\s*:\s*([0-9.]+)$', re.I)
CONS_RE  = re.compile(r'^CONSTRAINT\s*:\s*(.+)$',                  re.I)

SUM_RE   = re.compile(r'^SUM\(\s*"?([^")]+)"?\s*\)', re.I)
COUNT_OBJ_RE = re.compile(r'^COUNT\(\s*[^)]*\)$', re.I)

NUM = r'-?[0-9.]+'

# existing
SUMSTAR_RE     = re.compile(fr'^SUM\(\s*([^)]+)\s*\*\s*([^)]+)\s*\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
SUMPROD_RE     = re.compile(fr'^SUMPRODUCT\(\s*([A-Za-z0-9_ ]+)\s*,\s*([A-Za-z0-9_ ]+)\s*\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
AGG_SIMPLE_RE  = re.compile(fr'^SUM\(([^)]+)\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
AGG_ADD_SUB_RE = re.compile(fr'^SUM\(\s*([^)]+)\)\s*([+\-])\s*SUM\(\s*([^)]+)\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
AGG_SCALE_RE   = re.compile(fr'^(?:({NUM})\s*\*\s*)?SUM\(\s*([^)]+)\)(?:\s*/\s*({NUM}))?\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
RATIO_RE       = re.compile(fr'^SUM\(\s*([^)]+)\)\s*/\s*SUM\(\s*([^)]+)\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)

COUNT_RE       = re.compile(r'^COUNT\(([^)]*?)\)\s*(<=|>=|=|<|>)\s*([0-9]+)$', re.I)
AVG_RE         = re.compile(fr'^AVG\(([^)]+)\)\s*(<=|>=|=|<|>)\s*({NUM})$',   re.I)

ITEM_RATIO_RE  = re.compile(fr'^([A-Za-z0-9_ ]+)\s*/\s*([A-Za-z0-9_ ]+)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
ITEM_ADD_SUB_RE= re.compile(fr'^([A-Za-z0-9_ ]+)\s*([+\-])\s*([A-Za-z0-9_ ]+)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
ITEM_SCALE_RE  = re.compile(fr'^(?:({NUM})\s*\*\s*)?([A-Za-z0-9_ ]+)(?:\s*/\s*({NUM}))?\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
ITEM_PROD_RE   = re.compile(fr'^([A-Za-z0-9_ ]+)\s*\*\s*([A-Za-z0-9_ ]+)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)

# ------- NEW: GROUPSUM patterns -------
GROUPSUM_RE         = re.compile(r'GROUPSUM\(\s*"?([^")]+)"?\s*\)', re.I)
ITEM_RATIO_GS_RE    = re.compile(fr'^([A-Za-z0-9_ ]+)\s*/\s*GROUPSUM\(\s*"?([^")]+)"?\s*\)\s*(<=|>=|=|<|>)\s*({NUM})$', re.I)
ITEM_RATIO_2GS_RE   = re.compile(fr'^([A-Za-z0-9_ ]+)\s*/\s*GROUPSUM\(\s*"?([^")]+)"?\s*\)\s*=\s*([A-Za-z0-9_ ]+)\s*/\s*GROUPSUM\(\s*"?([^")]+)"?\s*\)$', re.I)

COND_RE  = re.compile(fr'^\(?\s*([A-Za-z0-9_ ]+)\s*\)?\s*(<=|>=|=|<|>)\s*("?[^"]+"?|{NUM})\s*$', re.I)

# ---------- helpers ----------
def scale_to_int(series):
    k = 1
    for v in series:
        if isinstance(v, float):
            d = len(f'{v:.10f}'.rstrip("0").split('.')[-1])
            k = max(k, 10 ** min(d, 3))
    return [int(round(v * k)) for v in series], k

def clean(t):
    return ' '.join(str(t).replace('\u00A0', ' ').strip().upper().split())

# ---------- public parse() ----------
def parse(txt: str):
    ot = oe = None
    tol = None
    cons = []
    for ln in txt.strip().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        if (m := OBJ_RE.match(ln)):
            ot, oe = m.group(1).upper(), m.group(2).strip()
        elif (m := TOL_RE.match(ln)):
            tol = float(m.group(1))
        elif (m := CONS_RE.match(ln)):
            cons.append(m.group(1).strip())
        else:
            raise ValueError(f"Bad line:\n{ln}")
    if not ot:
        raise ValueError("Missing objective.")
    return ot, oe, tol, cons

# ---------- build_model ----------
def build_model(df: pd.DataFrame, ot, oe, tol, cons):
    mdl = cp_model.CpModel()
    n = len(df)
    x = [mdl.NewBoolVar(f'x{i}') for i in range(n)]
    cache = {}

    def col(c):
        c = c.strip('"')
        if c not in df.columns:
            raise ValueError(f"Column '{c}' not found.")
        if c not in cache:
            cache[c] = scale_to_int(df[c])
        return cache[c]

    # -------- NEW: GROUPSUM variable factory --------
    gsum_cache = {}
    def get_group_sum(col_name: str):
        col_name = col_name.strip('"')
        if col_name in gsum_cache:
            return gsum_cache[col_name]
        ints, sc = col(col_name)
        gvar = mdl.NewIntVar(0, sum(ints), f"GSUM_{col_name}")
        mdl.Add(gvar == sum(ints[i] * x[i] for i in range(n)))
        gsum_cache[col_name] = (gvar, sc)
        return gvar, sc
    # -------------------------------------------------

    def sum_expr(c):
        ints, _ = col(c)
        return sum(ints[i] * x[i] for i in range(n))

    cnt = sum(x)
    obj = cnt if COUNT_OBJ_RE.match(oe) else sum_expr(SUM_RE.match(oe).group(1).strip())
    (mdl.Maximize if ot == 'MAXIMIZE' else mdl.Minimize)(obj)

    def add_lin(expr, op, tgt_float):
        tgt = int(round(tgt_float))
        if op in ('<', '<='):
            return mdl.Add(expr <= tgt - (op == '<'))
        if op in ('>', '>='):
            return mdl.Add(expr >= tgt + (op == '>'))
        return mdl.Add(expr == tgt)

    # --- constraints loop ---
    for rule in cons:

        # existing patterns (unchanged) ------------------------------
        if (m := SUMSTAR_RE.match(rule)):
            A, B, op, val = m.group(1).strip(), m.group(2).strip(), m.group(3), float(m.group(4))
            intsA, scA = col(A); intsB, scB = col(B)
            lcm = scA * scB
            expr = sum(intsA[i] * intsB[i] * x[i] for i in range(n))
            add_lin(expr, op, val * lcm); continue
        if (m := SUMPROD_RE.match(rule)):
            A, B, op, val = m.group(1).strip(), m.group(2).strip(), m.group(3), float(m.group(4))
            intsA, scA = col(A); intsB, scB = col(B); lcm = scA * scB
            add_lin(sum(intsA[i] * intsB[i] * x[i] for i in range(n)), op, val * lcm); continue
        if (m := AGG_SIMPLE_RE.match(rule)):
            c, op, val = m.groups()
            add_lin(sum_expr(c.strip()), op, float(val) * col(c.strip())[1]); continue
        if (m := AGG_ADD_SUB_RE.match(rule)):
            A, sign, B, op, val = m.groups(); A, B = A.strip(), B.strip()
            exprA, scA = sum_expr(A), col(A)[1]; exprB, scB = sum_expr(B), col(B)[1]
            lcm = scA * scB
            expr = (lcm // scA) * exprA + (1 if sign == '+' else -1) * (lcm // scB) * exprB
            add_lin(expr, op, float(val) * lcm); continue
        if (m := AGG_SCALE_RE.match(rule)):
            k1, A, k2, op, val = m.groups(); A = A.strip(); val = float(val)
            expr, sc = sum_expr(A), col(A)[1]
            coef = Fraction(k1) if k1 else Fraction(1)
            if k2: coef /= Fraction(k2)
            add_lin(coef.numerator * expr, op, val * sc * coef.denominator); continue
        if (m := RATIO_RE.match(rule)):
            A, B, op, val = m.groups(); A, B, val = A.strip(), B.strip(), float(val)
            sumA, scA = sum_expr(A), col(A)[1]; sumB, scB = sum_expr(B), col(B)[1]
            d = 10 ** len(str(val).split('.')[-1]); num = int(round(val * d))
            lhs = d * scB * sumA; rhs = num * scA * sumB
            if op in ('<', '<='):  mdl.Add(lhs <= rhs - (op == '<'))
            elif op in ('>', '>='):mdl.Add(lhs >= rhs + (op == '>'))
            else:                 mdl.Add(lhs == rhs); continue
        if (m := COUNT_RE.match(rule)):
            _, op, val = m.groups(); add_lin(cnt, op, int(val)); continue
        if (m := AVG_RE.match(rule)):
            c, op, val = m.groups()
            add_lin(sum_expr(c.strip()), op, float(val) * col(c.strip())[1] * cnt); continue

        # -------- NEW: Column / GROUPSUM(Column) op constant --------
        if (m := ITEM_RATIO_GS_RE.match(rule)):
            colA, colGS, op, val = m.groups()
            colA, colGS, val = colA.strip(), colGS.strip(), float(val)
            intsA, scA = col(colA)
            gsum_var, scG = get_group_sum(colGS)
            d = 10 ** len(str(val).split('.')[-1]); num = int(round(val * d))
            for i in range(n):
                lhs = d * scG * intsA[i]
                rhs = num * scA * gsum_var
                if op in ('<', '<='):
                    mdl.Add(lhs <= rhs - (op == '<')).OnlyEnforceIf(x[i])
                elif op in ('>', '>='):
                    mdl.Add(lhs >= rhs + (op == '>')).OnlyEnforceIf(x[i])
                else:
                    mdl.Add(lhs == rhs).OnlyEnforceIf(x[i])
            continue

        # -------- NEW: ratio equality with two group sums ----------
        if (m := ITEM_RATIO_2GS_RE.match(rule)):
            colA, gs1, colB, gs2 = [g.strip() for g in m.groups()]
            intsA, scA = col(colA); g1, scG1 = get_group_sum(gs1)
            intsB, scB = col(colB); g2, scG2 = get_group_sum(gs2)
            lcm = scA * scB  # common factor for ints
            for i in range(n):
                lhs = (lcm // scA) * intsA[i] * g2 * scG2
                rhs = (lcm // scB) * intsB[i] * g1 * scG1
                mdl.Add(lhs == rhs).OnlyEnforceIf(x[i])
            continue

        # ----- per-row expressions (existing) -----
        if (m := ITEM_RATIO_RE.match(rule)):
            A, B, op, val = m.groups()
            A, B, val = A.strip(), B.strip(), float(val)
            intsA, scA = col(A); intsB, scB = col(B)
            d = 10 ** len(str(val).split('.')[-1]); num = int(round(val * d))
            for i in range(n):
                lhs = d * scB * intsA[i]; rhs = num * scA * intsB[i]
                if op in ('<', '<='):
                    mdl.Add(lhs <= rhs - (op == '<')).OnlyEnforceIf(x[i])
                elif op in ('>', '>='):
                    mdl.Add(lhs >= rhs + (op == '>')).OnlyEnforceIf(x[i])
                else:
                    mdl.Add(lhs == rhs).OnlyEnforceIf(x[i])
            continue
        if (m := ITEM_ADD_SUB_RE.match(rule)):
            A, sign, B, op, val = m.groups()
            A, B, val = A.strip(), B.strip(), float(val)
            intsA, scA = col(A); intsB, scB = col(B); lcm = scA * scB; tgt = val * lcm
            for i in range(n):
                expr = (lcm // scA) * intsA[i] + (1 if sign == '+' else -1) * (lcm // scB) * intsB[i]
                add_lin(expr, op, tgt).OnlyEnforceIf(x[i])
            continue
        if (m := ITEM_SCALE_RE.match(rule)):
            k1, A, k2, op, val = m.groups()
            A, val = A.strip(), float(val)
            coef = Fraction(k1) if k1 else Fraction(1)
            if k2: coef /= Fraction(k2)
            intsA, sc = col(A)
            for i in range(n):
                add_lin(coef.numerator * intsA[i], op, val * sc * coef.denominator).OnlyEnforceIf(x[i])
            continue
        if (m := ITEM_PROD_RE.match(rule)):
            A, B, op, val = m.groups()
            A, B, val = A.strip(), B.strip(), float(val)
            intsA, scA = col(A); intsB, scB = col(B); lcm = scA * scB; tgt = val * lcm
            for i in range(n):
                add_lin(intsA[i] * intsB[i], op, tgt).OnlyEnforceIf(x[i])
            continue

        # ---------- fallback row filter ----------
        mc = COND_RE.match(rule)
        if not mc:
            raise ValueError(f"Bad condition:\n{rule}")
        c, op, raw = mc.groups()
        c, raw = c.strip(), raw.strip()
        for i in range(n):
            if raw.startswith('"'):
                ok = clean(df.loc[i, c]) == clean(raw.strip('"'))
            else:
                v = float(raw); cell = df.loc[i, c]
                ok = {'<=': cell <= v, '>=': cell >= v, '<': cell < v, '>': cell > v, '=': cell == v}[op]
            if not ok:
                mdl.Add(x[i] == 0)

    # ---------- SETVALUE ----------
    if ot == 'SETVALUE':
        target = float(re.search(r'=\s*(-?[0-9.]+)', oe).group(1))
        base = SUM_RE.match(oe).group(1).strip()
        sc = col(base)[1]
        tgt = int(round(target * sc))
        if tol is None:
            add_lin(obj, '=', tgt)
        else:
            d = int(round(tol * sc))
            mdl.Add(obj >= tgt - d); mdl.Add(obj <= tgt + d)

    return mdl, x

# ---------- thin wrapper ----------
def solve(df: pd.DataFrame, rules: str) -> pd.DataFrame:
    """Parse *rules*, optimise, and return df with a boolean 'Selected'."""
    ot, oe, tol, cons = parse(rules)
    mdl, x = build_model(df, ot, oe, tol, cons)
    solver = cp_model.CpSolver()
    st = solver.Solve(mdl)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("No feasible solution.")
    out = df.copy()
    out["Selected"] = [bool(solver.Value(b)) for b in x]
    return out
