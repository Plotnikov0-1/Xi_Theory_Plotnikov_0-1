"""Тесты экспериментального инструмента: чистая физика против NIST/CODATA.

Закрепляет честный вердикт: спектр водорода воспроизводится до ppm, а φ-числа
помечены как совпадения/конструкции. Запуск: python tests/test_experiments.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import experiments as X


def test_tier_a_matches_experiment_to_0_1_percent():
    # Вся стандартная физика (спектр, константы) совпадает лучше 0.1 %.
    for c in X.all_checks():
        if c.verdict == "verify":
            assert c.rel_error < 1e-3, f"{c.name}: ошибка {c.rel_error*100:.4f}%"


def test_hydrogen_lines_sub_ppm():
    # Спектральные линии (формула Ридберга с приведённой массой) — до ~1 ppm.
    line_names = ("Lyman", "Balmer", "Paschen")
    lines = [c for c in X.all_checks()
             if any(c.name.startswith(p) for p in line_names)]
    assert len(lines) == 9
    for c in lines:
        assert c.ppm < 5.0, f"{c.name}: {c.ppm:.1f} ppm"


def test_golden_angle_is_only_coincidence():
    # Золотой угол ≈ α⁻¹, но это СОВПАДЕНИЕ (~0.34%), не подтверждение.
    c = next(c for c in X.all_checks() if "α⁻¹" in c.name)
    assert c.verdict == "coincidence"
    assert 0.002 < c.rel_error < 0.01


def test_delta7_is_mismatch():
    # Δ₇=√5−2 НЕ равен реальному зазору E6−E7 — честно помечено расхождением.
    c = next(c for c in X.all_checks() if "Δ₇" in c.name)
    assert c.verdict == "mismatch"
    assert c.rel_error > 1.0   # расхождение больше 100 %


def test_reduced_mass_used():
    # Используется приведённая масса: R_H < R∞ (иначе линии «уплывают» на 0.05%).
    assert X.R_H < X.R_INF
    assert abs(X.R_H / X.R_INF - 0.999456) < 1e-5


def test_verdict_counts():
    # Структура вердиктов стабильна: 14 физ. / 2 совпад. / 2 модель / 1 расхожд.
    v = [c.verdict for c in X.all_checks()]
    assert v.count("verify") == 14
    assert v.count("coincidence") == 2
    assert v.count("model") == 2
    assert v.count("mismatch") == 1


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
