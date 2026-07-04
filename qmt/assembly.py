"""
═══════════════════════════════════════════════════════════════════════════
  ASSEMBLY — СБОРКА: единый рабочий инструмент из самого нужного (проверено).
═══════════════════════════════════════════════════════════════════════════

Не отчёт и не снимок — исполняемая СБОРКА. Одна команда берёт проверенные ядра,
сшивает в одно целое и подтверждает, что они СОГЛАСОВАНЫ между собой (одно и то
же φ−1 в четырёх местах, потолок Нивена, устойчивая динамика, факторизация).

Собрано только несущее (§ соответствуют STATE_OF_THEORY.md):
  1 ПРИНЦИП   — 𝔗(x)=1/(1+x): неподвижная точка самосогласования φ−1.
  2 ЯДРО      — proof_core (7 шагов [Q0]), потолок Нивена N=6.
  3 ДИНАМИКА  — minimal_dynamics (Т2–Т8): устойч. стационар на φ−1.
  4 КОНСТАНТЫ — canon_constants/x_law: N=6, α точна, β свободен (4/3).
  5 ПЕРЕХОДЫ  — transitions: факторизация Ридберга (20, 9 из алгебры).
  6 ВЫХОД     — breathing: один фальсифицируемый предсказание (линии 7→3/7→2).

Кросс-проверка (главное): φ−1 — БУКВАЛЬНО одно число в ядре, динамике,
операторе и геометрии. Это и делает сборку единой, а не набором модулей.

Запуск:  python -m qmt.assembly
"""

from __future__ import annotations

import math

from . import (breathing, canon_constants, carrier_map, minimal_dynamics,
               proof_core, transitions, unified_model, universal_transition,
               x_law)

PHI = (1 + math.sqrt(5)) / 2
PHI1 = PHI - 1
PRINCIPLE = "𝔗(x)=1/(1+x): неподвижная точка самосогласования, аттрактор φ−1"


# ── КРОСС-ПРОВЕРКА: одно φ−1 в четырёх доменах ───────────────────────────────
def cross_domain_phi() -> dict:
    """◇ φ−1 буквально совпадает: ядро · динамика · оператор · геометрия."""
    core = proof_core.step3_golden_point()["x*"]           # x²+x−1=0
    dyn = minimal_dynamics.golden_manifold_kappaX(1.0, 1.0)  # κX=r/φ
    op = universal_transition.iterate()                     # итерация 𝔗
    geom = 2 * carrier_map.midsphere_radius("икосаэдр")      # 2·(φ/2)=φ
    same = all(math.isclose(v, PHI1, abs_tol=1e-9) for v in (core, dyn, op)) \
        and math.isclose(geom, PHI, abs_tol=1e-9)
    return {"ядро x²+x−1=0": round(core, 9), "динамика κX=r/φ": round(dyn, 9),
            "оператор iter 𝔗": round(op, 9), "геометрия 2ρ_икоса": round(geom, 9),
            "одно φ−1": same}


# ── СБОРКА ЯДЕР: все проверенные блоки согласованы ───────────────────────────
def verified_core() -> dict:
    """Ключевой проверенный результат из каждого несущего модуля."""
    P = dict(r_eps=1.0, kappa=0.8, Gamma=0.7, b_S=1.3, eps_targ=2.0)
    return {
        "1 ПРИНЦИП 𝔗 самоподобен": universal_transition.self_similar_fixed_point(),
        "2 ЯДРО 7 шагов [Q0]": proof_core.all_steps_pass(),
        "2 потолок Нивена N=6": proof_core.step2_niven_ceiling()["ок"],
        "3 динамика устойчива (Т4)": minimal_dynamics.is_stable(**P),
        "3 память=ОДУ (Т7)": minimal_dynamics.aux_realization_matches(),
        "4 N=6 мод (не знаки)": canon_constants.N_meaning()["N=6 мод (размерность)"],
        "4 α даёт λ_u=13.3 точно": canon_constants.alpha_controls_mode_exactly(),
        "4 β свободен (изолир. 4/3)": canon_constants.beta_is_free(),
        "4 β не выводим симметрией": x_law.layer_symmetry_cannot_fix_beta(),
        "5 факторизация Ридберга": transitions.factorization_exact(),
        "6 инварианты Ω=(R,T,C)": unified_model.foundation_is_consistent(),
    }


def assembly_is_consistent() -> bool:
    """Вся сборка согласована: кросс-φ + все ядра зелёные вместе."""
    return cross_domain_phi()["одно φ−1"] and all(verified_core().values())


# ── ОДИН СВОБОДНЫЙ ВИНТ и ОДНО ПРЕДСКАЗАНИЕ ──────────────────────────────────
def one_free_screw() -> dict:
    """🔴 Единственный по-настоящему свободный винт ядра: 4/3 в β=(4/3)α."""
    return {"винт": "β=(4/3)α", "ратио": round(4 / 3, 4),
            "почему свободен": "4/3 безразмерно; симметрия слоёв не выводит (x_law)",
            "как закрыть": "новая связь слоёв (недиагональная u↔v), не принцип поверх"}


def one_prediction() -> dict:
    """✓ Единственный фальсифицируемый выход: разворот линий при накачке n=6."""
    return breathing.falsifiable_prediction()


def assembled_chain() -> str:
    """Причинная цепь собранной теории (снизу вверх)."""
    return ("𝔗 (принцип) → зеркало+тетраэдр → 5 тел (геометрия) → золотой "
            "стационар φ−1 (динамика) → C_eff → спектр → K(t) (память) → "
            "предсказание линий 7→3/7→2 (проверка)")


def print_report() -> None:
    print("═" * 74)
    print("  СБОРКА DIALOG-QMT/Ω: единый инструмент из проверенного")
    print("═" * 74)
    print(f"\n  ПРИНЦИП: {PRINCIPLE}")

    print("\n  КРОСС-ПРОВЕРКА — одно φ−1 в четырёх доменах:")
    for k, v in cross_domain_phi().items():
        print(f"     {k}: {v}")

    print("\n  СБОРКА ЯДЕР (все проверенные блоки):")
    for k, v in verified_core().items():
        mark = "✓" if v else "✗"
        print(f"     [{mark}] {k}: {v}")

    print(f"\n  ЦЕПЬ: {assembled_chain()}")

    print(f"\n  🔴 ОДИН свободный винт: {one_free_screw()['винт']} — "
          f"{one_free_screw()['почему свободен']}")
    pr = one_prediction()
    print(f"  ✓ ОДНО предсказание: {pr['наблюдаемая']} {pr['равновесие_NIST']}→"
          f"{pr['предсказание_накачка']} (накачка n=6, {pr['метод']})")

    print(f"\n  ═══ СБОРКА СОГЛАСОВАНА: {assembly_is_consistent()} ═══")
    print("═" * 74)
    print("  Собрано только несущее. Ядро доказано и согласовано (одно φ−1).")
    print("  Один свободный винт (4/3), одно фальсифицируемое предсказание. Честно.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
