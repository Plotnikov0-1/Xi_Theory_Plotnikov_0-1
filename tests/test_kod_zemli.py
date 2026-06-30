import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import kod_zemli as K

def test_on_sphere():
    assert K.on_sphere()

def test_seed_generates_cube():
    assert K.seed_generates_cube()
    assert len(K.generate_cube()) == 8

def test_mirror_is_negation():
    import numpy as np
    assert (K.mirror_inversion() == -K.TETRAHEDRON).all()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
