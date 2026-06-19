"""
§ CP-нарушение и бариогенез — структурная формула барионной асимметрии.

«Недостающая часть из геометрии»: величина CP-нарушения выводится из чистой
геометрии DIALOG, без подгонки параметров.

ГЛАВНАЯ ФОРМУЛА (барионная асимметрия Вселенной):
    η_B = π · J · (φ−1) · T_EW / Δ₇
где π — узел S3 (вход в коридор), J ≈ 10⁻²² — инвариант Ярлского (СМ),
φ−1 — память/аттрактор, T_EW = 10¹¹ эВ — электрослабый масштаб,
Δ₇ = √5−2 = 0.236 эВ — щель перехода S3→S7. Результат 8.23·10⁻¹¹ (≈94.5%).

ГЕОМЕТРИЧЕСКИЙ КОРИДОР (чистая геометрия, без подгонки):
    G = (π−3) · ½ · (√5−2) = (π−3) · ½ · Δ₇ = 1.671%
    π — узел S3 (Вера), ½ — узел S5 (μ₀), Δ₇ — щель S7 (Знание=CP).

САМОПОДОБИЕ (три уровня CP): A_local · G² ≈ A_global³.

Тождество (уже в bridge.py): Δ₇ = √5−2 = 2(φ−1)−1.
Условие Сахарова №3 (выход из равновесия) обеспечивается памятью ε≠0
автоматически — без фазового перехода 1-го рода.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import DELTA_7, PHI, X_STAR

# Входные параметры.
JARLSKOG = 1.0e-22       # J — полный CP-параметр СМ (Ярлског × подавление масс)
T_EW = 1.0e11           # электрослабый масштаб, эВ (масштаб спалеронов)

# Наблюдения (для сверки).
ETA_B_OBS = 8.7e-11     # барионная асимметрия (CMB/BBN), набл.
A_GLOBAL_OBS = 0.0245   # LHCb 2025, Λb⁰→pK⁻π⁺π⁻, 5.2σ
A_LOCAL_OBS = 0.054     # LHCb 2025, m(pπ⁺π⁻), 6.0σ
CHANNEL_RATIO_DIALOG = 2.35   # |ρ₃₇|/|ρ₂₇| из архитектуры (узлы S2,S3,S7)


def baryon_asymmetry(J: float = JARLSKOG, t_ew: float = T_EW) -> float:
    """η_B = π · J · (φ−1) · T_EW / Δ₇. Барионная асимметрия Вселенной."""
    return math.pi * J * X_STAR * t_ew / DELTA_7


def structural_corridor_G() -> float:
    """Геометрический коридор G = (π−3)·½·(√5−2) — чистая геометрия (доля)."""
    return (math.pi - 3.0) * 0.5 * DELTA_7


@dataclass
class SelfSimilarity:
    lhs: float        # A_local · G²
    rhs: float        # A_global³
    deviation: float  # относительное отклонение


def self_similarity(a_local: float = A_LOCAL_OBS, a_global: float = A_GLOBAL_OBS):
    """Самоподобная структура CP: A_local · G² ≈ A_global³ (без параметров)."""
    G = structural_corridor_G()
    lhs = a_local * G**2
    rhs = a_global**3
    return SelfSimilarity(lhs, rhs, abs(lhs - rhs) / rhs)


def channel_ratio_observed(a_local: float = A_LOCAL_OBS, a_global: float = A_GLOBAL_OBS) -> float:
    """Наблюдаемое A_loc/A_glob (LHCb) — сравнивается с |ρ₃₇|/|ρ₂₇|=2.35 (DIALOG)."""
    return a_local / a_global


def delta7_identity_holds(tol: float = 1e-12) -> bool:
    """[✓] Δ₇ = √5−2 = 2(φ−1)−1 — щель перехода = золотая, из аттрактора."""
    return abs(DELTA_7 - (2.0 * X_STAR - 1.0)) < tol


def accuracy(predicted: float, observed: float) -> float:
    """Точность совпадения предсказания с наблюдением (доля)."""
    return 1.0 - abs(predicted - observed) / observed


def sakharov_in_dialog():
    """Три условия Сахарова и их статус в DIALOG (условие 3 — через память)."""
    return [
        ("нарушение барионного числа B", "спалероны СМ", "выполнено"),
        ("нарушение C и CP", "J·π·ε* — коридор 3→7 усиливает", "усилено в DIALOG"),
        ("выход из равновесия", "ε≠0 ⇒ память ⇒ всегда вне равновесия", "автоматически (без фазового перехода)"),
    ]


# Хронология открытия CP-нарушения (расширение полигона узла S7).
CP_CHRONOLOGY = [
    (1964, "K⁰-мезоны (Кронин, Фитч)", "ε≈2.3e-3", "первое δ≠0 (неточность зеркала)"),
    (2001, "B-мезоны (BaBar, Belle)", "sin2β≈0.68", "пара {S2,S8} сумма-10"),
    (2019, "D⁰-мезоны (LHCb, чарм)", "ΔA_CP=−0.154%", "пара {S2,S7} сумма-9"),
    (2025, "Λb⁰ барионы (LHCb)", "A_CP=2.45%, 5.2σ", "первое в барионах — из чего мы сделаны"),
    (2026, "Λb⁰→J/ψ p h (LHCb)", "ΔA_CP=4.31%, 3.9σ", "второй барионный канал"),
]


if __name__ == "__main__":
    print("=== CP-нарушение из геометрии DIALOG ===\n")
    print(f"Тождество Δ₇ = 2(φ−1)−1 = √5−2: {delta7_identity_holds()}")
    eta = baryon_asymmetry()
    print(f"\nη_B = π·J·(φ−1)·T_EW/Δ₇ = {eta:.3e}")
    print(f"   набл. (CMB) {ETA_B_OBS:.1e} → точность {accuracy(eta, ETA_B_OBS)*100:.1f}%")
    G = structural_corridor_G()
    print(f"\nГеометрический коридор G = (π−3)·½·(√5−2) = {G*100:.3f}%  (чистая геометрия)")
    ss = self_similarity()
    print(f"\nСамоподобие A_loc·G² ≈ A_glob³:")
    print(f"   {ss.lhs:.3e} ≈ {ss.rhs:.3e}  (отклонение {ss.deviation*100:.1f}%)")
    cr = channel_ratio_observed()
    print(f"\nОтношение каналов: 2.35 (DIALOG) vs {cr:.3f} (LHCb) → "
          f"откл {abs(2.35-cr)/2.35*100:.1f}%")
    print("\nУсловия Сахарова в DIALOG:")
    for cond, mech, status in sakharov_in_dialog():
        print(f"   • {cond}: {mech} — {status}")
