import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import clock_geometry as C

def test_1648_double_key():
    h = C.hands_1648()
    assert h["hour=2·72"] and h["minute=4·72"] and h["between"] == 144.0
    t = C.one_third_is_tetrahedral()
    assert t["tetra=109.47"] and abs(t["16/48"] - 1/3) < 1e-12

def test_golden_equator_exact():
    assert C.golden_on_equator_is_exact()

def test_mod3_families():
    m = C.mod3_families()
    assert m["√2 (2 mod3)"] == [2, 5, 8, 11]
    assert m["π (0 mod3)"] == [3, 6, 9, 12]
    assert m["φ (1 mod3)"] == [1, 4, 7, 10]
    assert m["тёмные 2·5·8·11 = класс 2"]

def test_cube_diagonal():
    c = C.cube_along_diagonal()
    assert c["poles+two rings of 3"] and c["arcsin(1/3)°"] == 19.47

def test_star_and_saddle():
    assert C.star_12_5_single_polygon()
    assert C.center_is_saddle()

def test_misread_5over3_not_phi():
    r = C.lissajous_ratio_is_fibonacci_not_phi()
    assert r["3,5 соседи Фибоначчи"]
    assert not r["равно φ"]            # честно: 5/3 ≠ φ
    assert r["LCM(5,3)"] == 15

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
