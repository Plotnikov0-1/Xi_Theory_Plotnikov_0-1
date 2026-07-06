import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import clock_gears as G

def test_decagon_octagon():
    assert G.decagon_is_phi()      # 10 зубьев = φ
    assert G.octagon_is_silver()   # 8 зубьев = 1+√2

def test_ring_lcm():
    r = G.ring_is_lcm()
    assert r["40=LCM(8,10)"] and r["передача 10-колеса"] == 4 and r["передача 8-колеса"] == 5

def test_edges_12():
    e = G.edges_closed()
    assert e["всего рёбер"] == 12 and e["= 12-каркас"]

def test_teeth_totals():
    t = G.teeth_totals()
    assert t["малые"] == 72 and t["кольца"] == 80 and t["всего"] == 152

def test_dodeca_and_families():
    d = G.dodecahedron_is_phi_symmetry()
    assert d["|G| икосаэдра"] == 120 and d["3 держателя × 4 колеса"] == 12
    f = G.two_metallic_families()
    assert f["золото φ"]["teeth"] == 10 and f["серебро √2"]["teeth"] == 8

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
