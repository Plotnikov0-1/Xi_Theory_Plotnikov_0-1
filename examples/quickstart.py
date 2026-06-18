#!/usr/bin/env python3
"""
Быстрый старт DIALOG QMT — короткая демонстрация всех компонентов фреймворка.

Запуск из корня проекта:  python examples/quickstart.py
"""

from __future__ import annotations

import os
import sys

# Чтобы пример работал при запуске из любой папки.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qmt import constants as C
from qmt import dynamics, hydrogen, matrix6x6, nodes, sincerity, tunneling


def main():
    print("=" * 60)
    print("DIALOG QMT v11.0 — демонстрация фреймворка")
    print("=" * 60)

    print("\n[1] Базовые константы")
    print(f"  a·ω = c        : {C.COMPTON_LENGTH * C.ZITTER_FREQ:.4e} м/с")
    print(f"  φ-аттрактор X* : {C.X_STAR:.6f}  (= φ−1)")
    print(f"  τ_bridge       : {C.TAU_BRIDGE * 1e15:.2f} фс")
    print(f"  Γ*             : {C.GAMMA_STAR:.4f}")

    print("\n[2] Узлы S0–S9 (φ-оптимальные отмечены ✓)")
    for nd in hydrogen.NODES:
        e = "  —  " if nd.energy_ev is None else f"{nd.energy_ev:6.3f}"
        print(f"  S{nd.index} [{'✓' if nd.on_fibonacci else ' '}] E={e} эВ  {nd.name}")

    print("\n[3] Топология Sum-9")
    chk = nodes.verify_sum9()
    print(f"  5 резонансных пар, сумма=9: {chk.pairs_ok}; все узлы покрыты: {chk.covers_all}")

    print("\n[4] Матрица 6×6")
    inv = matrix6x6.spectral_invariants()
    print(f"  λ = {inv.eigvals.round(2)}  | след = {inv.trace:.0f} (Sum-9)")
    R = matrix6x6.rhythm_invariant(C.OMEGA_SYS, inv.delta_min, C.GAMMA_DECO)
    print(f"  инвариант ритма ℛ = {R:.3f}  (зона баланса)")

    print("\n[5] Динамика: φ-аттрактор при μ_crit = 0.5")
    print(f"  X*(μ=0.5) = {dynamics.steady_state_load(0.5):.6f}  (эталон {C.X_STAR:.6f})")

    print("\n[6] Туннель S6→S7")
    t_wkb, t_coh, ratio = tunneling.wkb_vs_coherent(0.0)
    print(f"  T_WKB = {t_wkb:.2e}  →  T_когерент = {t_coh:.4f}  (усиление ×{ratio:.1e})")

    print("\n[7] Параметр искренности S(ε)")
    for e in (0.0, 0.5, 1.0):
        print(f"  ε={e:.1f}: S_Fib={sincerity.s_fibonacci(e):.3f}  "
              f"S_tunnel={sincerity.s_tunnel(e):.4f}")
    print(f"  теорема монотонности: {sincerity.monotonicity_holds()}")

    print("\nГотово. Для графиков выполните:  python visualize.py")


if __name__ == "__main__":
    main()
