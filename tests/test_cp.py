"""
Тесты CP-нарушения и бариогенеза: структурная формула η_B, геометрический
коридор, самоподобие, отношение каналов — сверка с наблюдениями.
Запуск:  python tests/test_cp.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import cp_baryogenesis as CP


def test_delta7_identity():
    # Δ₇ = √5−2 = 2(φ−1)−1 — щель перехода = золотая.
    assert CP.delta7_identity_holds()


def test_baryon_asymmetry_value():
    # η_B = π·J·(φ−1)·T_EW/Δ₇ ≈ 8.23·10⁻¹¹, точность к наблюдению > 94%.
    eta = CP.baryon_asymmetry()
    assert math.isclose(eta, 8.23e-11, rel_tol=2e-3)
    assert CP.accuracy(eta, CP.ETA_B_OBS) > 0.94


def test_structural_corridor_geometry():
    # G = (π−3)·½·(√5−2) = 1.671% — чистая геометрия (π, ½, Δ₇).
    G = CP.structural_corridor_G()
    assert math.isclose(G, 0.016712, rel_tol=1e-4)
    # Эквивалентная запись через Δ₇.
    assert math.isclose(G, (math.pi - 3) * 0.5 * CP.DELTA_7, rel_tol=1e-12)


def test_self_similarity():
    # A_local·G² ≈ A_global³ с отклонением < 3% (без подгонки).
    ss = CP.self_similarity()
    assert ss.deviation < 0.03
    assert math.isclose(ss.lhs, 1.508e-5, rel_tol=2e-2)
    assert math.isclose(ss.rhs, 1.471e-5, rel_tol=2e-2)


def test_channel_ratio():
    # |ρ₃₇|/|ρ₂₇| = 2.35 (DIALOG) ≈ A_loc/A_glob = 2.20 (LHCb), откл < 7%.
    cr = CP.channel_ratio_observed()
    assert math.isclose(cr, 2.204, rel_tol=1e-3)
    assert abs(CP.CHANNEL_RATIO_DIALOG - cr) / CP.CHANNEL_RATIO_DIALOG < 0.07


def test_sakharov_three_conditions():
    # Три условия Сахарова; условие 3 — через память ε≠0 (без фазового перехода).
    conds = CP.sakharov_in_dialog()
    assert len(conds) == 3
    assert "память" in conds[2][1] or "ε" in conds[2][1]


def test_chronology():
    # Хронология CP: от K⁰ (1964) до барионов Λb (2025).
    years = [c[0] for c in CP.CP_CHRONOLOGY]
    assert 1964 in years and 2025 in years
    assert years == sorted(years)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов CP/бариогенеза пройдены.")


if __name__ == "__main__":
    _run_all()
