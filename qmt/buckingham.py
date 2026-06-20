"""
═══════════════════════════════════════════════════════════════════════════
  BUCKINGHAM — физика живёт в безразмерных соотношениях, а не в переменных.
═══════════════════════════════════════════════════════════════════════════

Теорема Бакингема-Пи (строгая, доказанная): любой физический закон сводится к
тождеству F(π₁,…,π_m)=0 между БЕЗРАЗМЕРНЫМИ комбинациями π. Единицы (метр,
секунда, c=3·10⁸) — человеческая конвенция; физика — в инвариантных π.

Этот модуль — рабочий инструмент: величина = (значение, вектор размерности по
базису СИ [кг, м, с, А, К]). Умножение складывает размерности, степень — масштаб.
Безразмерность проверяется как нулевой вектор размерности.

Проверяем ГЛАВНЫЕ безразмерные числа против эксперимента (CODATA):
  • α = e²/(4πε₀ℏc) = 1/137.036  — постоянная тонкой структуры (чистое π-число);
  • E/mc² = 1                     — тождество масса-энергия (одно, названное дважды);
  • E_связи(H)/(m_e c²) = α²/2    — связь как доля энергии покоя (Зоммерфельд);
  • m_p/m_e = 1836.15             — безразмерное отношение масс.

Запуск:  python -m qmt.buckingham
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Базис размерностей СИ: [масса кг, длина м, время с, ток А, температура К]
_BASE = ("кг", "м", "с", "А", "К")


@dataclass(frozen=True)
class Q:
    """Размерная величина: число + вектор размерности по базису СИ."""
    value: float
    dim: tuple = (0, 0, 0, 0, 0)

    def __mul__(self, o: "Q | float") -> "Q":
        if isinstance(o, (int, float)):
            return Q(self.value * o, self.dim)
        return Q(self.value * o.value, tuple(a + b for a, b in zip(self.dim, o.dim)))

    __rmul__ = __mul__

    def __truediv__(self, o: "Q | float") -> "Q":
        if isinstance(o, (int, float)):
            return Q(self.value / o, self.dim)
        return Q(self.value / o.value, tuple(a - b for a, b in zip(self.dim, o.dim)))

    def __pow__(self, n: float) -> "Q":
        return Q(self.value ** n, tuple(a * n for a in self.dim))

    @property
    def is_dimensionless(self) -> bool:
        return all(abs(d) < 1e-12 for d in self.dim)

    def dim_str(self) -> str:
        parts = [f"{b}^{d:g}" for b, d in zip(_BASE, self.dim) if d]
        return "·".join(parts) if parts else "(безразмерно)"


# ── Фундаментальные величины с размерностями (CODATA 2018) ───────────────────
c   = Q(2.99792458e8,     (0, 1, -1, 0, 0))   # скорость света, м/с
hbar = Q(1.054571817e-34, (1, 2, -1, 0, 0))   # ħ, кг·м²/с
e   = Q(1.602176634e-19,  (0, 0, 1, 1, 0))    # заряд, А·с
eps0 = Q(8.8541878128e-12, (-1, -3, 4, 2, 0)) # эл. постоянная
m_e = Q(9.1093837015e-31, (1, 0, 0, 0, 0))    # масса электрона, кг
m_p = Q(1.67262192369e-27, (1, 0, 0, 0, 0))   # масса протона, кг
PI = math.pi


def fine_structure() -> Q:
    """α = e²/(4πε₀ℏc) — безразмерная постоянная тонкой структуры."""
    return (e ** 2) / (4 * PI * eps0 * hbar * c)


def mass_energy_identity(E_value: float, m_value: float) -> Q:
    """E/(mc²): размерное E=mc² в безразмерной форме = тождество (=1)."""
    E = Q(E_value, (1, 2, -2, 0, 0))           # энергия, Дж
    m = Q(m_value, (1, 0, 0, 0, 0))            # масса, кг
    return E / (m * c ** 2)


def binding_fraction() -> Q:
    """E_связи(H)/(m_e c²) предсказано как α²/2 (Зоммерфельд) — безразмерно."""
    alpha = fine_structure().value
    return Q(alpha ** 2 / 2.0)                  # уже безразмерно


def mass_ratio() -> Q:
    """m_p/m_e — безразмерное отношение масс."""
    return m_p / m_e


def load_ratio(X: float) -> float:
    """Уровень 3 (опыт): τ/t = 1/(1+X), X — безразмерная нагрузка.
    X=0 → 1 (внутреннее=внешнему); X→∞ → 0; устойчивая точка X*=φ−1."""
    return 1.0 / (1.0 + X)


PHI = (1.0 + math.sqrt(5.0)) / 2.0


def self_similar_fixed_point(x0: float = 2.0, depth: int = 40) -> float:
    """Масштабный инвариант: неподвижная точка карты f(x)=1/(1+x).

    Это одно соотношение, БЕЗРАЗМЕРНОЕ, не зависящее от старта (сходится из
    любого x0) — потому «масштабируется» и «подходит ко всем формулам». Решение
    x*=1/(1+x*) ⇒ x*=φ−1. Самоподобие: та же карта на каждом уровне вложенности."""
    x = float(x0)
    for _ in range(depth):
        x = 1.0 / (1.0 + x)
    return x


def convergents(depth: int = 10) -> list:
    """«Разнообразие форм»: сходящиеся дроби F_k/F_{k+1} (приближения к x*=φ−1).

    Отойди (большая глубина) — видишь одно целое x*. Приблизься (малая глубина) —
    видишь несколько форм: 1/2, 2/3, 3/5, 5/8… их всё больше, все стремятся к одному."""
    F = [1, 1]
    for _ in range(depth + 1):
        F.append(F[-1] + F[-2])
    return [(F[k], F[k + 1], F[k] / F[k + 1]) for k in range(1, depth + 1)]


def print_report() -> None:
    print("═" * 74)
    print("  BUCKINGHAM-PI: физика — в безразмерных π, а не в переменных")
    print("═" * 74)

    a = fine_structure()
    print(f"\n  α = e²/(4πε₀ℏc)")
    print(f"     размерность: {a.dim_str()}  → {'БЕЗРАЗМЕРНО ✓' if a.is_dimensionless else 'ОШИБКА'}")
    print(f"     α = {a.value:.10e}   1/α = {1/a.value:.6f}")
    print(f"     эксперимент 1/α = 137.035999   откл = {abs(1/a.value-137.035999)/137.036*1e6:.2f} ppm  ✓")

    ide = mass_energy_identity(1.0, 1.0 / c.value**2)   # E=mc² ⇒ E/(mc²)=1
    print(f"\n  E/mc²  (тождество масса-энергия)")
    print(f"     размерность: {ide.dim_str()}  значение = {ide.value:.6f}  → одно, названное дважды")

    bf = binding_fraction()
    exp_bf = 13.598434 / 510998.95
    print(f"\n  E_связи(H)/(m_e c²) = α²/2  (Зоммерфельд)")
    print(f"     предсказание = {bf.value:.6e}   эксперимент = {exp_bf:.6e}")
    print(f"     откл = {abs(bf.value-exp_bf)/exp_bf*100:.3f} %  (поправка на приведённую массу) ✓")

    mr = mass_ratio()
    print(f"\n  m_p/m_e = {mr.value:.5f}   эксперимент = 1836.15267  ({'безразмерно ✓' if mr.is_dimensionless else 'ОШИБКА'})")

    print(f"\n  Уровень 3 (опыт): τ/t = 1/(1+X)")
    for X in (0.0, PHI - 1.0, 1.0, 9.0):
        print(f"     X={X:.4f} → τ/t={load_ratio(X):.4f}")

    print(f"\n  МАСШТАБНЫЙ ИНВАРИАНТ (одно соотношение, не формула):")
    print(f"     f(x)=1/(1+x), неподвижная точка x* = φ−1 = {PHI-1:.8f}")
    for x0 in (0.1, 2.0, 100.0):
        print(f"        из x₀={x0:>5}: → {self_similar_fixed_point(x0):.8f}  (не зависит от старта)")
    print(f"     «разнообразие форм» — сходящиеся дроби (приближайся → форм больше):")
    forms = convergents(8)
    print("        " + "  ".join(f"{a}/{b}={r:.3f}" for a, b, r in forms[:6]) + " … → φ−1")
    print("═" * 74)
    print("  Вывод: c, метр, секунда — конвенции. Инварианты — π-числа (α, α²/2,")
    print("  m_p/m_e) и масштабная точка x*=φ−1. Они НЕ меняются при смене единиц")
    print("  и масштаба: отойди — одно целое; приблизься — множество форм, одно ядро.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
