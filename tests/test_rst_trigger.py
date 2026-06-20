"""Тесты загадки «247» = триггер RST (2,4,7) как геометрия куба.

Закрепляет: (2,4,7) на одной грани, четвёртый угол = узел 1, сумма 13,
сдвиг {1,4,7}→{2,4,7}=CP, и честную развязку 247≠137.
Запуск: python tests/test_rst_trigger.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import rst_trigger as R


def test_trigger_on_one_face():
    assert R.trigger_on_one_face()
    assert R.face_of_trigger() == [1, 2, 4, 7]


def test_missing_corner_is_love():
    assert R.missing_corner() == 1   # узел 1 = Любовь


def test_trigger_sum_is_13():
    assert R.trigger_sum() == 13     # Фибоначчи (золотой порог)


def test_cp_shift_plus_one():
    s = R.cp_shift()
    assert s["{1,4,7}"] == 12 and s["{2,4,7}"] == 13
    assert s["сдвиг"] == 1


def test_247_is_not_alpha():
    # Честно: 1/247 и 2/247 НЕ равны α (разные объекты).
    v = R.vs_137()
    assert not v["1/247 == α?"]
    assert not v["2/247 == α?"]


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
