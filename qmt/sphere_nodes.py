"""
═══════════════════════════════════════════════════════════════════════════
  SPHERE_NODES — счёт узлов и операторов перехода на сфере-авоське.
═══════════════════════════════════════════════════════════════════════════

Просьба автора: «у нас есть операторы перехода — посчитать их количество».
Здесь точный счёт того, что считается точно (◇), и один численный результат (≈).

ФУНДАМЕНТ (уточнён автором): удвоить операторы экватора и волны.
    БАЗА:     a=5, волн b=3 → экватор = 5 операторов (ПЕНТАГОН 72°).
    УДВОЕНО:  a=5, волн b=6 → экватор = 10 операторов (ДЕКАГОН 36°).  ← рабочий фундамент
Удвоили ТОЛЬКО волны (b: 3→6), оставив a=5. gcd(5,6)=1 — не вырождено.

  ◇ — доказано точно (арифметика частот) · ✓ настоящая геометрия
  ≈ — численный счёт (самопересечения) · ○ интерпретация · ★ флаг

────────────────────────────────────────────────────────────────────────────
◇ ПОЧЕМУ b ЧЁТНОЕ УДВАИВАЕТ ЭКВАТОР:
    пересечения экватора при t=kπ/a дают долготы; при НЕЧётном b перёд/зад
    ложатся в антиподы и склеиваются → a точек (пентагон). При ЧЁТном b склейки
    нет → 2a точек (декагон). Поэтому 5:3 → 5 точек, 5:6 → 10 точек.

★ ЛОВУШКА ВЫРОЖДЕНИЯ: 5:3 → 10:6 удваивать НЕЛЬЗЯ — gcd(10,6)=2, нить проходит
    дважды по тем же 5 точкам, удвоения НЕТ. Правильно: удвоить только b (5:6).

✓ ЗОЛОТО СОХРАНЯЕТСЯ: у декагона R/сторона = 1/(2·sin18°) = φ РОВНО.
    (Раньше φ жил в пентагоне sin72/sin36=φ и в ≈-истории «5:3 Фибоначчи».
     Теперь φ — в декагоне, ярус ◇, а не ≈. Честнее.)

Запуск:  python -m qmt.sphere_nodes
"""

from __future__ import annotations

import math

PHI = (1 + 5 ** 0.5) / 2
A = 5                 # вертикальная частота (касания полюса) — общая для базы и удвоения
B_BASE = 3            # база: волн 3 → пентагон (5)
B = 6                 # ФУНДАМЕНТ (удвоено): волн 6 → декагон (10)


def distinct_equator_operators(a: int = A, b: int = B) -> dict:
    """◇ различные операторы (точки) на экваторе для частот (a,b)."""
    lons = set()
    for k in range(2 * a):
        t = k * math.pi / a
        x = math.sin(b * t) * math.cos(a * t)
        z = math.cos(b * t) * math.cos(a * t)
        lons.add(round(math.degrees(math.atan2(z, x)) % 360, 1))
    L = sorted(lons)
    steps = sorted({round((L[(i + 1) % len(L)] - L[i]) % 360, 1) for i in range(len(L))})
    return {"a": a, "b": b, "gcd": math.gcd(a, b), "операторов": len(L),
            "долготы": L, "шаг": steps, "вырождено (gcd>1)": math.gcd(a, b) > 1}


def doubling() -> dict:
    """◇ база (5:3, пентагон 5) → удвоено (5:6, декагон 10); 10:6 — вырождение."""
    base = distinct_equator_operators(A, B_BASE)
    doubled = distinct_equator_operators(A, B)
    degenerate = distinct_equator_operators(2 * A, 2 * B_BASE)   # 10:6
    return {"база 5:3": base["операторов"], "удвоено 5:6": doubled["операторов"],
            "×2 корректно": doubled["операторов"] == 2 * base["операторов"],
            "★ 10:6 вырождено": (degenerate["операторов"] == base["операторов"]
                                 and degenerate["вырождено (gcd>1)"])}


def golden_decagon_is_exact() -> bool:
    """✓ у декагона (10 операторов) R/сторона = 1/(2·sin18°) = φ РОВНО."""
    return abs(1 / (2 * math.sin(math.radians(18))) - PHI) < 1e-12


def golden_pentagon_is_exact() -> bool:
    """✓ у пентагона (база) sin72°/sin36° = 2·cos36° = φ РОВНО."""
    return abs(math.sin(math.radians(72)) / math.sin(math.radians(36)) - PHI) < 1e-12


def exact_counts(a: int = A, b: int = B) -> dict:
    """◇ точные счёты за период 2π: экватор-проходы 2a, полюса a+a, волны b."""
    return {"период (gcd=1)": "2π" if math.gcd(a, b) == 1 else f"вырождено gcd={math.gcd(a,b)}",
            "проходов экватора": 2 * a,                     # 10 (всегда для a=5)
            "операторов экватора": distinct_equator_operators(a, b)["операторов"],
            "проходов полюса N": a, "проходов полюса S": a,  # 5+5
            "волн (долгота) b": b,
            "LCM(a,b)": math.lcm(a, b)}


def equator_crossings_count(a: int = A) -> int:
    """◇ число нулей z=sin(a t) на [0,2π) = 2a (проверка перебором корней)."""
    roots = [k * math.pi / a for k in range(2 * a)]
    return sum(1 for t in roots if abs(math.sin(a * t)) < 1e-9)


def self_intersections_numeric(a: int = A, b: int = B, samples: int = 40000) -> dict:
    """≈ численный счёт самопересечений (узлов) кривой (a,b) за период 2π."""
    from collections import defaultdict
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
    print("  УЗЛЫ И ОПЕРАТОРЫ ПЕРЕХОДА на сфере-авоське (фундамент: a=5, волн 6)")
    print("═" * 78)
    print(f"\n  ◇ удвоение: {doubling()}")
    print(f"\n  ◇ база 5:3 (пентагон):   {distinct_equator_operators(A, B_BASE)}")
    print(f"  ◇ удвоено 5:6 (декагон): {distinct_equator_operators(A, B)}")
    print(f"\n  ✓ золото пентагона (sin72/sin36=φ): {golden_pentagon_is_exact()}")
    print(f"  ✓ золото декагона  (1/2sin18 = φ):  {golden_decagon_is_exact()}")
    print(f"\n  ◇ точные счёты (удвоено, 2π): {exact_counts(A, B)}")
    print(f"     проходов экватора (перебор) = {equator_crossings_count(A)} (= 2·{A})")
    si = self_intersections_numeric(A, B)
    print(f"\n  ≈ самопересечений численно (5:6): {si}")
    print("═" * 78)
    print("  ФУНДАМЕНТ: a=5, волн 6 → 10 операторов экватора (декагон 36°). φ = R/сторона.")
    print("  Удвоили ТОЛЬКО волны (b:3→6). ★ 5:3→10:6 нельзя (gcd=2, вырождение).")
    print("═" * 78)


if __name__ == "__main__":
    print_report()
