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

def test_interpretations_not_asserted():
    # интерпретации (○) — строки, НЕ булевы предикаты; НЕ идут в verify_all
    interp = F.interpretations()
    assert len(interp) >= 8
    for k, v in interp.items():
        assert isinstance(v, str) and (v.startswith("○") or v.startswith("≈"))

def test_native_54_not_asserted():
    # ключевое исправление стресс-теста: «нативная сфера 5:4» больше НЕ предикат ◇
    for fn in F.LAYERS:
        keys = " ".join(fn().keys()).lower()
        assert "5:4" not in keys and "нативно" not in keys

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
