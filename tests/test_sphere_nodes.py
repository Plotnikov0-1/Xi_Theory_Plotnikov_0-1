import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import sphere_nodes as S

def test_equator_structure_5_10_20():
    e = S.equator_structure(5, 3)
    assert e["оба нечёт"] is True
    assert e["операторов (крестов)"] == 5        # пентагон
    assert e["нитей (проходов)"] == 10
    assert e["дуг"] == 20
    assert e["пересечения есть"] is True

def test_parity_law():
    p = S.parity_law()
    assert p["нечёт·нечёт(копрост) → операторов = a"] == {3: 3, 5: 5, 7: 7, 9: 9, 11: 11}
    assert p["все равны a"] is True
    assert p["b чётное (5,6) → 0"] is True        # b=6 не даёт пересечений
    assert p["ровно 10 невозможно (перебор ≤15)"] is True

def test_even_b_has_no_operators():
    assert S.operators_count(5, 3) == 5
    assert S.operators_count(5, 6) == 0           # ★ моя ошибка исправлена

def test_golden_pentagon():
    assert S.golden_pentagon_is_exact()           # sin72/sin36 = φ

def test_exact_counts():
    e = S.exact_counts(5, 3)
    assert e["нитей (проходов экватора)"] == 10
    assert e["операторов (пересечений)"] == 5
    assert e["волн (долгота) b"] == 3
    assert S.equator_crossings_count(5) == 10

def test_self_intersections_range():
    si = S.self_intersections_numeric(5, 3, samples=30000)
    assert 25 <= si["узлов (~)"] <= 45
    assert si["из них полюса"] >= 1

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
