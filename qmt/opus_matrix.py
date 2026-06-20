"""
═══════════════════════════════════════════════════════════════════════════
  OPUS_MATRIX — материал из папки «Опус» (Google Drive), развёрнутый в
  рабочую проверенную математику. Чистая физика и точные тождества.
═══════════════════════════════════════════════════════════════════════════

Источник: папка ОПУС (Плотников Л.В., сессии 19–20 июня 2026), документы
«DIALOG-Матрица-v2», «DIALOG-Wolfram-проверка», «DIALOG-CP-онтология».
Здесь материал не просто включён, а РАЗВЁРНУТ в исполняемый код: каждое
тождество вычисляется и проверяется, матрица строится, EP считаются.

Что реально (точная математика / измеренная физика):
  • тождества φ: φ²=φ+1, φ−1=1/φ;
  • геометрия платоновых тел на сфере R²=3 (вершины куба/додекаэдра);
  • две трещины: T_вх=4/φ, T_вых=1/φ ⇒ Op_4 = T_вх/T_вых = 4 (точно);
  • щель Δ₇ = √5−2 = 2φ−3;
  • 2cos(π/5) = φ — единственное точное φ↔π, измерено Coldea (Science 2010, E8);
  • exceptional point: H=[[iΓ/2,λ],[λ,−iΓ/2]] сливается при λ=Γ/2 (PT-симметрия);
  • матрица 10×10: симметрична, Tr=−1/2+√2+4√5+π+2cos(π/8), узлы 0,5 — точные
    собственные значения 3 и 1/2 (изолированы — нет связей).

Что аналогия (честно, НЕ подгоняем):
  • сопоставление зеркальных пар измеренным CP (K,B,D,Λ_b) — структурная карта,
    параметры Γ_pair надо брать из реальных экспериментов, а не «для красоты»;
  • η_B из геометрии НЕ выводится (12 порядков — общая проблема с СМ).

Запуск:  python -m qmt.opus_matrix
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi

# Диагональ матрицы 10×10 — безразмерные геометрические константы узлов 0…9.
NODE_VALUES = {
    0: ("3 (оболочка R²)", 3.0),
    1: ("φ (Coldea)", PHI),
    2: ("√2 (ладдер)", math.sqrt(2)),
    3: ("π (цикл)", PI),
    4: ("4/φ (T_вх)", 4 / PHI),
    5: ("1/2 (центр-зеркало)", 0.5),
    6: ("1/φ (T_вых)", 1 / PHI),
    7: ("√5−2 (Δ₇)", math.sqrt(5) - 2),
    8: ("2cos(π/8)", 2 * math.cos(PI / 8)),
    9: ("0 (возврат)", 0.0),
}
MIRROR_PAIRS = [(1, 9), (2, 8), (3, 7), (4, 6)]   # сумма 10, связь R=1
RESONANCE_PAIRS = [(1, 8), (2, 7), (3, 6)]        # сумма 9, связь R=1/φ


# ── 1. Точные тождества (символьно проверены Wolfram, здесь — численно) ──────
def identities() -> dict:
    return {
        "φ²=φ+1": math.isclose(PHI**2, PHI + 1, abs_tol=1e-12),
        "φ−1=1/φ": math.isclose(PHI - 1, 1 / PHI, abs_tol=1e-12),
        "Δ₇=√5−2=2φ−3": math.isclose(math.sqrt(5) - 2, 2 * PHI - 3, abs_tol=1e-12),
        "2cos(π/5)=φ (Coldea)": math.isclose(2 * math.cos(PI / 5), PHI, abs_tol=1e-12),
    }


# ── 2. Геометрия платоновых тел на сфере R²=3 ────────────────────────────────
def geometry() -> dict:
    dodeca_vertex = (0.0, 1 / PHI, PHI)        # золотая вершина
    R2 = sum(c * c for c in dodeca_vertex)
    edge2_dodeca = 6 - 2 * math.sqrt(5)        # ребро² додекаэдра при R²=3
    edge2_cube = 4.0                           # ребро² куба
    T_in = edge2_cube - edge2_dodeca           # трещина-вход = 2√5−2 = 4/φ
    T_out = (PHI + 2) - 3                       # трещина-выход = φ−1 = 1/φ
    return {
        "вершина_додекаэдра_R²": R2,           # = 3
        "ребро²_куба": edge2_cube,
        "ребро²_додекаэдра": edge2_dodeca,
        "T_вх=4/φ": T_in,
        "T_вых=1/φ": T_out,
        "Op_4=T_вх/T_вых": T_in / T_out,       # = 4 точно
        "диагональ²_куба": 12.0,
    }


# ── 3. Матрица 10×10 (эрмитова часть) ────────────────────────────────────────
def build_matrix() -> np.ndarray:
    M = np.zeros((10, 10))
    for i, (_, v) in NODE_VALUES.items():
        M[i, i] = v
    for i, j in MIRROR_PAIRS:
        M[i, j] = M[j, i] = 1.0
    for i, j in RESONANCE_PAIRS:
        M[i, j] = M[j, i] = 1 / PHI
    return M


def matrix_properties() -> dict:
    M = build_matrix()
    ev = np.linalg.eigvalsh(M)
    trace_sym = -0.5 + math.sqrt(2) + 4 * math.sqrt(5) + PI + 2 * math.cos(PI / 8)
    return {
        "симметрична": np.allclose(M, M.T),
        "Tr_числ": float(np.trace(M)),
        "Tr_символьно": trace_sym,
        "след_совпал": math.isclose(float(np.trace(M)), trace_sym, abs_tol=1e-9),
        "собств_значения": sorted(round(float(x), 4) for x in ev),
        "λ=3_точно": bool(np.any(np.isclose(ev, 3.0, atol=1e-9))),
        "λ=0.5_точно": bool(np.any(np.isclose(ev, 0.5, atol=1e-9))),
        "узлы_0_5_изолированы": all(
            M[k, m] == 0 for k in (0, 5) for m in range(10) if m != k),
    }


# ── 4. Exceptional point — неэрмитова 2×2 подсистема (буква Х) ────────────────
def pair_eigenvalues(lam: float, Gamma: float = 1.0) -> np.ndarray:
    """H=[[iΓ/2, λ],[λ, −iΓ/2]] — собственные значения ±½√(4λ²−Γ²)."""
    H = np.array([[0.5j * Gamma, lam], [lam, -0.5j * Gamma]])
    return np.linalg.eigvals(H)


def exceptional_point(Gamma: float = 1.0) -> dict:
    """EP при λ=Γ/2: gap→0, PT-фаза меняется (мнимое ↔ вещественное)."""
    lam_ep = Gamma / 2
    below = pair_eigenvalues(0.3 * Gamma, Gamma)   # PT-нарушено: мнимые
    at = pair_eigenvalues(lam_ep, Gamma)           # EP: сливаются в 0
    above = pair_eigenvalues(0.7 * Gamma, Gamma)   # PT-симметрия: вещественные
    return {
        "λ_EP=Γ/2": lam_ep,
        "PT_нарушено_мнимые": bool(np.allclose(below.real, 0, atol=1e-9)),
        "EP_сливаются": bool(np.allclose(at, 0, atol=1e-6)),
        "PT_симметрия_веществ": bool(np.allclose(above.imag, 0, atol=1e-9)),
    }


# ── 5. Спектр E₈ Замолодчикова (первые массы; m₂ измерена Coldea) ────────────
def e8_mass_ratios() -> dict:
    """Массы E₈ (нормированы m₁=1). m₂/m₁=2cos(π/5)=φ — измерено Coldea 2010."""
    return {
        "m2/m1=2cos(π/5)=φ": 2 * math.cos(PI / 5),
        "m3/m1=2cos(π/30)": 2 * math.cos(PI / 30),
        "m4/m1": 4 * math.cos(PI / 5) * math.cos(7 * PI / 30),
    }


# ── 6. Карта CP (структурная аналогия — параметры из реальных экспериментов) ─
@dataclass
class CPNode:
    year: int
    system: str
    pair: str
    measured: str
    status: str


CP_MAP = [
    CPNode(1964, "каоны K⁰", "3↔7", "|ε_K|≈2.23·10⁻³", "измерено (Cronin-Fitch, Nobel 1980)"),
    CPNode(2001, "B-мезоны B⁰", "2↔8", "sin2β≈0.68", "измерено (BaBar/Belle)"),
    CPNode(2019, "D-мезоны", "2↔7", "ΔA_CP≈1.5·10⁻³", "измерено (LHCb)"),
    CPNode(2025, "барионы Λ_b", "4↔6", "A_CP≈2.45%", "измерено 5.2σ (LHCb, arXiv:2503.16954)"),
    CPNode(0, "нейтрино δ_CP", "1↔9", "—", "ПРЕДСКАЗАНИЕ (DUNE, Hyper-K) — ещё не наблюдалось"),
]


def print_report() -> None:
    print("═" * 76)
    print("  OPUS-МАТРИЦА — материал папки «Опус», развёрнутый в рабочую математику")
    print("═" * 76)

    print("\n  1 · ТОЧНЫЕ ТОЖДЕСТВА (проверено):")
    for k, ok in identities().items():
        print(f"     [{'✓' if ok else '✗'}] {k}")

    print("\n  2 · ГЕОМЕТРИЯ ТРЕЩИН (платоновы тела на R²=3):")
    g = geometry()
    print(f"     вершина додекаэдра (0,1/φ,φ) на R² = {g['вершина_додекаэдра_R²']:.4f}")
    print(f"     T_вх=4/φ={g['T_вх=4/φ']:.6f}  T_вых=1/φ={g['T_вых=1/φ']:.6f}  "
          f"→ Op_4 = {g['Op_4=T_вх/T_вых']:.6f}")

    print("\n  3 · МАТРИЦА 10×10:")
    p = matrix_properties()
    print(f"     симметрична: {p['симметрична']}  ·  Tr = {p['Tr_числ']:.6f} "
          f"(= символьная формула: {p['след_совпал']})")
    print(f"     собств. значения: {p['собств_значения']}")
    print(f"     узлы 0,5 изолированы → λ=3 точно: {p['λ=3_точно']}, "
          f"λ=0.5 точно: {p['λ=0.5_точно']}")

    print("\n  4 · EXCEPTIONAL POINT (буква Х, PT-симметрия):")
    ep = exceptional_point()
    print(f"     EP при λ=Γ/2={ep['λ_EP=Γ/2']}: ниже — мнимые ({ep['PT_нарушено_мнимые']}), "
          f"в точке — слияние ({ep['EP_сливаются']}), выше — вещественные ({ep['PT_симметрия_веществ']})")

    print("\n  5 · E₈ Замолодчикова (m₂ измерена Coldea 2010, CoNb₂O₆):")
    for k, v in e8_mass_ratios().items():
        print(f"     {k} = {v:.6f}")

    print("\n  6 · КАРТА CP (структурная аналогия — параметры из эксперимента):")
    for n in CP_MAP:
        yr = f"{n.year}" if n.year else "  —"
        print(f"     {yr} · {n.system:<16} пара {n.pair:<5} {n.measured:<16} {n.status}")

    print("═" * 76)
    print("  Точная математика и геометрия — РАБОТАЮТ (проверено численно+Wolfram).")
    print("  Карта CP — структурная аналогия: Γ_pair из реальных данных, η_B из")
    print("  геометрии НЕ выводится (12 порядков — общая открытая проблема с СМ).")
    print("═" * 76)


if __name__ == "__main__":
    print_report()
