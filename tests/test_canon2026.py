"""
Тесты канона 2026: φ как оператор сборки и эффективная матрица памяти.
Запуск:  python tests/test_canon2026.py
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import constants as C
from qmt import effective_matrix as EM
from qmt import phi_operator as P


# --- φ-оператор --------------------------------------------------------------

def test_fixed_point_is_phi_minus_one():
    # Итерация T(x)=1/(1+x) сходится к φ−1.
    assert math.isclose(P.fixed_point(), C.X_STAR, rel_tol=1e-9)
    assert math.isclose(P.fixed_point(x0=10.0), C.X_STAR, rel_tol=1e-9)


def test_stability_multiplier():
    # |T'(φ−1)| = 1/φ² ≈ 0.382 < 1.
    assert math.isclose(P.stability_multiplier(), 1 / C.PHI**2, rel_tol=1e-12)
    assert P.stability_multiplier() < 1.0


def test_two_independent_derivations_of_phi():
    # φ−1 из самосогласованности = φ−1 из динамики (два независимых пути).
    assert math.isclose(P.self_consistent_fraction(), C.X_STAR, rel_tol=1e-12)
    assert P.two_derivations_agree()


def test_regime_family():
    # x − 1/x = k: k=0→1, k=1→φ, k=2→1+√2 (серебряное сечение; в документе
    # подписано «≈1+φ», но точное значение — 1+√2 = 2.41421).
    assert math.isclose(P.regime(0), 1.0, rel_tol=1e-12)
    assert math.isclose(P.regime(1), C.PHI, rel_tol=1e-12)
    assert math.isclose(P.regime(2), 1 + math.sqrt(2), rel_tol=1e-9)


def test_m_eff_linear_in_memory():
    # Режимная масса m_eff = m₀ + μ·ε.
    assert math.isclose(P.m_eff(0.0, m0=1.0, mu=2.0), 1.0)
    assert math.isclose(P.m_eff(0.5, m0=1.0, mu=2.0), 2.0)


# --- Эффективная матрица -----------------------------------------------------

def test_base_matrix_sum9():
    # C = circ(1.5,0.5,0,0,0,0.5): след=9 (Sum-9), δλ_min=0.5.
    Cm = EM.base_matrix()
    assert math.isclose(np.trace(Cm), 9.0, rel_tol=1e-12)
    assert math.isclose(EM.min_gap(Cm), 0.5, rel_tol=1e-9)


def test_effective_matrix_symmetric():
    # C_eff = C + 1.8 uuᵀ + 2.4 vvᵀ симметрична.
    Ceff = EM.effective_matrix()
    assert np.allclose(Ceff, Ceff.T)


def test_collective_eigenvalue():
    # u=(1..1) — собственный вектор C_eff с λ = 2.5 + 1.8·6 = 13.3.
    vals, _ = EM.spectrum()
    assert np.any(np.isclose(vals, 13.3, atol=1e-6))


def test_channel_weights_normalized():
    # g_k = |⟨e₇, v_k⟩|² суммируются в 1 (ортонормированный базис).
    _, g = EM.channel_weights()
    assert math.isclose(g.sum(), 1.0, rel_tol=1e-9)


def test_memory_kernel_initial_value():
    # K(0) = Σ_k g_k = 1.
    assert math.isclose(EM.memory_kernel(0.0).real, 1.0, rel_tol=1e-9)


def test_breathing_law():
    # ℒ = Ω·δλ_min/γ.
    assert math.isclose(EM.breathing_law(2.0, 0.5, 0.25), 4.0, rel_tol=1e-12)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов канона 2026 пройдены.")


if __name__ == "__main__":
    _run_all()
