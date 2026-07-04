import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import hydrogen_prediction as H

def test_mechanism_balmer_forbidden():
    assert H.balmer_forbidden_from_high_l()          # 7→2 запрещён из l≥3
    assert H.S2[3] == 0.0 and H.S3[3] > 0

def test_statistical_baseline():
    b = H.statistical_baseline()
    assert 0.3 < b < 1.0                              # ≈ 0.60–0.77 (в районе базы)

def test_ratio_monotone_in_high_l():
    assert H.ratio_at_high_l_fraction(0.9) > H.ratio_at_high_l_fraction(0.5)
    assert H.ratio_at_high_l_fraction(0.95) > 5.5

def test_threshold_and_achievable():
    f = H.threshold_fraction(5.5)
    assert 0.9 < f < 0.95                             # ~93%
    assert H.prediction_is_achievable()

def test_infinite_when_pure_high_l():
    assert H.line_ratio({3: 1}) == float("inf")       # чистый l=3 → 7→2 гаснет

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
