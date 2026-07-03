import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import canon_constants as K

def test_alpha_exact_collective_mode():
    assert math.isclose(K.collective_mode(9/5), 13.3)
    assert K.alpha_controls_mode_exactly()

def test_beta_is_free():
    assert K.beta_is_free()
    assert K.scan_rational_beta() == []          # никакой рациональный β не спасает
    assert math.isclose(K.beta_over_alpha(), 4/3)

def test_beta_spectrum_irrational_at_2_4():
    assert not K.beta_spectrum_rational(12, 5)   # β=2.4 иррационален

def test_N_is_modes_not_digits():
    nm = K.N_meaning()
    assert nm["N=6 мод (размерность)"]
    assert nm["«6 знаков» имеет смысл"] is False
    assert K.phi_inv3_is_irrational()

def test_epsX_is_not_e():
    ex = K.eps_X_is_not_e()
    assert not ex["это e?"]                       # 2.721 ≠ e

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
