"""
Тесты моста геометрия ↔ физика. Проверяют, что величины уравнений движения и
физики являются точными геометрическими соотношениями (символьно, sympy).
Запуск:  python tests/test_bridge.py
"""

from __future__ import annotations

import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import bridge as B
from qmt import constants as Cn


def test_all_bridges_hold():
    # Все символьные мосты выполнены (разность = 0).
    for br in B.all_bridges():
        assert br.holds, br.name


def test_phi_attractor_is_golden():
    # X* = φ − 1 = 1/φ.
    assert sp.simplify(B.X_STAR - 1 / B.PHI) == 0


def test_tunnel_barrier_from_attractor():
    # Δ₇ = 2φ − 3 = 2·X* − 1 — барьер туннеля выводится из φ-аттрактора.
    assert sp.simplify(B.DELTA_7 - (2 * B.PHI - 3)) == 0
    assert sp.simplify(B.DELTA_7 - (2 * B.X_STAR - 1)) == 0


def test_tau_bridge_matches_constants():
    # τ_bridge из золотой формулы совпадает с физической константой (~2.79 фс).
    assert abs(B.tau_bridge_from_phi() - Cn.TAU_BRIDGE) / Cn.TAU_BRIDGE < 1e-9


def test_mirror_operator_is_sum10():
    # Зеркало −I = X⊗X⊗X переводит узел n в узел 10−n.
    assert B.mirror_maps_sum10()


def test_mirror_operator_is_involution():
    # (X⊗X⊗X)² = I — зеркало, применённое дважды, возвращает исходное.
    import numpy as np
    op = B.mirror_operator()
    assert np.allclose(op @ op, np.eye(8))


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов моста пройдены.")


if __name__ == "__main__":
    _run_all()
