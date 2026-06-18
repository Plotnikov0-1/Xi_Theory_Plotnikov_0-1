"""
DIALOG QMT — Quantum Memory Transition Theory.
Минимальный вычислительный фреймворк теории (v11.0).

Подмодули:
    constants  — физические и модельные константы (a·ω=c, φ-аттрактор, τ_bridge…)
    hydrogen   — базис узлов S0–S9 на орбиталях водорода
    nodes      — топология Sum-9, резонансные пары, матрица 7×7
    spectral   — спектральная плотность резервуара J(ω)
    dynamics   — система четырёх уравнений движения, бифуркация
    matrix6x6  — спектральный анализ циркулянтной матрицы (Sum-9, инвариант ритма)
    tunneling  — туннель S6→S7 (WKB и когерентный)
    sincerity  — параметр искренности S = Tr(ρ·Π_φ), теорема монотонности
"""

from __future__ import annotations

from . import (
    constants,
    dynamics,
    hydrogen,
    matrix6x6,
    nodes,
    sincerity,
    spectral,
    tunneling,
)

__version__ = "11.0"
__all__ = [
    "constants",
    "hydrogen",
    "nodes",
    "spectral",
    "dynamics",
    "matrix6x6",
    "tunneling",
    "sincerity",
]
