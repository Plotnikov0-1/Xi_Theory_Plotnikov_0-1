import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import ten_operators as T

PHI = (1 + 5 ** 0.5) / 2

def test_transition_constants():
    assert abs(T.transition_constant(1) - (PHI - 1)) < 1e-12   # φ−1
    assert abs(T.transition_constant(3) - PHI) < 1e-12          # φ
    assert abs(T.transition_constant(5) - 2) < 1e-12            # диаметр

def test_operators_identity():
    ops = T.operators()
    assert set(ops) == {1, 2, 3, 4, 5}
    assert "φ" in ops[3]["identity"]

def test_golden_relations_all_true():
    rel = T.golden_relations()
    assert all(rel.values())                                    # все соотношения точны

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
