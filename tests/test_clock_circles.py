import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import clock_circles as CC

def test_layers_families():
    m = CC.layers_map_to_families()
    assert m["чёрные {2,5,8,11}"]["семья"] == "√2" and m["чёрные {2,5,8,11}"]["mod3"] == [2]
    assert m["белые {3,6,9,12}"]["семья"] == "π" and m["белые {3,6,9,12}"]["mod3"] == [0]
    assert m["пустые {1,4,7,10}"]["mod3"] == [1]

def test_phi_channels_empty():
    assert CC.phi_channels_empty()
    assert CC.CHANNELS == [1, 4, 7, 10]

def test_tangent_ring():
    t = CC.twelve_tangent_ring(1.0)
    assert t["касание (d=2r)"] and t["число кругов"] == 12
    assert abs(t["r/R"] - 0.2588) < 1e-3

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
