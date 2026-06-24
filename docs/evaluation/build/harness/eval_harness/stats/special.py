"""Special functions used by the statistics layer.

Implemented in pure Python (math only) so the statistical core runs and tests
anywhere without scipy. The regularised incomplete beta function backs both the
Student's-t survival function (Welch's t-test p-value) and the F-distribution
CDF (ICC significance), using the standard Lentz continued-fraction expansion
(Numerical Recipes §6.4) — accurate to ~1e-10 across the ranges we use.
"""
from __future__ import annotations

import math

_MAXIT = 300
_FPMIN = 1e-300


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (Lentz's method)."""
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _FPMIN:
        d = _FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, _MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-12:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta function I_x(a, b), 0 <= x <= 1."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def student_t_sf(t: float, df: float) -> float:
    """Survival function P(T > t) for Student's t with df degrees of freedom."""
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    half = 0.5 * betainc(df / 2.0, 0.5, x)  # = P(T > |t|)
    return half if t > 0 else 1.0 - half


def f_sf(f: float, d1: float, d2: float) -> float:
    """Survival function P(F > f) for the F-distribution with (d1, d2) df."""
    if f <= 0:
        return 1.0
    x = d2 / (d2 + d1 * f)
    return betainc(d2 / 2.0, d1 / 2.0, x)
