import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import sphere_nodes as S

def test_doubling():
    d = S.doubling()
    assert d["база 5:3"] == 5 and d["удвоено 5:6"] == 10
    assert d["×2 корректно"] is True
    assert d["★ 10:6 вырождено"] is True          # 5:3→10:6 нельзя (gcd=2)

def test_equator_operators_pentagon_decagon():
    base = S.distinct_equator_operators(5, 3)
    dbl = S.distinct_equator_operators(5, 6)
    assert base["операторов"] == 5 and base["шаг"] == [72.0]      # пентагон
    assert dbl["операторов"] == 10 and dbl["шаг"] == [36.0]       # декагон
    assert not dbl["вырождено (gcd>1)"]

def test_golden_preserved():
    assert S.golden_pentagon_is_exact()            # sin72/sin36 = φ
    assert S.golden_decagon_is_exact()             # 1/(2 sin18) = φ

def test_exact_counts_doubled():
    e = S.exact_counts(5, 6)
    assert e["проходов экватора"] == 10
    assert e["операторов экватора"] == 10
    assert e["проходов полюса N"] == 5 and e["проходов полюса S"] == 5
    assert e["волн (долгота) b"] == 6
    assert S.equator_crossings_count(5) == 10

def test_self_intersections_range():
    si = S.self_intersections_numeric(5, 6, samples=30000)
    assert 35 <= si["узлов (~)"] <= 60             # 5:6 плотнее базы
    assert si["из них полюса"] >= 1

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
