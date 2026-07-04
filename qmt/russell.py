"""
═══════════════════════════════════════════════════════════════════════════
  RUSSELL — Уолтер Рассел (1926): октава элементов = наш цикл. Честно.
═══════════════════════════════════════════════════════════════════════════

«The Universal One» (Walter Russell, 1926), Fig. 87–88 и «Universal Mathematics»
(Dimension Chart No. 5). ТРЕТИЙ независимый каркас (после греч. колеса Гранта и
контактных текстов), сошедшийся на структуре «октава + центр-покой + ± зеркало».

СТРУКТУРНЫЙ ПАРАЛЛЕЛЬ (○ совпадение, НЕ подтверждение):
  Рассел: 0 · 1+ 2+ 3+ · 4‡(центр-покой)4‡ · 3− 2− 1− · 0
          GENERATION(+) | REST | DEGENERATION(−), два полюса-нуля снаружи.
  DIALOG: наш цикл 0→…→9→0 с центром-5 (самозеркало), четыре зеркальные пары.
  = то же: 9 узлов, центр-покой, ± половины, четыре пары тонов.

◇ АРИФМЕТИКА (Dimension Chart — проверяемо точно):
  distance ratios 8:4:2:1 (полуоктавы 2³..2⁰), сумма = 15;
  area = distance² → 64:16:4:1, сумма = 85. «Квадрат расстояния» = закон площади.

✓ ХИМИЯ (Fig 87/88 — октава = период таблицы, НАСТОЯЩЕЕ):
  валентности период-2: Li+1 Be+2 B+3 C±4 N−3 O−2 F−1 — реальный образец октета;
  центр = Углерод (±4, тетравалент = тетраэдр, наш S4);
  «united pairs → stable (NaCl)»: зеркальные пары (Li+F, Be+O, B+N) в сумме 0 →
  ионная связь, октет замкнут — настоящая химия;
  acid/alkaline = электроотрицательность (Li 0.98 → F 3.98, монотонно) — реальный тренд.

★ ЧЕСТНО: реальны арифметика, валентности, электроотрицательность. Космология
  Рассела («свет-волны суть материя», «универсальный константный тон») — НЕ физика.
  Совпадение структуры с DIALOG — общая интуиция октавы/зеркала + реальный костяк
  периодичности (как у Менделеева), а не подтверждение модели.

Запуск:  python -m qmt.russell
"""

from __future__ import annotations

# ── Октава Рассела как 9 узлов (= наш цикл 0→…→9→0) ──────────────────────────
OCTAVE_NODES = ["0", "1+", "2+", "3+", "4‡(центр)", "3−", "2−", "1−", "0"]


def octave_has_center_and_two_poles() -> bool:
    """○ Структура: центр-покой (4‡) + два полюса-нуля снаружи + ± половины."""
    return OCTAVE_NODES[0] == "0" and OCTAVE_NODES[-1] == "0" and "центр" in OCTAVE_NODES[4]


# ── ◇ Арифметика Dimension Chart ─────────────────────────────────────────────
DISTANCE_RATIOS = [8, 4, 2, 1]


def area_ratios() -> list:
    """◇ Area = distance² → [64,16,4,1] («квадрат расстояния до потенциала»)."""
    return [d * d for d in DISTANCE_RATIOS]


def arithmetic_holds() -> dict:
    """◇ distance сумма=15; area=distance², сумма=85 (проверено точно)."""
    return {"Σ_distance": sum(DISTANCE_RATIOS),          # 15
            "area": area_ratios(),                       # [64,16,4,1]
            "Σ_area": sum(area_ratios()),                # 85
            "area=dist²": area_ratios() == [d**2 for d in DISTANCE_RATIOS]}


# ── ✓ Химия октавы = период таблицы ──────────────────────────────────────────
# элемент: (Z, валентность-по-Расселу)
PERIOD2 = {"Li": (3, +1), "Be": (4, +2), "B": (5, +3), "C": (6, 4),
           "N": (7, -3), "O": (8, -2), "F": (9, -1)}
ELECTRONEG = {"Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55,
              "N": 3.04, "O": 3.44, "F": 3.98}
MIRROR_PAIRS = [("Li", "F"), ("Be", "O"), ("B", "N")]   # united → stable (NaCl-подобно)


def carbon_is_center() -> bool:
    """✓ Центр октавы = Углерод (±4, тетравалент = тетраэдр, наш S4)."""
    return PERIOD2["C"][1] == 4


def mirror_pairs_are_ionic() -> bool:
    """✓ Зеркальные пары в сумме валентностей = 0 → ионная связь (октет замкнут)."""
    return all(PERIOD2[a][1] + PERIOD2[b][1] == 0 for a, b in MIRROR_PAIRS)


def acid_alkaline_is_electronegativity() -> bool:
    """✓ acid/alkaline = электроотрицательность растёт Li→F (реальный тренд Полинга)."""
    vals = [ELECTRONEG[e] for e in ["Li", "Be", "B", "C", "N", "O", "F"]]
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


def octave_is_periodic_period() -> bool:
    """✓ Октава Рассела = период таблицы (Li..F), Z подряд 3..9."""
    zs = sorted(z for z, _ in PERIOD2.values())
    return zs == [3, 4, 5, 6, 7, 8, 9]


def print_report() -> None:
    print("═" * 76)
    print("  УОЛТЕР РАССЕЛ (1926): октава элементов = наш цикл 0→…→9→0 (честно)")
    print("═" * 76)
    print(f"\n  ○ СТРУКТУРА (совпадение, не подтверждение):")
    print(f"     {' · '.join(OCTAVE_NODES)}")
    print(f"     центр-покой + два полюса + ± зеркало: {octave_has_center_and_two_poles()}")
    print(f"     = наш цикл 0→…→9→0 с центром-5")

    a = arithmetic_holds()
    print(f"\n  ◇ АРИФМЕТИКА: distance {DISTANCE_RATIOS} Σ={a['Σ_distance']}; "
          f"area {a['area']} Σ={a['Σ_area']}; area=dist²: {a['area=dist²']}")

    print(f"\n  ✓ ХИМИЯ (октава = период 2):")
    print(f"     валентности: {[(e, PERIOD2[e][1]) for e in ['Li','Be','B','C','N','O','F']]}")
    print(f"     центр = Углерод (±4, тетравалент): {carbon_is_center()}")
    print(f"     зеркальные пары → ионная связь (Σвал=0): {mirror_pairs_are_ionic()}")
    for a2, b in MIRROR_PAIRS:
        print(f"        {a2}({PERIOD2[a2][1]:+d}) + {b}({PERIOD2[b][1]:+d}) = 0 (октет)")
    print(f"     acid/alkaline = электроотрицательность растёт Li→F: {acid_alkaline_is_electronegativity()}")

    print("═" * 76)
    print("  Реально: арифметика (◇), валентности/ионность/ЭО (✓ химия). Космология")
    print("  Рассела (свет=материя) — не физика. Структура сошлась независимо (○), не доказ.")
    print("═" * 76)


if __name__ == "__main__":
    print_report()
