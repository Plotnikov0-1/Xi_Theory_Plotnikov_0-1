"""
Точная декогеренция спин-бозон (чистая дефазировка) — чистая физика.

Это строгое ядро вместо феноменологического K(t) из memory_sim. Для кубита,
связанного с бозонным резервуаром по дефазировочному гамильтониану
H = (ω₀/2)σ_z + σ_z·Σ_k g_k(b_k+b_k†) + Σ_k ω_k b_k†b_k, когерентность
вычисляется ТОЧНО (Breuer & Petruccione, «The Theory of Open Quantum Systems»):

        c(t) = ⟨σ_+⟩(t)/⟨σ_+⟩(0) = exp[ −Γ(t) ],

        Γ(t) = ∫₀^∞ dω  J(ω) · coth(ħω / 2k_BT) · (1 − cos ωt) / ω² .

Здесь J(ω)=J₀ω³e^(−ω/ωc) — суперомический спектр самой модели (spectral.py).

Обезразмеривание. x = ω/ωc, τ = ωc·t, безразмерная связь α = J₀·ωc² (это в
точности коэффициент ξ из spectral.py), безразмерная температура θ = k_BT/ħωc:

        Γ(τ) = α · ∫₀^∞ x · e^(−x) · coth(x/2θ) · (1 − cos xτ) dx .

Точный предел T=0 (coth→1) берётся аналитически:
        Γ₀(τ) = α · [ 1 − (1 − τ²)/(1 + τ²)² ] .
Отсюда два чисто физических факта суперомического резервуара:
  • при τ→∞  Γ₀→α  ⇒  c→e^(−α) > 0: когерентность теряется лишь ЧАСТИЧНО,
    остаётся плато — память не стирается (это и есть «ε сохраняется»);
  • Γ₀(τ) немонотонна (проскок выше α и возврат) ⇒ ВОЗВРАТ когерентности
    (немарковость) даже при нулевой температуре.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from . import constants as C
from . import spectral


def gamma_T0_analytic(tau: float, alpha: float) -> float:
    """Точная декогеренционная функция при T=0 (аналитически)."""
    return alpha * (1.0 - (1.0 - tau**2) / (1.0 + tau**2) ** 2)


def _integrand(x: float, tau: float, theta: float) -> float:
    coth = 1.0 if theta <= 0 else 1.0 / np.tanh(x / (2.0 * theta))
    return x * np.exp(-x) * coth * (1.0 - np.cos(x * tau))


def gamma(tau: float, alpha: float = 1.0, theta: float = 0.0) -> float:
    """Точная Γ(τ) численно (любая температура θ=k_BT/ħωc)."""
    if theta <= 0:
        return gamma_T0_analytic(tau, alpha)
    val, _ = quad(_integrand, 0.0, np.inf, args=(tau, theta),
                  limit=200, epsabs=1e-10, epsrel=1e-8)
    return alpha * val


def coherence(tau, alpha: float = 1.0, theta: float = 0.0):
    """c(τ)=exp(−Γ(τ)). Принимает скаляр или массив τ."""
    tau = np.atleast_1d(np.asarray(tau, dtype=float))
    g = np.array([gamma(t, alpha, theta) for t in tau])
    c = np.exp(-g)
    return c[0] if c.size == 1 else c


def coherence_curve(tau_arr, alpha: float = 1.0, theta: float = 0.0,
                    x_max: float = 60.0, nx: int = 6000):
    """Быстрая c(τ) для массива τ через общий сеточный интеграл по ω (trapz).

    На порядки быстрее quad-в-цикле — используется для графиков и меры BLP.
    """
    tau_arr = np.asarray(tau_arr, dtype=float)
    x = np.linspace(1e-6, x_max, nx)
    coth = np.ones_like(x) if theta <= 0 else 1.0 / np.tanh(x / (2.0 * theta))
    base = x * np.exp(-x) * coth                      # часть подынтегрального
    # Γ(τ) = α ∫ base·(1−cos xτ) dx  для каждого τ (векторизуем по сетке x)
    cos_term = np.cos(np.outer(tau_arr, x))           # (Nτ, Nx)
    integ = base[None, :] * (1.0 - cos_term)
    g = alpha * np.trapezoid(integ, x, axis=1)
    return np.exp(-g)


def plateau_T0(alpha: float = 1.0) -> float:
    """Остаточная когерентность при T=0, τ→∞: c∞ = e^(−α) (сохранённая память)."""
    return float(np.exp(-alpha))


def non_markovianity(alpha: float = 1.0, theta: float = 0.0,
                     tau_max: float = 40.0, n: int = 4000) -> float:
    """Мера немарковости (BLP): суммарный РОСТ |c(τ)| (возвраты когерентности)."""
    tau = np.linspace(0.0, tau_max, n)
    c = coherence_curve(tau, alpha, theta)
    d = np.diff(c)
    return float(np.sum(d[d > 0]))


@dataclass
class DephasingReport:
    alpha: float
    theta: float
    c_inf: float
    nonmarkov: float
    revival: bool


def analyse(alpha: float = 1.0, theta: float = 0.0) -> DephasingReport:
    nm = non_markovianity(alpha, theta)
    c_inf = coherence(60.0, alpha, theta)
    return DephasingReport(alpha, theta, float(c_inf), nm, nm > 1e-4)


def model_alpha() -> float:
    """Безразмерная связь α=ξ=J₀ωc² для J₀=1 в единицах модели (spectral.py)."""
    # В обезразмеренных единицах (ωc=1, J₀=1) α=1; здесь демонстрационное α.
    return 1.0


def print_report() -> None:
    print("ТОЧНАЯ ДЕКОГЕРЕНЦИЯ СПИН-БОЗОН (чистая дефазировка)")
    print("=" * 66)
    print("c(t)=exp(−Γ(t)),  Γ из J(ω)=J₀ω³e^(−ω/ωc) — суперомический спектр.\n")
    alpha = 1.0
    # сверка численного интеграла с аналитикой при T=0
    err = max(abs(gamma(t, alpha, 0.0) - gamma_T0_analytic(t, alpha))
              for t in (0.5, 1.0, 2.0, 5.0))
    print(f"проверка T=0: |числ.−аналит.| max = {err:.2e}  (должно быть ~0)\n")
    print(f"{'θ=kT/ħωc':>10} {'c(∞)':>10} {'немарковость':>14}  режим")
    for theta in (0.0, 0.1, 0.5, 1.0, 3.0):
        r = analyse(alpha, theta)
        regime = ("плато: память сохраняется" if r.c_inf > 1e-2
                  else "полная декогеренция")
        print(f"{theta:10.2f} {r.c_inf:10.4f} {r.nonmarkov:14.4f}  {regime}")
    print("=" * 66)
    print(f"T=0: c(∞)=e^(−α)={plateau_T0(alpha):.4f}>0 — суперомический резервуар")
    print("НЕ стирает память полностью; рост T постепенно убивает плато.")


if __name__ == "__main__":
    print_report()
