"""Тесты космологии из транскрипта: эпохи БВ + шифр числа возраста.

Закрепляет: порядок эпох совпадает с физикой; «Асимметрия»=бариогенезис (CP);
возраст в пределах ~13.8 млрд; шифр числа (Q3) — без 0 и 9.
Запуск: python tests/test_cosmo_timeline.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import cosmo_timeline as C


def test_epoch_sequence_order():
    # Эпохи идут в правильном физическом порядке (Планк → рекомбинация).
    names = [e.name for e in C.EPOCHS]
    assert names[0] == "Планк"
    assert "БАРИОГЕНЕЗИС" in names[2]
    assert names[-1] == "Рекомбинация"


def test_asymmetry_is_baryogenesis():
    a = C.asymmetry_epoch()
    assert "CP" in a.physics
    assert "Асимметрии Мира" in a.transcript


def test_age_in_real_range():
    # Возраст из транскрипта в пределах реального ~13.8 млрд (откл < 0.5%).
    assert abs(C.age_ratio() - 1.0) < 0.005
    assert 13.7e9 < C.AGE_TRANSCRIPT < 13.9e9


def test_number_cipher_missing_0_and_9():
    # Шифр: в числе присутствуют цифры 1..8, отсутствуют границы 0 и 9.
    c = C.number_cipher()
    assert c["отсутствуют"] == [0, 9]
    assert c["присутствуют"] == [1, 2, 3, 4, 5, 6, 7, 8]


def test_central_crack_456():
    # Сердце числа: 456 = трещина 4/φ : ½ : 1/φ, Op_4=4, палиндром 565.
    cc = C.central_crack()
    assert abs(cc["Op_4=T_вх/T_вых"] - 4.0) < 1e-9
    assert abs(cc["6 → T_вых=1/φ=φ−1 (аттрактор)"] - ((5**0.5 - 1) / 2)) < 1e-9
    assert cc["палиндром_565"] == "565"


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
