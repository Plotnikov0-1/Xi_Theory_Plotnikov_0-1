import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import operator_algebra as OA

def test_transition_matrix():
    assert len(OA.edges()) == 12                      # рёбра куба
    assert len(OA.STATES) == 8

def test_invariant_spectrum():
    assert OA.invariant_spectrum() == [-3.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 3.0]

def test_R_is_automorphism():
    Rmap = {n: OA.R(n) for n in OA.STATES}
    assert OA.is_automorphism(Rmap)

def test_the_door():
    d = OA.the_door()
    assert d["дверь"]                                 # φ≠id, но I сохранён
    assert d["R двигает узлов"] == 8
    assert d["спектр сохранён"]

def test_closure_and_bipartite():
    assert OA.is_connected()                          # замыкание по путям
    assert OA.is_bipartite()                          # каждый переход меняет тетраэдр

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
