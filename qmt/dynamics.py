"""
§4 — Динамическая система DIALOG QMT: четыре уравнения движения.

    dX/dt = F₁(X) − γ·X − μ·X + ξ·ε      X — нагрузка (осциллятор)
    dε/dt = η·X − ξ·ε                     ε — параметр памяти
    dμ/dt = α(μ_target − μ) − κ·X·μ       μ — проводимость σ(t,x)
    dτ/dt = 1/(1 + X)                     τ — внутреннее (субъективное) время

где F₁(X) = X₀/(1 + X/X₀) — функция Хилла.

Ключевой результат (§4.2): при квазистатическом ε и γ = η уравнение для X
сводится к dX/dt = F₁(X) − μ·X. Его стационарная точка

    X* = X₀ · (−1 + √(1 + 4/μ)) / 2

при X₀ = φ−1 и μ = μ_crit = 0.5 даёт ровно X* = φ − 1 = 0.618 — φ-аттрактор.
μ_crit = 0.5 совпадает со структурным параметром μ₀ (узел S5, точка выбора).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from .constants import MU_CRIT, PHI, X_STAR


@dataclass
class Params:
    """Параметры динамической системы (нормированные единицы)."""

    X0: float = PHI - 1.0     # масштаб функции Хилла (даёт X* = φ−1 при μ=0.5)
    gamma: float = 1.0        # затухание (γ = η из теоремы A4)
    eta: float = 1.0          # накопление памяти (γ = η)
    xi: float = 1.0           # дисперсия памяти (скорость релаксации ε)
    alpha: float = 0.5        # восстановление проводимости к μ_target
    kappa: float = 1.0        # подавление μ нагрузкой (главный параметр IBM)
    mu_target: float = 0.6    # целевая проводимость (управляющий параметр)


def hill(x: float, x0: float) -> float:
    """Функция Хилла F₁(X) = X₀ / (1 + X/X₀)."""
    return x0 / (1.0 + x / x0)


def equations(t: float, state, p: Params):
    """Правая часть системы ОДУ. state = (X, ε, μ, τ)."""
    X, eps, mu, tau = state
    dX = hill(X, p.X0) - p.gamma * X - mu * X + p.xi * eps
    deps = p.eta * X - p.xi * eps
    dmu = p.alpha * (p.mu_target - mu) - p.kappa * X * mu
    dtau = 1.0 / (1.0 + X)
    return [dX, deps, dmu, dtau]


def integrate(p: Params, state0=(0.05, 0.0, 0.6, 0.0), t_max=60.0, n=600):
    """Численно проинтегрировать систему. Возвращает (t, Y) где Y[k] — переменная k."""
    t_eval = np.linspace(0.0, t_max, n)
    sol = solve_ivp(
        equations, (0.0, t_max), list(state0), t_eval=t_eval,
        args=(p,), method="RK45", rtol=1e-8, atol=1e-10,
    )
    return sol.t, sol.y


def steady_state_load(mu: float, x0: float = PHI - 1.0) -> float:
    """Стационарная нагрузка X*(μ) редуцированной системы (квазистат. ε, γ=η).

    X* = X₀ · (−1 + √(1 + 4/μ)) / 2.  При μ = 0.5, X₀ = φ−1 → X* = φ−1.
    """
    if mu <= 0:
        return math.inf
    return x0 * (-1.0 + math.sqrt(1.0 + 4.0 / mu)) / 2.0


def bifurcation_curve(mu_values=None, x0: float = PHI - 1.0):
    """Кривая X*(μ) для диаграммы бифуркации. Возвращает (mu_array, X_array)."""
    if mu_values is None:
        mu_values = np.linspace(0.1, 1.5, 200)
    mu_values = np.asarray(mu_values, dtype=float)
    X = np.array([steady_state_load(m, x0) for m in mu_values])
    return mu_values, X


def jacobian_eigenvalues(mu: float = MU_CRIT, x0: float = PHI - 1.0):
    """Собственные значения якобиана редуцированной 1D-системы в X*(μ).

    g(X) = F₁(X) − μ·X;  g'(X) = −X₀²/(X₀+X)² − μ.
    Отрицательность g'(X*) означает устойчивость φ-аттрактора.
    """
    xs = steady_state_load(mu, x0)
    gprime = -(x0**2) / (x0 + xs) ** 2 - mu
    return xs, gprime


if __name__ == "__main__":
    print(f"X*(μ=0.5) = {steady_state_load(MU_CRIT):.6f}  (эталон φ−1 = {X_STAR:.6f})")
    xs, gp = jacobian_eigenvalues(MU_CRIT)
    print(f"якобиан g'(X*) = {gp:.4f}  (< 0 ⇒ устойчиво)")
    t, Y = integrate(Params())
    print(f"После интегрирования: X→{Y[0, -1]:.4f}, ε→{Y[1, -1]:.4f}, μ→{Y[2, -1]:.4f}, τ→{Y[3, -1]:.4f}")
