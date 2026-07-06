import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import clock_layers as L

def test_three_squares():
    assert L.three_squares()
    assert L.quotient_is_Z3()
    cs = L.clock_cosets()
    assert cs["π"]["points"] == [3, 6, 9, 12]
    assert cs["φ"]["points"] == [1, 4, 7, 10]
    assert cs["√2"]["points"] == [2, 5, 8, 11]
    assert [cs[f]["rotation°"] for f in ("π", "φ", "√2")] == [0, 30, 60]

def test_phi_channels():
    p = L.phi_family_are_channels()
    assert p["φ-канал"] and p["Ю на 10 ∈ φ-канал"]

def test_membrane_structure():
    m = L.membrane_vs_structure()
    assert m["мембрана √2"] and m["структура π"]

def test_layers_and_lissajous():
    assert L.layers_are_transitions()["depth=transition"]
    lp = L.lissajous_period(5, 3)
    assert lp["coprime"] and lp["period"] == "15π"

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
