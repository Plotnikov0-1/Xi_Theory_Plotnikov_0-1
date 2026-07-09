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

def test_equilateral_triangles():
    t = CC.equilateral_ray_triangles(1.0)
    assert t["число треугольников"] == 12
    assert t["вершина = основание"]                    # ◇ радиус вершины = длина основания
    assert abs(t["радиус вершины"] - 0.517638) < 1e-5

def test_inner_dodecagon_circles():
    d = CC.inner_dodecagon_circles(1.0)
    assert d["через 2 вершины (охват 1 ребро)"] and d["= ρ·√3/2 = ρ·cos30°"]
    assert abs(d["внутр. пересечение соседних"] - 0.866025) < 1e-5

def test_scale_six_across():
    s = CC.scale_six_across(1.0)
    assert abs(s["кругов на диаметр при R√2/4"] - 5.657) < 1e-2   # 4√2 ≈ 5.66 ≈ 6
    assert s["круг вписан в луч-треугольник"]

def test_black_white_tangency():
    t = CC.black_white_tangency(1.0, 0.6)
    assert t["условие r≥ρ/2"] and t["чёрный глубже белого"]
    assert t["чёрный центр (касается 2 соседей)"] is not None

def test_ring_intersection():
    ri = CC.ring_intersection_inner_12gon(0.52, 0.159)
    assert ri["круги пересекаются (disc≥0)"] and ri["12 точек = внутр. 12-угольник"]
    assert ri["r_int (точка пересечения)"] is not None

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
