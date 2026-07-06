import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import fundament as F

def test_all_layers_hold():
    assert F.verify_all()

def test_each_layer_bools_true():
    for fn in F.LAYERS:
        for k, v in fn().items():
            if isinstance(v, bool):
                assert v, f"{fn.__name__}: {k} is False"

def test_seven_layers():
    assert len(F.LAYERS) == 7

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
