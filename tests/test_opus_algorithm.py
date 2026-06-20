"""Тесты последних документов Опуса (ПЛ-01М…05М) в рабочей форме.

Закрепляет точные следствия алгоритма T(x)=1/(1+x): след φ−1, скорости 1/φ²
и 1/φ⁴, неподвижную точку памяти при любом ε, ε_крит, и Δ₇=(φ−1)³.
Запуск: python tests/test_opus_algorithm.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import opus_algorithm as A

PHI = (1 + math.sqrt(5)) / 2
X_STAR = PHI - 1


def test_algorithm_trace_is_phi_minus_1_from_any_start():
    for x0 in (0.1, 2.0, 100.0):
        assert abs(A.iterate(x0) - X_STAR) < 1e-9


def test_contraction_rate_is_inv_phi_squared():
    assert math.isclose(A.contraction_rate(), 1 / PHI**2, abs_tol=1e-12)


def test_double_apply_is_rate_squared():
    # (T∘T)′ = 1/φ⁴ = (1/φ²)² — структурный смысл квадрата.
    assert math.isclose(A.double_apply_rate(), A.contraction_rate()**2, abs_tol=1e-12)
    assert math.isclose(A.double_apply_rate(), 1 / PHI**4, abs_tol=1e-12)


def test_continued_fraction_is_phi():
    assert math.isclose(A.continued_fraction_phi(), PHI, abs_tol=1e-9)


def test_memory_fixed_point_independent_of_eps():
    # Третий путь φ−1 — один и тот же при любом ε.
    for eps in (0.0, 0.276, 0.5, 0.9):
        assert abs(A.memory_fixed_point(eps) - X_STAR) < 1e-9


def test_eps_crit_value():
    assert math.isclose(A.eps_crit(), (5 - math.sqrt(5)) / 10, abs_tol=1e-12)
    assert math.isclose(A.eps_crit(), 2 / (5 + math.sqrt(5)), abs_tol=1e-12)


def test_delta7_three_exact_forms():
    # Δ₇ = √5−2 = 2(φ−1)−1 = (φ−1)³ — двойное дно (линейно/кубически).
    f = A.delta7_forms()
    target = math.sqrt(5) - 2
    for v in f.values():
        assert math.isclose(v, target, abs_tol=1e-12)
    assert math.isclose(f["(φ−1)³"], (PHI - 1)**3, abs_tol=1e-12)


def test_electron_a_omega_equals_c():
    aw = A.electron_a_omega_c()
    assert math.isclose(aw["a·ω"], aw["c"], rel_tol=1e-9)


def test_born_observable_normalized():
    psi = 1 / math.sqrt(2) + 1j / math.sqrt(2)
    assert math.isclose(A.born_observable(psi), 1.0, abs_tol=1e-12)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
