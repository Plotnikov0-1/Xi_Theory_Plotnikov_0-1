import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import interface as I

def test_eight_nodes():
    assert len(I.INTERFACE) == 8

def test_saddle():
    assert I.saddle_is_max()

def test_quartic():
    q = I.quartic_critical_points()
    assert q["дно(5) x=0"] and q["барьер(3) x=−1"] and q["барьер(7) x=+1"]

def test_cube_no_phi():
    assert I.cube_spectrum_no_phi()

def test_two_exits():
    t = I.two_exits()
    assert t["узел3 прыжок"]                  # прыжок работает рано
    assert not t["узел7 прыжок"]              # прыжок не работает поздно
    assert t["узел7 прощение (ε→0)"]          # прощение открывает выход
    assert I.two_distinct_exits()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
