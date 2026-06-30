import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import vibration as V

def test_mass_frequency_roundtrip():
    w=V.compton_frequency()
    assert math.isclose(V.mass_from_frequency(w), V.M_E, rel_tol=1e-9)

def test_heavier_higher_frequency():
    assert V.heavier_is_higher_frequency()

def test_unified_a_omega_c():
    u=V.unified_a_omega_c()
    assert math.isclose(u["a·ω"], u["c"], rel_tol=1e-9)

def test_wave_relation():
    # v=λf: f=v/λ; при λ=1, v=c → f=c
    assert math.isclose(V.wave_relation(1.0, V.C), V.C, rel_tol=1e-12)

def test_time_is_ratio():
    assert math.isclose(V.time_is_space_over_velocity(300.0, V.C), 300.0/V.C, rel_tol=1e-12)

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
