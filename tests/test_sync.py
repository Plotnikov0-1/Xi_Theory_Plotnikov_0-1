"""
Тесты синхронизации геометрия ↔ водород: размещение цифр, правила отбора,
совпадение с реальными спектральными линиями.
Запуск:  python tests/test_sync.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import sync as Y


def test_number_placement():
    # Вершины 1,2,3,4,6,7,8,9; центр 5; оболочка 0.
    assert Y.VERTICES == [1, 2, 3, 4, 6, 7, 8, 9]
    assert Y.CENTER == 5 and Y.SHELL == 0


def test_selection_counts():
    # 10 прямых + 3 резонанса + 4 зеркала = 17 разрешённых; 11 запрещённых; всего 28.
    c = Y.selection_counts()
    assert c == {"прямой": 10, "резонанс": 3, "зеркало": 4, "запрещён": 11}
    assert len(Y.allowed_transitions()) == 17
    assert len(Y.forbidden_transitions()) == 11
    assert len(Y.all_transitions()) == 28


def test_mirror_is_sum10_parity():
    # Зеркало = сумма-10, диагональ тела (Хэмминг 3 = инверсия −I).
    for t in Y.all_transitions():
        if t.kind == "зеркало":
            assert t.a + t.b == 10
            assert Y.hamming(t.a, t.b) == 3


def test_resonance_is_sum9():
    # Резонанс = сумма-9.
    for t in Y.all_transitions():
        if t.kind == "резонанс":
            assert t.a + t.b == 9


def test_hydrogen_lines_match_theory():
    # Геометрия порождает реальные линии водорода, совпадающие с документом.
    by_pair = {(t.a, t.b): t for t in Y.all_transitions()}
    # 1↔2 = Лайман α ≈ 121.5 нм.
    assert math.isclose(by_pair[(1, 2)].wavelength_nm, 121.5, abs_tol=0.5)
    # 2↔7 (резонанс Sum-9) ≈ 397 нм (Бальмер H-ζ из PDF).
    assert math.isclose(by_pair[(2, 7)].wavelength_nm, 397.0, abs_tol=1.0)
    # 3↔7 (зеркало) ≈ 1005 нм (Пашен δ из PDF).
    assert math.isclose(by_pair[(3, 7)].wavelength_nm, 1005.0, abs_tol=2.0)


def test_forbidden_have_no_channel():
    # Запрещённые — это диагонали грани без канала (не сумма-9, не сумма-10, не ребро).
    for t in Y.forbidden_transitions():
        assert not t.allowed
        assert t.a + t.b not in (9, 10)
        assert Y.hamming(t.a, t.b) == 2


def test_tetrahedron_start():
    # Минимум — тетраэдр {1,6,7,8}.
    tet, trans = Y.tetrahedron_start()
    assert sorted(tet) == [1, 6, 7, 8]
    assert len(trans) == 6


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов синхронизации пройдены.")


if __name__ == "__main__":
    _run_all()
