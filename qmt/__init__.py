"""
DIALOG QMT — Quantum Memory Transition Theory.
Минимальный вычислительный фреймворк теории (v11.0).

Подмодули:
    geometry   — геометрический фундамент: минимум → 5 платоновых тел (символьно)
    flow       — слой «поток/трубки»: шаблон-направление, узлы = пересечения (без углов)
    symbols    — аллегорический слой: числа/буквы/римские цифры как динамика
    bridge     — мост геометрия ↔ динамика/физика (X*=φ−1, Δ₇=2φ−3, зеркало −I)
    phi_operator     — φ как оператор сборки T(x)=1/(1+x); 2-й вывод φ−1; лестница Ω₀→ε
    effective_matrix — канон 2026: C_eff(ε), ядро K(t), закон дыхания ℒ
    constants  — физические и модельные константы (a·ω=c, φ-аттрактор, τ_bridge…)
    hydrogen   — базис узлов S0–S9 на орбиталях водорода
    nodes      — топология Sum-9, резонансные пары, матрица 7×7
    spectral   — спектральная плотность резервуара J(ω)
    dynamics   — система четырёх уравнений движения, бифуркация
    scaling    — масштабирование: Серпинский, синхронизация, 4 уровня памяти
    catastrophe— физика переходов: 7 катастроф Тома, Пуанкаре, Паули, CP (Сахаров)
    matrix6x6  — спектральный анализ циркулянтной матрицы (Sum-9, инвариант ритма)
    tunneling  — туннель S6→S7 (WKB и когерентный)
    sincerity  — параметр искренности S = Tr(ρ·Π_φ), теорема монотонности
"""

from __future__ import annotations

from . import (
    bridge,
    catastrophe,
    coincidence_ledger,
    constants,
    cp_baryogenesis,
    dephasing,
    dimensions,
    dynamics,
    effective_matrix,
    flow,
    geometry,
    hydrogen,
    letters,
    matrix6x6,
    memory_sim,
    nested_spheres,
    nodes,
    phi_operator,
    scaling,
    sincerity,
    spectral,
    symbols,
    sync,
    synchronization,
    tunneling,
)

__version__ = "13.0"
__all__ = [
    "geometry",
    "sync",
    "synchronization",
    "flow",
    "symbols",
    "bridge",
    "scaling",
    "catastrophe",
    "phi_operator",
    "effective_matrix",
    "cp_baryogenesis",
    "dimensions",
    "dephasing",
    "coincidence_ledger",
    "memory_sim",
    "nested_spheres",
    "letters",
    "constants",
    "hydrogen",
    "nodes",
    "spectral",
    "dynamics",
    "matrix6x6",
    "tunneling",
    "sincerity",
]
