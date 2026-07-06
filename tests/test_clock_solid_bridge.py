import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import clock_solid_bridge as B

def test_cube_eight_nodes():
    c = B.cube_is_eight_clock_nodes()
    assert c["узлы"] == [1, 2, 3, 4, 6, 7, 8, 9] and c["без 5 и 0"]
    assert c["−I (антиподы)"] and c["зеркало сумма-10"] == [(1, 9), (2, 8), (3, 7), (4, 6)]

def test_cube_hexagon():
    h = B.cube_diagonal_hexagon()
    assert h["2 полюса + 6-угольник"] and h["arcsin(1/3)°"] == 19.47

def test_three_golden_rectangles():
    r = B.icosa_three_golden_rectangles()
    assert r["групп"] == 3 and r["по 4 вершины"] and r["3×4=12"]
    assert r["каждый золотой (отн=φ)"]

def test_phi_enters_dodeca():
    p = B.phi_enters_at_dodeca()
    assert p["8+12=20"] and p["золотые R²=3"] and p["φ в кубе (целые ±1)"] is False

def test_two_gears():
    g = B.two_gears_two_groups()
    assert g["φ живёт в 120"]

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
