import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import greek_wheel as G

def test_mirror_involution():
    assert all(G.mirror(G.mirror(p)) == p for p in range(1, 25))

def test_all_pairs_sum_24():
    assert G.all_pairs_sum_24()
    assert len(G.mirror_pairs()) == 11

def test_decompose_22_plus_2():
    d = G.decompose_24()
    assert d["парных_позиций"] == 22
    assert d["осевые_нули"] == [12, 24]
    assert d["22+2"]

def test_axis_fixed_points():
    assert G.is_axis(12) and G.is_axis(24)
    assert not G.is_axis(1)

def test_24_is_tetra_flags():
    ft = G.flags_tetrahedron()
    assert ft["flags_4E"] == 24 and ft["равно_24"]
    assert ft["euler"] == 2

def test_369_subgroup():
    assert G.three_six_nine_subgroup()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
