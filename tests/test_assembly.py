import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import assembly as A

def test_cross_domain_phi():
    cd = A.cross_domain_phi()
    assert cd["одно φ−1"]
    # три домена дают φ−1, геометрия даёт φ
    assert math.isclose(cd["ядро x²+x−1=0"], cd["динамика κX=r/φ"], abs_tol=1e-9)
    assert math.isclose(cd["оператор iter 𝔗"], A.PHI1, abs_tol=1e-9)

def test_verified_core_all_green():
    core = A.verified_core()
    assert all(core.values())
    assert len(core) == 11

def test_assembly_consistent():
    assert A.assembly_is_consistent()

def test_one_free_screw():
    fs = A.one_free_screw()
    assert fs["винт"] == "β=(4/3)α"
    assert math.isclose(fs["ратио"], 4/3, abs_tol=1e-4)

def test_one_prediction():
    pr = A.one_prediction()
    assert pr["равновесие_NIST"] == 0.60

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
