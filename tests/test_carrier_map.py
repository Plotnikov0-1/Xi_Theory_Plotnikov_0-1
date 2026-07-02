import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import carrier_map as M

def test_schlafli_counts():
    assert M.schlafli_counts(4, 3) == (8, 12, 6)     # куб
    assert M.schlafli_counts(3, 5) == (12, 30, 20)   # икосаэдр
    assert M.schlafli_counts(3, 3) == (4, 6, 4)      # тетраэдр

def test_euler_all_solids():
    assert M.euler_holds()

def test_phi_on_p5_edges():
    assert M.phi_lives_on_p5_edges()

def test_tetra_octa_tile():
    assert M.tetra_octa_tile()

def test_cuboctahedron_balance():
    assert M.cuboctahedron_balance()

def test_arrow_omega_cubed():
    assert M.arrow_from_omega_cubed()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
