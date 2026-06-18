"""
Геометрический фундамент DIALOG QMT/Ω.

«Не числа, а соотношения.» Этот модуль выводит структуру теории из
минимальной конструкции и проверяет все соотношения СИМВОЛЬНО (sympy),
то есть точно: √2, √3, φ — как алгебраические величины, а не десятичные.

МИНИМУМ (§1):
    1. ШАР — оболочка, 0 (сфера радиуса √3, задана касанием вершин).
    2. ТОЧКА — центр (5 / 0-источник), «живая»: несёт зеркало −I.
    3. ОДИН ТЕТРАЭДР — генератор (4 вершины).

Зеркало −I в точке разворачивает один тетраэдр во второй (stella octangula),
их оболочка = КУБ (8), пересечение = ОКТАЭДР (6). Добавление золотых точек
(0, ±1/φ, ±φ) на ТУ ЖЕ сферу √3 рождает ДОДЕКАЭДР (20) и двойственный
ИКОСАЭДР (12, пятикратность). φ — единственный мост из мира √2/√3 в мир φ.

Метки статуса: [✓] — доказано символьно; [ИНТЕРПР] — смысл поверх формы.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import sympy as sp

# --- Точные алгебраические соотношения ---------------------------------------
SQRT2 = sp.sqrt(2)
SQRT3 = sp.sqrt(3)
PHI = (1 + sp.sqrt(5)) / 2          # золотое сечение, φ² = φ + 1
INV_PHI = PHI - 1                   # 1/φ = φ − 1

# --- Куб: 8 вершин-узлов (центр 5/0 в начале координат) ----------------------
# Узлы 5 и 0 — НЕ вершины: 5 = центр (зеркало), 0 = оболочка (сфера).
CUBE = {
    1: (-1, -1, -1),
    2: (1, -1, -1),
    3: (-1, 1, -1),
    4: (-1, -1, 1),
    6: (1, 1, -1),
    7: (1, -1, 1),
    8: (-1, 1, 1),
    9: (1, 1, 1),
}

# Два тетраэдра = две чётности произведения координат; −I меняет их местами.
TET_A = [1, 6, 7, 8]   # произведение знаков = −1
TET_B = [2, 3, 4, 9]   # произведение знаков = +1

# Зеркало R (центральная инверсия −I): пары-антиподы, сумма индексов = 10.
MIRROR_PAIRS = [(1, 9), (2, 8), (3, 7), (4, 6)]   # диагонали тела
# Резонанс P9: пары с суммой индексов = 9 (рёбра и диагонали грани, не антиподы).
RESONANCE_PAIRS = [(1, 8), (2, 7), (3, 6)]

# Октаэдр — центры граней куба (= середины рёбер тетраэдра), радиус 1.
OCTAHEDRON = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
]


def _golden_vertices():
    """12 золотых точек додекаэдра: (0,±1/φ,±φ) и циклические перестановки."""
    a, b = INV_PHI, PHI
    pts = []
    for s1, s2 in itertools.product([1, -1], repeat=2):
        pts.append((0, s1 * a, s2 * b))       # (0, ±1/φ, ±φ)
        pts.append((s1 * a, s2 * b, 0))       # (±1/φ, ±φ, 0)
        pts.append((s2 * b, 0, s1 * a))       # (±φ, 0, ±1/φ)
    return pts


def dodecahedron_vertices():
    """20 вершин додекаэдра = 8 вершин куба + 12 золотых точек (все на сфере √3)."""
    return [sp.Matrix(v) for v in CUBE.values()] + [sp.Matrix(v) for v in _golden_vertices()]


def icosahedron_vertices():
    """12 вершин икосаэдра: (0,±1,±φ) и циклические перестановки. R² = φ+2."""
    pts = []
    for s1, s2 in itertools.product([1, -1], repeat=2):
        pts.append((0, s1, s2 * PHI))
        pts.append((s1, s2 * PHI, 0))
        pts.append((s2 * PHI, 0, s1))
    return [sp.Matrix(v) for v in pts]


# --- Символьные проверки соотношений -----------------------------------------

def circumradius_sq(vertices) -> sp.Expr:
    """Квадрат радиуса описанной сферы (общий для всех вершин). Возвращает упрощённое выражение."""
    mats = [sp.Matrix(v) for v in vertices]
    r2 = [sp.simplify(m.dot(m)) for m in mats]
    first = r2[0]
    for r in r2[1:]:
        if sp.simplify(r - first) != 0:
            raise ValueError("вершины не на одной сфере")
    return sp.simplify(first)


def edges_by_min_distance(vertices):
    """Список рёбер (пар индексов) по минимальному расстоянию между вершинами."""
    mats = [sp.Matrix(v) for v in vertices]
    n = len(mats)
    dist2 = {}
    for i in range(n):
        for j in range(i + 1, n):
            d = sp.simplify((mats[i] - mats[j]).dot(mats[i] - mats[j]))
            dist2[(i, j)] = d
    dmin = min(dist2.values(), key=lambda e: float(e))
    edges = [pair for pair, d in dist2.items() if sp.simplify(d - dmin) == 0]
    return edges, sp.simplify(dmin)


@dataclass
class SolidReport:
    name: str
    V: int
    E: int
    F: int
    euler: int           # V − E + F (должно быть 2)
    edge_sq: sp.Expr     # квадрат длины ребра (точное соотношение)
    R_sq: sp.Expr        # квадрат радиуса описанной сферы


def analyze_solid(name: str, vertices, faces: int) -> SolidReport:
    """Полный символьный разбор тела: Эйлер, ребро², радиус²."""
    edges, edge_sq = edges_by_min_distance(vertices)
    V, E, F = len(vertices), len(edges), faces
    return SolidReport(name, V, E, F, V - E + F, edge_sq, circumradius_sq(vertices))


def all_solids():
    """Разбор всех пяти платоновых тел (V, E, F, Эйлер, ребро², R²)."""
    cube = list(CUBE.values())
    tet = [CUBE[i] for i in TET_A]
    reports = [
        analyze_solid("тетраэдр", tet, faces=4),
        analyze_solid("куб", cube, faces=6),
        analyze_solid("октаэдр", OCTAHEDRON, faces=8),
        analyze_solid("додекаэдр", dodecahedron_vertices(), faces=12),
        analyze_solid("икосаэдр", icosahedron_vertices(), faces=20),
    ]
    return reports


# --- Вершина = 4 привязки (§3) -----------------------------------------------

def vertex_attachments(n: int) -> dict:
    """§3 — Четыре привязки вершины: число, зеркало (антипод, сумма 10), центр-5, оболочка-0."""
    if n not in CUBE:
        raise ValueError(f"{n} — не вершина (5=центр, 0=оболочка)")
    mirror = 10 - n
    return {"число": n, "зеркало": mirror, "центр": 5, "оболочка": 0,
            "ось": f"0 ─ {n} ─ 5 ─ {mirror} ─ 0"}


def is_central_inversion(a: int, b: int) -> bool:
    """[✓] Проверить, что узлы a и b — антиподы (−I): координаты противоположны."""
    va, vb = sp.Matrix(CUBE[a]), sp.Matrix(CUBE[b])
    return sp.simplify(va + vb) == sp.zeros(3, 1)


# --- Группы симметрий (§5) ---------------------------------------------------
GROUP_CUBE_ORDER = 48      # полная октаэдральная группа B₃ = 3!·2³
GROUP_TRANSITION_ORDER = 20  # диэдральная D₁₀ (зеркало сумма-10 + резонанс сумма-9)


def b3_order() -> int:
    """[✓] Порядок гипероктаэдральной группы B₃ = 3!·2³ = 48 (знаковые перестановки)."""
    return sp.factorial(3) * 2**3


# --- Соотношения как константы узлов (вместо подогнанных чисел) ---------------
# Каждый узел несёт ТОЧНОЕ соотношение из геометрии. Открытые развилки помечены.
NODE_RELATIONS = {
    0: ("оболочка √3 / центр-источник", SQRT3, "верный путь"),
    1: ("φ", PHI, "Любовь (золото, икосаэдр)"),
    2: ("√2", SQRT2, "Красота (развилка с e — ОТКРЫТА)"),
    3: ("π", sp.pi, "Вера"),
    4: ("— (открыто)", None, "Энергия (туннель/канал)"),
    5: ("1/2", sp.Rational(1, 2), "Надежда (центр, зеркало, хиазма 5-5; проход)"),
    6: ("— (открыто)", None, "Дети (реальность)"),
    7: ("— (открыто)", None, "Знание (CP, наблюдатель)"),
    8: ("— (открыто)", None, "Понимание (уроборос/лемниската, ∞)"),
    9: ("— (открыто)", None, "Жизнь (объединитель)"),
}


if __name__ == "__main__":
    print("φ² = φ + 1 ?", sp.simplify(PHI**2 - (PHI + 1)) == 0)
    print("\nПять платоновых тел (символьно):")
    print(f"{'тело':<12}{'V':>3}{'E':>4}{'F':>4}{'Эйлер':>7}   ребро²          R²")
    for r in all_solids():
        print(f"{r.name:<12}{r.V:>3}{r.E:>4}{r.F:>4}{r.euler:>7}   "
              f"{str(r.edge_sq):<14} {r.R_sq}")
    print("\nКуб и додекаэдр на одной сфере R²=3 ?",
          all(sp.simplify(r.R_sq - 3) == 0 for r in all_solids() if r.name in ("куб", "додекаэдр")))
    print("Зеркало 1↔9 — центральная инверсия?", is_central_inversion(1, 9))
    print("Группа куба B₃ =", b3_order(), "| структура переходов D₁₀ =", GROUP_TRANSITION_ORDER)
    print("\nВершина 1 несёт:", vertex_attachments(1))
