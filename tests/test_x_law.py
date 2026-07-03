import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import x_law as X

def test_layer_symmetry_no_4_3():
    ratios = X.layer_symmetry_ratios()
    assert all(r is None or abs(r - 4/3) > 2e-3 for r in ratios.values())
    assert X.layer_symmetry_cannot_fix_beta()

def test_normal_form_gap():
    assert math.isclose(X.normal_form_gap(0, 0.3), 0.6)      # δλ_min=2g
    assert X.normal_form_gap(0.5, 0.3) > X.normal_form_gap(0, 0.3)  # мин при Δ=0

def test_epsX_not_universal():
    assert X.eps_X_is_not_universal()
    assert abs(X.gap_minimum_location(1, 0.3, math.e) - math.e) < 1e-2

def test_memory_diverges_at_EP():
    assert X.memory_diverges_at_EP(0) == math.inf
    assert X.memory_diverges_at_EP(0.5) == 1.0

def test_x_law_fixes_neither():
    assert X.x_law_fixes_neither()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
