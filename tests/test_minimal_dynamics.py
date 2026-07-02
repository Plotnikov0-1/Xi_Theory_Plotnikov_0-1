import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import minimal_dynamics as M

P = dict(r_eps=1.0, kappa=0.8, Gamma=0.7, b_S=1.3, eps_targ=2.0)

def test_t3_unique_positive_stationary():
    assert M.unique_positive_root(**P)
    es, Ss, Xs = M.stationary_point(**P)
    assert es > 0 and 0 <= Ss <= 1
    assert abs(Ss + Xs - 1) < 1e-12

def test_t4_stability_and_det_formula():
    assert M.is_stable(**P)
    assert M.regime_type(**P) in ("узел", "фокус", "критическое затухание")

def test_t2_domain_invariant():
    assert M.domain_invariant(**P)

def test_t5_golden_manifold():
    assert M.golden_special_case(1.0)
    assert abs(M.golden_manifold_kappaX(1.0, 1.0) - 1.0/M.PHI) < 1e-12

def test_corollary_chain():
    assert M.corollary_chain()

def test_t7_aux_mode_realization():
    assert M.aux_realization_matches()

def test_t8_x_regime_gap():
    assert M.gap_minimal_at_delta_zero()
    assert M.x_regime_gap(0, 0) == 0
    assert abs(M.x_regime_gap(0, 0.1) - 0.2) < 1e-12

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
