"""
§ Эффективная матрица памяти C_eff и ядро K(t) (канон 2026, Документ IV).

Старая циркулянтная матрица C — нижний рациональный каркас (Sum-9), а рабочая
матрица модели — эффективная C_eff с коллективной и дифференциальной деформациями:

    C = circ(1.5, 0.5, 0, 0, 0, 0.5)          # Tr=9, δλ_min=0.5, N=6
    C_eff = C + α·u·uᵀ + β·v·vᵀ
    u = (1,1,1,1,1,1)ᵀ,  v = (1,1,1,−1,−1,−1)ᵀ,  α = 1.8 (=9/5),  β = 2.4

Мост геометрия → память (детерминированно, без феноменологии):
    C_eff → (λ_k, v_k) → g_k → J_d(ω) → K(t)
    канал наблюдения (IBM): ĉ = e₇,  g_k = η·|⟨ĉ, v_k⟩|²
    J_d(ω) = Σ_k g_k δ(ω − Ω λ_k)
    K(t)   = Σ_k g_k e^{−(γ_k + iΩ λ_k) t}

Закон дыхания (режимный инвариант): ℒ = Ω·δλ_min/γ. Две опорные точки:
    ε* = φ⁻¹ ≈ 0.618 → ℒ ≈ 1.667  (устойчивая память, ритм держится);
    ε_X ≈ e  ≈ 2.721 → ℒ ≈ 0.093  (разлом: щель закрывается, мягкая мода).
"""

from __future__ import annotations

import numpy as np

from .constants import E as E_CONST
from .constants import X_STAR

ALPHA = 1.8          # коллективная деформация (= 9/5)
BETA = 2.4           # дифференциальная (симметрийно-ломающая)
U_VEC = np.ones(6)
V_VEC = np.array([1.0, 1.0, 1.0, -1.0, -1.0, -1.0])
CHANNEL_INDEX = 5    # ĉ = e₇ — локальный канал наблюдения через узел S7

# Две опорные точки закона дыхания (канон 2026).
REFERENCE_POINTS = {
    "устойчивая память": (X_STAR, 1.667, "ε*=φ⁻¹: ритм держится, память распределена"),
    "X-разлом": (E_CONST, 0.093, "ε_X≈e: δλ_min→0, мягкая мода, коллапс режима"),
}


def base_matrix() -> np.ndarray:
    """Базовая циркулянтная матрица C = circ(1.5,0.5,0,0,0,0.5) (Sum-9 каркас)."""
    first_row = np.array([1.5, 0.5, 0.0, 0.0, 0.0, 0.5])
    return np.array([np.roll(first_row, i) for i in range(6)])


def effective_matrix(alpha: float = ALPHA, beta: float = BETA) -> np.ndarray:
    """Эффективная матрица C_eff = C + α·uuᵀ + β·vvᵀ."""
    C = base_matrix()
    return C + alpha * np.outer(U_VEC, U_VEC) + beta * np.outer(V_VEC, V_VEC)


def spectrum(matrix=None):
    """Собственные значения и векторы (λ_k, v_k) симметричной матрицы."""
    if matrix is None:
        matrix = effective_matrix()
    vals, vecs = np.linalg.eigh(matrix)
    return vals, vecs


def channel_weights(eta: float = 1.0, channel: int = CHANNEL_INDEX):
    """Веса мод g_k = η·|⟨ĉ, v_k⟩|² для канала ĉ = e_channel (узел S7)."""
    vals, vecs = spectrum()
    c = np.zeros(6)
    c[channel] = 1.0
    g = eta * np.abs(vecs.T @ c) ** 2
    return vals, g


def memory_kernel(t, Omega: float = 1.0, gamma: float = 0.1, eta: float = 1.0):
    """Ядро памяти K(t) = Σ_k g_k·e^{−(γ + iΩλ_k)t}. Принимает скаляр/массив t."""
    vals, g = channel_weights(eta)
    t = np.atleast_1d(np.asarray(t, float))
    K = np.array([np.sum(g * np.exp(-(gamma + 1j * Omega * vals) * tt)) for tt in t])
    return K if K.size > 1 else K[0]


def spectral_density(Omega: float = 1.0, eta: float = 1.0):
    """Дискретная J_d(ω) = Σ_k g_k δ(ω−Ωλ_k): частоты ω_k=Ωλ_k и веса g_k."""
    vals, g = channel_weights(eta)
    return Omega * vals, g


def min_gap(matrix=None) -> float:
    """Минимальный зазор между различными собственными значениями (δλ_min)."""
    vals, _ = spectrum(matrix)
    distinct = np.unique(np.round(vals, 9))
    return float(np.min(np.diff(np.sort(distinct))))


def breathing_law(Omega: float, delta_min: float, gamma: float) -> float:
    """Закон дыхания ℒ = Ω·δλ_min/γ (режимный инвариант)."""
    return Omega * delta_min / gamma


if __name__ == "__main__":
    C = base_matrix()
    print(f"C: след = {np.trace(C):.0f} (Sum-9), δλ_min = {min_gap(C)}")
    Ceff = effective_matrix()
    print(f"C_eff симметрична? {np.allclose(Ceff, Ceff.T)}")
    vals, g = channel_weights()
    print("λ_k :", np.round(vals, 3))
    print("g_k :", np.round(g, 3), " (Σg_k =", round(g.sum(), 3), ")")
    print(f"K(0) = {memory_kernel(0.0):.3f}  (= Σg_k)")
    print("\nопорные точки закона дыхания:")
    for name, (eps, L, meaning) in REFERENCE_POINTS.items():
        print(f"  {name}: ε={eps:.3f}, ℒ≈{L} — {meaning}")
