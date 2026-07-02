import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import transitions as T

def test_rydberg_factorization_exact():
    assert T.factorization_exact()
    assert T.center_mirror_quantum_zero()

def test_mirror_matches_rydberg():
    for n in range(1, 5):
        assert abs(abs(T.mirror_factored(n)) - T.rydberg_dE(n, 10 - n)) < 1e-9

def test_transition_temperatures():
    # 4↔6 «земной» шёпот ~5480 К
    assert abs(T.transition_temperature(4, 6) - 5482) < 20
    assert T.whisper_is_only_terrestrial()

def test_choice_creates_rhythm():
    assert T.choice_creates_rhythm()
    ring = T.ring_spectrum()
    assert ring == [0.5, 1.0, 1.0, 2.0, 2.0, 2.5]
    assert abs(sum(ring) - 9.0) < 1e-9   # Tr=9

def test_cube_hamming_honest():
    assert T.cube_hamming_classes() == {1: 12, 2: 12, 3: 4}
    assert T.mirrors_are_clean_antipodes()
    assert T.resonances_are_mixed_hamming()   # → 10+3+4 = модель, не геометрия

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
