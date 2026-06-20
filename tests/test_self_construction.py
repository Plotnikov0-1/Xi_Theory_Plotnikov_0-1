"""Тесты: почему самоконструкция даёт ИМЕННО вес φ−1, а не другой.

Закрепляет три ответа: единственность (самосогласование), самоподобие,
устойчивость (φ−1 хуже всех приближается рациональными).
Запуск: python tests/test_self_construction.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import self_construction as S

PHI = (1 + math.sqrt(5)) / 2
X_STAR = PHI - 1


def test_unique_positive_self_consistent_ratio():
    # r=1/(1+r) даёт ровно один положительный корень = φ−1.
    r = S.self_consistent_ratio()
    assert r["единственный_положительный"]
    assert math.isclose(r["r₊"], X_STAR, abs_tol=1e-12)
    assert r["r₋"] < 0


def test_self_similarity_only_at_phi():
    # часть/часть = часть/целое только при весе φ−1.
    assert S.self_similarity(X_STAR)["самоподобно"]
    assert not S.self_similarity(0.5)["самоподобно"]
    assert not S.self_similarity(0.7)["самоподобно"]


def test_phi_continued_fraction_all_ones():
    cf = S.continued_fraction(X_STAR, 8)
    assert cf[0] == 0
    assert all(a == 1 for a in cf[1:])


def test_phi_is_most_stable():
    # φ−1 хуже всех приближается рациональными → самый устойчивый вес.
    s_phi = S.stability(X_STAR)
    for other in (math.sqrt(2) - 1, math.e - 2, math.pi - 3, 0.5):
        assert s_phi > S.stability(other)


def test_rational_has_zero_stability():
    # Рациональное (1/2) приближается точно → устойчивость 0 (защёлкивается).
    assert math.isclose(S.stability(0.5), 0.0, abs_tol=1e-12)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
