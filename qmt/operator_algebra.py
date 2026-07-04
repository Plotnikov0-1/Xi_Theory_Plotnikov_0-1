"""
═══════════════════════════════════════════════════════════════════════════
  OPERATOR_ALGEBRA — теория как (S, T, G, I): «дверь» = автоморфизм инварианта.
═══════════════════════════════════════════════════════════════════════════

Строгая форма идеи «поиграть с формулой и открыть дверь» (change of variables /
ковариантность / фактор-пространство 𝓕/G). Формула — не объект, а элемент класса
эквивалентности F∈[F]_G. Физика = 𝓕/G: разные записи одного состояния — один объект.

ЧЕТЫРЕ СЛОЯ (всё проверено на кубе):
  S — состояния: 8 узлов-вершин куба {1,2,3,4,6,7,8,9} (базис, не значения).
  T — переходы: матрица рёбер (Хэмминг-1), 12 рёбер, степень 3. ◇
  G — группа допустимых преобразований = Aut(T) = 48 (полная симметрия куба). ◇
  I — инвариант = спектр T = {−3, −1,−1,−1, 1,1,1, 3}. ◇

★ «ДВЕРЬ» ФОРМАЛИЗОВАНА:
    ∃φ∈G:  φ(T) ≠ T поточечно,  но  I(φT) = I(T).
    Конкретно φ = R (зеркало n↦10−n = антипод = −I): двигает ВСЕ 8 узлов,
    но спектр сохранён. Это ковариантность: −I меняет разметку, физика та же.
    Дверь — не метафора, а нетривиальный автоморфизм, сохраняющий инвариант.

Связь с нашим ядром: (S,T,G,I) — строгая форма триплета Ω=(R,T,C). Зеркало R —
и генератор G, и «дверь». φ-режим живёт в семействе p=5 (Aut=120 → E₈, McKay).
Замыкание T_ij∘T_jk→T_ik держится по путям (граф связный); настоящий РАЗРЫВ —
там, где зеркальные пары как рёбра дают 5 компонент (см. node5, димеры).

Запуск:  python -m qmt.operator_algebra
"""

from __future__ import annotations

import cmath
import math
from itertools import combinations, permutations

# S — состояния: координаты 8 вершин куба
COORDS = {1: (-1, -1, -1), 2: (1, -1, -1), 3: (-1, 1, -1), 4: (-1, -1, 1),
          6: (1, 1, -1), 7: (1, -1, 1), 8: (-1, 1, 1), 9: (1, 1, 1)}
STATES = list(COORDS)


def hamming(a: int, b: int) -> int:
    return sum(x != y for x, y in zip(COORDS[a], COORDS[b]))


# ── T — матрица переходов ────────────────────────────────────────────────────
def edges() -> set:
    """T: рёбра куба (Хэмминг-1) — разрешённые одношаговые переходы."""
    return {frozenset((a, b)) for a, b in combinations(STATES, 2) if hamming(a, b) == 1}


def adjacency() -> list:
    """Матрица смежности T (8×8) в порядке STATES."""
    E = edges()
    return [[1 if frozenset((a, b)) in E else 0 for b in STATES] for a in STATES]


# ── I — инвариант (спектр) ───────────────────────────────────────────────────
def _sym_eigs(mat: list) -> list:
    """Собственные значения симметричной 8×8 (Якоби)."""
    n = len(mat)
    a = [row[:] for row in mat]
    for _ in range(200):
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


def invariant_spectrum() -> list:
    """◇ I = спектр T = {−3,−1,−1,−1,1,1,1,3} (инвариант теории)."""
    return _sym_eigs(adjacency())


# ── G — группа преобразований ────────────────────────────────────────────────
def R(n: int) -> int:
    """Зеркало R(n)=10−n = антипод = центральная инверсия −I."""
    return 10 - n


def is_automorphism(perm: dict) -> bool:
    """◇ φ∈G ⟺ перестановка сохраняет множество рёбер T."""
    E = edges()
    return all(frozenset((perm[a], perm[b])) in E for e in E for a, b in [tuple(e)])


def aut_group_order() -> int:
    """◇ |G| = |Aut(T)| — полная группа симметрии куба (=48)."""
    E = edges()
    cnt = 0
    for pm in permutations(STATES):
        perm = dict(zip(STATES, pm))
        if all(frozenset((perm[a], perm[b])) in E for e in E for a, b in [tuple(e)]):
            cnt += 1
    return cnt


# ── «ДВЕРЬ»: φ(T)≠T поточечно, но I инвариантен ──────────────────────────────
def the_door() -> dict:
    """★ R двигает все узлы, но сохраняет спектр → дверь реальна (ковариантность)."""
    Rmap = {n: R(n) for n in STATES}
    moved = sum(1 for n in STATES if Rmap[n] != n)
    is_auto = is_automorphism(Rmap)
    # спектр под R (перестановка сопряжением) — тот же
    return {"R автоморфизм T": is_auto, "R двигает узлов": moved,
            "спектр сохранён": is_auto,      # автоморфизм ⇒ спектр инвариантен
            "дверь": is_auto and moved > 0}


# ── замыкание и разрывы ──────────────────────────────────────────────────────
def is_connected() -> bool:
    """◇ Замыкание по путям T_ij∘T_jk→T_ik достижимо ⟺ граф связный."""
    E = edges()
    seen, stack = {STATES[0]}, [STATES[0]]
    while stack:
        v = stack.pop()
        for w in STATES:
            if frozenset((v, w)) in E and w not in seen:
                seen.add(w); stack.append(w)
    return len(seen) == len(STATES)


def is_bipartite() -> bool:
    """◇ Двудолен ⟺ каждый переход меняет тетраэдр (чёрное/белое)."""
    E = edges()
    color = {STATES[0]: 0}
    stack = [STATES[0]]
    while stack:
        v = stack.pop()
        for w in STATES:
            if frozenset((v, w)) in E:
                if w not in color:
                    color[w] = 1 - color[v]; stack.append(w)
                elif color[w] == color[v]:
                    return False
    return True


# ── четыре слоя и фактор-пространство ────────────────────────────────────────
def four_layers() -> dict:
    """(S, T, G, I) — строгая форма теории."""
    return {
        "S состояния": f"{len(STATES)} узлов куба {STATES}",
        "T переходы": f"{len(edges())} рёбер (Хэмминг-1), степень 3",
        "G группа": f"Aut(T) = 48 (симметрия куба); генератор R=−I",
        "I инвариант": f"спектр {invariant_spectrum()}",
        "физика=𝓕/G": "разметки, связанные R∈G, — один объект (ковариантность)",
    }


def print_report() -> None:
    print("═" * 74)
    print("  ТЕОРИЯ КАК (S,T,G,I): «дверь» = автоморфизм инварианта")
    print("═" * 74)
    print(f"\n  S · состояния: {len(STATES)} узлов {STATES}")
    print(f"  T · переходы: {len(edges())} рёбер (Хэмминг-1), степень 3")
    print(f"  I · инвариант = спектр T: {invariant_spectrum()}")
    print(f"  G · группа Aut(T) = {aut_group_order()} (симметрия куба)")

    d = the_door()
    print(f"\n  ★ ДВЕРЬ: R=−I автоморфизм T: {d['R автоморфизм T']}, "
          f"двигает {d['R двигает узлов']}/8 узлов, спектр сохранён")
    print(f"     ∃φ∈G: φ(T)≠T поточечно, но I(φT)=I(T) → дверь реальна: {d['дверь']}")
    print(f"     смысл: −I меняет разметку, инвариант (физика) тот же = ковариантность")

    print(f"\n  замыкание по путям (связный): {is_connected()}")
    print(f"  двудолен (каждый переход меняет тетраэдр): {is_bipartite()}")
    print(f"  🔴 разрыв: зеркальные пары как рёбра → 5 компонент (node5, димеры)")

    print("\n  ═══ ФАКТОР-ПРОСТРАНСТВО: физика = 𝓕/G ═══")
    for k, v in four_layers().items():
        print(f"     {k}: {v}")
    print("═" * 74)
    print("  «Дверь» строго = нетривиальный автоморфизм R, сохраняющий инвариант I.")
    print("  (S,T,G,I) — строгая форма Ω=(R,T,C). Формула = элемент класса [F]_G.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
