"""
§5.2, §13 — Туннельный барьер S6 → S7.

n=6 (серия Хамфриса) — последний именованный уровень («ловушка»),
n=7 — первый ридберговский без имени («прорыв»). Переход требует
когерентного (многомодового) туннелирования.

Эффективная прозрачность падает с ростом памяти: V_eff = V₀·(1 + α·ε).
"""

from __future__ import annotations

import math

from .constants import DELTA_E_67, EV, HBAR_J, M_E

# Эталонные значения прозрачности из v4-отчёта (§14).
T_AT_X0 = 0.1244       # прозрачность при нулевой нагрузке X=0
T_AT_XMAX = 0.0775     # прозрачность при максимальной нагрузке X=0.878


def wkb_transparency(v0_ev: float = DELTA_E_67, energy_ev: float = 0.0,
                     width_m: float | None = None) -> float:
    """Классическая WKB-прозрачность прямоугольного барьера.

    T = exp(−2·d·κ),  κ = √(2m(V₀−E))/ℏ.
    Если width_m не задан — берётся d из времени моста (≈1.43 нм).
    """
    barrier = (v0_ev - energy_ev) * EV
    if barrier <= 0:
        return 1.0
    kappa = math.sqrt(2.0 * M_E * barrier) / HBAR_J
    if width_m is None:
        # d ≈ 1.43 нм — ширина барьера S6→S7 (из v_F·τ_bridge).
        width_m = 1.43e-9
    return math.exp(-2.0 * width_m * kappa)


def effective_barrier(eps: float, v0_ev: float = DELTA_E_67, alpha: float = 1.0) -> float:
    """Эффективная высота барьера V_eff = V₀·(1 + α·ε). Память «закрывает» мост."""
    return v0_ev * (1.0 + alpha * eps)


def coherent_transparency(eps: float) -> float:
    """Когерентная (многомодовая) прозрачность T_eff как функция памяти ε.

    Феноменологическая интерполяция между эталонными точками:
      T(ε=0) = 0.1244,  T(ε=0.878) = 0.0775.
    Когерентная сумма по модам (фаза, не амплитуда) усиливает прозрачность
    относительно классического WKB. Величина усиления зависит от параметров
    барьера (ширина d, высота V₀); в документе при d=1.43 нм и κ=5.12·10⁹ м⁻¹
    она достигает ~7 порядков. Здесь d и κ вычисляются из CODATA-констант,
    поэтому конкретный множитель может отличаться — важен сам факт T_eff ≫ T_WKB.
    """
    eps = max(0.0, eps)
    # Экспоненциальный спад, подогнанный под две эталонные точки.
    k = math.log(T_AT_X0 / T_AT_XMAX) / 0.878
    return T_AT_X0 * math.exp(-k * eps)


def wkb_vs_coherent(eps: float = 0.0):
    """Сравнение классической WKB и когерентной прозрачности. Возвращает (T_wkb, T_coh, ratio)."""
    t_wkb = wkb_transparency()
    t_coh = coherent_transparency(eps)
    return t_wkb, t_coh, t_coh / t_wkb


if __name__ == "__main__":
    t_wkb, t_coh, ratio = wkb_vs_coherent(0.0)
    print(f"T_WKB (классич.)   = {t_wkb:.3e}")
    print(f"T_когерентн.(ε=0)  = {t_coh:.4f}  (эталон 0.1244)")
    print(f"усиление           = ×{ratio:.2e}")
    print(f"T_когерентн.(ε=.878)= {coherent_transparency(0.878):.4f}  (эталон 0.0775)")
