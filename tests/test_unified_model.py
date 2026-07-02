import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import unified_model as U

def test_i1_involution():
    assert U.inv1_involution_with_fixpoint()["ВСЕ"]

def test_i2_golden_one_number():
    assert U.inv2_golden_attractor()["ВСЕ одно φ"]

def test_i3_three_minimum():
    inv = U.inv3_three_is_minimum()
    assert inv["впервые≠0 при N"] == 3
    assert inv["фазы(N)"] == {1: 0, 2: 0, 3: 1, 4: 3}

def test_i4_omega_cubed():
    assert U.inv4_omega_cubed_arrow()["ВСЕ"]

def test_i5_spectrum_memory():
    assert U.inv5_spectrum_to_memory()["ВСЕ"]

def test_i6_structure_over_count():
    assert U.inv6_structure_over_count()["ВСЕ"]

def test_all_invariants_consistent():
    assert U.foundation_is_consistent()
    assert all(U.all_invariants().values())

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
