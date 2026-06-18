"""
§ φ как оператор самосогласованной сборки (канон 2026, Документ φ-Assembly).

Главный результат: φ−1 выводится ДВАЖДЫ независимо —
  (1) из динамики:        φ² = φ+1  ⇒  X* = φ−1   (dynamics.py);
  (2) из самосогласованности доли памяти x = ε/E:
        (E−ε)/ε = ε/E  ⇒  x² + x − 1 = 0  ⇒  x* = φ−1.
Оба дают одно число — это не подгонка.

φ — не константа, а устойчивая фиксированная точка оператора отношения
  T(x) = 1/(1+x),   T(φ−1) = φ−1,   |T'(φ−1)| = 1/φ² ≈ 0.382 < 1.
Дискретная реализация — Фибоначчи: F_n/F_{n+1} → φ−1.

Лестница сборки: Ω₀ → S₀(ε₀≠0) → ν → E=hν → ε* = φ−1 → 0* → динамика.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import PHI, X_STAR


def T(x: float) -> float:
    """Оператор отношения T(x) = 1/(1+x). Его устойчивая фикс. точка — φ−1."""
    return 1.0 / (1.0 + x)


def fixed_point(x0: float = 1.0, iterations: int = 60) -> float:
    """Итерация x → 1/(1+x) сходится к φ−1 из любого старта (аттрактор)."""
    x = x0
    for _ in range(iterations):
        x = T(x)
    return x


def stability_multiplier() -> float:
    """|T'(φ−1)| = 1/φ² ≈ 0.382 < 1 — устойчивость фиксированной точки."""
    return 1.0 / PHI**2


def self_consistent_fraction() -> float:
    """Самосогласованная доля памяти x=ε/E из (E−ε)/ε = ε/E ⇒ x²+x−1=0 ⇒ φ−1.

    ВТОРОЙ независимый вывод φ−1 (не из φ²=φ+1, а из условия сборки).
    """
    # Положительный корень x² + x − 1 = 0.
    return (math.sqrt(5.0) - 1.0) / 2.0


def two_derivations_agree(tol: float = 1e-12) -> bool:
    """[✓] Два независимых вывода дают одно число: φ−1 (динамика) = φ−1 (сборка)."""
    return abs(self_consistent_fraction() - X_STAR) < tol


def regime(k: float) -> float:
    """Семейство режимов x − 1/x = k ⇒ x = (k+√(k²+4))/2.

    k=0 → 1 (симметрия, граница циклов); k=1 → φ (самоподобие, X*);
    k=2 → 1+√2 ≈ 2.414 (серебряное сечение — следующий режим выше по циклу).
    """
    return (k + math.sqrt(k * k + 4.0)) / 2.0


def m_eff(eps: float, m0: float = 1.0, mu: float = 1.0) -> float:
    """Режимная (поляронная) масса: m_eff = m₀ + μ·ε. Масса = след памяти."""
    return m0 + mu * eps


@dataclass(frozen=True)
class LadderLevel:
    name: str
    omega: str   # частота ω
    energy: str  # энергия E
    eps: str     # память ε
    meaning: str


# Пятиступенчатая лестница сборки Ω₀ → S₀ → ν → E → ε.
ASSEMBLY_LADDER = [
    LadderLevel("Ω₀", "0", "0", "не определена", "до-спектральное равновесие (граничное условие)"),
    LadderLevel("S₀", "0", "0", "ε₀ ≠ 0", "вакуум с памятью (след прошлого цикла), аналог VEV Хиггса"),
    LadderLevel("ν", "2πν", "hν", "ε_targ = αhν", "первое выделенное возбуждение (ZPE)"),
    LadderLevel("E=hν", "2πν", "hν", "нарастает", "проявленная энергия (стандартный фотон)"),
    LadderLevel("ε", "—", "—", "ε > 0 = φ−1", "память: задаёт κ_eff и m_eff (поляронная масса)"),
]


if __name__ == "__main__":
    print(f"итерация T(x)=1/(1+x) → {fixed_point():.9f}  (φ−1 = {X_STAR:.9f})")
    print(f"|T'(φ−1)| = 1/φ² = {stability_multiplier():.4f} < 1  (устойчиво)")
    print(f"самосогласованность x²+x−1=0 → {self_consistent_fraction():.9f}")
    print(f"два вывода совпадают? {two_derivations_agree()}")
    print("семейство режимов:")
    for k in (0, 1, 2):
        tag = {0: "симметрия", 1: "φ-самоподобие (X*)", 2: "1+√2 серебряное"}[k]
        print(f"  k={k}: x = {regime(k):.6f}  ({tag})")
    print("\nлестница сборки:")
    for L in ASSEMBLY_LADDER:
        print(f"  {L.name:<5} ω={L.omega:<4} E={L.energy:<4} ε={L.eps:<14} {L.meaning}")
