import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import triad_zeros as T

def test_three_plus_one():
    tp = T.three_plus_one()
    assert tp["φ"]["zero"] == 10 and tp["√2"]["zero"] == 11 and tp["π"]["zero"] == 12
    assert all(v["same class"] for v in tp.values())
    assert (tp["φ"]["zero mod3"], tp["√2"]["zero mod3"], tp["π"]["zero mod3"]) == (1, 2, 0)

def test_z4():
    assert T.each_family_is_Z4()

def test_thirteen():
    e = T.thirteen_echo()
    assert e["re-entry at"] == 1 and e["=6·13"] and e["Σ√2=2·13"]

def test_sums_means():
    fm = T.family_sums_means()
    assert fm["φ"]["Σ"] == 22 and fm["√2"]["Σ"] == 26 and fm["π"]["Σ"] == 30
    assert fm["φ"]["mean"] == 5.5 and fm["√2"]["mean"] == 6.5 and fm["π"]["mean"] == 7.5

def test_cosmology_flagged_hypothesis():
    c = T.cosmology_is_hypothesis()
    assert c["derived"] is False and len(c["три источника"]) == 3

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
