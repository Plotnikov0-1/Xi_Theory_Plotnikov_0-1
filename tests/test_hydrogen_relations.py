import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import hydrogen_relations as HR

def test_n2_count_four_ways():
    assert HR.n2_count_holds()
    c = HR.n2_count(4)
    assert c["C₁+1"] == c["S³_(ℓ+1)²"] == c["(2j+1)²"] == c["Σ(2l+1)"] == 16

def test_parity_bipartite():
    assert HR.transition_graph_bipartite()
    assert HR.lrl_parity_mirror_pair()
    assert HR.parity(0) == 1 and HR.parity(1) == -1

def test_cycle_return():
    assert HR.kepler_period_scaling()
    assert HR.bound_states_on_compact_S3()
    assert HR.revival_time_ratio(30) == 20.0     # 2·30/3

def test_transition_graph_so42():
    assert HR.so42_dimension() == 15
    assert HR.whole_spectrum_one_multiplet()

def test_all_bridges_and_nulls():
    assert HR.all_bridges_hold()
    nr = HR.null_results()
    assert "НЕТ" in nr["φ в водороде"]           # честный нулевой результат: φ нет

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
