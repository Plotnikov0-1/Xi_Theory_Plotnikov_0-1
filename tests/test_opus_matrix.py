"""Тесты материала папки «Опус», развёрнутого в рабочую математику.

Закрепляет: тождества φ, геометрию трещин Op_4=4, матрицу 10×10 (след,
неподвижные точки 3 и 0.5), exceptional point при λ=Γ/2, Coldea 2cos(π/5)=φ.
Запуск: python tests/test_opus_matrix.py
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import opus_matrix as O

PHI = (1 + math.sqrt(5)) / 2


def test_identities_all_true():
    assert all(O.identities().values())


def test_geometry_op4_is_exactly_four():
    g = O.geometry()
    assert math.isclose(g["вершина_додекаэдра_R²"], 3.0, abs_tol=1e-12)
    assert math.isclose(g["T_вх=4/φ"], 4 / PHI, abs_tol=1e-12)
    assert math.isclose(g["T_вых=1/φ"], 1 / PHI, abs_tol=1e-12)
    assert math.isclose(g["Op_4=T_вх/T_вых"], 4.0, abs_tol=1e-12)


def test_matrix_symmetric_and_trace():
    p = O.matrix_properties()
    assert p["симметрична"]
    assert p["след_совпал"]
    assert math.isclose(p["Tr_числ"], 14.84783719, abs_tol=1e-6)


def test_matrix_fixed_points_3_and_half():
    # Узлы 0 и 5 изолированы → точные собственные значения 3 и 0.5.
    p = O.matrix_properties()
    assert p["узлы_0_5_изолированы"]
    assert p["λ=3_точно"] and p["λ=0.5_точно"]


def test_exceptional_point_phases():
    ep = O.exceptional_point(Gamma=1.0)
    assert math.isclose(ep["λ_EP=Γ/2"], 0.5, abs_tol=1e-12)
    assert ep["PT_нарушено_мнимые"]      # λ<Γ/2: чисто мнимые
    assert ep["EP_сливаются"]            # λ=Γ/2: слияние в 0
    assert ep["PT_симметрия_веществ"]    # λ>Γ/2: вещественные


def test_pair_eigenvalues_coalesce_at_ep():
    e = O.pair_eigenvalues(0.5, 1.0)
    assert np.allclose(e, 0, atol=1e-6)


def test_coldea_e8_golden_ratio():
    # 2cos(π/5)=φ — измерено Coldea 2010 (m₂/m₁ в CoNb₂O₆).
    r = O.e8_mass_ratios()
    assert math.isclose(r["m2/m1=2cos(π/5)=φ"], PHI, abs_tol=1e-12)
    assert math.isclose(r["m3/m1=2cos(π/30)"], 1.989044, abs_tol=1e-5)


def test_cp_map_has_prediction():
    # Карта CP содержит измеренные системы и одно предсказание (1↔9, нейтрино).
    pred = [n for n in O.CP_MAP if "ПРЕДСКАЗАНИЕ" in n.status]
    assert len(pred) == 1 and pred[0].pair == "1↔9"


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
