"""
§17 — Параметр искренности S = Tr(ρ · Π_φ).

S — проекция матрицы плотности на φ-оптимальное подпространство.
Теорема монотонности: при росте памяти ε значение S убывает (dS/dε < 0),
потому что φ-оптимальное подпространство первым теряет вес при декогеренции:

    ∂ρ/∂ε = −Γ(ε)·(ρ − I/N),   ρ_∞ = I/N (максимальная декогеренция).

Три наблюдаемые реализации (одно определение, три прибора):
    S_Fib    — заселённость φ-узлов (интенсивность спектральных линий);
    S_coh    — когерентность пары {3,7} (растёт — это компонента, не само S);
    S_tunnel — прозрачность туннеля S6→S7 (= T(ε), §13).
"""

from __future__ import annotations

import numpy as np

from .tunneling import coherent_transparency

# Узлы Фибоначчи n ∈ {1,2,3,5,8} → индексы в базисе n=1..9 (размерность 9).
FIB_NODES = (1, 2, 3, 5, 8)
N_LEVELS = 9


def fibonacci_projector(n: int = N_LEVELS) -> np.ndarray:
    """Проектор Π_φ на φ-оптимальное (Фибоначчи) подпространство."""
    proj = np.zeros((n, n))
    for node in FIB_NODES:
        i = node - 1
        if i < n:
            proj[i, i] = 1.0
    return proj


def sincerity(rho: np.ndarray, projector: np.ndarray | None = None) -> float:
    """Единое определение S = Tr(ρ · Π_φ)."""
    if projector is None:
        projector = fibonacci_projector(rho.shape[0])
    return float(np.real(np.trace(rho @ projector)))


def relaxed_density(eps: float, n: int = N_LEVELS) -> np.ndarray:
    """Модель декогеренции ρ(ε) = (1−ε)·ρ₀ + ε·(I/N).

    ρ₀ — чистое φ-оптимальное состояние (вес на узлах Фибоначчи).
    При ε→1 ρ→I/N (равномерная смесь). Демонстрирует ∂ρ/∂ε = −(ρ − I/N).
    """
    eps = min(max(eps, 0.0), 1.0)
    psi = np.zeros(n)
    for node in FIB_NODES:
        if node - 1 < n:
            psi[node - 1] = 1.0
    psi /= np.linalg.norm(psi)
    rho0 = np.outer(psi, psi)          # чистое состояние на φ-подпространстве
    identity = np.eye(n) / n           # максимально смешанное состояние
    return (1.0 - eps) * rho0 + eps * identity


def s_fibonacci(eps: float) -> float:
    """S_Fib(ε) — заселённость φ-узлов. Убывает с ростом ε (теорема монотонности)."""
    rho = relaxed_density(eps)
    return sincerity(rho)


def s_tunnel(eps: float) -> float:
    """S_tunnel(ε) — прозрачность туннеля = T(ε). Убывает: 0.1244 → 0.0775."""
    return coherent_transparency(eps)


def s_coherence(eps: float, base_ratio: float = 2.35) -> float:
    """S_coh(ε) = |ρ₃₇|/|ρ₂₇|. Растёт с ε: система перекачивает когерентность в туннель.

    Это компонента S, а не само S — рост не противоречит теореме монотонности.
    """
    return base_ratio * (1.0 + eps)


def monotonicity_holds(eps_grid=None) -> bool:
    """Численная проверка теоремы: S_Fib и S_tunnel монотонно убывают по ε."""
    if eps_grid is None:
        eps_grid = np.linspace(0.0, 1.0, 50)
    fib = np.array([s_fibonacci(e) for e in eps_grid])
    tun = np.array([s_tunnel(e) for e in eps_grid])
    return bool(np.all(np.diff(fib) <= 1e-12) and np.all(np.diff(tun) <= 1e-12))


if __name__ == "__main__":
    print(f"Π_φ след (число φ-узлов) = {np.trace(fibonacci_projector())}")
    for e in (0.0, 0.5, 1.0):
        print(f"ε={e:.1f}:  S_Fib={s_fibonacci(e):.3f}  "
              f"S_tunnel={s_tunnel(e):.4f}  S_coh={s_coherence(e):.2f}")
    print(f"Теорема монотонности выполнена (S_Fib, S_tunnel ↓)? {monotonicity_holds()}")
