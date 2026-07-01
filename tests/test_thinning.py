import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import thinning as T

def test_thinner_more_transparent():
    assert T.thinner_is_more_transparent()
    assert T.tunnel_transparency(0.001) > T.tunnel_transparency(1.0)

def test_plasma_frequency_positive():
    assert T.plasma_frequency() > 0

def test_shannon_scales_with_bandwidth():
    assert math.isclose(T.shannon_capacity(2e9,10), 2*T.shannon_capacity(1e9,10), rel_tol=1e-9)

def test_two_cracks_are_different():
    tc=T.two_cracks_problem()
    assert not tc["одна_трещина"]   # π−3 ≠ √5−2 честно

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
