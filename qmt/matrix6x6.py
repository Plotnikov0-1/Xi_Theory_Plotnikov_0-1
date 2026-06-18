"""
§12 — Циркулянтная матрица 6×6 активного ядра (узлы S1–S3, S5–S8).

Собственные значения: λ_k = a + 2b·cos(2πk/6), k = 0…5, при a=1.5, b=0.5.
След = 6a = 9.0 — топологический инвариант Sum-9.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def eigenvalues(a: float = 1.5, b: float = 0.5, n: int = 6) -> np.ndarray:
    """Спектр циркулянтной матрицы: λ_k = a + 2b·cos(2πk/n)."""
    k = np.arange(n)
    return a + 2.0 * b * np.cos(2.0 * np.pi * k / n)


def circulant_matrix(a: float = 1.5, b: float = 0.5, n: int = 6) -> np.ndarray:
    """Симметричная циркулянтная матрица с диагональю a и связью b (соседи по кольцу)."""
    M = np.zeros((n, n))
    for i in range(n):
        M[i, i] = a
        M[i, (i + 1) % n] = b
        M[i, (i - 1) % n] = b
    return M


@dataclass
class SpectralInvariants:
    trace: float           # след = Σλ (Sum-9)
    determinant: float     # произведение λ
    variance: float        # дисперсия спектра
    delta_min: float       # минимальный зазор между различными λ
    eigvals: np.ndarray


def spectral_invariants(a: float = 1.5, b: float = 0.5, n: int = 6) -> SpectralInvariants:
    """Спектральные инварианты матрицы 6×6."""
    lam = eigenvalues(a, b, n)
    trace = float(lam.sum())
    determinant = float(np.prod(lam))
    variance = float(lam.var())
    distinct = np.unique(np.round(lam, 9))
    gaps = np.diff(np.sort(distinct))
    delta_min = float(gaps.min()) if len(gaps) else 0.0
    return SpectralInvariants(trace, determinant, variance, delta_min, lam)


def rhythm_invariant(omega_sys: float, delta_min: float, gamma: float) -> float:
    """§A4 — Инвариант ритма ℛ = Ω_sys · δλ_min / γ.

    ℛ ≈ 0.21 — система на нижней границе зоны баланса (устойчивый режим).
    ℛ ≪ 0.3 → декогеренция; 0.3–3.0 → баланс; ℛ ≫ 3.0 → рекуррентная петля.
    """
    return omega_sys * delta_min / gamma


def perturbation_scan(deltas=(0.0, 0.10, 0.20, 0.30), a: float = 1.5, b: float = 0.5):
    """§12.3 — Устойчивость к возмущению связи b → b + δ.

    Возвращает список (δ, δλ_min). При δ > δ_c ≈ 0.15 минимальный зазор
    схлопывается — система теряет устойчивость.
    """
    out = []
    for d in deltas:
        inv = spectral_invariants(a, b + d)
        out.append((d, inv.delta_min))
    return out


if __name__ == "__main__":
    inv = spectral_invariants()
    print("λ_k       :", np.round(inv.eigvals, 3))
    print(f"след       = {inv.trace}  (Sum-9 = 9.0)")
    print(f"определит. = {inv.determinant}")
    print(f"дисперсия  = {inv.variance:.3f}")
    print(f"δλ_min     = {inv.delta_min}")
    from .constants import GAMMA_DECO, OMEGA_SYS
    R = rhythm_invariant(OMEGA_SYS, inv.delta_min, GAMMA_DECO)
    print(f"ℛ (ритм)   = {R:.3f}  (баланс на нижней границе ~0.21)")
