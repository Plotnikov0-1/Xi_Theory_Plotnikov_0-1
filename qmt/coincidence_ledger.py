"""
Ledger совпадений — честная оценка «насколько удивительно попадание».

Главная ловушка любой теории, где числа (φ, π, e, √5…) «совпадают» с
наблюдениями: при достаточном переборе комбинаций часть совпадёт случайно
(проблема множественных сравнений / look-elsewhere effect).

Сила теории не в том, что число совпало, а в том, какова ВЕРОЯТНОСТЬ
совпасть случайно. Этот модуль её честно оценивает: берёт «алфавит»
простых констант, перебирает короткие комбинации и считает, какая доля
из них попадает в наблюдаемое значение с заданной точностью.

Если в окно ±5% попадает, скажем, 8% случайных комбинаций — то одно
совпадение почти ничего не доказывает (p≈0.08). Если 0.01% — это сильно.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

# Алфавит «фундаментальных» констант, которыми обычно жонглируют.
ALPHABET = {
    "φ": (1 + math.sqrt(5)) / 2,
    "φ−1": (math.sqrt(5) - 1) / 2,
    "π": math.pi,
    "e": math.e,
    "√2": math.sqrt(2),
    "√3": math.sqrt(3),
    "√5": math.sqrt(5),
    "2": 2.0,
    "3": 3.0,
    "½": 0.5,
}


@dataclass
class LedgerResult:
    target: float
    tol: float
    n_total: int
    n_hits: int
    p_random: float
    examples: list

    def verdict(self) -> str:
        if self.p_random < 0.001:
            return "СИЛЬНО (случайно почти невозможно)"
        if self.p_random < 0.01:
            return "ЗАМЕТНО (случайность маловероятна)"
        if self.p_random < 0.05:
            return "СЛАБО (на грани значимости)"
        return "НЕ ЗНАЧИМО (легко получить случайно)"


def _combos(depth: int):
    """Все комбинации a∘b и a∘b∘c с операциями ×, ÷ из алфавита."""
    names = list(ALPHABET)
    ops = [("×", lambda x, y: x * y), ("÷", lambda x, y: x / y)]
    # пары
    for a, b in itertools.product(names, repeat=2):
        for sym, f in ops:
            yield f"{a}{sym}{b}", f(ALPHABET[a], ALPHABET[b])
    if depth >= 3:
        for a, b, cc in itertools.product(names, repeat=3):
            for s1, f1 in ops:
                for s2, f2 in ops:
                    yield (f"{a}{s1}{b}{s2}{cc}",
                           f2(f1(ALPHABET[a], ALPHABET[b]), ALPHABET[cc]))


def estimate(target: float, tol: float = 0.05, depth: int = 3) -> LedgerResult:
    """Какая доля коротких комбинаций констант попадает в target ± tol·target."""
    lo, hi = target * (1 - tol), target * (1 + tol)
    n_total = 0
    hits = []
    for expr, val in _combos(depth):
        n_total += 1
        if lo <= val <= hi:
            hits.append((expr, val))
    p = len(hits) / n_total if n_total else 0.0
    return LedgerResult(target, tol, n_total, len(hits), p, hits[:8])


# Целевые «успехи» теории, заявленные как совпадения.
TARGETS = {
    "X* = φ−1 ≈ 0.618 (аттрактор)": 0.6180339887,
    "Δ₇ = √5−2 ≈ 0.236 (щель)": math.sqrt(5) - 2,
    "отношение каналов 2.20 (LHCb)": 2.20,
    "коридор G·100 ≈ 1.67": 1.671,
}


def print_report(tol: float = 0.05) -> None:
    print(f"LEDGER СОВПАДЕНИЙ (окно ±{tol*100:.0f}%, перебор пар и троек констant)")
    print("=" * 70)
    for label, tgt in TARGETS.items():
        r = estimate(tgt, tol=tol)
        print(f"\nЦель: {label}")
        print(f"  попало {r.n_hits} из {r.n_total} комбинаций  "
              f"⇒ p_random ≈ {r.p_random:.4f}  → {r.verdict()}")
        if r.examples:
            ex = ", ".join(f"{e}={v:.3f}" for e, v in r.examples[:4])
            print(f"  напр.: {ex}")
    print("\n" + "=" * 70)
    print("Как читать: малое p_random ⇒ совпадение трудно получить случайно ⇒")
    print("оно содержательно. Большое p_random ⇒ это могло выйти само собой.")
    print("Честный вывод: φ−1 и √5−2 — это ОПРЕДЕЛЕНИЯ внутри теории (Q0/Q1),")
    print("а вот совпадения с экспериментом надо взвешивать именно так.")


if __name__ == "__main__":
    print_report()
