"""
§1.2, §A1 — Спектральная плотность резервуара J(ω).

Из трёх аксиом (3D ЭМ-вакуум ρ∝ω², дипольная связь |g|²∝ω, обрез
exp(−ω/ωc)) следует суперомический спектр:

    J(ω) = J₀ · ω³ · exp(−ω/ωc)

Суперомичность (J ∝ ω³) означает: при ω → 0 система не декогерирует —
немарковский режим сохраняется.
"""

from __future__ import annotations

import numpy as np

from .constants import OMEGA_C


def spectral_density(omega, j0: float = 1.0, omega_c: float = OMEGA_C):
    """J(ω) = J₀·ω³·exp(−ω/ωc). Принимает скаляр или массив numpy."""
    omega = np.asarray(omega, dtype=float)
    return j0 * omega**3 * np.exp(-omega / omega_c)


def eta_coefficient(j0: float = 1.0, omega_c: float = OMEGA_C) -> float:
    """Скорость затухания η = ∫₀^∞ J(ω) dω = 6·J₀·ωc⁴ (Γ(4)=6).

    (В документе приведена нормировочно иная запись (4/π)J₀ωc³; здесь
    используется прямой аналитический интеграл ∫ω³e^(−ω/ωc)dω = 6·ωc⁴.)
    """
    return 6.0 * j0 * omega_c**4


def xi_coefficient(j0: float = 1.0, omega_c: float = OMEGA_C) -> float:
    """Дисперсия памяти ξ = ∫₀^∞ J(ω)/ω² dω = J₀·ωc²  (∫ω e^(−ω/ωc)dω = ωc²)."""
    return j0 * omega_c**2


def eta_over_xi(omega_c: float = OMEGA_C) -> float:
    """Отношение η/ξ = 6·ωc² (аналитически, без подгонки)."""
    return 6.0 * omega_c**2


def low_frequency_exponent(omega, j0: float = 1.0, omega_c: float = OMEGA_C):
    """Локальный наклон log J / log ω. При ω ≪ ωc стремится к 3 (суперомичность).

    Подтверждение: Franco et al., PNAS 2023 — измеренный наклон ω^(2.8–3.2).
    """
    omega = np.asarray(omega, dtype=float)
    j = spectral_density(omega, j0, omega_c)
    log_o = np.log(omega)
    log_j = np.log(j)
    return np.gradient(log_j, log_o)


if __name__ == "__main__":
    w = np.linspace(0.01, 3.0, 5) * OMEGA_C
    print("ω/ωc :", (w / OMEGA_C).round(2))
    print("J(ω) :", spectral_density(w))
    print(f"η/ξ  = {eta_over_xi():.4e}  (= 6·ωc²)")
    print(f"наклон при ω→0 ≈ {low_frequency_exponent(np.array([0.01*OMEGA_C, 0.02*OMEGA_C]))[0]:.2f}")
