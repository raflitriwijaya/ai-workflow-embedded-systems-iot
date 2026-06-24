"""Inter-rater reliability (spec HG-3: IRR ≥ 0.80 for human-reviewed items).

Two complementary estimators are provided:

* **Fleiss' kappa** — for the discrete 0–3 rubric categories, any number of raters
  per item. This is the natural fit for the HR rubric dimensions (spec §4.2).
* **ICC(2,1) / ICC(2,k)** — two-way random-effects intraclass correlation for
  treating reviewer scores as continuous, with an F-test p-value via the
  pure-Python F survival function.
"""
from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass

from .special import f_sf

IRR_GATE = 0.80  # spec HG-3


# ── Fleiss' kappa ─────────────────────────────────────────────────────────────
def build_fleiss_matrix(
    ratings_per_item: Sequence[Sequence[int]], categories: Sequence[int]
) -> list[list[int]]:
    """Convert per-item lists of category labels into an item×category count matrix.

    Every item must have been rated by the same number of raters (Fleiss' kappa
    requirement). Raises ValueError otherwise.
    """
    cat_index = {c: i for i, c in enumerate(categories)}
    counts: list[list[int]] = []
    n_raters = None
    for item in ratings_per_item:
        if n_raters is None:
            n_raters = len(item)
        elif len(item) != n_raters:
            raise ValueError("Fleiss' kappa requires an equal number of raters per item")
        row = [0] * len(categories)
        for label in item:
            if label not in cat_index:
                raise ValueError(f"rating {label!r} not in declared categories {list(categories)}")
            row[cat_index[label]] += 1
        counts.append(row)
    return counts


def fleiss_kappa(matrix: Sequence[Sequence[int]]) -> float:
    """Fleiss' kappa from an item×category count matrix."""
    N = len(matrix)
    if N == 0:
        raise ValueError("empty matrix")
    n = sum(matrix[0])
    if n < 2:
        raise ValueError("Fleiss' kappa requires ≥2 raters per item")
    if any(sum(row) != n for row in matrix):
        raise ValueError("every item must have the same rater count")

    # P_i: extent of agreement for item i
    p_items = []
    for row in matrix:
        agree = sum(c * c for c in row) - n
        p_items.append(agree / (n * (n - 1)))
    p_bar = statistics.fmean(p_items)

    # p_j: proportion of all assignments to category j
    totals = [sum(matrix[i][j] for i in range(N)) for j in range(len(matrix[0]))]
    grand = N * n
    p_cats = [t / grand for t in totals]
    p_e = sum(p * p for p in p_cats)

    if p_e >= 1.0:
        return 1.0  # all raters used a single category for every item → perfect by convention
    return (p_bar - p_e) / (1.0 - p_e)


# ── Intraclass correlation ────────────────────────────────────────────────────
@dataclass
class ICCResult:
    icc_single: float    # ICC(2,1) — reliability of a single rater
    icc_average: float   # ICC(2,k) — reliability of the mean of k raters
    f: float
    df1: float
    df2: float
    p_value: float

    def as_dict(self) -> dict:
        return {
            "icc_single": self.icc_single,
            "icc_average": self.icc_average,
            "f": self.f,
            "df1": self.df1,
            "df2": self.df2,
            "p_value": self.p_value,
        }


def icc(data: Sequence[Sequence[float]]) -> ICCResult:
    """ICC(2,1) and ICC(2,k), two-way random effects, absolute agreement.

    ``data`` is an N×k matrix: N subjects (items) rated by the same k raters.
    """
    N = len(data)
    if N < 2:
        raise ValueError("ICC requires ≥2 subjects")
    k = len(data[0])
    if k < 2:
        raise ValueError("ICC requires ≥2 raters")
    if any(len(row) != k for row in data):
        raise ValueError("ragged matrix: every subject needs k ratings")

    flat = [x for row in data for x in row]
    grand = statistics.fmean(flat)
    row_means = [statistics.fmean(row) for row in data]
    col_means = [statistics.fmean([data[i][j] for i in range(N)]) for j in range(k)]

    ss_total = sum((x - grand) ** 2 for x in flat)
    ss_rows = k * sum((rm - grand) ** 2 for rm in row_means)
    ss_cols = N * sum((cm - grand) ** 2 for cm in col_means)
    ss_err = ss_total - ss_rows - ss_cols

    df_rows = N - 1
    df_cols = k - 1
    df_err = df_rows * df_cols

    msr = ss_rows / df_rows
    msc = ss_cols / df_cols
    mse = ss_err / df_err if df_err > 0 else 0.0

    denom_single = msr + (k - 1) * mse + (k / N) * (msc - mse)
    icc_single = (msr - mse) / denom_single if denom_single != 0 else 0.0
    denom_avg = msr + (msc - mse) / N
    icc_average = (msr - mse) / denom_avg if denom_avg != 0 else 0.0

    f = msr / mse if mse > 0 else float("inf")
    p = f_sf(f, df_rows, df_err) if mse > 0 else 0.0
    return ICCResult(
        icc_single=icc_single, icc_average=icc_average,
        f=f, df1=df_rows, df2=df_err, p_value=p,
    )
