"""
СИНХРОНИЗАЦИЯ: геометрия ↔ физика водорода — рабочая модель.

Здесь собрано то, чем пользуемся: где на геометрии стоят арабские цифры, какие
переходы разрешены, какие запрещены, и как всё синхронизировано с квантовой
динамикой атома водорода. Начало — тетраэдр (минимум): шар + точка + 4 вершины.

РАЗМЕЩЕНИЕ ЦИФР:
  * вершины куба (8): числа 1,2,3,4,6,7,8,9 (узлы-состояния);
  * центр: 5 (зеркало −I, ψ(0)≠0, наблюдатель-ось);
  * оболочка R=√3: 0 (вакуум/граница, ионизация водорода n→∞).
Каждое число n ↔ уровень водорода n: E_n = −13.6/n².

ПРАВИЛО ОТБОРА (классификация по геометрии куба = 3 бита):
  * Хэмминг 1 (ребро)        → ПРЯМОЙ шаг (разрешён, один квант);
  * сумма-9 (резонанс)        → РЕЗОНАНСНЫЙ канал (разрешён, туннель);
  * сумма-10 (диагональ тела) → ЗЕРКАЛО −I (разрешён, чётность/инверсия);
  * прочие диагонали грани    → ЗАПРЕЩЕНО (нет канала).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from . import hydrogen as H
from .geometry import CUBE, MIRROR_PAIRS, RESONANCE_PAIRS, TET_A

VERTICES = sorted(CUBE.keys())          # 1,2,3,4,6,7,8,9
CENTER = 5                              # зеркало −I, ψ(0)≠0
SHELL = 0                              # оболочка/вакуум, ионизация
SUM10 = {frozenset(p) for p in MIRROR_PAIRS}      # зеркало
SUM9 = {frozenset(p) for p in RESONANCE_PAIRS}    # резонанс
# Прямая «линейка»: 1→2→…→9→0 (цикл, по часовой стрелке) — из топологии двух линеек.
LADDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


def _bits(n: int) -> int:
    x, y, z = CUBE[n]
    return ((1 if x > 0 else 0) << 2) | ((1 if y > 0 else 0) << 1) | (1 if z > 0 else 0)


def hamming(a: int, b: int) -> int:
    """Геометрическое расстояние = число различных бит (рёбер куба между узлами)."""
    return bin(_bits(a) ^ _bits(b)).count("1")


@dataclass(frozen=True)
class Transition:
    a: int
    b: int
    kind: str            # 'прямой' / 'резонанс' / 'зеркало' / 'запрещён'
    allowed: bool
    channel: str         # физический канал
    dE_eV: float         # энергия перехода в водороде
    wavelength_nm: float  # длина волны (нм)


def classify(a: int, b: int) -> Transition:
    """Классифицировать переход a↔b и синхронизировать с водородом."""
    pair = frozenset((a, b))
    h = hamming(a, b)
    if pair in SUM10:
        kind, allowed, channel = "зеркало", True, "инверсия −I (чётность, сумма-10)"
    elif pair in SUM9:
        kind, allowed, channel = "резонанс", True, "туннель Sum-9 (сумма-9)"
    elif h == 1:
        kind, allowed, channel = "прямой", True, "ребро куба (один квант, Δ один бит)"
    else:
        kind, allowed, channel = "запрещён", False, "нет канала (диагональ грани)"
    lo, hi = min(a, b), max(a, b)
    dE = H.energy_level(lo) - H.energy_level(hi) if lo >= 1 else 0.0
    lam = H.transition_wavelength(hi, lo) * 1e9 if lo >= 1 else float("inf")
    return Transition(a, b, kind, allowed, channel, abs(dE), lam)


def all_transitions():
    """Все 28 пар вершин с классификацией и водородными линиями."""
    return [classify(a, b) for a, b in itertools.combinations(VERTICES, 2)]


def allowed_transitions():
    """Разрешённые переходы (прямой/резонанс/зеркало)."""
    return [t for t in all_transitions() if t.allowed]


def forbidden_transitions():
    """Запрещённые переходы (диагонали грани без канала)."""
    return [t for t in all_transitions() if not t.allowed]


def selection_counts() -> dict:
    """Сводка: сколько переходов каждого типа."""
    out = {"прямой": 0, "резонанс": 0, "зеркало": 0, "запрещён": 0}
    for t in all_transitions():
        out[t.kind] += 1
    return out


def tetrahedron_start():
    """Минимум: тетраэдр-генератор {1,6,7,8} и переходы внутри него (резонансы)."""
    tet = TET_A
    trans = [classify(a, b) for a, b in itertools.combinations(tet, 2)]
    return tet, trans


if __name__ == "__main__":
    print("Размещение цифр: вершины", VERTICES, "| центр 5 | оболочка 0")
    print(f"\nСводка переходов: {selection_counts()}")
    print("\nРазрешённые переходы (a↔b, тип, λ водорода):")
    for t in allowed_transitions():
        print(f"  {t.a}↔{t.b}  {t.kind:<9} {t.channel:<34} λ={t.wavelength_nm:7.1f} нм")
    print("\nЗапрещённые (диагонали грани, нет канала):")
    print("  ", [f"{t.a}-{t.b}" for t in forbidden_transitions()])
    tet, tt = tetrahedron_start()
    print(f"\nМинимум-тетраэдр {tet}: внутренние переходы —",
          {t.kind for t in tt})
