import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import roots_of_unity as R

def test_i_and_mirror():
    n = R.i_is_node()
    assert n["i = узел"] == 3 and n["i²=−1 = узел"] == 6
    assert R.mul_i(1) == 4 and R.mul_i(10) == 1      # +3 генератор
    assert R.mirror(1) == 7 and R.mirror(5) == 11    # +6 зеркало

def test_families_are_i_orbits():
    f = R.families_are_i_orbits()
    assert f["= три семьи"] and f["12/порядок(i)=4 → 3 орбиты"]

def test_node_constants():
    # угол узла 3 = 90° (это i); узел 6 = 180° (это −1)
    assert R.node_angle_deg(3) == 90 and R.node_angle_deg(6) == 180
    c3 = R.node_constant(3)
    assert c3["семья (○)"] == "π"

def test_arrow_involution():
    a = R.arrow_of_time()
    assert a["i² инволюция (T²=1)"]

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
