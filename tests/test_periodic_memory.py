import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import periodic_memory as P

def test_fe_is_binding_peak():
    assert P.fe_is_peak()
    fe=P.binding_per_nucleon(26,56)
    assert 8.5 < fe < 8.9

def test_fusion_threshold_at_fe():
    assert P.fusion_releases_energy(6) and not P.fusion_releases_energy(92)

def test_delta_z_18_homologous():
    assert P.homologous_pair(22,40)   # Ti-Zr
    assert P.homologous_pair(23,41)   # V-Nb
    assert not P.homologous_pair(22,41)

def test_digit_root_preserved_mod9():
    assert P.digit_root(22)==P.digit_root(40)==4

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
