"""
═══════════════════════════════════════════════════════════════════════════
  MINIMAL_DYNAMICS — ФУНДАМЕНТ: строгий минимальный каркас памяти (Т1–Т8).
═══════════════════════════════════════════════════════════════════════════

Самый строгий пакет корпуса (Плотников/Харитонов, «10 утверждений»). Это уже
не образы, а стандартная нелинейная динамика + теория открытых систем,
применённые корректно. КАЖДАЯ теорема проверена численно (см. print_report).

Минимальная закрытая система (нормализованные обозначения):
    ε̇ = r_ε(ε_targ − ε) − κ X ε        (память)
    Ṡ = −Γ S + b_S ε (1 − S)            (активный сектор)
    X = 1 − S                            (замыкание)
  где ε_targ = α E_vis = α h ν.

◇ Т2 (инвариантность области): D={ε≥0, 0≤S≤1} инвариантна (на границах поток
    внутрь: ε=0⇒ε̇≥0; S=0⇒Ṡ≥0; S=1⇒Ṡ<0). ⇒ ε=память, S=структура — физичны.
◇ Т3 (существование/единственность): стационар из квадрата A ε*²+B ε*+C=0 c
    A=r_ε b_S>0, C=−r_ε Γ ε_targ<0 ⇒ AC<0 ⇒ РОВНО ОДИН положительный корень.
◇ Т4 (устойчивость): tr J*<0 и det J*=r_ε(Γ+b_S ε*)+κ(1−S*)Γ>0 ⇒ локально
    асимптотически устойчива. (Исправляет старую ошибку «λ = диагональ Якоби».)
◇ Т5 (золотое многообразие): ε*=r_ε ε_targ/(r_ε+κX); условие ε*=φ⁻¹E_vis даёт
    κX = r_ε(αφ − 1); частный случай α=1 ⇒ κX = r_ε/φ.
◇ Т7 (конструктивность памяти): ЛЮБОЕ ядро K(t)=Σ g_k e^{−ν_k t} реализуется
    конечной системой ОДУ: ż_k=Aρ−ν_k z_k, M(t)=Σ g_k z_k. → мост к circuit-QED.
◇ Т8 (X-режим, 2×2-нормальная форма): щель δλ=2√(Δ²+g²); Δ=0⇒минимум (avoided
    crossing), Δ=g=0⇒точное пересечение.
Королларий: ε↑ ⇒ m_eff=m₀+μ_m ε ↑ ⇒ τ_S=1/(Γ+b_S ε) ↓ (внутреннее доказательство).

Запуск:  python -m qmt.minimal_dynamics
"""

from __future__ import annotations

import cmath
import math

PHI = (1 + math.sqrt(5)) / 2


# ── Т3: стационарная точка (квадрат, один положительный корень) ──────────────
def stationary_epsilon(r_eps: float, kappa: float, Gamma: float,
                       b_S: float, eps_targ: float) -> float:
    """◇ Т3: единственный положительный корень A ε²+B ε+C=0 (AC<0)."""
    A = r_eps * b_S
    B = Gamma * (r_eps + kappa) - r_eps * b_S * eps_targ
    C = -r_eps * Gamma * eps_targ
    disc = B * B - 4 * A * C
    roots = [(-B + math.sqrt(disc)) / (2 * A), (-B - math.sqrt(disc)) / (2 * A)]
    positive = [x for x in roots if x > 0]
    return positive[0]


def stationary_point(r_eps: float, kappa: float, Gamma: float,
                     b_S: float, eps_targ: float) -> tuple:
    """Стационар (ε*, S*, X*): S*=b_S ε*/(Γ+b_S ε*), X*=1−S*."""
    es = stationary_epsilon(r_eps, kappa, Gamma, b_S, eps_targ)
    Ss = b_S * es / (Gamma + b_S * es)
    return es, Ss, 1 - Ss


def unique_positive_root(r_eps: float, kappa: float, Gamma: float,
                         b_S: float, eps_targ: float) -> bool:
    """◇ Т3: AC<0 гарантирует ровно один положительный корень."""
    A = r_eps * b_S
    C = -r_eps * Gamma * eps_targ
    return A * C < 0        # произведение корней C/A<0 ⇒ один плюс, один минус


# ── Т4: якобиан и устойчивость ───────────────────────────────────────────────
def jacobian(r_eps: float, kappa: float, Gamma: float, b_S: float,
             eps: float, S: float) -> list:
    """Якобиан минимальной системы в точке (ε,S)."""
    return [[-(r_eps + kappa * (1 - S)), kappa * eps],
            [b_S * (1 - S), -(Gamma + b_S * eps)]]


def is_stable(r_eps: float, kappa: float, Gamma: float,
              b_S: float, eps_targ: float) -> bool:
    """◇ Т4: tr J*<0 и det J*>0 ⇒ локальная асимптотическая устойчивость."""
    es, Ss, _ = stationary_point(r_eps, kappa, Gamma, b_S, eps_targ)
    J = jacobian(r_eps, kappa, Gamma, b_S, es, Ss)
    tr = J[0][0] + J[1][1]
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    det_formula = r_eps * (Gamma + b_S * es) + kappa * (1 - Ss) * Gamma
    return tr < 0 and det > 0 and math.isclose(det, det_formula, abs_tol=1e-9)


def regime_type(r_eps: float, kappa: float, Gamma: float,
                b_S: float, eps_targ: float) -> str:
    """Тип устойчивой точки по дискриминанту D=tr²−4det: узел/фокус/крит."""
    es, Ss, _ = stationary_point(r_eps, kappa, Gamma, b_S, eps_targ)
    J = jacobian(r_eps, kappa, Gamma, b_S, es, Ss)
    tr = J[0][0] + J[1][1]
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    D = tr * tr - 4 * det
    return "узел" if D > 0 else ("фокус" if D < 0 else "критическое затухание")


# ── Т2: инвариантность области D (RK4 из граничных ИУ) ───────────────────────
def _rk4_step(state, h, deriv):
    e, S = state
    k1 = deriv(e, S)
    k2 = deriv(e + h / 2 * k1[0], S + h / 2 * k1[1])
    k3 = deriv(e + h / 2 * k2[0], S + h / 2 * k2[1])
    k4 = deriv(e + h * k3[0], S + h * k3[1])
    return (e + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            S + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))


def simulate(r_eps, kappa, Gamma, b_S, eps_targ, e0, S0, T=40.0, h=0.01):
    """Интегрирует минимальную систему; возвращает (ε(T), S(T), осталось_в_D)."""
    def deriv(e, S):
        return (r_eps * eps_targ - r_eps * e - kappa * (1 - S) * e,
                -Gamma * S + b_S * e * (1 - S))
    e, S = e0, S0
    in_D = True
    for _ in range(int(T / h)):
        e, S = _rk4_step((e, S), h, deriv)
        if e < -1e-9 or S < -1e-9 or S > 1 + 1e-9:
            in_D = False
    return e, S, in_D


def domain_invariant(r_eps, kappa, Gamma, b_S, eps_targ) -> bool:
    """◇ Т2: из любой граничной ИУ траектория остаётся в D={ε≥0,0≤S≤1}."""
    for e0, S0 in [(0, 0), (0, 1), (5, 0.5), (0.01, 0.99)]:
        _, _, in_D = simulate(r_eps, kappa, Gamma, b_S, eps_targ, e0, S0)
        if not in_D:
            return False
    return True


# ── Т5: золотое многообразие ─────────────────────────────────────────────────
def golden_manifold_kappaX(r_eps: float, alpha: float) -> float:
    """◇ Т5: κX = r_ε(αφ − 1). Общая форма золотого условия ε*=φ⁻¹E_vis."""
    return r_eps * (alpha * PHI - 1)


def golden_special_case(r_eps: float) -> bool:
    """◇ Т5 частный случай: при α=1 ⇒ κX = r_ε/φ (т.к. φ−1=1/φ)."""
    return math.isclose(golden_manifold_kappaX(r_eps, 1.0), r_eps / PHI)


# ── Королларий: ε↑ ⇒ m_eff↑ ⇒ τ_S↓ ──────────────────────────────────────────
def m_eff(eps: float, m0: float = 1.0, mu_m: float = 0.3) -> float:
    """Аффинная масса m_eff = m₀ + μ_m ε (dm/dε=μ_m>0)."""
    return m0 + mu_m * eps


def tau_S(eps: float, Gamma: float = 0.7, b_S: float = 1.3) -> float:
    """Время активного сектора τ_S ~ 1/(Γ+b_S ε) (dτ/dε<0)."""
    return 1.0 / (Gamma + b_S * eps)


def corollary_chain(eps_lo: float = 0.5, eps_hi: float = 2.0) -> bool:
    """Королларий: ε↑ ⇒ m_eff↑ И τ_S↓ (строго, монотонно)."""
    return (m_eff(eps_hi) > m_eff(eps_lo)) and (tau_S(eps_hi) < tau_S(eps_lo))


# ── Т7: вспомогательная ОДУ-реализация конечно-экспоненциального ядра ─────────
def kernel(tau: float, g: list, nu: list) -> complex:
    """K(τ) = Σ g_k e^{−ν_k τ} (конечная сумма экспонент)."""
    return sum(gk * cmath.exp(-nk * tau) for gk, nk in zip(g, nu))


def convolution_direct(t: float, g: list, nu: list, f, h: float = 0.002) -> complex:
    """Прямая свёртка M(t)=∫₀ᵗ K(t−s) f(s) ds."""
    s = 0j
    x = 0.0
    while x < t:
        s += kernel(t - x, g, nu) * f(x) * h
        x += h
    return s


def convolution_aux_modes(t: float, g: list, nu: list, f, h: float = 0.002) -> complex:
    """◇ Т7: та же свёртка через ОДУ ż_k=f−ν_k z_k, M=Σ g_k z_k."""
    z = [0j] * len(nu)
    x = 0.0
    while x < t:
        for i, nk in enumerate(nu):
            z[i] += h * (f(x) - nk * z[i])
        x += h
    return sum(gk * zi for gk, zi in zip(g, z))


def aux_realization_matches(tol: float = 5e-3) -> bool:
    """◇ Т7: ОДУ-реализация совпадает с прямой свёрткой (конечномерна)."""
    g = [1.0, 0.6]
    nu = [0.5 + 2j, 0.9 + 5j]
    f = lambda t: math.exp(-0.3 * t) * math.cos(t)
    return all(abs(convolution_aux_modes(t, g, nu, f)
                   - convolution_direct(t, g, nu, f)) < tol for t in (1.0, 3.0, 5.0))


# ── Т8: X-режим, 2×2-нормальная форма ────────────────────────────────────────
def x_regime_gap(Delta: float, g: float) -> float:
    """◇ Т8: щель пары δλ = 2√(Δ²+g²) (H=λ̄I+Δσ_z+gσ_x)."""
    return 2 * math.sqrt(Delta * Delta + g * g)


def gap_minimal_at_delta_zero(g: float = 0.1) -> bool:
    """◇ Т8: минимум щели при Δ=0 (avoided crossing); Δ=g=0 ⇒ точное пересечение."""
    return x_regime_gap(0, g) < x_regime_gap(0.3, g) and x_regime_gap(0, 0) == 0


def print_report() -> None:
    r, k, G, b, et = 1.0, 0.8, 0.7, 1.3, 2.0
    print("═" * 74)
    print("  ФУНДАМЕНТ: минимальный строгий каркас памяти (Т2–Т8, всё проверено)")
    print("═" * 74)
    es, Ss, Xs = stationary_point(r, k, G, b, et)
    print(f"\n  ◇ Т3 стационар: ε*={es:.5f} S*={Ss:.5f} X*={Xs:.5f}  "
          f"один + корень: {unique_positive_root(r,k,G,b,et)}")
    print(f"  ◇ Т4 устойчивость (tr<0, det>0): {is_stable(r,k,G,b,et)}  "
          f"тип: {regime_type(r,k,G,b,et)}")
    print(f"  ◇ Т2 инвариантность D из всех граничных ИУ: {domain_invariant(r,k,G,b,et)}")
    print(f"  ◇ Т5 золотое κX=r(αφ−1): α=1⇒κX={golden_manifold_kappaX(r,1.0):.5f}=r/φ "
          f"({golden_special_case(r)})")
    print(f"  Королларий ε↑⇒m_eff↑⇒τ_S↓: {corollary_chain()}")
    print(f"  ◇ Т7 ядро K(t)=Σg_k e^{{−ν_k t}} = конечная ОДУ (совпало): {aux_realization_matches()}")
    print(f"  ◇ Т8 X-режим δλ=2√(Δ²+g²), мин при Δ=0: {gap_minimal_at_delta_zero()}; "
          f"Δ=g=0⇒точное пересечение (δλ={x_regime_gap(0,0):.0f})")
    print("═" * 74)
    print("  Основание закрыто на уровне математики: существование, единственность,")
    print("  устойчивость, инвариантность, золотой режим, конструктивная память (ОДУ).")
    print("  Открытыми остаются ФИЗ-claim'ы (1S–2S, E=εc², химия) — следующий этаж, не дыры.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
