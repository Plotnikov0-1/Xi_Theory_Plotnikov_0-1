import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import relations as R

def test_mirror_involution():
    assert R.mirror_is_involution()
    assert math.isclose(R.mirror(R.PHI-1), R.PHI, rel_tol=1e-9)  # 1/(φ−1)=φ

def test_fixed_point_is_phi_minus_1():
    assert math.isclose(R.fixed_point(), R.PHI-1, abs_tol=1e-9)

def test_self_product_real_normalized():
    assert math.isclose(R.self_product(1/math.sqrt(2)+1j/math.sqrt(2)), 1.0, abs_tol=1e-12)

def test_dimensionless_invariant():
    assert R.is_dimensionless_invariant(R.ALPHA, 1e9)

def test_catalog_has_alpha_and_third():
    names=[r.name for r in R.catalog()]
    assert any('α = v₁/c' in n for n in names)
    assert any('1/3' in n for n in names)

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
