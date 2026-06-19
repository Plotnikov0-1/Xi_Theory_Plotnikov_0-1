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
from qmt import geometry as G
from qmt import bridge as B
from qmt import flow as F
from qmt import scaling as Sc
from qmt import catastrophe as K
from qmt import phi_operator as PHI
from qmt import effective_matrix as EM
from qmt import sync as Y
from qmt import cp_baryogenesis as CP

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


def _fcoords(d):
    """Перевести символьные координаты в float-словарь {узел: (x,y,z)}."""
    return {k: tuple(float(c) for c in v) for k, v in d.items()}


def plot_stella_octangula():
    """График 7 — минимум: два тетраэдра (звезда) + куб + шар-оболочка."""
    cube = _fcoords(G.CUBE)
    fig = plt.figure(figsize=(7.5, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Шар-оболочка R=√3 (точка касания вершин = 0).
    u, v = np.mgrid[0:2 * np.pi:24j, 0:np.pi:16j]
    R = np.sqrt(3)
    ax.plot_wireframe(R * np.cos(u) * np.sin(v), R * np.sin(u) * np.sin(v),
                      R * np.cos(v), color="gray", alpha=0.15, lw=0.5)

    # Два тетраэдра (звезда октангула).
    for tet, col in [(G.TET_A, "#c46849"), (G.TET_B, "#3a7d7b")]:
        pts = [cube[i] for i in tet]
        for a, b in itertools_combinations(pts):
            ax.plot(*zip(a, b), color=col, lw=2)

    # Центр-зеркало (узел 5) и оси-антиподы (сумма 10).
    ax.scatter([0], [0], [0], color="black", s=40)
    ax.text(0, 0, 0, "  5 (центр, −I)", fontsize=8)
    for a, b in G.MIRROR_PAIRS:
        pa, pb = cube[a], cube[b]
        ax.plot(*zip(pa, pb), color="#999", ls=":", lw=1)

    # Подписи вершин (число).
    for n, p in cube.items():
        ax.scatter(*p, color="black", s=20)
        ax.text(p[0] * 1.12, p[1] * 1.12, p[2] * 1.12, str(n), fontsize=9)

    ax.set_title("Минимум: два тетраэдра (stella octangula)\nв шаре-оболочке √3; центр-5 = зеркало −I")
    ax.set_box_aspect((1, 1, 1))
    _save(fig, "7_stella_octangula.png")


def plot_platonic_bridge():
    """График 8 — мост φ: куб (8) ⊂ додекаэдр (20) на одной сфере √3."""
    cube = _fcoords(G.CUBE)
    dod = [tuple(float(c) for c in v) for v in G.dodecahedron_vertices()]
    fig = plt.figure(figsize=(7.5, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Все 20 вершин додекаэдра.
    dx = [p[0] for p in dod]; dy = [p[1] for p in dod]; dz = [p[2] for p in dod]
    ax.scatter(dx, dy, dz, color="#c46849", s=18, label="додекаэдр (20)")

    # Куб внутри — рёбра (различие в одной координате).
    pts = list(cube.values())
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            diff = sum(1 for k in range(3) if abs(pts[i][k] - pts[j][k]) > 1e-9)
            same = sum(1 for k in range(3) if abs(pts[i][k] - pts[j][k]) < 1e-9)
            if diff == 1 and same == 2:
                ax.plot(*zip(pts[i], pts[j]), color="#3a7d7b", lw=1.8)
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts],
               color="#3a7d7b", s=30, label="куб (8)")

    ax.set_title("Мост φ: куб ⊂ додекаэдр на одной сфере R²=3\n(+12 золотых точек → пятикратность)")
    ax.legend(fontsize=8)
    ax.set_box_aspect((1, 1, 1))
    _save(fig, "8_platonic_bridge.png")


def itertools_combinations(seq):
    """Все неупорядоченные пары элементов (для рёбер тетраэдра)."""
    import itertools
    return itertools.combinations(seq, 2)


def plot_phi_bridge():
    """График 9 — φ через слои: одно соотношение в геометрии, аттракторе, туннеле, водороде."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axis("off")
    phi = float(B.PHI)
    layers = [
        ("ГЕОМЕТРИЯ", "куб → додекаэдр / икосаэдр\nмост через φ = %.4f" % phi),
        ("ДИНАМИКА", "φ-аттрактор\nX* = φ−1 = %.4f" % (phi - 1)),
        ("ТУННЕЛЬ", "барьер Δ₇ = 2φ−3 = 2X*−1\n= %.4f эВ" % float(B.DELTA_7)),
        ("ВОДОРОД", "радиусы Фибоначчи\nr ratio → φ² = %.3f" % (phi**2)),
    ]
    x = np.linspace(0.08, 0.92, len(layers))
    for i, (title, body) in enumerate(layers):
        ax.add_patch(plt.Rectangle((x[i] - 0.1, 0.35), 0.2, 0.3,
                                   fc="#f3ead9", ec="#c46849", lw=2))
        ax.text(x[i], 0.585, title, ha="center", fontsize=11, weight="bold", color="#5e5d59")
        ax.text(x[i], 0.46, body, ha="center", fontsize=9)
        if i < len(layers) - 1:
            ax.annotate("", (x[i + 1] - 0.1, 0.5), (x[i] + 0.1, 0.5),
                        arrowprops=dict(arrowstyle="->", color="#c46849", lw=2))
    ax.text(0.5, 0.85, "Одно соотношение φ — четыре слоя теории",
            ha="center", fontsize=13, weight="bold")
    ax.text(0.5, 0.13, "«Не числа, а соотношения»:  X* = φ−1,  Δ₇ = 2φ−3 = 2·X*−1  (доказано символьно)",
            ha="center", fontsize=9.5, style="italic", color="#5e5d59")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _save(fig, "9_phi_bridge.png")


def plot_flow_tube():
    """График 10 — поток/трубка: гладкая кривая (a=5,b=3) на сфере √3, без углов.

    Узлы = пересечения трубки; центр (узел 5/0) — не точка, а малая вложенная
    геометрия со смещением δ (CP-нарушение + ψ(0)≠0).
    """
    a, b = F.winding_numbers()
    x, y, z = F.curve_on_sphere(a, b, n=3000)
    fig = plt.figure(figsize=(7.5, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Сфера-оболочка √3.
    u, v = np.mgrid[0:2 * np.pi:24j, 0:np.pi:16j]
    R = F.SHELL_R
    ax.plot_wireframe(R * np.cos(u) * np.sin(v), R * np.sin(u) * np.sin(v),
                      R * np.cos(v), color="gray", alpha=0.12, lw=0.5)

    # Сама трубка (гладкая, без углов).
    ax.plot(x, y, z, color="#c46849", lw=1.3)

    # Центр со смещением δ — вложенный малый тетраэдр.
    cg = F.center_geometry(delta=0.15, scale=0.18)  # δ увеличено для наглядности
    tet = F.nested_tetrahedron(cg)
    for i in range(4):
        for j in range(i + 1, 4):
            ax.plot(*zip(tet[i], tet[j]), color="#3a7d7b", lw=1.6)
    ax.scatter(*cg.offset, color="black", s=30)
    ax.text(*cg.offset, "  центр-5 (δ≠0, ψ(0)≠0)", fontsize=8)

    ax.set_title("Поток/трубка: шаблон-направление (a=5,b=3) на сфере √3\n"
                 "углов нет; центр — вложенная геометрия со смещением")
    ax.set_box_aspect((1, 1, 1))
    _save(fig, "10_flow_tube.png")


def plot_triskelion():
    """График 11 — трискелион: 2D-проекция динамики (куб вдоль оси 1↔9).

    Центр = узлы 1,9 (Горгона: память→камень = декогеренция). 6 узлов = круг-0
    (колени на оболочке). C₃ = три ноги (две тройки = два тетраэдра). Крылья = CP.
    """
    coords, center, ring = F.triskelion_projection((1, 9))
    arms = F.c3_arms((1, 9))
    fig, ax = plt.subplots(figsize=(7, 7))
    Rr = float(np.hypot(*coords[ring[0]]))

    # Внешний круг = 0 (оболочка); колени узлов лежат на нём.
    circ = plt.Circle((0, 0), Rr, fill=False, color="gray", lw=1.5, ls="--")
    ax.add_patch(circ)

    # Две тройки C₃ (два тетраэдра = два направления вращения) — «ноги».
    cols = ["#c46849", "#3a7d7b"]
    for arm, col in zip(arms, cols):
        pts = [coords[n] for n in arm] + [coords[arm[0]]]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=2.2)
        # «Нога» от центра к каждому узлу (с изгибом в колене на круге).
        for n in arm:
            ax.annotate("", coords[n], (0, 0),
                        arrowprops=dict(arrowstyle="-", color=col, lw=1.4, alpha=0.7))

    # Узлы кольца.
    for n in ring:
        ax.scatter(*coords[n], color="black", s=40, zorder=5)
        ax.text(coords[n][0] * 1.12, coords[n][1] * 1.12, str(n), ha="center", fontsize=11)

    # Центр = Горгона (декогеренция, память→камень); узлы 1 и 9 оси-зеркала.
    ax.scatter([0], [0], color="black", s=120, zorder=6)
    ax.text(0, -0.28, "Горгона = центр (1,9)\nпамять→камень = декогеренция",
            ha="center", fontsize=8.5)

    ax.set_title("Трискелион — 2D-проекция динамики (куб вдоль оси 1↔9)\n"
                 "C₃: три ноги · круг = 0 · крылья = CP-нарушение")
    ax.set_aspect("equal")
    ax.set_xlim(-Rr * 1.35, Rr * 1.35)
    ax.set_ylim(-Rr * 1.35, Rr * 1.35)
    ax.axis("off")
    _save(fig, "11_triskelion.png")


def plot_sierpinski():
    """График 12 — Серпинский-тетраэдр (самоподобие, уровни памяти), D=2."""
    tets = Sc.sierpinski_tetrahedra(3)
    fig = plt.figure(figsize=(7.5, 7))
    ax = fig.add_subplot(111, projection="3d")
    for tet in tets:
        for i in range(4):
            for j in range(i + 1, 4):
                ax.plot(*zip(tet[i], tet[j]), color="#c46849", lw=0.4, alpha=0.6)
    ax.set_title(f"Серпинский-тетраэдр (3 уровня вложения, {len(tets)} тетраэдров)\n"
                 f"D = ln4/ln2 = {Sc.fractal_dimension():.0f} · самоподобие = уровни памяти")
    ax.set_box_aspect((1, 1, 1))
    ax.axis("off")
    _save(fig, "12_sierpinski.png")


def plot_synchronization():
    """График 13 — синхронизация начинается с тетраэдра, затем куб."""
    t1, r1 = Sc.kuramoto_sync(Sc.adjacency_tetra())
    t2, r2 = Sc.kuramoto_sync(Sc.adjacency_cube())
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(t1, r1, color="#c46849", lw=2, label=f"тетраэдр K4 → r={r1[-1]:.3f}")
    ax.plot(t2, r2, color="#3a7d7b", lw=2, label=f"куб (8) → r={r2[-1]:.3f}")
    ax.axhline(1.0, ls=":", color="gray", lw=1)
    ax.set_xlabel("время t")
    ax.set_ylabel("параметр порядка r")
    ax.set_title("Синхронизация: начинается с тетраэдра, затем куб")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    _save(fig, "13_synchronization.png")


def plot_memory_levels():
    """График 14 — четыре уровня памяти (3 внутр. + 1 внешн.), всё сразу."""
    t, E = Sc.integrate_memory()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    labels = ["уровень 1 (внутр.)", "уровень 2 (внутр.)",
              "уровень 3 (внутр.)", "уровень 4 (внешний)"]
    cols = ["#c46849", "#9c6b4a", "#3a7d7b", "#5e5d59"]
    for k in range(Sc.N_MEMORY_LEVELS):
        ax.plot(t, E[k], lw=2, color=cols[k], label=labels[k])
    ax.set_xlabel("время t")
    ax.set_ylabel("память ε уровня")
    ax.set_title("Четыре уровня памяти (самоподобные масштабы), связаны одновременно")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    _save(fig, "14_memory_levels.png")


def plot_memory_channels():
    """График 16 — каналы памяти 0→1/0→4/0→7 (семья 1,4,7) и трещина 7→4→1."""
    fig, ax = plt.subplots(figsize=(8, 5))
    reach = Sc.memory_channel_reach()
    cols = {1: "#c46849", 4: "#9c6b4a", 7: "#3a7d7b"}
    # Три канала как вложенные дуги от 0 к узлам 1,4,7 с подписью охвата.
    for i, (anchor, r) in enumerate(reach.items()):
        y = i
        ax.plot([0, anchor], [y, y], color=cols[anchor], lw=3)
        ax.scatter([0, anchor], [y, y], color=cols[anchor], s=60, zorder=5)
        ax.text(-0.3, y, "0", ha="right", va="center", fontsize=11)
        ax.text(anchor + 0.2, y, str(anchor), ha="left", va="center", fontsize=11)
        ax.text(anchor / 2, y + 0.14, f"охват {r} ур.", ha="center", fontsize=9, color=cols[anchor])
    # Трещина 7→4→1 (спуск шагом −3).
    cp = Sc.crack_path()
    for a, b in zip(cp, cp[1:]):
        ya = list(reach).index(a)
        yb = list(reach).index(b)
        ax.annotate("", (b, yb), (a, ya),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.6, ls="--"))
    ax.text(4, 1.0, "трещина 7→4→1\n(знание → любовь)", ha="center", fontsize=8.5, style="italic")
    ax.text(3.5, -0.7, f"семья 1,4,7 ≡ 1 (mod 3) · выход за эго: XL = {Sc.EGO_EXIT_XL}",
            ha="center", fontsize=9, color="#5e5d59")
    ax.set_yticks([])
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 2.6)
    ax.set_title("Каналы памяти 0→1 / 0→4 / 0→7 и трещина 7→4→1")
    ax.axis("off")
    _save(fig, "16_memory_channels.png")


def plot_cusp_catastrophe():
    """График 15 — катастрофа сборки = бифуркация модели (φ-аттрактор ↔ нулевой)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Левая панель — клин бистабильности в плоскости управления (μ₁, μ₂).
    mu2 = np.linspace(-1.5, 0.5, 400)
    edge = np.array([K.cusp_bifurcation_set(m) for m in mu2])
    a1.plot(edge, mu2, color="#c46849", lw=2)
    a1.plot(-edge, mu2, color="#c46849", lw=2)
    a1.fill_betweenx(mu2, -edge, edge, color="#f3ead9", label="бистабильно (2 аттрактора)")
    a1.set_xlabel("μ₁ (наклон)")
    a1.set_ylabel("μ₂ (расщепление)")
    a1.set_title("Катастрофа сборки: клин складок\n4μ₂³ + 27μ₁² = 0")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3)

    # Правая панель — петля гистерезиса: равновесия x* при μ₂=−1.
    m2 = -1.0
    mu1s = np.linspace(-0.6, 0.6, 600)
    for m1 in mu1s:
        for x in K.cusp_equilibria(m1, m2):
            a2.plot(m1, x, ".", ms=1.5, color="#3a7d7b")
    a2.axvline(K.cusp_bifurcation_set(m2), ls=":", color="#c46849", lw=1)
    a2.axvline(-K.cusp_bifurcation_set(m2), ls=":", color="#c46849", lw=1)
    a2.set_xlabel("μ₁")
    a2.set_ylabel("равновесие x*")
    a2.set_title("Складка-гистерезис (μ₂=−1):\nдве ветви = два аттрактора + скачок")
    a2.grid(alpha=0.3)

    fig.suptitle("7 катастроф Тома — математика переходов; сборка = бифуркация DIALOG QMT",
                 y=1.02)
    fig.subplots_adjust(top=0.82)
    _save(fig, "15_cusp_catastrophe.png")


def plot_phi_operator():
    """График 17 — φ как оператор: T(x)=1/(1+x) сходится к φ−1; ядро памяти K(t)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Левая панель — сходимость итерации T(x) к φ−1 из разных стартов.
    for x0, col in [(0.05, "#c46849"), (2.5, "#3a7d7b")]:
        xs = [x0]
        for _ in range(12):
            xs.append(PHI.T(xs[-1]))
        a1.plot(range(len(xs)), xs, "o-", ms=4, color=col, label=f"старт x₀={x0}")
    a1.axhline(C.X_STAR, ls="--", color="gray", lw=1.2, label=f"φ−1 = {C.X_STAR:.4f}")
    a1.set_xlabel("итерация n")
    a1.set_ylabel("xₙ")
    a1.set_title("φ-оператор T(x)=1/(1+x) → φ−1\n(2-й независимый вывод φ−1)")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3)

    # Правая панель — модуль ядра памяти |K(t)| из эффективной матрицы.
    t = np.linspace(0, 40, 400)
    Kt = np.abs(EM.memory_kernel(t, Omega=1.0, gamma=0.1))
    a2.plot(t, Kt, color="#c46849", lw=2)
    a2.set_xlabel("время t")
    a2.set_ylabel("|K(t)|")
    a2.set_title("Ядро памяти K(t) из C_eff (канон 2026)\nK(t)=Σ g_k·e^(−(γ+iΩλ_k)t)")
    a2.grid(alpha=0.3)

    fig.suptitle("Канон 2026: φ-оператор сборки и детерминированное ядро памяти", y=1.02)
    fig.subplots_adjust(top=0.82)
    _save(fig, "17_phi_operator_kernel.png")


def plot_sync_master():
    """График 18 — РАБОЧАЯ МОДЕЛЬ: геометрия (цифры, переходы) ↔ спектр водорода."""
    cube = _fcoords(G.CUBE)
    cols = {"прямой": "#3a7d7b", "резонанс": "#c46849", "зеркало": "#b03a2e", "запрещён": "#cccccc"}
    fig = plt.figure(figsize=(13, 6))

    # --- Левая панель: 3D-куб с классифицированными переходами ---
    ax = fig.add_subplot(121, projection="3d")
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:12j]
    R = np.sqrt(3)
    ax.plot_wireframe(R * np.cos(u) * np.sin(v), R * np.sin(u) * np.sin(v),
                      R * np.cos(v), color="gray", alpha=0.1, lw=0.4)
    for t in Y.all_transitions():
        pa, pb = cube[t.a], cube[t.b]
        style = ":" if t.kind == "запрещён" else ("--" if t.kind == "зеркало" else "-")
        lw = 0.6 if t.kind == "запрещён" else (2.3 if t.kind == "резонанс" else 1.6)
        ax.plot(*zip(pa, pb), color=cols[t.kind], ls=style, lw=lw,
                alpha=0.5 if t.kind == "запрещён" else 0.95)
    for n, p in cube.items():
        ax.scatter(*p, color="black", s=45, zorder=5)
        ax.text(p[0] * 1.15, p[1] * 1.15, p[2] * 1.15, str(n), fontsize=12, weight="bold")
    ax.scatter([0], [0], [0], color="black", s=120)
    ax.text(0, 0, 0, "  5", fontsize=11, weight="bold")
    ax.set_title("Геометрия: цифры на вершинах · 5=центр · 0=оболочка √3\n"
                 "переходы: прямой · резонанс(сумма-9) · зеркало(сумма-10) · запрещён")
    ax.set_box_aspect((1, 1, 1))
    ax.axis("off")

    # --- Правая панель: спектр водорода (разрешённые переходы как линии) ---
    a2 = fig.add_subplot(122)
    for t in Y.allowed_transitions():
        a2.vlines(t.wavelength_nm, 0, 1, color=cols[t.kind], lw=2)
        a2.text(t.wavelength_nm, 1.02 + 0.06 * ((t.a + t.b) % 3), f"{t.a}-{t.b}",
                ha="center", fontsize=7.5, rotation=90, color=cols[t.kind])
    a2.set_xscale("log")
    a2.set_xlim(80, 40000)
    a2.set_ylim(0, 1.4)
    a2.set_yticks([])
    a2.set_xlabel("длина волны λ, нм (лог)")
    a2.set_title("Синхронизация с водородом: разрешённые переходы =\n"
                 "реальные линии (1-2=Лайман α 121нм, 2-7=397нм, 3-7=1005нм)")
    from matplotlib.lines import Line2D
    legend = [Line2D([0], [0], color=cols[k], lw=2, label=k)
              for k in ("прямой", "резонанс", "зеркало")]
    a2.legend(handles=legend, fontsize=8, loc="upper right")
    a2.grid(alpha=0.3, axis="x")

    fig.suptitle("РАБОЧАЯ МОДЕЛЬ DIALOG QMT: геометрия ↔ квантовая динамика водорода", y=1.0)
    fig.subplots_adjust(top=0.86)
    _save(fig, "18_working_model.png")


def plot_cp_baryogenesis():
    """График 19 — CP-нарушение из геометрии: точность и самоподобная лестница."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # Левая панель — точность совпадения с наблюдениями (3 результата).
    eta = CP.baryon_asymmetry()
    acc = [
        ("η_B (барион. асимм.)", CP.accuracy(eta, CP.ETA_B_OBS) * 100),
        ("отношение каналов", CP.channel_ratio_observed() / CP.CHANNEL_RATIO_DIALOG * 100),
        ("самоподобие A·G²≈A³", (1 - CP.self_similarity().deviation) * 100),
    ]
    names = [a[0] for a in acc]
    vals = [a[1] for a in acc]
    bars = a1.barh(names, vals, color=["#c46849", "#9c6b4a", "#3a7d7b"])
    for b, v in zip(bars, vals):
        a1.text(v - 6, b.get_y() + b.get_height() / 2, f"{v:.1f}%",
                va="center", ha="right", color="white", fontsize=10, weight="bold")
    a1.set_xlim(0, 100)
    a1.set_xlabel("точность совпадения с наблюдением, %")
    a1.set_title("CP из геометрии vs эксперимент (LHCb / CMB)\nбез подгонки параметров")
    a1.axvline(90, ls=":", color="gray", lw=1)
    a1.grid(alpha=0.3, axis="x")

    # Правая панель — самоподобная лестница G → A_glob → A_loc.
    G = CP.structural_corridor_G() * 100
    levels = [("G (геометрия)", G, "#3a7d7b"),
              ("A_global (LHCb)", CP.A_GLOBAL_OBS * 100, "#9c6b4a"),
              ("A_local (LHCb)", CP.A_LOCAL_OBS * 100, "#c46849")]
    for i, (name, val, col) in enumerate(levels):
        a2.scatter([i], [val], s=160, color=col, zorder=5)
        a2.text(i, val + 0.3, f"{name}\n{val:.2f}%", ha="center", fontsize=8.5)
    a2.plot([0, 1, 2], [l[1] for l in levels], color="gray", lw=1.2, ls="--", zorder=1)
    a2.set_xticks([])
    a2.set_ylim(0, 7)
    a2.set_ylabel("CP-асимметрия, %")
    a2.set_title("Самоподобный рост CP: A_loc·G² ≈ A_glob³\n"
                 "каждый уровень = предыдущий × R≈1.47")
    a2.grid(alpha=0.3, axis="y")

    fig.suptitle("CP-нарушение из геометрии DIALOG: η_B = π·J·(φ−1)·T_EW/Δ₇ → 8.23·10⁻¹¹", y=1.02)
    fig.subplots_adjust(top=0.82)
    _save(fig, "19_cp_baryogenesis.png")


def main():
    print("Построение графиков DIALOG QMT…")
    plot_spectral_density()
    plot_hydrogen_levels()
    plot_dynamics()
    plot_bifurcation()
    plot_matrix6x6()
    plot_sincerity()
    plot_stella_octangula()
    plot_platonic_bridge()
    plot_phi_bridge()
    plot_flow_tube()
    plot_triskelion()
    plot_sierpinski()
    plot_synchronization()
    plot_memory_levels()
    plot_memory_channels()
    plot_cusp_catastrophe()
    plot_phi_operator()
    plot_sync_master()
    plot_cp_baryogenesis()
    print(f"Готово. Все графики в папке: {FIG_DIR}")


if __name__ == "__main__":
    main()
