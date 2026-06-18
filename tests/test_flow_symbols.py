"""
Тесты слоя «поток/трубки» и символьного слоя.
Запуск:  python tests/test_flow_symbols.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import flow
from qmt import symbols as S


def test_curve_lies_on_shell():
    # Кривая-трубка целиком на сфере-оболочке √3 (узел 0).
    assert flow.lies_on_sphere(5, 3)
    assert math.isclose(flow.SHELL_R, math.sqrt(3), rel_tol=1e-12)


def test_curve_is_smooth_no_angles():
    # «Углов нет»: касательная нигде не ноль — кривая гладкая.
    assert flow.is_smooth(5, 3)
    assert flow.is_smooth(3, 2)


def test_winding_numbers_invariant():
    # Инвариант потока — числа намотки (a, b) = (5, 3): центр-5 и π-узел-3.
    assert flow.winding_numbers() == (5, 3)


def test_crossings_exist_but_not_invariant():
    # Пересечения есть (узлы), но это лишь иллюстрация (не инвариант).
    assert flow.approximate_crossings(5, 3, n=200) > 0


def test_center_is_nested_offset_geometry():
    # Центр — не точка: вложенная геометрия со смещением δ и ψ(0)≠0.
    cg = flow.center_geometry(delta=1e-3)
    assert cg.psi0_nonzero
    assert cg.delta > 0
    assert abs((cg.offset**2).sum() ** 0.5 - cg.delta) < 1e-12
    tet = flow.nested_tetrahedron(cg)
    assert tet.shape == (4, 3)


def test_triskelion_projection_hexagon():
    # Трискелион = проекция куба вдоль оси 1↔9: центр (Горгона) + правильный 6-угольник.
    import numpy as np
    coords, center, ring = flow.triskelion_projection((1, 9))
    assert set(center) == {1, 9}                     # ось-зеркало в центр
    assert set(ring) == {2, 3, 4, 6, 7, 8}           # 6 узлов на круге
    radii = [np.hypot(*coords[n]) for n in ring]
    assert np.allclose(radii, radii[0])              # правильный шестиугольник


def test_triskelion_c3_two_triangles():
    # C₃-симметрия: три «ноги» = две тройки (два тетраэдра, два направления).
    arms = flow.c3_arms((1, 9))
    sets = sorted(sorted(a) for a in arms)
    assert sets == [[2, 3, 4], [6, 7, 8]]


def test_true_path_map_complete():
    # «Верный путь»: 0–9 присутствуют, имена канонические.
    tp = S.true_path()
    for n in range(0, 10):
        assert n in tp
    assert tp[1] == "любовь" and tp[7] == "знания" and tp[9] == "жизнь"
    assert "доброта" in tp[0]


def test_mirror_pairs_sum10():
    # Зеркало числа = сумма 10 (5 — это «2 в зеркале»).
    m, _, _ = S.mirror_pair_meaning(2)
    assert m == 8
    m2, _, _ = S.mirror_pair_meaning(5)
    assert m2 == 5  # 5 — самоотражение (центр)


def test_roman_dynamics_present():
    # Римские цифры как динамика перехода: X=крест, L=открытый путь, XL=цель.
    assert "крест" in S.ROMAN["X"].name
    assert "XL" in S.ROMAN and "XI" in S.ROMAN


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов потока/символов пройдены.")


if __name__ == "__main__":
    _run_all()
