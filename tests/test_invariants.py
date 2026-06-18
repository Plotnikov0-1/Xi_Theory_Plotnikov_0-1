"""
Тесты-инварианты: проверяют, что расчёты фреймворка совпадают с числовыми
результатами документа DIALOG QMT v11.0. Запуск:  python -m pytest -q
(или просто  python tests/test_invariants.py).
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

# Чтобы тесты работали при прямом запуске из любой папки.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import constants as C
from qmt import dynamics, matrix6x6, nodes, sincerity, tunneling


def test_central_identity_a_omega_equals_c():
    # §1.1 — a·ω = c тождественно.
    assert math.isclose(C.COMPTON_LENGTH * C.ZITTER_FREQ, C.C, rel_tol=1e-9)


def test_phi_attractor():
    # §1.4 — X* = φ − 1 = 0.618034.
    assert math.isclose(C.X_STAR, 0.6180339887, rel_tol=1e-9)
    # И из золотого сечения: φ² = φ + 1.
    assert math.isclose(C.PHI**2, C.PHI + 1.0, rel_tol=1e-12)


def test_tau_bridge():
    # §1.5 — τ_bridge = ℏ/Δ7 ≈ 2.79 фс, Δ7 = √5 − 2.
    assert math.isclose(C.DELTA_7, math.sqrt(5) - 2, rel_tol=1e-12)
    assert math.isclose(C.TAU_BRIDGE * 1e15, 2.79, abs_tol=0.02)


def test_structural_parameters():
    # §3.2 — λ₀ = 9/5, μ₀ = 1/2, Xc = 3.6.
    assert C.LAMBDA_0 == 1.8
    assert C.MU_0 == 0.5
    assert math.isclose(C.X_C, 3.6, rel_tol=1e-12)


def test_resonance_amplitude_star():
    # §3.3 — Γ* ≈ 0.485 при X = X*.
    assert math.isclose(C.GAMMA_STAR, 0.485, abs_tol=0.001)


def test_sum9_topology():
    # §3.1 — все пары дают сумму 9 и покрывают узлы 0–9.
    chk = nodes.verify_sum9()
    assert chk.pairs_ok and chk.covers_all and chk.pair_count == 5


def test_interaction_matrix_symmetric():
    # §3.3 — матрица 7×7 симметрична (детальное балансирование).
    M, _ = nodes.interaction_matrix_7x7()
    assert np.allclose(M, M.T)


def test_matrix6x6_trace_is_sum9():
    # §12 — след матрицы 6×6 равен 9 (топология Sum-9).
    inv = matrix6x6.spectral_invariants()
    assert math.isclose(inv.trace, 9.0, rel_tol=1e-12)
    assert sorted(np.round(inv.eigvals, 3)) == [0.5, 1.0, 1.0, 2.0, 2.0, 2.5]


def test_rhythm_invariant_balance():
    # §A4 — инвариант ритма ℛ ≈ 0.21 (нижняя граница зоны баланса).
    inv = matrix6x6.spectral_invariants()
    R = matrix6x6.rhythm_invariant(C.OMEGA_SYS, inv.delta_min, C.GAMMA_DECO)
    assert math.isclose(R, 0.21, abs_tol=0.03)


def test_dynamics_phi_attractor():
    # §4.2 — стационарная нагрузка при μ_crit = 0.5 равна φ−1.
    assert math.isclose(dynamics.steady_state_load(0.5), C.X_STAR, rel_tol=1e-9)
    # И эта точка устойчива (g'(X*) < 0).
    _, gprime = dynamics.jacobian_eigenvalues(0.5)
    assert gprime < 0


def test_tunneling_reference_points():
    # §13 — когерентная прозрачность в эталонных точках.
    assert math.isclose(tunneling.coherent_transparency(0.0), 0.1244, abs_tol=1e-4)
    assert math.isclose(tunneling.coherent_transparency(0.878), 0.0775, abs_tol=1e-4)
    # Когерентное туннелирование мощнее классического WKB (фаза, не амплитуда).
    t_wkb, t_coh, ratio = tunneling.wkb_vs_coherent(0.0)
    assert ratio > 1.0


def test_sincerity_monotonicity():
    # §17.2 — теорема монотонности: S_Fib и S_tunnel убывают с ростом ε.
    assert sincerity.monotonicity_holds()


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
