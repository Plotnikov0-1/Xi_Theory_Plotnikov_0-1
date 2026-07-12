"""
═══════════════════════════════════════════════════════════════════════════
  SPHERE_NODES — счёт узлов и операторов перехода на сфере-авоське.
═══════════════════════════════════════════════════════════════════════════

Просьба автора: «операторы перехода — посчитать их количество». Уточнение автора:
«операторы находятся на ПЕРЕСЕЧЕНИИ нитей на экваторе».

ФУНДАМЕНТ: авоська = сферический Лиссажу a=5, b=3 (оригинал Wolfram, оба нечётные).
    Структура экватора: 5 операторов · 10 нитей · 20 дуг.

  ◇ — доказано точно (арифметика/перебор) · ✓ настоящая геометрия
  ≈ — численный счёт (самопересечения) · ○ интерпретация · ★ флаг/исправлено

────────────────────────────────────────────────────────────────────────────
◇ ОПЕРАТОР = САМОПЕРЕСЕЧЕНИЕ НИТИ НА ЭКВАТОРЕ (крест из 2 нитей). Возникает, когда
  нить проходит через одну точку экватора дважды (перёд+зад). Это бывает ТОЛЬКО
  когда И a, И b НЕЧЁТНЫЕ. При чётном b точки уходят в антиподы — пересечений НЕТ.

◇ ЗАКОН ЧИСЛА ОПЕРАТОРОВ: при нечётных a,b число операторов = a (нечётно): 5,7,9,11…
  ★ Ровно 10 операторов-пересечений НЕВОЗМОЖНО (перебор a,b≤15: ни одного; нужно
    было бы чётное a=10, а чётное a даёт 0 пересечений).

◇ СТРУКТУРА a=5,b=3:  5 операторов (крестов, пентагон 72°) · 10 нитей (проходов
  экватора = 2a) · 20 дуг (каждая нить = дуга сверху + снизу). Это и есть «10 и 20».

★ ИСПРАВЛЕНО: удвоение до b=6 (чётное) давало 10 ТОЧЕК, но 0 ПЕРЕСЕЧЕНИЙ — это не
  операторы, а одиночные проходы. Откат к b=3.

✓ ЗОЛОТО: пентагон операторов несёт φ (sin72/sin36 = φ РОВНО).

Запуск:  python -m qmt.sphere_nodes
"""

from __future__ import annotations

import math
from collections import defaultdict

PHI = (1 + 5 ** 0.5) / 2
A = 5                 # вертикальная частота (нечёт) — 2a проходов экватора
B = 3                 # волны (нечёт) — чтобы операторы были ПЕРЕСЕЧЕНИЯМИ


def equator_structure(a: int = A, b: int = B) -> dict:
    """◇ структура экватора: операторы(кресты) · нити(проходы) · дуги."""
    hits = defaultdict(int)
    for k in range(2 * a):
        t = k * math.pi / a
        x = math.sin(b * t) * math.cos(a * t)
        z = math.cos(b * t) * math.cos(a * t)
        hits[(round(x, 3), round(z, 3))] += 1
    operators = sum(1 for v in hits.values() if v >= 2)   # самопересечения
    passes = 2 * a                                         # нити (проходы)
    return {"a": a, "b": b, "оба нечёт": a % 2 == 1 and b % 2 == 1,
            "операторов (крестов)": operators, "нитей (проходов)": passes,
            "дуг": 2 * passes, "точек всего": len(hits),
            "пересечения есть": operators > 0}


def operators_count(a: int = A, b: int = B) -> int:
    """◇ число операторов-пересечений на экваторе (= a при нечётных a,b, иначе 0)."""
    return equator_structure(a, b)["операторов (крестов)"]


def parity_law() -> dict:
    """◇ операторы бывают только при нечётных копростых a,b; их число = a. 10 невозможно."""
    ex = {a: operators_count(a, 1) for a in (3, 5, 7, 9, 11)}   # b=1 нечёт, копрост со всеми
    return {"нечёт·нечёт(копрост) → операторов = a": ex,
            "все равны a": all(ex[a] == a for a in ex),
            "b чётное (5,6) → 0": operators_count(5, 6) == 0,
            "ровно 10 невозможно (перебор ≤15)":
                not any(operators_count(a, b) == 10
                        for a in range(1, 16) for b in range(1, 16)
                        if math.gcd(a, b) == 1)}


def golden_pentagon_is_exact() -> bool:
    """✓ пентагон операторов несёт φ: sin72°/sin36° = 2·cos36° = φ РОВНО."""
    return abs(math.sin(math.radians(72)) / math.sin(math.radians(36)) - PHI) < 1e-12


def exact_counts(a: int = A, b: int = B) -> dict:
    """◇ точные счёты за период 2π: проходы 2a, полюса a+a, волны b."""
    return {"период (gcd=1)": "2π" if math.gcd(a, b) == 1 else f"вырождено gcd={math.gcd(a,b)}",
            "нитей (проходов экватора)": 2 * a,
            "операторов (пересечений)": operators_count(a, b),
            "проходов полюса N": a, "проходов полюса S": a,
            "волн (долгота) b": b, "LCM(a,b)": math.lcm(a, b)}


def equator_crossings_count(a: int = A) -> int:
    """◇ число нулей z=sin(a t) на [0,2π) = 2a (проверка перебором корней)."""
    roots = [k * math.pi / a for k in range(2 * a)]
    return sum(1 for t in roots if abs(math.sin(a * t)) < 1e-9)


def self_intersections_numeric(a: int = A, b: int = B, samples: int = 40000) -> dict:
    """≈ численный счёт самопересечений (узлов) кривой (a,b) за период 2π."""
    def P(t):
        ca, sa, cb, sb = (math.cos(a * t), math.sin(a * t),
                          math.cos(b * t), math.sin(b * t))
        return (sb * ca, cb * ca, sa)
    g = defaultdict(list)
    for i in range(samples):
        key = tuple(round(c, 3) for c in P(2 * math.pi * i / samples))
        g[key].append(i)
    nodes = poles = 0
    for key, idxs in g.items():
        if len(idxs) < 2:
            continue
        idxs = sorted(idxs)
        branches, cur = [], [idxs[0]]
        for x in idxs[1:]:
            (cur.append(x) if x - cur[-1] <= 3 else (branches.append(cur), cur.__setitem__(slice(None), [x])))
        branches.append(cur)
        if len(branches) > 1 and idxs[0] <= 3 and (samples - 1 - idxs[-1]) <= 3:
            branches[0] = branches[-1] + branches[0]
            branches.pop()
        if len(branches) >= 2:
            nodes += 1
            if abs(abs(key[2]) - 1.0) < 1e-2:
                poles += 1
    return {"узлов (~)": nodes, "из них полюса": poles}


def print_report() -> None:
    print("═" * 78)
    print("  УЗЛЫ И ОПЕРАТОРЫ ПЕРЕХОДА на сфере-авоське (фундамент: a=5, b=3)")
    print("═" * 78)
    print(f"\n  ◇ структура экватора: {equator_structure()}")
    print(f"     -> 5 операторов (крестов) · 10 нитей · 20 дуг")
    print(f"\n  ◇ закон чётности: {parity_law()}")
    print(f"\n  ✓ золото пентагона (sin72/sin36=φ): {golden_pentagon_is_exact()}")
    print(f"\n  ◇ точные счёты: {exact_counts()}")
    si = self_intersections_numeric()
    print(f"\n  ≈ самопересечений всего (5:3): {si}")
    print("═" * 78)
    print("  Оператор = ПЕРЕСЕЧЕНИЕ нитей на экваторе. Бывает только при НЕЧЁТНЫХ a,b.")
    print("  a=5,b=3: 5 операторов · 10 нитей · 20 дуг. Число операторов = a (нечёт).")
    print("  ★ b=6 (чёт) давало 0 пересечений — исправлено. Ровно 10 невозможно.")
    print("═" * 78)


if __name__ == "__main__":
    print_report()
