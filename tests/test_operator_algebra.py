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

def test_phi_invariant_of_120_not_48():
    assert OA.cube_has_no_phi()                       # G=48: целые, φ нет
    assert OA.icosa_has_sqrt5()                       # G=120: √5 в спектре
    assert OA.golden_is_invariant_of_120_not_48()     # φ вынуждено, не назначено
    import math
    phi, minus = OA.A5_character_phi()
    assert math.isclose(phi, OA.PHI) and math.isclose(minus, -1/OA.PHI)

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
