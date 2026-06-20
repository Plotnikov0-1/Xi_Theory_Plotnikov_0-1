"""Тесты: Бакингем (безразмерные π) и Cycles (оператор 1-4-7, CP-снятие m).

Закрепляет точную математику и экспериментальные якоря.
Запуск: python tests/test_buckingham_cycles.py
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import buckingham as B
from qmt import cycles as Cy


# ── Бакингем ─────────────────────────────────────────────────────────────────
def test_fine_structure_dimensionless_and_137():
    a = B.fine_structure()
    assert a.is_dimensionless
    assert abs(1.0 / a.value - 137.035999) < 1e-3


def test_mass_energy_identity_is_one():
    # E/(mc²) = 1, безразмерно (тождество масса-энергия).
    r = B.mass_energy_identity(1.0, 1.0 / B.c.value**2)
    assert r.is_dimensionless
    assert math.isclose(r.value, 1.0, abs_tol=1e-9)


def test_binding_fraction_is_alpha_squared_over_two():
    # E_связи(H)/(m_e c²) = α²/2 совпадает с экспериментом до 0.1%.
    pred = B.binding_fraction().value
    exp = 13.598434 / 510998.95
    assert abs(pred - exp) / exp < 1e-3


def test_mass_ratio_dimensionless():
    mr = B.mass_ratio()
    assert mr.is_dimensionless
    assert abs(mr.value - 1836.15267) < 0.01


# ── Cycles ───────────────────────────────────────────────────────────────────
def test_permutation_spectrum_cube_roots():
    # σ(P) = {1, ω, ω²}, каждое ×3; P³ = I.
    assert Cy.is_cube_root_spectrum()


def test_invariant_projector_rank3():
    Pi = Cy.invariant_projector()
    assert np.allclose(Pi @ Pi, Pi)          # проектор
    assert np.linalg.matrix_rank(Pi) == 3    # наблюдаемое подпространство


def test_no_perturbation_means_degeneracy():
    base = Cy.m_levels_cp(E0=-3.4, a=0.0, b=0.0)
    assert not base["вырождение_снято"]
    assert not base["CP_нарушено"]


def test_odd_perturbation_lifts_degeneracy_and_breaks_mirror():
    cp = Cy.m_levels_cp(E0=-3.4, a=0.05, b=0.0)
    assert cp["вырождение_снято"]
    assert cp["CP_нарушено"]                 # E_{+m} ≠ E_{−m}
    assert math.isclose(cp["зеркальная_асимметрия"][1], 0.10, abs_tol=1e-9)


def test_zeeman_anchor_real():
    # Линейный наклон = реальный эффект Зеемана: μ_B·B·m.
    assert math.isclose(Cy.zeeman_split_eV(1.0, 1), Cy.MU_B_EV_PER_T, rel_tol=1e-12)
    assert Cy.MU_B_EV_PER_T > 0


def test_cp_needs_three_generations():
    # CP-нарушение СМ требует ровно 3 поколений: фаз=0 при N<3, =1 при N=3.
    assert Cy.cp_phases_sm(1)["CP_фазы"] == 0
    assert Cy.cp_phases_sm(2)["CP_фазы"] == 0
    assert Cy.cp_phases_sm(3)["CP_фазы"] == 1
    assert Cy.cp_phases_sm(3)["CP_возможно"]
    assert not Cy.cp_phases_sm(2)["CP_возможно"]


def test_cp_channels_count():
    # Все каналы CP в спине l = l нечётных мультиполей; триада l=1 → ровно 1.
    assert Cy.cp_channels(1)["CP_наруш_каналы"] == 1
    assert Cy.cp_channels(2)["CP_наруш_каналы"] == 2
    assert Cy.cp_channels(1)["нечётные_мультиполи"] == [1]


def test_cp_full_decomposition_odd_is_signal():
    # Полный CP-сигнал = нечётная часть; чисто чётный спектр → CP=0.
    sym = Cy.cp_full_decomposition({-1: 5.0, 0: 3.0, 1: 5.0})
    assert not sym["CP_нарушено"]
    asym = Cy.cp_full_decomposition({-1: 4.0, 0: 3.0, 1: 5.0})
    assert asym["CP_нарушено"]
    assert math.isclose(asym["полный_CP_сигнал"], 1.0, abs_tol=1e-12)


# ── Масштабный инвариант (Бакингем) ──────────────────────────────────────────
def test_scale_invariant_fixed_point():
    # f(x)=1/(1+x) сходится к φ−1 из любого старта (масштабная инвариантность).
    target = (math.sqrt(5) - 1) / 2
    for x0 in (0.1, 2.0, 100.0):
        assert abs(B.self_similar_fixed_point(x0) - target) < 1e-9


def test_convergents_approach_fixed_point():
    # «Разнообразие форм»: сходящиеся дроби стремятся к φ−1.
    target = (math.sqrt(5) - 1) / 2
    forms = B.convergents(15)
    assert abs(forms[-1][2] - target) < 1e-4
    assert forms[0] == (1, 2, 0.5)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
