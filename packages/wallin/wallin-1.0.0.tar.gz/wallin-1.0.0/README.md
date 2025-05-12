# Wallin

Wallin is a simple, expressive optimization library that lets you define constraints and objectives in plain English. It’s designed for business analysts, accountants, and operations pros who want to solve real-world allocation problems without having to learn an optimization language.

Built on top of Google OR-Tools, Wallin turns your Excel data and rule logic into a solvable optimization model.

---

## Features

- **Plain English syntax**: Write rules like `SUM(Cost) <= 1000` or `Location = "NY"`
- **Aggregate constraints**: SUM, COUNT, AVG, SUMPRODUCT, ratios, and scaled sums
- **Row-level logic**: Filter rows with conditions like `State = "CA"` or `Profit / Cost > 1.5`
- **Support for SETVALUE objectives with tolerance**  
- **Per-row math**: Ratios, addition, subtraction, multiplication  
- **Robust scaling for decimal precision**
- **No boilerplate**: One function call to solve and return selected rows

---

## Installation

Clone the repo locally or install with:

```bash
pip install wallin
```

---

## How It Works

Wallin expects two inputs:

1. A **Pandas DataFrame** (from Excel, CSV, etc.)
2. A **multi-line string of rules** written in plain English

It returns the same DataFrame with a `Selected` column marking which rows were chosen by the optimizer.

---

## Example

```python
import pandas as pd
import wallin as wl

# Load your Excel file
df = pd.read_excel("Transaction Detail.xlsx")

# Define rules
RULES = """
MAXIMIZE: SUM(Profit)
CONSTRAINT: COGS/Profit < 0.06
CONSTRAINT: SUMPRODUCT(COGS, Profit) <= 60000
CONSTRAINT: Location = "NC"
"""

# Solve
result = wl.solve(df, RULES)

# Get selected rows
selected = result[result["Selected"]]
selected.to_excel("selected_rows.xlsx", index=False)
```

---

## Supported Syntax

### Objectives

```text
MAXIMIZE: SUM(Profit)
MINIMIZE: COUNT(*)
SETVALUE: SUM(Amount) = 100
TOLERANCE: 1.5         # (optional, used with SETVALUE)
```

### Aggregate Constraints

```text
CONSTRAINT: SUM(Cost) <= 1000
CONSTRAINT: COUNT(*) = 5
CONSTRAINT: AVG(Score) > 3.5
CONSTRAINT: SUM(COGS) + SUM(Fees) <= 2000
CONSTRAINT: 2 * SUM(Value) / 3 >= 50
CONSTRAINT: SUM(COGS) / SUM(Profit) <= 0.2
CONSTRAINT: SUM(COGS * Profit) <= 30000
CONSTRAINT: SUMPRODUCT(COGS, Profit) <= 30000
```

### Row-level Math

```text
CONSTRAINT: Profit / Cost >= 1.5
CONSTRAINT: Score + Bonus >= 10
CONSTRAINT: 3 * Cost / 2 <= 500
CONSTRAINT: COGS * Profit < 2000
```

### Row Filters (text/numbers)

```text
CONSTRAINT: Region = "West"
CONSTRAINT: Profit >= 50 AND Profit <= 100
CONSTRAINT: State = "CA" OR State = "NY"
```

---

## Output

The output DataFrame contains a `Selected` column marking which rows were chosen. You can filter it like this:

```python
selected = result[result["Selected"]]
```

---

## License

MIT License. Free to use, modify, and distribute.
