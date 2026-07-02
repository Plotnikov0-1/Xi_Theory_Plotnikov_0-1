import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import hydrogen_temperature as H

def test_peak_near_balmer_max():
    # узел 2 (Бальмер) пик в реальном диапазоне звёзд класса A (~8-10 кК)
    T2 = H.peak_temperature(2, 1e19)
    assert 8000 < T2 < 10000

def test_increase_and_converge():
    assert H.temperatures_increase_and_converge(1e19)

def test_peak_asymmetric():
    # «середина ложна» — пик смещён от середины полумаксимумов
    assert H.peak_is_asymmetric(2, 1e19)

def test_absolute_depends_on_environment():
    # абсолют задаёт МИР: выше n_e → выше T
    assert H.peak_temperature(2, 1e20) > H.peak_temperature(2, 1e19)

def test_doppler_scales_as_sqrt_T():
    w1, w2 = H.doppler_width(3000), H.doppler_width(30000)
    import math
    assert math.isclose(w2 / w1, math.sqrt(10), rel_tol=1e-6)
    # абсолют: Hα при 3000 К ≈ 25.6 пм
    assert abs(w1 / 1e-12 - 25.6) < 0.5

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
