"""
Тесты физики переходов: 7 катастроф, сборка=бифуркация, Пуанкаре, Паули, Сахаров.
Запуск:  python tests/test_catastrophe.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import catastrophe as K


def test_seven_catastrophes():
    # [✓] Ровно 7 элементарных катастроф Тома (= 7 взаимодействий, узел 7).
    assert K.catastrophe_count() == 7
    codims = [c.codim for c in K.CATASTROPHES]
    assert codims == [1, 2, 3, 4, 3, 3, 4]


def test_cuspoids_and_umbilics():
    # 4 куспоида (A-серия) + 3 омбилики (D-серия).
    a_series = [c for c in K.CATASTROPHES if c.ade.startswith("A")]
    d_series = [c for c in K.CATASTROPHES if c.ade.startswith("D")]
    assert len(a_series) == 4 and len(d_series) == 3


def test_cusp_is_model_bifurcation():
    # Сборка = бифуркация модели: бистабильность ⇔ три равновесия.
    assert K.cusp_is_bistable(0.0, -1.0)            # φ-аттрактор ↔ нулевой
    assert len(K.cusp_equilibria(0.0, -1.0)) == 3
    assert not K.cusp_is_bistable(1.0, 1.0)         # моностабильно


def test_cusp_bifurcation_set():
    # Граница складок 4μ₂³+27μ₁²=0: на ней кратный корень (переход бистаб./моно).
    mu2 = -1.0
    mu1_edge = K.cusp_bifurcation_set(mu2)
    assert math.isclose(mu1_edge, math.sqrt(4.0 / 27.0), rel_tol=1e-9)
    # Чуть внутри клина — бистабильно, чуть снаружи — нет.
    assert K.cusp_is_bistable(mu1_edge - 0.01, mu2)
    assert not K.cusp_is_bistable(mu1_edge + 0.01, mu2)


def test_poincare_recurrence_finite():
    # Пуанкаре: золотой поворот почти возвращается за конечное число шагов.
    n = K.poincare_return_time(eps=0.05)
    assert n > 0


def test_pauli_distinct_levels():
    # Паули: одинаковые уровни запрещены; разные — разрешены.
    assert K.pauli_distinct_levels([0.49, 0.31, 0.16, 0.19])
    assert not K.pauli_distinct_levels([0.2, 0.2, 0.3, 0.4])


def test_sakharov_three_conditions():
    # Сахаров: ровно три условия CP/асимметрии.
    conds = K.sakharov_conditions()
    assert len(conds) == 3
    assert K.cp_asymmetry(0.0) == 0.0            # точное зеркало ⇒ нет CP


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов физики переходов пройдены.")


if __name__ == "__main__":
    _run_all()
