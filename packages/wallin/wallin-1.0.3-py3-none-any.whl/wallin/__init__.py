"""
Wallin – lightweight optimiser DSL (v1.9.8).

Top‑level helpers
-----------------
parse()        -> split rule text into parts
build_model()  -> create OR‑Tools model (+ decision variables)
solve()        -> run solver & return DataFrame with 'Selected' flag
"""

from .solver import parse, build_model, solve

__all__ = ["parse", "build_model", "solve"]
__version__ = "1.9.8"
