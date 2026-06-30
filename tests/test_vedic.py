"""Тесты ведической структуры: юги 4:3:2:1, Сатья=12³, троица=CP-тройка."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import vedic as V

def test_satya_is_12_cubed():
    assert V.satya_is_12_cubed()
    assert V.YUGAS["Сатья"] // 1000 == 1728

def test_yuga_ratio_4321():
    assert V.yuga_ratio() == [4, 3, 2, 1]
    assert V.MAHA_YUGA == 4_320_000
    assert V.KALPA == 4_320_000_000

def test_necessity_of_third_is_cp3():
    nt = V.necessity_of_third()
    assert nt[2] == 0 and nt[3] == 1   # CP требует 3 поколений

def test_age_not_a_yuga_multiple():
    assert not V.fits_age()["кратно"]   # честно: фит не идеален

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')

if __name__=='__main__': _run_all()
