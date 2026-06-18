"""
Слой «поток / трубки»: структура без углов.

Принцип (уточнение автора): геометрия — это ШАБЛОН и НАПРАВЛЕНИЕ («куда и как
двигаться»), а не жёсткая форма. Форма может быть любой — всё движется ПО
константам. Углов нигде нет: есть только пересечения гладких линий («трубок»),
которые состоят из этой геометрии и ею управляются. Узлы — НЕ угловые вершины,
а МЕСТА ПЕРЕСЕЧЕНИЯ гладкой кривой.

ИНВАРИАНТ здесь — не конкретная форма и не точное число пересечений (оно зависит
от проекции), а ЧИСЛА НАМОТКИ (a, b): они задают «как двигаться». Сама кривая —
лишь одна реализация шаблона.

Кривая задаётся целыми числами намотки (a, b) — берутся из узлов (например
центр-5 и π-узел-3 → a=5, b=3, как на референсной картинке Wolfram):

    2D-проекция:  x = sin(b t)·cos(a t),  y = sin(a t)
    на сфере √3:  x = sin(b t)cos(a t),  y = sin(b t)sin(a t),  z = cos(b t)

Центр (узел 5/0) — не точка, а МАЛАЯ ВЛОЖЕННАЯ ГЕОМЕТРИЯ со смещением δ.
Смещение δ = неточность зеркала −I (CP-нарушение) И одновременно знак того,
что у центра есть внутренняя структура (ψ₅s(0) ≠ 0 — амплитуда в центре).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

SHELL_R = math.sqrt(3)        # радиус оболочки-0
CENTER_NODE = 5               # центр = узел 5 (Надежда, ось, ψ(0)≠0)

# Параметры намотки по умолчанию: центр-5 и π-узел-3 (как на референсе a=5,b=3).
DEFAULT_A = 5
DEFAULT_B = 3


def _period(a: int, b: int) -> float:
    """Полный период кривой: t ∈ [0, lcm(a,b)·π]."""
    return math.lcm(a, b) * math.pi


def curve_2d(a: int = DEFAULT_A, b: int = DEFAULT_B, n: int = 2000):
    """2D-проекция кривой (как на референсной картинке). Возвращает (x, y)."""
    t = np.linspace(0.0, _period(a, b), n)
    return np.sin(b * t) * np.cos(a * t), np.sin(a * t)


def curve_on_sphere(a: int = DEFAULT_A, b: int = DEFAULT_B, n: int = 2000, R: float = SHELL_R):
    """Кривая-трубка на сфере-оболочке R=√3. Возвращает (x, y, z)."""
    t = np.linspace(0.0, _period(a, b), n)
    x = np.sin(b * t) * np.cos(a * t)
    y = np.sin(b * t) * np.sin(a * t)
    z = np.cos(b * t)
    return R * x, R * y, R * z


def lies_on_sphere(a: int = DEFAULT_A, b: int = DEFAULT_B, R: float = SHELL_R) -> bool:
    """[✓] Проверить, что кривая целиком лежит на сфере R (x²+y²+z² = R²)."""
    x, y, z = curve_on_sphere(a, b, n=500, R=R)
    r2 = x**2 + y**2 + z**2
    return bool(np.allclose(r2, R**2, atol=1e-9))


def is_smooth(a: int = DEFAULT_A, b: int = DEFAULT_B, n: int = 4000) -> bool:
    """[✓] «Углов нет»: касательная нигде не обращается в ноль (кривая гладкая, C¹)."""
    t = np.linspace(0.0, _period(a, b), n)
    dx = b * np.cos(b * t) * np.cos(a * t) - a * np.sin(b * t) * np.sin(a * t)
    dy = a * np.cos(a * t)
    speed = np.sqrt(dx**2 + dy**2)
    return bool(speed.min() > 1e-6)


def _segments_cross(a1, a2, b1, b2) -> bool:
    """Пересекаются ли отрезки a1a2 и b1b2 (строго)."""
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    d1 = cross(b1, b2, a1)
    d2 = cross(b1, b2, a2)
    d3 = cross(a1, a2, b1)
    d4 = cross(a1, a2, b2)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def winding_numbers() -> tuple[int, int]:
    """ИНВАРИАНТ потока — числа намотки (a, b). Задают «как двигаться», не форму."""
    return DEFAULT_A, DEFAULT_B


def approximate_crossings(a: int = DEFAULT_A, b: int = DEFAULT_B, n: int = 300) -> int:
    """ПРИБЛИЗИТЕЛЬНОЕ число пересечений 2D-проекции (НЕ инвариант теории!).

    Зависит от проекции и дискретизации. Инвариант — числа намотки (a,b);
    это лишь иллюстрация «узлы = пересечения трубок, а не углы».
    """
    x, y = curve_2d(a, b, n)
    pts = np.column_stack([x, y])
    seg_a = pts[:-1]
    seg_b = pts[1:]
    found = []
    s = len(seg_a)
    for i in range(s):
        ai, bi = seg_a[i], seg_b[i]
        for j in range(i + 2, s):
            if i == 0 and j == s - 1:
                continue  # концы замкнутой кривой — соседи
            if _segments_cross(ai, bi, seg_a[j], seg_b[j]):
                found.append(((ai + bi) / 2 + (seg_a[j] + seg_b[j]) / 2) / 2)
    # Слить близкие пересечения в один узел.
    nodes = []
    for p in found:
        if not any(np.hypot(p[0] - q[0], p[1] - q[1]) < 0.02 for q in nodes):
            nodes.append(p)
    return len(nodes)


# --- Центр как вложенная геометрия со смещением ------------------------------

@dataclass
class CenterGeometry:
    """Центр (узел 5/0): малая вложенная геометрия со смещением δ."""

    scale: float          # размер вложенной структуры (доля оболочки)
    offset: np.ndarray    # смещение центра от начала координат (вектор δ)
    delta: float          # |δ| — параметр асимметрии (CP-нарушение)
    psi0_nonzero: bool    # ψ₅s(0) ≠ 0 — у центра есть амплитуда (он не пуст)


def center_geometry(delta: float = 1e-3, direction=(1, 1, 1), scale: float = 0.12) -> CenterGeometry:
    """Центр = вложенный малый тетраэдр/шар, смещённый на δ.

    Смещение δ — неточность зеркала −I (CP-нарушение, перевес вещества) И знак
    внутренней структуры центра. δ = 0 вернуло бы «мёртвую» точную точку.
    """
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    return CenterGeometry(
        scale=scale,
        offset=delta * d,
        delta=delta,
        psi0_nonzero=True,
    )


def nested_tetrahedron(center: CenterGeometry):
    """Координаты малого вложенного тетраэдра в центре (со смещением δ)."""
    # Тот же тетраэдр-генератор tetA = {1,6,7,8}, уменьшенный и смещённый.
    base = np.array([(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)], dtype=float)
    return base * center.scale + center.offset


# --- Трискелион: 2D-проекция динамики вдоль 3-осной диагонали ----------------
# Куб, спроецированный перпендикулярно оси-зеркалу 1↔9 = (1,1,1): два узла оси
# уходят в центр (Горгона), шесть — в правильный шестиугольник; симметрия C₃ =
# три «ноги». Колени на внешнем круге = узлы на оболочке-0. Крылья = CP-нарушение.

from . import geometry as _G  # noqa: E402


def triskelion_projection(axis=(1, 9)):
    """Проекция вершин куба перпендикулярно оси-диагонали (по умолчанию 1↔9).

    Возвращает (coords2d, center_nodes, ring_nodes):
      coords2d — {узел: (x, y)} в плоскости проекции;
      center_nodes — узлы, ушедшие в центр (концы оси, «Горгона»);
      ring_nodes — 6 узлов шестиугольника (на круге).
    """
    a, b = axis
    n = np.array(_G.CUBE[b], float) - np.array(_G.CUBE[a], float)
    n = n / np.linalg.norm(n)
    # Ортонормированный базис плоскости, перпендикулярной оси.
    tmp = np.array([1.0, 0.0, 0.0])
    if abs(n @ tmp) > 0.9:
        tmp = np.array([0.0, 1.0, 0.0])
    e1 = tmp - (tmp @ n) * n
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)

    coords, center_nodes, ring_nodes = {}, [], []
    for node, v in _G.CUBE.items():
        v = np.array(v, float)
        p = (float(v @ e1), float(v @ e2))
        coords[node] = p
        (center_nodes if np.hypot(*p) < 1e-9 else ring_nodes).append(node)
    return coords, center_nodes, ring_nodes


def c3_arms(axis=(1, 9)):
    """Три «ноги» трискелиона = орбиты узлов под поворотом C₃ вокруг оси.

    Поворот на 120° вокруг (1,1,1) циклирует координаты (x,y,z)→(z,x,y).
    Возвращает список троек узлов (по 2 узла на ногу × 3 — два тетраэдра).
    """
    coords, _center, ring = triskelion_projection(axis)
    # Поворот C₃ по координатам для оси (1,1,1).
    def rot(node):
        x, y, z = _G.CUBE[node]
        target = (z, x, y)
        for k, v in _G.CUBE.items():
            if tuple(v) == target:
                return k
        return node
    seen, arms = set(), []
    for node in ring:
        if node in seen:
            continue
        orbit = [node]
        seen.add(node)
        nxt = rot(node)
        while nxt not in seen:
            orbit.append(nxt)
            seen.add(nxt)
            nxt = rot(nxt)
        arms.append(orbit)
    return arms


if __name__ == "__main__":
    a, b = winding_numbers()
    print(f"Шаблон-направление, числа намотки (a={a}, b={b}) — ИНВАРИАНТ:")
    print(f"  лежит на сфере √3 ? {lies_on_sphere(a, b)}")
    print(f"  гладкая (углов нет) ? {is_smooth(a, b)}")
    print(f"  пересечений (приблизит., не инвариант) ≈ {approximate_crossings(a, b)}")
    cg = center_geometry()
    print(f"\nЦентр: смещение |δ| = {cg.delta}, ψ(0)≠0 = {cg.psi0_nonzero}")
    print(f"  вложенный тетраэдр (вершина 0):\n  {nested_tetrahedron(cg)[0]}")
