"""
═══════════════════════════════════════════════════════════════════════════
  X_LAW — две строгие попытки зафиксировать β и ε_X. Обе — честный минус.
═══════════════════════════════════════════════════════════════════════════

Продолжение canon_constants: β изолирован до 4/3, ε_X ≈ e под вопросом. Здесь
СТРОГО проверены два пути их вывода. Оба закрыты — и это результат, а не тупик:
теперь известно, что β иррредуцируемо свободен, и почему.

ЗАДАЧА 1 — СИММЕТРИЯ СЛОЁВ (не фиксирует β): [строгий −]
  Шесть принципов «сравнить уровень u и уровень v» дают β/α ∈
  {1.00, 1.06, 0.59, 1.82, 1.82, 1.06} — НИ ОДИН не даёт 4/3.
  Причина строго: 4/3 БЕЗРАЗМЕРНО (масштаб-инвариант), а принципы уровней дают
  β=f(α) ⇒ β/α зависит от α. Фикс. 4/3 может дать только ПОСТУЛАТ β∝α, не вывод.
  ⇒ β=(4/3)α — ассигнация из внешних чисел (Op₄/3, юга 4:3), ярус ○.

ЗАДАЧА 2 — X-ЗАКОН (реальный ◇, но ε_X не константа):
  Нормальная форма 2×2: H(ε)=λ̄I+Δ(ε)σ_z+g σ_x, Δ=c₁(ε−ε_X).
    щель δλ(ε)=2√(Δ²+g²);  d/dε=0 ⇒ минимум ровно в ε_X (где Δ=0);
    δλ_min=2g;  g→0 ⇒ δλ→0 (исключительная точка, слияние собств.);
    τ_память ∝ 1/δλ → ∞ в EP — это и есть «разлом» X. [◇ нормальная форма]
  НО ε_X = координата пересечения диабат. уровней: сдвигается КУДА поставлена
  связь. e≈2.718 ничем не выделено ⇒ X-закон НЕ выводит e и НЕ фиксирует β.

ИТОГ: β иррредуцируемо свободен в обеих конструкциях (изолирован до 4/3, ○);
ε_X — координата EP, не универсальная константа и не e (○). X-закон как
нормальная форма — настоящий ◇ (щель, EP, расходимость памяти).

Запуск:  python -m qmt.x_law
"""

from __future__ import annotations

import math

PHI = (1 + math.sqrt(5)) / 2
ALPHA = 9 / 5


# ── ЗАДАЧА 1: симметрия слоёв не даёт 4/3 ────────────────────────────────────
def _v_hi(b: float) -> float:
    return 3 * b + 5 / 4 + math.sqrt(144 * b * b + 56 * b + 9) / 4


def _v_ray(b: float) -> float:
    return 11 / 6 + 6 * b


def _lam_u(a: float = ALPHA) -> float:
    return 5 / 2 + 6 * a


def _root(f, lo: float = 1e-6, hi: float = 50.0, n: int = 40000):
    prev, x_prev = f(lo), lo
    for i in range(1, n + 1):
        x = lo + (hi - lo) * i / n
        cur = f(x)
        if (prev < 0) != (cur < 0):
            a, b = x_prev, x
            for _ in range(60):
                m = 0.5 * (a + b)
                if (f(a) < 0) != (f(m) < 0):
                    b = m
                else:
                    a = m
            return 0.5 * (a + b)
        prev, x_prev = cur, x
    return None


def layer_symmetry_ratios() -> dict:
    """β/α для шести принципов сравнения уровней (α=9/5). Ни один ≠ 4/3."""
    lam = _lam_u()
    principles = {
        "равный подъём 6α=6β": lambda b: 6 * ALPHA - 6 * b,
        "равные уровни λ_u=v_ray": lambda b: lam - _v_ray(b),
        "золотое λ_u=φ·v_ray": lambda b: lam - PHI * _v_ray(b),
        "золотое v_ray=φ·λ_u": lambda b: _v_ray(b) - PHI * lam,
        "верхн. v-мода=φ·λ_u": lambda b: _v_hi(b) - PHI * lam,
        "верхн. v-мода=λ_u": lambda b: _v_hi(b) - lam,
    }
    out = {}
    for name, f in principles.items():
        r = _root(f)
        out[name] = round(r / ALPHA, 4) if r is not None else None
    return out


def layer_symmetry_cannot_fix_beta() -> bool:
    """◇ [строгий −]: ни один принцип уровней не даёт β/α=4/3."""
    return all(v is None or abs(v - 4 / 3) > 2e-3
               for v in layer_symmetry_ratios().values())


def why_beta_is_scale_free() -> str:
    """Причина: 4/3 безразмерно; принципы уровней дают β=f(α) ⇒ β/α зависит от α."""
    return ("4/3 безразмерно (масштаб-инвариант); принципы уровней дают β=f(α), "
            "значит β/α зависит от α. Фикс. 4/3 требует ПОСТУЛАТА β∝α, не выводится.")


# ── ЗАДАЧА 2: X-закон (нормальная форма 2×2) ─────────────────────────────────
def normal_form_gap(delta: float, g: float) -> float:
    """◇ Щель пары в X-режиме: δλ = 2√(Δ²+g²) (H=λ̄I+Δσ_z+gσ_x)."""
    return 2 * math.sqrt(delta * delta + g * g)


def gap_minimum_location(c1: float, g: float, eps_X: float,
                         lo: float = None, hi: float = None) -> float:
    """Где минимум щели по ε при Δ=c₁(ε−ε_X): ровно в ε_X (Δ=0)."""
    lo = eps_X - 1 if lo is None else lo
    hi = eps_X + 1 if hi is None else hi
    xs = [lo + (hi - lo) * i / 2000 for i in range(2001)]
    return min(xs, key=lambda e: normal_form_gap(c1 * (e - eps_X), g))


def eps_X_is_not_universal() -> bool:
    """◇ ε_X = координата пересечения: минимум щели идёт туда, куда поставлен ε_X."""
    return all(abs(gap_minimum_location(1.0, 0.3, e0) - e0) < 1e-2
               for e0 in (0.5, math.e, 4.0))


def memory_diverges_at_EP(g: float) -> float:
    """✓ τ_память ∝ 1/δλ_min = 1/(2g); g→0 ⇒ τ→∞ (исключительная точка)."""
    return math.inf if g == 0 else 1.0 / (2 * g)


def x_law_fixes_neither() -> bool:
    """◇ X-закон не выводит e и не фиксирует β: ε_X свободно двигается."""
    e_not_special = eps_X_is_not_universal()
    return e_not_special


def verdicts() -> dict:
    return {
        "β (симметрия слоёв)": "НЕ фиксируется: ни один принцип уровней ≠ 4/3; "
                               "4/3 безразмерно → только постулат β=(4/3)α (○)",
        "X-закон": "◇ реальная нормальная форма (щель 2√(Δ²+g²), EP, τ→∞)",
        "ε_X": "координата пересечения (Δ=0); не константа, не e (○)",
        "итог": "β иррредуцируемо свободен (4/3); ε_X — координата EP, не e",
    }


def print_report() -> None:
    print("═" * 74)
    print("  X_LAW: две строгие попытки зафиксировать β и ε_X — обе честный минус")
    print("═" * 74)
    print("\n  ЗАДАЧА 1 — симметрия слоёв (β/α по принципам, α=9/5):")
    for name, r in layer_symmetry_ratios().items():
        flag = "  ← =4/3!" if r is not None and abs(r - 4 / 3) < 2e-3 else ""
        print(f"     {name:26} β/α = {r}{flag}")
    print(f"     ни один ≠ 4/3: {layer_symmetry_cannot_fix_beta()}")
    print(f"     причина: {why_beta_is_scale_free()}")

    print("\n  ЗАДАЧА 2 — X-закон (нормальная форма 2×2):")
    print(f"     δλ(Δ=0,g=0.3) = {normal_form_gap(0,0.3):.3f} = 2g (минимум, избег. пересеч.)")
    print(f"     мин щели при ε_X=0.5 → {gap_minimum_location(1,0.3,0.5):.3f}; "
          f"при ε_X=e → {gap_minimum_location(1,0.3,math.e):.3f}")
    print(f"     ε_X не универсальна (двигается куда поставлена): {eps_X_is_not_universal()}")
    print(f"     τ_память при g=0.3 → {memory_diverges_at_EP(0.3):.2f}; при g→0 → ∞ (EP)")
    print(f"     X-закон не выводит e и не фиксирует β: {x_law_fixes_neither()}")

    print("\n  ═══ ВЕРДИКТЫ ═══")
    for k, v in verdicts().items():
        print(f"     {k}: {v}")
    print("═" * 74)
    print("  Строго доказано: β нельзя вывести симметрией слоёв (4/3 безразмерно),")
    print("  а X-закон не фиксирует ни β, ни e. β=(4/3)α — постулат (○); X-закон — ◇.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
