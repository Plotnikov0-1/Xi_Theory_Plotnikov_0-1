"""
Тесты слоя масштабирования и уровней памяти.
Запуск:  python tests/test_scaling.py
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import scaling as Sc


def test_sierpinski_dimension():
    # [✓] Размерность Серпинского-тетраэдра = ln4/ln2 = 2.
    assert math.isclose(Sc.fractal_dimension(), 2.0, rel_tol=1e-12)


def test_sierpinski_counts():
    # Число под-тетраэдров на уровне L равно 4**L.
    for L in range(4):
        assert Sc.subtetra_count(L) == 4 ** L
        assert len(Sc.sierpinski_tetrahedra(L)) == 4 ** L


def test_synchronization_starts_at_tetrahedron():
    # Синхронизация начинается с тетраэдра: K4 синхронизируется не хуже куба.
    _, r_tetra = Sc.kuramoto_sync(Sc.adjacency_tetra())
    _, r_cube = Sc.kuramoto_sync(Sc.adjacency_cube())
    assert r_tetra[-1] > 0.9            # тетраэдр почти полностью синхронен
    assert r_tetra[-1] >= r_cube[-1] - 1e-6  # тетраэдр синхронизируется не хуже куба


def test_cube_graph_is_3_regular():
    # Граф куба: каждая вершина имеет ровно 3 соседа.
    A = Sc.adjacency_cube()
    assert np.all(A.sum(axis=1) == 3)


def test_memory_rates_self_similar():
    # Самоподобие: ξ_k = ξ0·2^k — глубже уровень, быстрее релаксация.
    rates = Sc.memory_rates(Sc.MemoryHierarchy(xi0=1.0, ratio=2.0))
    assert np.allclose(rates, [1, 2, 4, 8])


def test_memory_hierarchy_four_levels():
    # Иерархия памяти: 4 уровня (3 внутр. + 1 внешн.), все конечны.
    t, E = Sc.integrate_memory()
    assert E.shape[0] == Sc.N_MEMORY_LEVELS == 4
    assert np.all(np.isfinite(E))
    # Внутренние уровни убывают по глубине (быстрее релаксация → меньше ε).
    assert E[0, -1] > E[1, -1] > E[2, -1]


def test_mod3_family_147():
    # [✓] Узлы 1,4,7 — один класс по модулю 3 (семья якорей каналов).
    assert len({Sc.mod3_class(n) for n in Sc.MOD3_ANCHORS}) == 1
    assert Sc.mod3_class(1) == 1
    fams = Sc.mod3_families()
    assert fams[1] == [1, 4, 7] and fams[0] == [3, 6, 9] and fams[2] == [2, 5, 8]


def test_memory_channels_reach():
    # Каналы 0→1/0→4/0→7 охватывают 3/2/1 уровня.
    reach = Sc.memory_channel_reach()
    assert reach == {1: 3, 4: 2, 7: 1}


def test_crack_path_descends_by_three():
    # Трещина 7→4→1: спуск шагом −3 (знание → любовь).
    path = Sc.crack_path()
    assert path == (7, 4, 1)
    assert all(path[i] - path[i + 1] == 3 for i in range(len(path) - 1))


def test_ego_exit_is_xl_40():
    # 40 = XL = выход за эго.
    assert Sc.EGO_EXIT_XL == 40


def test_internal_projections_self_similar():
    # Внутренние проекции = самоподобные копии = 4**level.
    assert Sc.internal_projections(2) == 16


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов масштабирования пройдены.")


if __name__ == "__main__":
    _run_all()
