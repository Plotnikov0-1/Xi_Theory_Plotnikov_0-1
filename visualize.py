#!/usr/bin/env python3
"""
Визуализация теории DIALOG QMT.

Строит шесть ключевых графиков и сохраняет их в папку figures/:
    1. Спектральная плотность резервуара J(ω).
    2. Уровни водорода и узлы S0–S9.
    3. Динамическая система: эволюция X, ε, μ, τ.
    4. Диаграмма бифуркации X*(μ) с φ-аттрактором.
    5. Спектр матрицы 6×6 и устойчивость к возмущению.
    6. Параметр искренности S(ε) — теорема монотонности.

Запуск:  python visualize.py
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")  # без графического дисплея — сохраняем в файлы
import matplotlib.pyplot as plt
import numpy as np

from qmt import constants as C
from qmt import dynamics, hydrogen, matrix6x6, sincerity, spectral

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")


def _save(fig, name: str):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  сохранено: figures/{name}")


def plot_spectral_density():
    """График 1 — суперомический спектр J(ω) = J₀·ω³·exp(−ω/ωc)."""
    w = np.linspace(0.001, 6.0, 500) * C.OMEGA_C
    j = spectral.spectral_density(w)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(w / C.OMEGA_C, j / j.max(), color="#c46849", lw=2)
    ax.axvline(1.0, ls="--", color="gray", lw=1, label="ω = ωc (обрез)")
    ax.set_xlabel("ω / ωc")
    ax.set_ylabel("J(ω) (норм.)")
    ax.set_title("Спектральная плотность резервуара  J(ω) = J₀·ω³·e^(−ω/ωc)")
    ax.legend()
    ax.grid(alpha=0.3)
    _save(fig, "1_spectral_density.png")


def plot_hydrogen_levels():
    """График 2 — уровни водорода и узлы DIALOG QMT."""
    fig, ax = plt.subplots(figsize=(7, 5))
    for nd in hydrogen.NODES:
        if nd.energy_ev is None:
            continue
        color = "#c46849" if nd.on_fibonacci else "#5e5d59"
        ax.hlines(nd.energy_ev, 0.1, 0.9, color=color, lw=2)
        ax.text(0.92, nd.energy_ev, f"S{nd.index} ({nd.orbital})",
                va="center", fontsize=9, color=color)
    ax.set_xlim(0, 1.4)
    ax.set_xticks([])
    ax.set_ylabel("E_n = −13.6/n²  (эВ)")
    ax.set_title("Уровни водорода ↔ узлы S0–S9\n(оранжевые — φ-оптимальная траектория Фибоначчи)")
    ax.grid(axis="y", alpha=0.3)
    _save(fig, "2_hydrogen_levels.png")


def plot_dynamics():
    """График 3 — эволюция переменных X, ε, μ, τ во времени (две панели)."""
    t, Y = dynamics.integrate(dynamics.Params(mu_target=0.6))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))

    # Левая панель — динамическое ядро X, ε, μ.
    for k, lab, col in [(0, "X — нагрузка", "#c46849"),
                        (1, "ε — память", "#5e5d59"),
                        (2, "μ — проводимость", "#3a7d7b")]:
        a1.plot(t, Y[k], lw=2, label=lab, color=col)
    a1.axhline(C.X_STAR, ls=":", color="#c46849", lw=1.5, label=f"φ−1 = {C.X_STAR:.3f}")
    a1.set_xlabel("время t (норм.)")
    a1.set_ylabel("значение")
    a1.set_title("Ядро динамики: X, ε, μ")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3)

    # Правая панель — субъективное время τ (растёт замедляясь при нагрузке).
    a2.plot(t, Y[3], lw=2, color="#9c6b4a")
    a2.set_xlabel("время t (норм.)")
    a2.set_ylabel("τ — внутреннее время")
    a2.set_title("Субъективное время τ:  dτ/dt = 1/(1+X)")
    a2.grid(alpha=0.3)

    fig.suptitle("Динамическая система DIALOG QMT: четыре уравнения движения")
    _save(fig, "3_dynamics.png")


def plot_bifurcation():
    """График 4 — диаграмма бифуркации: φ-аттрактор при μ_crit = 0.5."""
    mu, X = dynamics.bifurcation_curve()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(mu, X, color="#c46849", lw=2, label="X*(μ) — стационарная нагрузка")
    ax.axvline(C.MU_CRIT, ls="--", color="gray", lw=1, label="μ_crit = 0.5 (бифуркация)")
    ax.axhline(C.X_STAR, ls=":", color="#5e5d59", lw=1)
    ax.scatter([C.MU_CRIT], [C.X_STAR], color="#c46849", zorder=5, s=60)
    ax.annotate(f"φ-аттрактор\n(0.5, {C.X_STAR:.3f})",
                (C.MU_CRIT, C.X_STAR), textcoords="offset points",
                xytext=(20, 20), fontsize=9)
    ax.set_xlabel("проводимость μ")
    ax.set_ylabel("стационарная нагрузка X*")
    ax.set_title("Бифуркация: φ-аттрактор X* = φ−1 при μ = μ_crit = 0.5")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    _save(fig, "4_bifurcation.png")


def plot_matrix6x6():
    """График 5 — спектр матрицы 6×6 и устойчивость к возмущению."""
    inv = matrix6x6.spectral_invariants()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))

    a1.stem(range(6), np.sort(inv.eigvals)[::-1])
    a1.set_xlabel("мода k")
    a1.set_ylabel("λ_k")
    a1.set_title(f"Спектр 6×6 (след = {inv.trace:.0f} = Sum-9)")
    a1.grid(alpha=0.3)

    deltas = np.linspace(0.0, 0.35, 60)
    gaps = [matrix6x6.spectral_invariants(b=0.5 + d).delta_min for d in deltas]
    a2.plot(deltas, gaps, color="#c46849", lw=2)
    a2.axvline(0.15, ls="--", color="gray", lw=1, label="δ_c ≈ 0.15 (порог)")
    a2.set_xlabel("возмущение связи δ")
    a2.set_ylabel("δλ_min")
    a2.set_title("Устойчивость к возмущению симметрии")
    a2.legend(fontsize=8)
    a2.grid(alpha=0.3)
    _save(fig, "5_matrix6x6.png")


def plot_sincerity():
    """График 6 — параметр искренности S(ε): теорема монотонности."""
    eps = np.linspace(0.0, 1.0, 100)
    fib = [sincerity.s_fibonacci(e) for e in eps]
    tun = [sincerity.s_tunnel(e) for e in eps]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.3))

    a1.plot(eps, fib, color="#c46849", lw=2)
    a1.set_xlabel("память ε")
    a1.set_ylabel("S_Fib — заселённость φ-узлов")
    a1.set_title("S_Fib(ε) убывает  (dS/dε < 0)")
    a1.grid(alpha=0.3)

    a2.plot(eps, tun, color="#5e5d59", lw=2)
    a2.set_xlabel("память ε")
    a2.set_ylabel("S_tunnel = T(ε)")
    a2.set_title("Прозрачность туннеля убывает: 0.1244 → 0.0775")
    a2.grid(alpha=0.3)
    _save(fig, "6_sincerity.png")


def main():
    print("Построение графиков DIALOG QMT…")
    plot_spectral_density()
    plot_hydrogen_levels()
    plot_dynamics()
    plot_bifurcation()
    plot_matrix6x6()
    plot_sincerity()
    print(f"Готово. Все графики в папке: {FIG_DIR}")


if __name__ == "__main__":
    main()
