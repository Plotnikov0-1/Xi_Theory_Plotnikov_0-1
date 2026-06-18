"""
Символьные тесты геометрического фундамента (sympy). Каждое утверждение из
блока «СБОРКА» помеченное [✓] проверяется точно. Запуск:
    python tests/test_geometry.py
"""

from __future__ import annotations

import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import geometry as G


def test_golden_relation():
    # φ² = φ + 1 — основа всего золотого мира.
    assert sp.simplify(G.PHI**2 - (G.PHI + 1)) == 0
    assert sp.simplify(G.INV_PHI - 1 / G.PHI) == 0


def test_five_solids_euler():
    # Все пять платоновых тел: V − E + F = 2.
    for r in G.all_solids():
        assert r.euler == 2, r.name


def test_solid_edge_and_radius_relations():
    # Точные соотношения рёбер и радиусов (а не десятичные числа).
    rep = {r.name: r for r in G.all_solids()}
    assert sp.simplify(rep["тетраэдр"].edge_sq - 8) == 0
    assert sp.simplify(rep["куб"].edge_sq - 4) == 0
    assert sp.simplify(rep["октаэдр"].edge_sq - 2) == 0           # ребро = √2
    assert sp.simplify(rep["додекаэдр"].edge_sq - (6 - 2 * sp.sqrt(5))) == 0
    # Радиусы: куб и додекаэдр на ОДНОЙ сфере R² = 3.
    assert sp.simplify(rep["куб"].R_sq - 3) == 0
    assert sp.simplify(rep["додекаэдр"].R_sq - 3) == 0
    assert sp.simplify(rep["октаэдр"].R_sq - 1) == 0
    # Икосаэдр: R² = φ + 2.
    assert sp.simplify(rep["икосаэдр"].R_sq - (G.PHI + 2)) == 0


def test_mirror_is_central_inversion():
    # Зеркало (сумма 10) = центральная инверсия −I; все 4 пары антиподальны.
    for a, b in G.MIRROR_PAIRS:
        assert a + b == 10
        assert G.is_central_inversion(a, b)


def test_resonance_sum9():
    # Резонанс P9: сумма индексов = 9, и это НЕ антиподы (не −I).
    for a, b in G.RESONANCE_PAIRS:
        assert a + b == 9
        assert not G.is_central_inversion(a, b)


def test_two_tetrahedra_partition_cube():
    # Два тетраэдра делят 8 вершин куба без пересечения; −I меняет их местами.
    assert set(G.TET_A) | set(G.TET_B) == set(G.CUBE.keys())
    assert set(G.TET_A) & set(G.TET_B) == set()
    for a in G.TET_A:
        mirror = 10 - a
        assert mirror in G.TET_B


def test_dodecahedron_contains_cube():
    # Додекаэдр (20) = куб (8) + 12 золотых точек; куб ⊂ додекаэдр.
    dod = G.dodecahedron_vertices()
    assert len(dod) == 20
    cube_pts = {tuple(sp.Matrix(v)) for v in G.CUBE.values()}
    dod_pts = {tuple(v) for v in dod}
    assert cube_pts <= dod_pts


def test_group_orders():
    # Полная группа куба B₃ = 48; структура переходов D₁₀ = 20.
    assert G.b3_order() == 48
    assert G.GROUP_CUBE_ORDER == 48
    assert G.GROUP_TRANSITION_ORDER == 20


def test_vertex_four_attachments():
    # Вершина несёт 4 привязки: число, зеркало, центр-5, оболочка-0.
    att = G.vertex_attachments(1)
    assert att["число"] == 1 and att["зеркало"] == 9
    assert att["центр"] == 5 and att["оболочка"] == 0


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} геометрических тестов пройдены.")


if __name__ == "__main__":
    _run_all()
