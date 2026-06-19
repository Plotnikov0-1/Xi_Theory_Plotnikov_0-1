"""
Размерный анализ формул DIALOG QMT — честный фильтр «физика vs число».

Зачем. Формула может давать «правильное число» и при этом быть физически
бессмысленной, если у неё не сходятся единицы измерения. Этот модуль вводит
минимальную систему размерностей (СИ: кг, м, с, А) и проверяет каждую
ключевую формулу теории. Результат — таблица со статусом:

    [РАЗМЕРНО ВЕРНО]  — единицы сходятся, формула может быть физическим законом;
    [БЕЗРАЗМЕРНО]     — обе стороны безразмерны (геометрия/отношение) — ок;
    [РАЗМЕРНЫЙ КОНФЛИКТ] — единицы НЕ сходятся: это эвристика/подгонка, не закон.

Это и есть граница Q1 (теорема) ↔ Q3 (догадка), проведённая объективно.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from . import constants as C

# Базис размерностей: (кг, м, с, А). Энергия = кг·м²·с⁻².
BASE = ("kg", "m", "s", "A")


@dataclass(frozen=True)
class Dim:
    """Физическая величина: численное значение + вектор размерности."""
    value: float
    d: tuple  # (kg, m, s, A)

    def __mul__(self, o: "Dim") -> "Dim":
        return Dim(self.value * o.value, tuple(a + b for a, b in zip(self.d, o.d)))

    def __truediv__(self, o: "Dim") -> "Dim":
        return Dim(self.value / o.value, tuple(a - b for a, b in zip(self.d, o.d)))

    def __pow__(self, n: float) -> "Dim":
        return Dim(self.value ** n, tuple(a * n for a in self.d))

    def units(self) -> str:
        parts = [f"{u}^{p:g}" for u, p in zip(BASE, self.d) if p != 0]
        return "·".join(parts) if parts else "безразм."

    def same_dim(self, o: "Dim", tol: float = 1e-9) -> bool:
        return all(abs(a - b) < tol for a, b in zip(self.d, o.d))


# --- Элементарные размерные величины (значения в СИ) -------------------------
def _d(value, kg=0, m=0, s=0, A=0):
    return Dim(value, (kg, m, s, A))


DIMLESS = _d(1.0)
LENGTH = _d(1.0, m=1)
TIME = _d(1.0, s=1)
ENERGY_J = _d(1.0, kg=1, m=2, s=-2)         # джоуль
FREQ = _d(1.0, s=-1)                         # рад/с
VELOCITY = _d(1.0, m=1, s=-1)

# Конкретные константы как размерные величины
c_ = _d(C.C, m=1, s=-1)
hbar_ = _d(C.HBAR_J, kg=1, m=2, s=-1)        # Дж·с
a_compton = _d(C.COMPTON_LENGTH, m=1)
omega_z = _d(C.ZITTER_FREQ, s=-1)
delta7_J = _d(C.DELTA_7 * C.EV, kg=1, m=2, s=-2)   # Δ7 как энергия (Дж)
tau_bridge = _d(C.TAU_BRIDGE, s=1)


@dataclass
class Check:
    name: str
    lhs: str
    rhs: str
    status: str
    detail: str


def _verdict(left: Dim, right: Dim) -> str:
    if left.same_dim(right):
        if left.d == (0, 0, 0, 0):
            return "[БЕЗРАЗМЕРНО]"
        return "[РАЗМЕРНО ВЕРНО]"
    return "[РАЗМЕРНЫЙ КОНФЛИКТ]"


def run_checks() -> list[Check]:
    """Проверяет размерности ключевых формул теории."""
    out: list[Check] = []

    # 1. Центральное тождество a·ω = c  ([✓] должно быть верно)
    left = a_compton * omega_z
    out.append(Check(
        "Тождество масштаба  a·ω = c", left.units(), c_.units(),
        _verdict(left, c_),
        f"a·ω = {left.value:.4e} {left.units()};  c = {c_.value:.4e} {c_.units()}"))

    # 2. Время моста  τ = ℏ/Δ₇  ([✓] должно быть верно)
    left = hbar_ / delta7_J
    out.append(Check(
        "Время моста  τ = ℏ/Δ₇", left.units(), tau_bridge.units(),
        _verdict(left, tau_bridge),
        f"ℏ/Δ₇ = {left.value:.4e} с;  τ_bridge = {tau_bridge.value:.4e} с"))

    # 3. Аттрактор φ−1 — безразмерное отношение энергий (E−ε)/ε
    left = (ENERGY_J / ENERGY_J)
    out.append(Check(
        "φ-аттрактор  X* = (E−ε)/ε", "безразм.", "безразм.",
        _verdict(left, DIMLESS),
        "отношение двух энергий — безразмерно, X*=φ−1 корректно как число"))

    # 4. Барионная асимметрия  η_B = π·J·(φ−1)·T_EW/Δ₇
    #    T_EW и Δ₇ — энергии, π·J·(φ−1) безразмерны ⇒ η_B имеет размерность
    #    энергия/энергия = безразмерно. ПРОВЕРЯЕМ честно.
    T_EW = _d(1e11 * C.EV, kg=1, m=2, s=-2)     # электрослабый масштаб (Дж)
    eta_left = (T_EW / delta7_J)                 # π·J·(φ−1) безразмерны
    out.append(Check(
        "Бариогенез  η_B ~ π·J·(φ−1)·T_EW/Δ₇", eta_left.units(), "безразм. (η_B)",
        _verdict(eta_left, DIMLESS),
        "T_EW/Δ₇ безразмерно ⇒ формула размерно НЕ запрещена, но J и масштабы "
        "выбраны так, чтобы попасть в число: это эвристика (Q3), не закон"))

    # 5. Коридор G = (π−3)·½·Δ₇ — здесь Δ₇ берётся как ЧИСЛО (эВ), а не энергия.
    #    π−3 и ½ безразмерны; «G в процентах» трактуется безразмерно ⇒
    #    физически это смешение: число эВ выдаётся за безразмерную долю.
    G_as_number = (C.PI - 3) * 0.5 * C.DELTA_7
    out.append(Check(
        "Коридор  G = (π−3)·½·Δ₇", "эВ (если Δ₇ — энергия)", "безразм. доля (%)",
        "[РАЗМЕРНЫЙ КОНФЛИКТ]",
        f"G={G_as_number:.5f}: Δ₇ входит как ЧИСЛО эВ, но G читается как доля — "
        "это совпадение чисел, не размерное равенство (честно: Q3)"))

    return out


def print_report() -> None:
    print("РАЗМЕРНЫЙ АНАЛИЗ ФОРМУЛ DIALOG QMT")
    print("=" * 64)
    for ch in run_checks():
        print(f"\n{ch.name}")
        print(f"    {ch.status}")
        print(f"    {ch.detail}")
    print("\n" + "=" * 64)
    print("Вывод: размерно верны только тождества a·ω=c и τ=ℏ/Δ₇ и безразмерные")
    print("отношения (φ-аттрактор). Формулы η_B и G — числовые эвристики (Q3):")
    print("они НЕ запрещены размерностью, но и не выводятся из неё.")


if __name__ == "__main__":
    print_report()
