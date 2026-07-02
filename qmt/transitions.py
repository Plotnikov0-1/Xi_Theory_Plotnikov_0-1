"""
═══════════════════════════════════════════════════════════════════════════
  TRANSITIONS — переходы куба: факторизация Ридберга, T_c, дыхание K(3,3).
═══════════════════════════════════════════════════════════════════════════

Лучшее из v12/doc-10, пропущенное через независимый расчёт (numpy/sympy).

◇ ФАКТОРИЗАЦИЯ РИДБЕРГА (точные тождества, проверено):
    зеркало  (n,10−n):  ΔE = R·20(5−n)/(n²(10−n)²)     20 из (10−n)²−n²=100−20n
    резонанс (n, 9−n):  ΔE = R·9(9−2n)/(n²(9−n)²)       9 из (9−n)²−n²=81−18n
  Числа группы переходов (20=|D₁₀|, 9=Sum-9) ВЫПАДАЮТ из алгебры Ридберга сами.
  При n=5 зеркальный квант = 0 (центр сам себе зеркало — перехода нет).

✓ T_c ПЕРЕХОДА = ΔE/k (порог разморозки канала). 4↔6 — единственный «земной»
  (0.472 эВ, ИК 2624 нм, 5482 К) — «шёпот». Остальные пары требуют кК–сотен кК.

◇ «ВЫБОР РОЖДАЕТ ДЫХАНИЕ» (K(3,3) между долями {2,3,4} и {6,7,8}):
    весь симметричный K33:  спектр {3, 1.5,1.5,1.5,1.5, 0} — ВЫРОЖДЕН (ℒ=0, разлом);
    выбор 1 из 6 гамильт. колец: C=1.5·I+0.5·A_кольца → {2.5,2,2,1,1,0.5}, δλ=0.5 (ритм).
  Ритм существует только при ВЫБОРЕ кольца — спектральная форма узла 5 (см. node5).

★ РАСХОЖДЕНИЕ [честно, нашёл при проверке]: разбор «28 пар = 10 рёбер + 3 рез. +
  4 зеркала» НЕ сходится с геометрией куба. Реально по Хэммингу: 12 рёбер + 12
  грань-диаг + 4 антипода = 28. Зеркала (сумма-10) = 4 антипода (Хэмминг 3) — чисто;
  но резонансы (сумма-9) {(1,8),(2,7),(3,6)} смешаны по Хэммингу [2,1,1], а рёбер
  12, не 10. Значит «10+3+4» — модельная разметка каналов, НЕ чистая комбинаторика.

Запуск:  python -m qmt.transitions
"""

from __future__ import annotations

from itertools import combinations

R_EV = 13.605693        # Ридберг (эВ)
K_EV = 8.617333e-5      # Больцман (эВ/К)
HC_NM_EV = 1239.841984  # h·c (эВ·нм)

# канонические координаты 8 вершин куба (узлы, центр 5 и оболочка 0 отдельно)
COORDS = {1: (-1, -1, -1), 2: (1, -1, -1), 3: (-1, 1, -1), 4: (-1, -1, 1),
          6: (1, 1, -1), 7: (1, -1, 1), 8: (-1, 1, 1), 9: (1, 1, 1)}


# ── ◇ Факторизация Ридберга ──────────────────────────────────────────────────
def rydberg_dE(n: int, m: int) -> float:
    """ΔE перехода n↔m по Ридбергу: R·|1/n² − 1/m²| (эВ)."""
    return R_EV * abs(1 / n**2 - 1 / m**2)


def mirror_factored(n: int) -> float:
    """◇ Зеркальный квант (n,10−n) = R·20(5−n)/(n²(10−n)²). При n=5 → 0."""
    m = 10 - n
    return R_EV * 20 * (5 - n) / (n**2 * m**2) if n != 5 else 0.0


def resonance_factored(n: int) -> float:
    """◇ Резонансный квант (n,9−n) = R·9(9−2n)/(n²(9−n)²)."""
    m = 9 - n
    return R_EV * 9 * (9 - 2 * n) / (n**2 * m**2)


def factorization_exact(tol: float = 1e-9) -> bool:
    """◇ Обе факторизации точны (20 и 9 из алгебры Ридберга)."""
    mir = all(abs(rydberg_dE(n, 10 - n) - abs(mirror_factored(n))) < tol for n in range(1, 5))
    res = all(abs(rydberg_dE(n, 9 - n) - abs(resonance_factored(n))) < tol
              for n in range(1, 5) if 9 - n != n)
    return mir and res


def center_mirror_quantum_zero() -> bool:
    """◇ При n=5 зеркальный квант = 0 (центр сам себе зеркало)."""
    return mirror_factored(5) == 0.0


# ── ✓ Температуры переходов T_c = ΔE/k ───────────────────────────────────────
PAIRS = {"4↔6 зерк": (4, 6), "3↔6 рез": (3, 6), "3↔7 зерк": (3, 7),
         "2↔7 рез": (2, 7), "2↔8 зерк": (2, 8), "1↔8 рез": (1, 8), "1↔9 зерк": (1, 9)}


def transition_temperature(n: int, m: int) -> float:
    """T_c = ΔE/k — порог разморозки канала (К)."""
    return rydberg_dE(n, m) / K_EV


def wavelength_nm(n: int, m: int) -> float:
    """λ = hc/ΔE (нм) — цвет/диапазон канала."""
    return HC_NM_EV / rydberg_dE(n, m)


def whisper_is_only_terrestrial() -> bool:
    """✓ 4↔6 — единственная пара с T_c в «земном» диапазоне (< 6000 К)."""
    temps = {k: transition_temperature(*v) for k, v in PAIRS.items()}
    return temps["4↔6 зерк"] < 6000 and all(
        t > 10000 for k, t in temps.items() if k != "4↔6 зерк")


# ── ◇ Выбор рождает дыхание: K(3,3) → кольцо ─────────────────────────────────
def _eigs(mat: list) -> list:
    """Собственные значения симметричной 6×6 (без numpy, метод Якоби)."""
    import math
    n = 6
    a = [row[:] for row in mat]
    for _ in range(100):
        # найти наибольший внедиагональный
        p, q, mx = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > mx:
                    mx, p, q = abs(a[i][j]), i, j
        if mx < 1e-12:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        phi = 0.5 * math.atan2(2 * apq, aqq - app) if aqq != app else math.pi / 4
        c, s = math.cos(phi), math.sin(phi)
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p] = c * akp - s * akq
            a[k][q] = s * akp + c * akq
        for k in range(n):
            akp, akq = a[p][k], a[q][k]
            a[p][k] = c * akp - s * akq
            a[q][k] = s * akp + c * akq
    return sorted(round(a[i][i], 6) for i in range(n))


def k33_full_spectrum() -> list:
    """◇ Полный K(3,3): C=1.5I+0.5·A. Спектр {3,1.5,1.5,1.5,1.5,0} — вырожден."""
    parts = ([0, 1, 2], [3, 4, 5])
    A = [[0.0] * 6 for _ in range(6)]
    for i in parts[0]:
        for j in parts[1]:
            A[i][j] = A[j][i] = 1.0
    C = [[1.5 * (i == j) + 0.5 * A[i][j] for j in range(6)] for i in range(6)]
    return _eigs(C)


def ring_spectrum() -> list:
    """◇ Одно гамильтоново кольцо: circ(1.5,0.5,0,0,0,0.5) → {0.5,1,1,2,2,2.5}."""
    c = [1.5, 0.5, 0, 0, 0, 0.5]
    C = [[c[(j - i) % 6] for j in range(6)] for i in range(6)]
    return _eigs(C)


def choice_creates_rhythm() -> bool:
    """◇ Полный K33 вырожден (δλ=0=разлом); кольцо даёт δλ_min=0.5 (ритм)."""
    full = k33_full_spectrum()
    ring = ring_spectrum()
    full_has_degeneracy = len(set(full)) < 6            # повтор λ ⇒ δλ=0
    ring_gap = min(b - a for a, b in zip(sorted(set(ring)), sorted(set(ring))[1:]))
    return full_has_degeneracy and abs(ring_gap - 0.5) < 1e-9


# ── ★ Честная комбинаторика куба (расхождение с разметкой 10+3+4) ─────────────
def hamming(a: int, b: int) -> int:
    return sum(x != y for x, y in zip(COORDS[a], COORDS[b]))


def cube_hamming_classes() -> dict:
    """◇ Чистая геометрия: 28 = 12 рёбер + 12 грань-диаг + 4 антипода."""
    cnt = {1: 0, 2: 0, 3: 0}
    for a, b in combinations(COORDS, 2):
        cnt[hamming(a, b)] += 1
    return cnt


def resonances_are_mixed_hamming() -> bool:
    """★ Резонансы (сумма-9) смешаны по Хэммингу [2,1,1] → не чистый класс."""
    res = [(a, b) for a, b in combinations(COORDS, 2) if a + b == 9]
    hs = sorted(hamming(a, b) for a, b in res)
    return hs == [1, 1, 2]


def mirrors_are_clean_antipodes() -> bool:
    """◇ Зеркала (сумма-10) = 4 антипода (Хэмминг 3) — чистый класс."""
    mir = [(a, b) for a, b in combinations(COORDS, 2) if a + b == 10]
    return len(mir) == 4 and all(hamming(a, b) == 3 for a, b in mir)


def print_report() -> None:
    print("═" * 74)
    print("  ПЕРЕХОДЫ КУБА: факторизация Ридберга · T_c · дыхание K(3,3)")
    print("═" * 74)
    print(f"\n  ◇ факторизация Ридберга точна (20 и 9 из алгебры): {factorization_exact()}")
    print(f"     центр n=5 зеркальный квант = 0: {center_mirror_quantum_zero()}")

    print("\n  ✓ T_c переходов (ΔE/k):")
    for lbl, (n, m) in PAIRS.items():
        print(f"     {lbl:9} ΔE={rydberg_dE(n,m):6.3f} эВ  λ={wavelength_nm(n,m):7.1f} нм  "
              f"T_c={transition_temperature(n,m):8.0f} К")
    print(f"     4↔6 — единственный «земной» (шёпот): {whisper_is_only_terrestrial()}")

    print("\n  ◇ выбор рождает дыхание:")
    print(f"     весь K33:   {k33_full_spectrum()}  — вырожден (ℒ=0)")
    print(f"     кольцо:     {ring_spectrum()}  — δλ=0.5 (ритм)")
    print(f"     ритм только при выборе кольца: {choice_creates_rhythm()}")

    print("\n  ★ РАСХОЖДЕНИЕ (честно): чистая геометрия куба vs разметка 10+3+4")
    print(f"     Хэмминг-классы 28 пар: {cube_hamming_classes()} (12 рёбер, не 10)")
    print(f"     зеркала = 4 чистых антипода: {mirrors_are_clean_antipodes()}")
    print(f"     резонансы смешаны [1,1,2]: {resonances_are_mixed_hamming()} → 10+3+4 = модель, не геометрия")
    print("═" * 74)
    print("  Взято проверенным: факторизация (◇), T_c (✓), дыхание K33 (◇).")
    print("  Отмечено расхождение: 10+3+4 ≠ чистый Хэмминг 12+12+4.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
