"""
МОСТ: геометрия ↔ динамика/физика.

«Не числа, а соотношения» — этот модуль показывает РАСЧЁТОМ, что величины из
уравнений движения и физики являются теми же геометрическими соотношениями.

Доказано символьно [✓]:
    X* (φ-аттрактор)      = φ − 1 = 1/φ          — золотой мост (куб→додекаэдр)
    Δ₇ (барьер туннеля)   = √5 − 2 = 2φ − 3 = 2·X* − 1   — золото, прямо из аттрактора
    √5                    = 2φ − 1
    ребро² додекаэдра     = 6 − 2√5 = 2·(1 − Δ₇)  — золотое тело ↔ барьер туннеля
    оболочка R            = √3 (= радиус куба и додекаэдра) — узел 0
    ребро октаэдра        = √2                     — узел 2 (кандидат)

И геометрия ↔ квант: зеркало −I (сумма 10) = оператор X⊗X⊗X на 3 кубитах.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp

from . import geometry as G

# Символьные величины обоих слоёв.
PHI = G.PHI
X_STAR = PHI - 1                 # φ-аттрактор динамики (= 1/φ)
DELTA_7 = sp.sqrt(5) - 2         # барьер туннеля S6→S7
SQRT2 = sp.sqrt(2)
SQRT3 = sp.sqrt(3)


@dataclass
class Bridge:
    name: str            # что связываем
    physics: str         # выражение в физике/динамике
    geometry: str        # то же как геометрическое соотношение
    identity: sp.Expr    # разность (должна быть 0)
    holds: bool          # тождество выполнено символьно


def _b(name, phys, geom, lhs, rhs) -> Bridge:
    diff = sp.simplify(lhs - rhs)
    return Bridge(name, phys, geom, diff, diff == 0)


def all_bridges():
    """Список проверенных мостов геометрия ↔ физика."""
    return [
        _b("φ-аттрактор", "X* (стационарная нагрузка)", "φ−1 = 1/φ (золотой мост)",
           X_STAR, 1 / PHI),
        _b("барьер туннеля", "Δ₇ = √5−2 (S6→S7)", "2φ−3 = 2·X*−1 (золото из аттрактора)",
           DELTA_7, 2 * X_STAR - 1),
        _b("корень √5", "√5 (в Δ₇ и серии)", "2φ−1 (золотая алгебра)",
           sp.sqrt(5), 2 * PHI - 1),
        _b("ребро додекаэдра", "6−2√5", "2·(1−Δ₇) (золотое тело ↔ барьер)",
           6 - 2 * sp.sqrt(5), 2 * (1 - DELTA_7)),
        _b("оболочка-0", "R оболочки", "√3 = радиус куба и додекаэдра (узел 0)",
           SQRT3, G.circumradius_sq(list(G.CUBE.values())) ** sp.Rational(1, 2)),
        _b("узел 2 (кандидат)", "константа узла 2", "√2 = ребро октаэдра",
           SQRT2, sp.sqrt(G.analyze_solid("октаэдр", G.OCTAHEDRON, 8).edge_sq)),
    ]


def tau_bridge_from_phi(hbar_ev: float = 6.582119569e-16) -> float:
    """τ_bridge = ℏ/Δ₇ = ℏ/(2φ−3) — время моста через золотое сечение (с)."""
    return hbar_ev / float(DELTA_7)


# --- Геометрия ↔ квант: зеркало −I как оператор 3 кубитов --------------------
# Вершина куба (±1,±1,±1) ↔ 3 бита (−1→0, +1→1) ↔ узел.
_PAULI_X = np.array([[0, 1], [1, 0]])


def _node_to_bits():
    """Сопоставление узел → целое 0..7 (3-битная строка координат)."""
    mapping = {}
    for n, (x, y, z) in G.CUBE.items():
        bits = ((1 if x > 0 else 0) << 2) | ((1 if y > 0 else 0) << 1) | (1 if z > 0 else 0)
        mapping[n] = bits
    return mapping


def mirror_operator():
    """Оператор зеркала −I = X⊗X⊗X (8×8). Переворачивает все 3 бита = антипод."""
    return np.kron(np.kron(_PAULI_X, _PAULI_X), _PAULI_X)


def mirror_maps_sum10() -> bool:
    """[✓] Проверить: X⊗X⊗X переводит узел n в узел 10−n (зеркало, сумма 10)."""
    op = mirror_operator()
    node_bits = _node_to_bits()
    bits_node = {b: n for n, b in node_bits.items()}
    for n, b in node_bits.items():
        # столбец b оператора указывает на образ базисного состояния |b>.
        target = int(np.argmax(op[:, b]))
        if bits_node[target] != 10 - n:
            return False
    return True


def summary():
    """Печать сводки мостов."""
    print("МОСТ геометрия ↔ физика (всё проверено символьно):\n")
    for br in all_bridges():
        mark = "[✓]" if br.holds else "[!]"
        print(f"  {mark} {br.name:<18} {br.physics:<26} = {br.geometry}")
    print(f"\n  τ_bridge = ℏ/(2φ−3) = {tau_bridge_from_phi() * 1e15:.3f} фс")
    print(f"  зеркало −I = X⊗X⊗X переводит n → 10−n: {mirror_maps_sum10()}")


if __name__ == "__main__":
    summary()
