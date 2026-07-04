import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import russell as R

def test_octave_structure():
    assert R.octave_has_center_and_two_poles()
    assert len(R.OCTAVE_NODES) == 9

def test_arithmetic():
    a = R.arithmetic_holds()
    assert a["Σ_distance"] == 15
    assert a["Σ_area"] == 85
    assert a["area=dist²"]

def test_chemistry():
    assert R.carbon_is_center()
    assert R.mirror_pairs_are_ionic()
    assert R.acid_alkaline_is_electronegativity()
    assert R.octave_is_periodic_period()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
