import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import proof_core as P

def test_step1_spectrum():
    s = P.step1_circulant_spectrum()
    assert s["ок"] and s["след"] == 9.0 and s["δλ_min"] == 0.5
    assert s["спектр"] == [0.5, 1.0, 1.0, 2.0, 2.0, 2.5]

def test_step2_niven_ceiling():
    s = P.step2_niven_ceiling()
    assert s["рациональные N (3..12)"] == [3, 4, 6]
    assert s["потолок = max"] == 6
    assert s["N=5 ломает"] and s["N=7 ломает"]

def test_step3_golden_point():
    assert P.step3_golden_point()["ок"]

def test_step4_identities():
    s = P.step4_golden_identities()
    assert s["ок"] and s["целая_часть√5"] == 2

def test_step5_cp_R_G():
    s = P.step5_cp_is_R_G()
    assert s["глоб.порядок"] == 12
    assert s["на {2,5,8} 3-цикл (120°)"]
    assert P.cp_permutation() == {1:9,2:5,3:7,4:6,5:8,6:1,7:3,8:2,9:4}

def test_step6_roots_of_unity():
    assert P.step6_roots_of_unity()["ок"]

def test_step7_spiral():
    assert P.step7_golden_spiral()["ок"]

def test_all_steps():
    assert P.all_steps_pass()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
