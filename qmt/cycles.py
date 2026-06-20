"""
═══════════════════════════════════════════════════════════════════════════
  CYCLES — структура 1-4-7 / 2-5-8 / 3-6-9 как оператор, и CP-нарушение
           как снятие вырождения m-уровней. Точная линейная алгебра.
═══════════════════════════════════════════════════════════════════════════

Часть 1 (точно). Система 1-4-7 / 2-5-8 / 3-6-9 = три независимых 3-цикла =
оператор перестановки P (9×9). Спектр: σ(P)={1,ω,ω²} (ω=e^{2πi/3}), каждое
×3. P³=I. Проектор на наблюдаемое: Π=(I+P+P²)/3 (λ=1 сектор). ω,ω² — скрытые
фазовые моды («туннель»).

Часть 2 (стандартная КМ). Каждый блок ↔ триада m∈{−1,0,+1} уровня l=1 водорода.
Без возмущения E_m=E_0 (вырождение по m, симметрия SO(3)). Возмущение, нечётное
по m, СНИМАЕТ вырождение и ломает зеркало m↔−m:
        E_m = E_0 + a·m + b·m³ ,   E_{+m} ≠ E_{−m}.

ЭКСПЕРИМЕНТАЛЬНЫЕ ЯКОРЯ (честно):
  • линейный член a·m = эффект Зеемана, a=μ_B·B — РЕАЛЕН и измерен (μ_B=5.79e-5 эВ/Тл);
  • истинное внутреннее CP/T-нарушение (без поля) = постоянный ЭДМ; эксперимент
    ограничивает ЭДМ электрона |d_e|<4.1e-30 e·см (ACME 2018) ≈ 0;
  • реальная барионная асимметрия Вселенной η_B≈6.1e-10 (Planck/BBN) — измерена,
    но из этой схемы НЕ выводится (аналогия, не вывод).

Запуск:  python -m qmt.cycles
"""

from __future__ import annotations

import numpy as np

CYCLES = ((1, 4, 7), (2, 5, 8), (3, 6, 9))   # три 3-цикла (метки 1..9)
W = np.exp(2j * np.pi / 3)                    # ω = e^{2πi/3}

# Экспериментальные величины (CODATA / измерения)
MU_B_EV_PER_T = 5.7883818060e-5     # магнетон Бора, эВ/Тл
EDM_E_BOUND_ECM = 4.1e-30           # верхний предел ЭДМ электрона, e·см (ACME 2018)
ETA_B = 6.1e-10                     # барионная асимметрия Вселенной (Planck/BBN)


def permutation_operator() -> np.ndarray:
    """Оператор P (9×9): три 3-цикла (1→4→7)(2→5→8)(3→6→9)."""
    P = np.zeros((9, 9))
    for cyc in CYCLES:
        for i in range(3):
            src = cyc[i] - 1
            dst = cyc[(i + 1) % 3] - 1
            P[dst, src] = 1.0
    return P


def spectrum() -> np.ndarray:
    """Собственные значения P (ожидается {1,ω,ω²} каждое ×3)."""
    return np.linalg.eigvals(permutation_operator())


def is_cube_root_spectrum() -> bool:
    """Проверка: спектр = кубические корни единицы, каждый кратности 3."""
    ev = spectrum()
    for target in (1.0 + 0j, W, W**2):
        if np.sum(np.isclose(ev, target, atol=1e-9)) != 3:
            return False
    return np.allclose(np.linalg.matrix_power(permutation_operator(), 3), np.eye(9))


def invariant_projector() -> np.ndarray:
    """Π=(I+P+P²)/3 — проектор на наблюдаемое (λ=1) подпространство."""
    P = permutation_operator()
    return (np.eye(9) + P + P @ P) / 3.0


def block_eigenvectors() -> dict:
    """Собственные векторы одного 3-цикла: v0=(1,1,1), v1=(1,ω,ω²), v2=(1,ω²,ω)."""
    return {"λ=1 (наблюдаемое)": np.array([1, 1, 1]),
            "ω (туннель)": np.array([1, W, W**2]),
            "ω² (туннель)": np.array([1, W**2, W])}


def m_levels_cp(E0: float = 0.0, a: float = 0.0, b: float = 0.0,
                m_values=(-1, 0, 1)) -> dict:
    """Уровни E_m = E0 + a·m + b·m³ для триады; снятие вырождения и зеркало.

    a — линейный (зеемановский / CP-нечётный) наклон; b — кубический CP-член.
    Возвращает энергии, факт снятия вырождения и зеркальную асимметрию.
    """
    E = {m: E0 + a * m + b * m**3 for m in m_values}
    degeneracy_lifted = len(set(round(v, 18) for v in E.values())) > 1
    # зеркальная (CP) асимметрия: E_{+m} − E_{−m}
    mirror_asym = {m: E[m] - E[-m] for m in m_values if m > 0}
    cp_violated = any(abs(v) > 1e-18 for v in mirror_asym.values())
    return {"E": E, "вырождение_снято": degeneracy_lifted,
            "зеркальная_асимметрия": mirror_asym, "CP_нарушено": cp_violated}


def zeeman_split_eV(B_tesla: float, m: int) -> float:
    """Реальный зеемановский сдвиг ΔE = μ_B·B·m (эВ) — измеряемая физика."""
    return MU_B_EV_PER_T * B_tesla * m


def print_report() -> None:
    print("═" * 74)
    print("  CYCLES: 1-4-7/2-5-8/3-6-9 как оператор · CP = снятие m-вырождения")
    print("═" * 74)

    print("\n  ЧАСТЬ 1 — точная алгебра (оператор перестановки P):")
    ev = spectrum()
    uniq = sorted({complex(round(z.real, 3), round(z.imag, 3)) for z in ev},
                  key=lambda z: (round(z.real, 2), round(z.imag, 2)))
    print(f"     спектр σ(P) = {uniq}  (каждое ×3)")
    print(f"     ω = e^(2πi/3) = {W:.3f}")
    print(f"     P³ = I : {np.allclose(np.linalg.matrix_power(permutation_operator(),3), np.eye(9))}")
    Pi = invariant_projector()
    print(f"     проектор Π=(I+P+P²)/3 : Π²=Π {np.allclose(Pi@Pi,Pi)}, ранг {np.linalg.matrix_rank(Pi)} (наблюдаемое)")
    print("     собств. векторы блока:")
    for k, v in block_eigenvectors().items():
        print(f"        {k:<20}: {np.round(v,3)}")

    print("\n  ЧАСТЬ 2 — CP-нарушение = снятие вырождения m (стандартная КМ):")
    base = m_levels_cp(E0=-3.4, a=0.0, b=0.0)
    print(f"     без возмущения: E_m = {[round(v,3) for v in base['E'].values()]} "
          f"→ вырождение (СR-симметрия)")
    cp = m_levels_cp(E0=-3.4, a=0.05, b=0.0)
    print(f"     с наклоном a=0.05: E_m = {[round(v,3) for v in cp['E'].values()]}")
    print(f"        вырождение снято: {cp['вырождение_снято']}, "
          f"зеркало m↔−m нарушено: {cp['CP_нарушено']} (E₊₁−E₋₁={cp['зеркальная_асимметрия'][1]:+.3f})")

    print("\n  ЭКСПЕРИМЕНТАЛЬНЫЕ ЯКОРЯ (честно):")
    print(f"     ✓ линейный наклон = эффект Зеемана: при B=1 Тл, m=+1 → "
          f"ΔE={zeeman_split_eV(1.0,1)*1e6:.2f} мкэВ  (μ_B измерен)")
    print(f"     ○ внутреннее CP без поля = ЭДМ электрона: |d_e|<{EDM_E_BOUND_ECM:.1e} e·см")
    print(f"        (ACME 2018) — эксперимент говорит: внутреннее CP ≈ 0")
    print(f"     ○ реальная барионная асимметрия η_B≈{ETA_B:.1e} (Planck/BBN) —")
    print(f"        измерена, но из этой схемы НЕ выводится (аналогия)")
    print("═" * 74)
    print("  Точная часть: спектр {1,ω,ω²} и снятие вырождения — строгая математика.")
    print("  Физическая часть: m-расщепление РЕАЛЬНО (Зееман); отождествление с")
    print("  космологическим CP — аналогия, не подтверждённый вывод.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
