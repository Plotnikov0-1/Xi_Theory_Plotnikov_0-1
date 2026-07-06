import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import sphere_nodes as S

def test_gears():
    g = S.gears()
    assert g["колесо-верт a"] == 5 and g["колесо-долгота b"] == 3
    assert g["соседи Фибоначчи"] and g["LCM (меш)"] == 15

def test_exact_counts():
    e = S.exact_counts()
    assert e["пересечений экватора"] == 10
    assert e["проходов полюса N"] == 5 and e["проходов полюса S"] == 5
    assert e["оборотов долготы"] == 3
    assert S.equator_crossings_count() == 10

def test_self_intersections_range():
    si = S.self_intersections_numeric(30000)
    # ~35 обычных узлов + 2 полюса; допускаем численный разброс
    assert 25 <= si["узлов (~)"] <= 45
    assert si["из них полюса"] >= 1

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
