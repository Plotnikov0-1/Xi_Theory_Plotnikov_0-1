"""Тесты «Монахи»: имена = зеркальные пары R (переворот), R²=I, палиндром ДЕРЕД.

Закрепляет прямую подсказку: структура зеркала −I (пары + само-зеркальный центр).
Запуск: python tests/test_monks.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import monks as M


def test_most_pairs_are_exact_reversals():
    # 23 из 24 пар — точный переворот строки (брат = имя наоборот).
    assert len(M.exact_pairs()) == 23
    assert len(M.approximate_pairs()) == 1


def test_reversal_is_involution():
    # R²=I — зеркало есть группа Z₂.
    assert M.is_involution()


def test_dered_is_self_mirror_palindrome():
    # ДЕРЕД (первый=последний монах) — палиндром = неподвижная точка R.
    assert M.is_palindrome(M.SELF_MIRROR)
    assert M.R(M.SELF_MIRROR) == M.SELF_MIRROR
    assert M.fixed_points() == ["ДЕРЕД"]


def test_specific_exact_pairs():
    for a, b in [("МУРРА", "АРРУМ"), ("НАККА", "АККАН"), ("МОББУ", "УББОМ"),
                 ("ОРКК", "ККРО"), ("ЭННЭК", "КЭННЭ")]:
        assert M.R(a) == b


def test_cube_correspondence_structure():
    c = M.cube_correspondence()
    assert c["куб: само-зеркало (центр)"] == 5
    assert (1, 9) in c["куб: зеркальные пары"]
    assert "ДЕРЕД" in c["монахи: само-зеркало (палиндром)"]


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
