import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import matrices_map as M

def test_block_c6_reproduces_doc1():
    assert M.reproduces_doc1_spectrum()          # C₆(φ,e,π)+0.3uuᵀ+0.4vvᵀ = док-1

def test_beta_ratio_4_3():
    assert M.beta_ratio_is_4_3()                 # 0.4/0.3 = 12/5÷9/5 = 4/3

def test_d6_dyn_phi_and_particle_hole():
    d = M.d6_has_phi_and_particle_hole()
    assert d["φ_в_спектре"] and d["частица-дырка"] and d["бесследовая"]

def test_eta_xi_relation():
    assert M.eta_xi_ratio() > 0
    assert math.isclose(M.eta_xi_ratio(1.0), 0.5)   # ξ/η=1/(2·1²)

def test_three_matrices():
    assert set(M.THREE_MATRICES) == {"D6_dyn (v8)", "M6_spec (v12)", "M3 (март)"}
    assert M.THREE_MATRICES["D6_dyn (v8)"]["φ_в_спектре"]

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
