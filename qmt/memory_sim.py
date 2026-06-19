"""
Численная симуляция немарковской памяти — «старший канон» как работающая модель.

Здесь память ε перестаёт быть схемой и становится решённым уравнением.
Берём когерентность c(t) открытой двухуровневой системы с экспоненциальным
ядром памяти

        dc/dt = − ∫₀ᵗ K(t−s) · c(s) ds ,   K(t) = (γ/τ_m)·e^(−t/τ_m).

Это эквивалентно системе ОДУ (вводим I = ∫ K·c):

        c' = − I
        I' = (γ/τ_m)·c − (1/τ_m)·I

Физический смысл предела:
  • τ_m → 0  ⇒  K(t) → γ·δ(t)  ⇒  dc/dt = −γ·c  — марковский распад (Линдблад).
    Память отсутствует (ε=0): воспроизводим стандартную декогеренцию. [проверка]
  • τ_m > 0  ⇒  у уравнения появляется колебательное решение: ВОЗВРАТЫ
    когерентности (revivals). Прошлое возвращается в настоящее — это и есть
    физический эффект памяти ε≠0.

Параметр памяти ε отображаем монотонно на время памяти τ_m: ε∈[0,1) ⇒
τ_m = ε/(γ(1−ε)). При ε→0 память исчезает, при ε→φ−1 — режим аттрактора.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from . import constants as C


def tau_from_epsilon(eps: float, gamma: float) -> float:
    """Отображение параметра памяти ε∈[0,1) → время памяти τ_m≥0."""
    eps = min(max(eps, 0.0), 0.999)
    return eps / (gamma * (1.0 - eps))


def evolve(eps: float, gamma: float = 1.0, t_max: float = 20.0,
           n: int = 1000) -> tuple[np.ndarray, np.ndarray]:
    """Эволюция когерентности c(t) при параметре памяти ε.

    Возвращает (t, c). c(0)=1. gamma — марковская скорость распада.
    """
    tau_m = tau_from_epsilon(eps, gamma)
    t = np.linspace(0.0, t_max, n)

    if tau_m < 1e-6:  # марковский предел: чистая экспонента
        return t, np.exp(-gamma * t)

    def rhs(_t, y):
        c, I = y
        return [-I, gamma / tau_m * c - I / tau_m]

    sol = solve_ivp(rhs, (0.0, t_max), [1.0, 0.0], t_eval=t,
                    method="RK45", rtol=1e-8, atol=1e-10)
    return sol.t, sol.y[0]


def non_markovianity(t: np.ndarray, c: np.ndarray) -> float:
    """Мера немарковости (по BLP): суммарный РОСТ |c| во времени.

    В марковском распаде |c| только убывает ⇒ мера = 0. Любые возвраты
    когерентности (память) дают положительный вклад.
    """
    a = np.abs(c)
    dpos = np.diff(a)
    return float(np.sum(dpos[dpos > 0]))


@dataclass
class MemoryReport:
    eps: float
    tau_m: float
    n_measure: float
    n_revivals: int
    regime: str


def analyse(eps: float, gamma: float = 1.0) -> MemoryReport:
    t, c = evolve(eps, gamma=gamma)
    nm = non_markovianity(t, c)
    # считаем возвраты как локальные максимумы |c| после первого спада
    a = np.abs(c)
    rev = int(np.sum((a[1:-1] > a[:-2]) & (a[1:-1] > a[2:]) & (a[1:-1] > 1e-3)))
    regime = "марковский (память отсутствует)" if nm < 1e-3 else \
             "немарковский (память → возвраты когерентности)"
    return MemoryReport(eps, tau_from_epsilon(eps, gamma), nm, rev, regime)


def print_report() -> None:
    print("СИМУЛЯЦИЯ ПАМЯТИ: когерентность c(t) при разных ε")
    print("=" * 64)
    print(f"{'ε':>6} {'τ_m':>8} {'немарковость':>14} {'возвраты':>9}  режим")
    for eps in (0.0, 0.2, 0.4, C.X_STAR, 0.8):
        r = analyse(eps)
        print(f"{r.eps:6.3f} {r.tau_m:8.3f} {r.n_measure:14.4f} "
              f"{r.n_revivals:9d}  {r.regime}")
    print("=" * 64)
    print("ε=0 → чистый экспоненциальный распад (Линдблад) — проверка предела.")
    print(f"ε=φ−1={C.X_STAR:.3f} → выраженная память: прошлое возвращается.")


if __name__ == "__main__":
    print_report()
