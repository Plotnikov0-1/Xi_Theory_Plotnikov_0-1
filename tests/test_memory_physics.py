"""Тесты физики памяти: Составитель карточек (память) + Мабу (EP).

Закрепляет: эффект распределения (минимум повторений), память=φ−1 при любом ε,
и ключевой факт — время памяти расходится у exceptional point.
Запуск: python tests/test_memory_physics.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import memory_physics as M

PHI = (1 + math.sqrt(5)) / 2


def test_spacing_optimum_is_ten_minutes():
    # Эффект распределения: минимум повторений (4) при интервале 10 мин.
    sp = M.spacing_optimum()
    assert sp["оптимум"] == "10 мин"
    assert sp["минимум"] == 4


def test_forgetting_curve_monotone():
    assert M.forgetting(0) == 1.0
    assert M.forgetting(1) > M.forgetting(2) > 0


def test_memory_is_structure_phi_minus_1():
    # Память = структура: неподвижная точка φ−1 при любом ε.
    for eps in (0.0, 0.3, 0.9):
        assert abs(M.memory_fixed_point(eps) - (PHI - 1)) < 1e-9


def test_ep_location():
    assert math.isclose(M.ep_lambda(1.0), 0.5, abs_tol=1e-12)


def test_memory_time_diverges_at_ep():
    # Ключевой факт: T(λ)→∞ при λ→Γ/2 (EP). Монотонно растёт к EP.
    assert M.memory_diverges_at_ep()
    assert M.memory_time(0.51) > M.memory_time(1.0) > M.memory_time(2.0)
    assert math.isinf(M.memory_time(0.5))     # на EP — бесконечно


def test_population_revives():
    # Население возвращается (немарковский backflow): P падает и снова растёт.
    ps = [M.population(0.75, t) for t in (0, 2, 4, 6)]
    assert ps[0] > 0.99            # старт почти 1
    assert min(ps) < 0.1           # падает почти к 0
    assert ps[3] > 0.5             # и возвращается


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
