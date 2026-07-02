import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import node5 as N

def test_only_s_touches_center():
    assert N.only_s_touches_center(5)
    assert N.psi_squared_at_origin(5,0) > 0
    assert N.psi_squared_at_origin(5,1) == 0

def test_pitchfork():
    assert N.pitchfork_fixed_points(-0.5) == [0.0]
    assert len(N.pitchfork_fixed_points(0.5)) == 3
    assert N.higgs_saddle_at_center(0.5)
    assert not N.center_unstable_above(-0.5)

def test_self_mirror_only_five():
    assert N.is_self_mirror(5)
    assert all(not N.is_self_mirror(n) for n in range(1,10) if n != 5)

def test_third_road():
    assert N.center_is_shortcut()
    assert N.ops_from_center_to_antipode() == 1
    assert N.steps_along_edges_to_antipode() == 3

def test_dimers_disconnected():
    assert N.mirror_graph_components() == 5
    assert N.is_disconnected_dimers()

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
