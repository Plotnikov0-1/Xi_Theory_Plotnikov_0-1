"""
Физика переходов: 7 катастроф Тома, Пуанкаре, Паули, CP (Сахаров).

DIALOG QMT — «теория переходов». Математика переходов — теория катастроф Рене
Тома: ровно СЕМЬ элементарных катастроф (как «7 взаимодействий» и узел 7).
Бифуркация модели (φ-аттрактор ↔ нулевой) — это катастрофа СБОРКИ (cusp).

Связки:
  * 7 катастроф        — классификация всех устойчивых переходов (Том 1972) [✓];
  * Пуанкаре           — возврат при сохранении меры: цикл S8→S9→S0→S1 [✓];
  * Сахаров / CP       — 3 условия асимметрии: смещение центра δ + неравновесность;
  * Паули              — запрет: 4 различных уровня памяти / 4 компоненты биспинора.

Источники см. в docs/physics.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Catastrophe:
    name: str            # имя
    ade: str             # символ ADE-классификации
    codim: int           # коразмерность (число управляющих параметров)
    state_dim: int       # число переменных состояния
    normal_form: str     # нормальная форма (потенциал)


# Семь элементарных катастроф Тома (коразмерность ≤ 4).
CATASTROPHES = [
    Catastrophe("складка (fold)", "A2", 1, 1, "x³/3 + μ·x"),
    Catastrophe("сборка (cusp)", "A3", 2, 1, "x⁴/4 + μ₂·x²/2 + μ₁·x"),
    Catastrophe("ласточкин хвост", "A4", 3, 1, "x⁵/5 + μ₃·x³/3 + μ₂·x²/2 + μ₁·x"),
    Catastrophe("бабочка", "A5", 4, 1, "x⁶/6 + μ₄·x⁴/4 + … + μ₁·x"),
    Catastrophe("гиперболическая омбилика", "D4+", 3, 2, "x₁³ + x₂³ − μ₃x₁x₂ − μ₂x₂ − μ₁x₁"),
    Catastrophe("эллиптическая омбилика", "D4−", 3, 2, "x₁³ − 3x₁x₂² − μ₃(x₁²+x₂²) − μ₂x₂ − μ₁x₁"),
    Catastrophe("параболическая омбилика", "D5", 4, 2, "x₁⁴ + x₁x₂² + μ₄x₂² + μ₃x₁² + μ₂x₂ + μ₁x₁"),
]


def catastrophe_count() -> int:
    """[✓] Число элементарных катастроф = 7 (= число взаимодействий, узел 7)."""
    return len(CATASTROPHES)


# --- Катастрофа сборки (cusp) = бифуркация модели ----------------------------

def cusp_potential(x, mu1: float, mu2: float):
    """Потенциал сборки V(x) = x⁴/4 + μ₂·x²/2 + μ₁·x."""
    x = np.asarray(x, float)
    return x**4 / 4 + mu2 * x**2 / 2 + mu1 * x


def cusp_equilibria(mu1: float, mu2: float):
    """Равновесия: корни V'(x) = x³ + μ₂·x + μ₁ = 0. Возвращает вещественные корни."""
    roots = np.roots([1.0, 0.0, mu2, mu1])
    return np.sort(roots[np.abs(roots.imag) < 1e-9].real)


def cusp_is_bistable(mu1: float, mu2: float) -> bool:
    """Бистабильность (два устойчивых состояния) ⇔ три вещественных равновесия.

    Это φ-аттрактор ↔ нулевой аттрактор модели: один и тот же переход — сборка.
    """
    return len(cusp_equilibria(mu1, mu2)) == 3


def cusp_bifurcation_set(mu2: float) -> float:
    """Множество складок сборки: 4·μ₂³ + 27·μ₁² = 0 ⇒ μ₁ = ±√(−4μ₂³/27).

    Внутри клина (|μ₁| < граница, μ₂ < 0) система бистабильна.
    """
    if mu2 >= 0:
        return 0.0
    return math.sqrt(-4.0 * mu2**3 / 27.0)


# --- Пуанкаре: возврат при сохранении меры -----------------------------------

def poincare_return_time(alpha: float | None = None, eps: float = 0.05,
                         x0: float = 0.0, max_iter: int = 100000) -> int:
    """Время возврата для поворота окружности x→(x+α) mod 1 (сохраняет меру).

    По теореме Пуанкаре система почти возвращается к началу. Возвращает первое n,
    при котором |xₙ − x₀| < eps. По умолчанию α = 1/φ (золотой, иррациональный) —
    цикл S8→S9→S0→S1 как возврат.
    """
    from .constants import PHI
    if alpha is None:
        alpha = 1.0 / PHI
    x = (x0 + alpha) % 1.0
    for n in range(1, max_iter + 1):
        d = abs(x - x0)
        if min(d, 1 - d) < eps:
            return n
        x = (x + alpha) % 1.0
    return -1


# --- Сахаров / CP: три условия асимметрии ------------------------------------

def sakharov_conditions() -> list[tuple[str, str]]:
    """Три условия Сахарова и их образ в DIALOG QMT."""
    return [
        ("нарушение барионного числа", "асимметрия узлов (не все пары точны)"),
        ("нарушение C и CP", "неточность зеркала −I — смещение центра δ ≠ 0"),
        ("выход из равновесия", "немарковская память ε (открытая система, не равновесие)"),
    ]


def cp_asymmetry(delta: float) -> float:
    """Мера CP-нарушения = смещение центра δ (0 ⇒ точное зеркало, мира нет)."""
    return abs(delta)


# --- Паули: запрет ⇒ различимость уровней ------------------------------------

def pauli_distinct_levels(levels) -> bool:
    """[✓] Принцип Паули: нет двух одинаковых уровней (как 4 компоненты биспинора)."""
    arr = np.round(np.asarray(levels, float), 9)
    return len(np.unique(arr)) == len(arr)


if __name__ == "__main__":
    print(f"Элементарных катастроф Тома: {catastrophe_count()}")
    for c in CATASTROPHES:
        print(f"  {c.ade:<4} {c.name:<26} codim={c.codim}  {c.normal_form}")
    print("\nСборка = бифуркация модели:")
    print(f"  бистабильно при (μ₁=0, μ₂=−1)? {cusp_is_bistable(0.0, -1.0)}  "
          f"равновесия={cusp_equilibria(0.0, -1.0)}")
    print(f"  моностабильно при (μ₁=1, μ₂=1)? {not cusp_is_bistable(1.0, 1.0)}")
    print(f"  граница складок при μ₂=−1: μ₁=±{cusp_bifurcation_set(-1.0):.3f}")
    print(f"\nПуанкаре: возврат (α=1/φ, eps=0.05) за n={poincare_return_time()} шагов")
    print("\nСахаров (CP) ↔ DIALOG QMT:")
    for cond, image in sakharov_conditions():
        print(f"  • {cond}: {image}")
    from .scaling import integrate_memory
    _, E = integrate_memory()
    print(f"\nПаули: 4 уровня памяти различны? {pauli_distinct_levels(E[:, -1])}")
