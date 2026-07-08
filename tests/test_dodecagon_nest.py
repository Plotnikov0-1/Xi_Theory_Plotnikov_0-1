import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import dodecagon_nest as D

def test_exact_ratios():
    assert abs(D.inner_ratio(3) - (math.sqrt(3) - 1)) < 1e-12          # три семьи
    assert abs(D.inner_ratio(5) - (2 - math.sqrt(3))) < 1e-12          # додекаграмма
    assert abs(D.inner_ratio(4) - 2 * math.sin(math.radians(15))) < 1e-12

def test_three_families():
    t = D.three_families_are_12_3()
    assert t["= {12/3}"] and t["= √3−1"]
    assert [3, 6, 9, 12] in t["три квадрата (шаг 3)"]

def test_nested():
    n = D.nested_three(1.0, 3)
    assert n["радиусы"][0] == 1.0 and abs(n["радиусы"][1] - (math.sqrt(3) - 1)) < 1e-4

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
