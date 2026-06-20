"""Тесты: 137 как отношение скоростей α=v₁/c (интуиция «137 про скорость»).

Закрепляет реальную выводимую физику: электрон в осн. состоянии H бежит в
137 раз медленнее света; α — отношение масштабов длины (каскад 1:α:α²).
Запуск: python tests/test_fine_structure_speed.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import fine_structure_speed as F


def test_alpha_is_137():
    assert math.isclose(1 / F.alpha(), 137.035999, abs_tol=1e-3)


def test_137_is_speed_ratio():
    # 1/α = c/v₁ — электрон в основном состоянии в 137 раз медленнее света.
    s = F.speed_ratio()
    assert math.isclose(s["1/α=c/v₁"], 137.035999, abs_tol=1e-3)
    assert math.isclose(s["v₁_м/с"], s["v₁_проверка"], rel_tol=1e-9)


def test_ground_speed_value():
    # v₁ ≈ 2188 км/с.
    assert math.isclose(F.electron_ground_speed(), 2.1877e6, rel_tol=1e-3)


def test_length_cascade_is_alpha():
    # a₀ : λ_C : r_e = 1 : α : α² — каждый шаг в 137 раз.
    L = F.length_cascade()
    assert math.isclose(L["λ_C/a₀"], F.alpha(), rel_tol=1e-6)
    assert math.isclose(L["r_e/λ_C"], F.alpha(), rel_tol=1e-6)


def test_zitterbewegung_a_omega_c():
    z = F.zitterbewegung()
    assert math.isclose(z["a·ω"], z["c"], rel_tol=1e-9)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
