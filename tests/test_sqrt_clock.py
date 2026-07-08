import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import sqrt_clock as SQ

def test_radicands_are_squares():
    assert [SQ.hour_radicand(n) for n in range(1, 13)] == [1,4,9,16,25,36,49,64,81,100,121,144]
    assert SQ.hydrogen_degeneracy(3) == {"n": 3, "n²": 9, "2n² (со спином)": 18}

def test_digit_root_sum9_mirror():
    assert SQ.dr_sequence() == [1,4,9,7,7,9,4,1,9,1,4,9]
    assert SQ.dr_set() == [1,4,7,9]
    assert SQ.sum9_digitroot_mirror()

def test_mod9_and_sum():
    assert set(SQ.n2_mod9()) == {0,1,4,7}
    s = SQ.sum_squares()
    assert s["=650"] and s["= 2·5²·13"]

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
