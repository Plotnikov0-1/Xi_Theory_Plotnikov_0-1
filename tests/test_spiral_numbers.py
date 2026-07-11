import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import spiral_numbers as S

def test_center_and_zeros():
    c = S.center_start()
    assert c["старт"] == 10 and c["как пара"] == "1:0"
    assert S.three_zeros() == [10, 11, 12]

def test_forty():
    f = S.forty_full_measure()
    assert f["=120/3"] and f["=4·10"]

def test_arrow_forward_spiral():
    a = S.arrow_always_forward(24, 12)
    assert a["числа монотонны (вперёд)"] and a["позиции повторяются (круг)"]
    assert a["спираль (винт), не круг"]
    assert S.spiral_position(10) == 10 and S.spiral_position(22) == 10   # позиция циклится

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
