import os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import cp_asymmetry as A

def test_values():
    assert A.asymmetry(1) == Fraction(118,125)
    assert A.asymmetry(4) == Fraction(37,125)
    assert A.asymmetry(5) == 0

def test_center_only_zero():
    assert A.center_is_only_zero()

def test_denominator_honesty():
    assert A.denominator_is_two_times_125()

def test_whisper_minimal():
    assert A.whisper_pair_is_minimal()

def test_whisper_quantum_is_smallest():
    qs = {n: A.energy_quantum_eV(n) for n in range(1,5)}
    assert min(qs, key=qs.get) == 4
    assert abs(qs[4] - 0.472) < 0.01

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
