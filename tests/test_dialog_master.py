"""Тесты ядра ДИАЛОГ, константы Ω_D и мастер-карты ↔ водород.

Закрепляют ключевые результаты сессии: единая константа диалога, синхронизация
геометрии узлов/переходов с атомом водорода, и согласованность слоёв.
Запуск:  python tests/test_dialog_master.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import (dialog, dialog_constant, master_map, three_quark, roman,
                 whisper, faces, spectral_colors)

PHI = (1 + math.sqrt(5)) / 2


def test_dialog_constant_modulus_is_phi_minus_1():
    # |Ω_D| = φ−1 — «расстояние между аспектами».
    assert math.isclose(dialog_constant.modulus(), PHI - 1, abs_tol=1e-12)


def test_dialog_constant_phase_is_golden_angle():
    # arg(Ω_D) = золотой угол 2π/φ² ≈ 137.508°.
    assert math.isclose(dialog_constant.phase_deg(), 360 / PHI**2, abs_tol=1e-9)


def test_dialog_converges():
    # |Ω_D| < 1 ⇒ итерация сходится (аспекты не важны, инвариант один).
    assert dialog_constant.converges()


def test_gamma_star_is_pi_over_4phi():
    # Точная φ·π-опора: Γ* = π/(4φ).
    assert math.isclose(dialog_constant.gamma_star_exact(), math.pi / (4 * PHI),
                        abs_tol=1e-12)


def test_euler_mirror():
    # e^{iπ} = −1 = зеркало −I (особый случай Ω_D на фазе π).
    assert dialog.self_reference()["e^{iπ} = −1 (зеркало)"]


def test_completed_crack_is_q3():
    # «Законченный 137.5 / трещина» помечено как Q3 (не вывод α⁻¹).
    d = dialog_constant.completed_and_crack()
    assert "Q3" in d["статус"]
    assert 0.4 < d["трещина_зазор"] < 0.55


def test_master_map_hydrogen_lines():
    # Узлы/переходы совпадают с реальными линиями водорода.
    v = master_map.verify()
    assert v["линии_водорода_сходятся"]


def test_master_map_triad_channels():
    # Триада А·Д·Л = семья каналов {1,4,7}, узлы — вершины, трещина 7→4→1.
    v = master_map.verify()
    assert v["триада_каналы"]
    assert v["триада_1_4_7_вершины"]
    assert v["трещина_7_4_1"]


def test_master_map_selection_counts():
    # 17 разрешённых / 11 запрещённых переходов.
    v = master_map.verify()
    assert v["разрешено"] == 17 and v["запрещено"] == 11


def test_baryon_three_and_cubes():
    # Барион = ровно 3 (синглет 1 раз); кубы 3³=27, 12³=1728.
    assert three_quark.singlet_multiplicity() == 1
    cp = three_quark.cube_parallels()
    assert cp["3³"] == 27 and cp["12³"] == 1728


def test_roman_rule_of_three():
    # Римская запись: символ не повторяется больше трёх раз.
    assert roman.verify_max_three()["правило_трёх"]


def test_whisper_not_weak_but_deaf():
    # Шёпот не слаб: при малых «одеждах» сигнал (память) есть всегда.
    assert whisper.not_weak_but_deaf()


def test_faces_twelve_colours():
    # 12 граней = 12 красок (двенадцать в 3+7+12).
    assert len(faces.faces()) == 12


def test_faces_match_balmer_lines():
    # Видимые переходы модели совпадают с серией Бальмера:
    # 2↔3=Hα(656), 2↔4=Hβ(486), 2↔6=Hδ(410).
    vis = {(d["a"], d["b"]): d["λ_нм"] for d in spectral_colors.model_visible_transitions()}
    assert math.isclose(vis[(2, 3)], 656.1, abs_tol=0.5)
    assert math.isclose(vis[(2, 4)], 486.0, abs_tol=0.5)
    assert math.isclose(vis[(2, 6)], 410.1, abs_tol=0.5)


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  OK  {fn.__name__}")
    print(f"\nВсе {len(fns)} тестов пройдены.")


if __name__ == "__main__":
    _run_all()
