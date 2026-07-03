import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import breathing as B

def test_breathing_collapses_to_gap():
    assert math.isclose(B.breathing_invariant(), 0.499, abs_tol=0.01)
    assert B.invariant_collapses_to_gap()          # ℐ≈0.5, не 1

def test_reaches_one_only_external():
    assert B.reaches_one_only_with_external()

def test_falsifiable_prediction():
    fp = B.falsifiable_prediction()
    assert fp["равновесие_NIST"] == 0.60
    assert "5.5" in fp["предсказание_накачка"]

def test_spectrum_incompatible():
    si = B.spectrum_incompatibility()
    assert not si["совместимо"]                    # α+β=1.59 ≠ 4.2
    assert abs(si["α+β_док1"] - 1.59) < 0.01

def test_negative_mode_impossible():
    assert B.negative_mode_impossible_from_circ()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
