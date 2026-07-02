import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import chemistry_check as C

def test_tunnel_258_real():
    assert C.tunnel_258_are_real_rules()

def test_vsepr_covers():
    assert C.vsepr_covers_2_to_9()
    assert C.tetra_is_4_octa_is_6()

def test_euler_molecules():
    assert C.euler_holds_for_molecules()

def test_orbital_series_odd():
    assert C.orbital_series_is_odd()
    assert C.orbital_counts()["d"] == (5, 10)

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
