"""Тесты морфологии конструкции [носитель × связь²].

Закрепляет: правило Борна реально, E/(mc²)=1, классификация границ.
Запуск: python tests/test_construction.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import construction as K


def test_born_rule_real_and_normalized():
    # ψ·ψ* вещественно, ≥0, и для нормированного ψ сумма = 1.
    psi = [1 / math.sqrt(2) + 0j, 1j / math.sqrt(2)]
    P = K.born_observable(psi)
    assert K.is_self_product_real(psi)
    assert math.isclose(sum(P), 1.0, abs_tol=1e-12)
    assert all(p >= -1e-12 for p in P)


def test_mass_energy_identity():
    # E=mc² в безразмерной форме = 1 (тождество).
    assert math.isclose(K.mass_energy_dimensionless(1.0, 1.0 / 2.99792458e8**2),
                        1.0, abs_tol=1e-9)


def test_emc2_derived_from_4momentum_self_contraction():
    # E=mc² ВЫВЕДЕНО: p^μp_μ=(mc)², при p=0 → E=mc².
    em = K.energy_momentum_invariant(2.0, 3.0, 1.0)
    assert math.isclose(em["p·p (инвариант)"], em["(mc)²"], abs_tol=1e-9)
    assert math.isclose(em["E_покоя=mc²"], 2.0, abs_tol=1e-12)


def test_invariant_preserved_under_boost():
    # Самосвёртка p·p=(mc)² одинакова для всех наблюдателей (значит — выведено).
    inv = K.boost_invariance(2.0, 3.0)
    target = 2.0**2 + 3.0**2 - 3.0**2  # = (mc)² = 4 (c=1, p·p=E²−p²=m²)
    for b in inv:
        assert math.isclose(b["p·p"], 4.0, abs_tol=1e-9)


def test_family_is_quadratic():
    # Семья «проявления» — степень 2 (или −2 обратная) по связи.
    for f in K.FAMILY:
        assert f.degree in (2, -2)


def test_boundary_not_quadratic():
    # Границы — это НЕ квадрат (передача, exp, log, порядок).
    for f in K.BOUNDARY:
        assert f.degree not in (2, -2)


def test_classify_labels():
    assert "квадрат" in K.classify(2)
    assert "передача" in K.classify(1)
    assert "самозамыкание" in K.classify("exp")


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
