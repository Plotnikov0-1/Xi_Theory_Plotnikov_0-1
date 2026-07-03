import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import universal_transition as UT

def test_operator():
    assert math.isclose(UT.T(0), 1.0)
    assert math.isclose(UT.T(1), 0.5)

def test_a_self_similar():
    assert UT.self_similar_fixed_point()
    assert math.isclose(UT.iterate(), UT.PHI1, abs_tol=1e-9)

def test_b_all_temperatures():
    assert UT.contains_all_temperatures()
    # лёд→пар: заселённость растёт с τ
    assert UT.occupation(1, 0.05) < UT.occupation(1, 100)

def test_c_step_temperature():
    assert abs(UT.step_temperature(0.472) - 5477) < 20

def test_d_mirror_center():
    assert UT.center_is_half()
    assert math.isclose(UT.mirror(0.5), 0.5)
    # Δ=0 на переходе даёт ½ при любой τ
    assert math.isclose(UT.occupation(0.0, 0.3), 0.5)

def test_e_universality():
    assert UT.same_form_different_params()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
