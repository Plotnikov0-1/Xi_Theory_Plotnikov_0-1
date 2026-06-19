"""
Квантовый эксперимент DIALOG QMT — фальсифицируемая проверка гипотезы памяти.

ГИПОТЕЗА (единственное настоящее предсказание теории, статус Q3):
память ε — самостоятельная физическая переменная. Тогда эффективная скорость
декогеренции линейно зависит от накопленной памяти:

        κ_eff(ε) = a + b·ε ,      причём  b ≠ 0.

Нулевая гипотеза (стандартная КМ без памяти): b = 0 (κ_eff не зависит от ε).
Эксперимент СПОСОБЕН отвергнуть теорию — это и делает её научной.

ПРОТОКОЛ (Рэмзи с управляемой памятью):
  1. Готовим систему-кубит в суперпозиции  |+⟩ = H|0⟩.
  2. N раз повторяем «цикл памяти»: слабое CRZ(θ) на регистр-память (ancilla),
     который удерживает фазовую историю. Параметр ε ≡ сила связи θ·(глубина).
  3. Закрываем интерферометр (H) и измеряем контраст V(N).
  4. Из спада V(N)=exp(−κ_eff·N) извлекаем κ_eff(ε).
  5. Сканируем ε, линейно фитим κ_eff(ε)=a+b·ε, проверяем значимость b≠0 (5σ).

Код запускается на numpy-симуляторе (всегда) и на Qiskit/реальном железе IBM
(если qiskit установлен) — функция build_circuit() даёт готовую схему.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from qmt import constants as C

# Истинное значение b в симуляции «как если бы DIALOG верна». В реальном
# эксперименте b — то, что измеряется; здесь задаём ненулевым, чтобы
# показать, КАК выглядел бы сигнал и какая нужна статистика.
B_TRUE_DIALOG = 0.045     # наклон (предсказание теории, иллюстративно)
A_BASE = 0.020            # базовая (марковская) скорость декогеренции


# --------------------------------------------------------------------------
# Численная модель измерения (то, что выдал бы квантовый компьютер)
# --------------------------------------------------------------------------
def kappa_true(eps: float, b: float) -> float:
    """Истинная κ_eff(ε)=a+b·ε для генерации синтетических данных."""
    return A_BASE + b * eps


def measure_contrast(eps: float, n_cycles: int, b: float,
                     n_shots: int, rng: np.random.Generator) -> float:
    """Контраст Рэмзи V(N) с дробовым (биномиальным) шумом измерения.

    Идеально V = exp(−κ·N); вероятность исхода p=(1+V)/2; считаем по n_shots.
    """
    V_ideal = np.exp(-kappa_true(eps, b) * n_cycles)
    p = 0.5 * (1.0 + V_ideal)
    hits = rng.binomial(n_shots, p)
    p_hat = hits / n_shots
    return 2.0 * p_hat - 1.0


def estimate_kappa(eps: float, b: float, n_shots: int,
                   rng: np.random.Generator,
                   cycles=(1, 2, 4, 8, 16)) -> tuple[float, float]:
    """Оценка κ_eff при данном ε: взвешенный фит ln V(N) = −κ·N.

    Веса берутся из биномиальной дисперсии измерения (гетероскедастичность):
    Var(V)=4p(1−p)/n_shots, Var(lnV)=Var(V)/V². Это убирает смещение наивного
    МНК по логарифму. Возвращает (κ, σ_κ).
    """
    Ns, lnV, wts = [], [], []
    for N in cycles:
        V = measure_contrast(eps, N, b, n_shots, rng)
        if V > 1e-2:                       # лог определён и устойчив
            p = 0.5 * (1.0 + V)
            var_V = 4.0 * p * (1.0 - p) / n_shots
            var_lnV = var_V / (V * V)
            Ns.append(N)
            lnV.append(np.log(V))
            wts.append(1.0 / max(var_lnV, 1e-12))
    if len(Ns) < 3:
        return float("nan"), float("inf")
    Ns = np.array(Ns, float)
    lnV = np.array(lnV, float)
    w = np.array(wts, float)
    A = np.vstack([Ns, np.ones_like(Ns)]).T
    W = np.diag(w)
    cov = np.linalg.inv(A.T @ W @ A)
    coef = cov @ A.T @ W @ lnV
    kappa = -coef[0]
    sigma_kappa = float(np.sqrt(cov[0, 0]))
    return kappa, sigma_kappa


@dataclass
class ExperimentResult:
    eps_grid: np.ndarray
    kappa: np.ndarray
    sigma: np.ndarray
    a_fit: float
    b_fit: float
    b_err: float
    significance: float    # b_fit / b_err в σ

    def verdict(self) -> str:
        if self.significance >= 5:
            return ("b≠0 на ≥5σ ⇒ память ε — физическая переменная "
                    "(DIALOG подтверждена)")
        if self.significance >= 2:
            return "намёк (2–5σ) ⇒ нужна бо́льшая статистика"
        return "b совместимо с 0 ⇒ DIALOG не подтверждается (стандартная КМ)"


def _one_fit(b_true, n_shots, eps_grid, rng):
    """Один прогон сканирования ε → точечные оценки (a, b, κ(ε), σκ(ε))."""
    kappa = np.zeros(len(eps_grid))
    sigma = np.zeros(len(eps_grid))
    for i, e in enumerate(eps_grid):
        kappa[i], sigma[i] = estimate_kappa(e, b_true, n_shots, rng)
    w = 1.0 / np.maximum(sigma, 1e-9) ** 2
    A = np.vstack([eps_grid, np.ones_like(eps_grid)]).T
    W = np.diag(w)
    cov = np.linalg.inv(A.T @ W @ A)
    coef = cov @ A.T @ W @ kappa
    return coef[1], coef[0], kappa, sigma     # a, b, κ, σκ


def run(b_true: float = B_TRUE_DIALOG, n_shots: int = 8192,
        n_eps: int = 9, seed: int = 0, n_mc: int = 200) -> ExperimentResult:
    """Полный прогон. σ(b) калибруется ЭМПИРИЧЕСКИ по n_mc повторам (Монте-Карло),
    а не из внутренней ковариации одного фита — иначе нуль даёт ложные 5σ.
    """
    rng = np.random.default_rng(seed)
    eps_grid = np.linspace(0.0, C.X_STAR, n_eps)   # 0 … φ−1
    # эталонный прогон (для графика κ(ε))
    a_fit, b_fit, kappa, sigma = _one_fit(b_true, n_shots, eps_grid, rng)
    # эмпирическая дисперсия наклона b при повторении эксперимента
    b_samples = np.array([_one_fit(b_true, n_shots, eps_grid, rng)[1]
                          for _ in range(n_mc)])
    b_err = float(np.std(b_samples, ddof=1))
    sig = abs(b_fit) / b_err if b_err > 0 else 0.0
    return ExperimentResult(eps_grid, kappa, sigma, a_fit, b_fit, b_err, sig)


# --------------------------------------------------------------------------
# Готовая схема Qiskit (запускается на реальном железе, если есть qiskit)
# --------------------------------------------------------------------------
def build_circuit(n_cycles: int, theta: float):
    """Схема Рэмзи с n_cycles циклами памяти. Требует qiskit (опционально)."""
    try:
        from qiskit import QuantumCircuit
    except ImportError as e:                       # pragma: no cover
        raise ImportError(
            "Для реального запуска нужен qiskit: pip install qiskit. "
            "Численная проверка (run()) работает и без него.") from e
    qc = QuantumCircuit(2, 1)        # 0 = система, 1 = регистр-память
    qc.h(0)
    for _ in range(n_cycles):
        qc.crz(theta, 0, 1)          # слабая запись фазы в память
        qc.rz(theta * 0.5, 1)        # эволюция памяти (удержание истории)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def print_report() -> None:
    print("КВАНТОВЫЙ ЭКСПЕРИМЕНТ DIALOG: κ_eff(ε) = a + b·ε")
    print("=" * 64)
    # 1) сценарий «DIALOG верна» (b≠0)
    r1 = run(b_true=B_TRUE_DIALOG, n_shots=8192, seed=1)
    print(f"\nСценарий A — теория верна (b_true={B_TRUE_DIALOG}):")
    print(f"  a={r1.a_fit:.4f}  b={r1.b_fit:.4f} ± {r1.b_err:.4f}  "
          f"⇒ {r1.significance:.1f}σ")
    print(f"  вывод: {r1.verdict()}")
    # 2) нулевой сценарий (b=0)
    r0 = run(b_true=0.0, n_shots=8192, seed=1)
    print(f"\nСценарий B — нулевая гипотеза (b_true=0):")
    print(f"  a={r0.a_fit:.4f}  b={r0.b_fit:.4f} ± {r0.b_err:.4f}  "
          f"⇒ {r0.significance:.1f}σ")
    print(f"  вывод: {r0.verdict()}")
    print("\n" + "=" * 64)
    print("Эксперимент различает две гипотезы ⇒ теория фальсифицируема (Q3).")
    print("На реальном железе: build_circuit(N, θ) → IBM Quantum / Aer.")


if __name__ == "__main__":
    print_report()
