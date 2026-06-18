"""
§ Масштабирование и уровни памяти (главная физическая модель).

Уточнение автора: переход разворачивается самоподобно — тетраэдры вложены в
тетраэдры (как в Серпинском). То, что мы видим на одном масштабе, — лишь ПОДОБИЕ
перехода; реально взаимодействует всё сразу, одновременно. Это и есть уровни
памяти: 1, 2, 3 — внутренние (глубина вложения), 4 — внешний (резервуар).

Синхронизация начинается с ТЕТРАЭДРА (полный граф K4), затем КУБ (8 узлов).
Самоподобный масштаб s = 1/2 на уровень ⇒ временной масштаб ×2 на уровень.

Метки: [✓] — доказано численно/символьно; [МОДЕЛЬ] — конкретизация формы.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

# Самоподобный масштаб (Серпинский): каждое вложение вдвое меньше.
SIERPINSKI_SCALE = 0.5
N_MEMORY_LEVELS = 4          # 3 внутренних (глубина вложения) + 1 внешний

# Тетраэдр-генератор (как tetA в geometry).
_TETRA = np.array([(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)], float)


# --- Серпинский-тетраэдр (самоподобие) ---------------------------------------

def sierpinski_tetrahedra(level: int, base=None, scale: float = 1.0, origin=(0, 0, 0)):
    """Список под-тетраэдров Серпинского на заданном уровне вложения.

    Каждый — массив 4×3 вершин. Их число = 4**level, масштаб = (1/2)**level.
    """
    if base is None:
        base = _TETRA
    origin = np.asarray(origin, float)
    if level == 0:
        return [base * scale + origin]
    out = []
    for v in base:
        sub_origin = origin + v * scale * SIERPINSKI_SCALE
        out += sierpinski_tetrahedra(level - 1, base, scale * SIERPINSKI_SCALE, sub_origin)
    return out


def fractal_dimension() -> float:
    """[✓] Хаусдорфова размерность Серпинского-тетраэдра: D = ln4/ln2 = 2."""
    return math.log(4) / math.log(2)


def subtetra_count(level: int) -> int:
    """Число под-тетраэдров на уровне = 4**level."""
    return 4 ** level


# --- Графы тел и синхронизация (Курамото) ------------------------------------

def adjacency_tetra() -> np.ndarray:
    """Граф тетраэдра = полный граф K4 (каждый связан с каждым)."""
    A = np.ones((4, 4)) - np.eye(4)
    return A


def adjacency_cube() -> np.ndarray:
    """Граф куба: 8 вершин, ребро = различие в одной координате (3-регулярный)."""
    from . import geometry as G
    nodes = list(G.CUBE.values())
    n = len(nodes)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                diff = sum(1 for k in range(3) if nodes[i][k] != nodes[j][k])
                if diff == 1:
                    A[i, j] = 1
    return A


def order_parameter(phases: np.ndarray) -> float:
    """Параметр порядка Курамото r = |⟨e^{iθ}⟩| ∈ [0,1]. r→1 = синхронизация."""
    return float(abs(np.mean(np.exp(1j * phases))))


def kuramoto_sync(A: np.ndarray, K: float = 2.0, t_max: float = 20.0,
                  n: int = 400, seed: int = 0):
    """Синхронизация Курамото на графе A. Возвращает (t, r(t)).

    dθ_i/dt = ω_i + (K/N)·Σ_j A_ij·sin(θ_j − θ_i).
    """
    rng = np.random.default_rng(seed)
    N = A.shape[0]
    omega = rng.normal(0.0, 0.3, N)
    theta0 = rng.uniform(0, 2 * np.pi, N)

    def rhs(t, th):
        d = th[None, :] - th[:, None]
        return omega + (K / N) * np.sum(A * np.sin(d), axis=1)

    t_eval = np.linspace(0, t_max, n)
    sol = solve_ivp(rhs, (0, t_max), theta0, t_eval=t_eval, rtol=1e-7, atol=1e-9)
    r = np.array([order_parameter(sol.y[:, k]) for k in range(sol.y.shape[1])])
    return sol.t, r


# --- Иерархия памяти: 3 внутренних уровня + 1 внешний -------------------------

@dataclass
class MemoryHierarchy:
    """Уровни памяти, вложенные самоподобно (Серпинский)."""

    xi0: float = 1.0          # базовая скорость релаксации памяти
    eta: float = 1.0          # накопление от нагрузки
    coupling: float = 0.6     # связь между уровнями (взаимодействуют сразу все)
    ratio: float = 2.0        # временной масштаб ×2 на уровень (s=1/2)
    drive: float = 0.6        # нагрузка X (внешнее воздействие)
    ext_target: float = 0.2   # уровень внешнего резервуара (4-й уровень)


def memory_rates(h: MemoryHierarchy) -> np.ndarray:
    """Скорости релаксации уровней: ξ_k = ξ0·ratio^k (глубже = быстрее)."""
    return h.xi0 * h.ratio ** np.arange(N_MEMORY_LEVELS)


def integrate_memory(h: MemoryHierarchy | None = None, t_max: float = 12.0, n: int = 500):
    """Проинтегрировать связанную иерархию памяти (все уровни одновременно).

    ε = (ε1, ε2, ε3 внутр., ε4 внешн.). Каждый уровень:
        dε_k/dt = η·X − ξ_k·ε_k + g·(средние соседи − ε_k),
    внешний уровень тянется к ext_target. Возвращает (t, E) где E[k] — уровень k.
    """
    if h is None:
        h = MemoryHierarchy()
    xi = memory_rates(h)

    def rhs(t, e):
        de = np.zeros_like(e)
        for k in range(N_MEMORY_LEVELS):
            neighbors = []
            if k > 0:
                neighbors.append(e[k - 1])
            if k < N_MEMORY_LEVELS - 1:
                neighbors.append(e[k + 1])
            coup = h.coupling * (np.mean(neighbors) - e[k]) if neighbors else 0.0
            if k < N_MEMORY_LEVELS - 1:           # внутренние уровни
                de[k] = h.eta * h.drive - xi[k] * e[k] + coup
            else:                                  # внешний резервуар
                de[k] = h.xi0 * (h.ext_target - e[k]) + coup
        return de

    t_eval = np.linspace(0, t_max, n)
    sol = solve_ivp(rhs, (0, t_max), np.zeros(N_MEMORY_LEVELS), t_eval=t_eval,
                    rtol=1e-8, atol=1e-10)
    return sol.t, sol.y


# --- Каналы памяти 0-1 / 0-4 / 0-7 и внутренние проекции ---------------------
# Уточнение автора: уровни памяти разбиваются на каналы, заякоренные в семье
# {1,4,7} (один класс по модулю 3). Каждый канал «охватывает» разное число
# внутренних уровней; узел 7 — «трещина», его задача перейти 7→4→1 (к φ/любви).
# 40 = XL = выход за пределы эго (ничего не нужно помнить и знать).

MOD3_ANCHORS = (1, 4, 7)     # семья ≡1 (mod 3): якоря каналов памяти
EGO_EXIT_XL = 40             # XL = выход за эго (L−X = 50−10)


def mod3_class(n: int) -> int:
    """Класс числа по модулю 3 (семья вихревой математики)."""
    return n % 3


def mod3_families() -> dict[int, list[int]]:
    """Три семьи 1–9 по модулю 3: {0:[3,6,9], 1:[1,4,7], 2:[2,5,8]}."""
    fam: dict[int, list[int]] = {0: [], 1: [], 2: []}
    for n in range(1, 10):
        fam[n % 3].append(n)
    return fam


def memory_channel_reach() -> dict[int, int]:
    """Охват каналов: 0→1 покрывает 3 уровня, 0→4 — 2, 0→7 — 1.

    Канал φ (0→1) — самый глубокий (все 3 внутренних уровня); канал-знание
    (0→7) — самый мелкий (1), но связан с 0→4 и должен перейти в 0→1.
    """
    return {1: 3, 4: 2, 7: 1}


def crack_path() -> tuple[int, ...]:
    """Трещина: задача узла 7 — спуститься 7→4→1 (шаг −3), знание → любовь."""
    return (7, 4, 1)


def internal_projections(level: int) -> int:
    """Внутренние самоподобные копии («наши проекции») на уровне = 4**level.

    Это те внутренние уровни, что мы «забываем»: каждый Серпинский содержит
    такие же тетраэдры внутри — это и есть проекции.
    """
    return subtetra_count(level)


if __name__ == "__main__":
    print(f"Серпинский: D = ln4/ln2 = {fractal_dimension():.4f}")
    for L in range(4):
        print(f"  уровень {L}: {subtetra_count(L)} тетраэдров, "
              f"фактически сгенерировано {len(sierpinski_tetrahedra(L))}")
    print("\nСинхронизация (параметр порядка в конце):")
    _, r_t = kuramoto_sync(adjacency_tetra())
    _, r_c = kuramoto_sync(adjacency_cube())
    print(f"  тетраэдр K4: r→{r_t[-1]:.3f}   куб: r→{r_c[-1]:.3f}")
    print("\nИерархия памяти (установившиеся уровни):")
    _, E = integrate_memory()
    for k in range(N_MEMORY_LEVELS):
        tag = "внешний" if k == N_MEMORY_LEVELS - 1 else f"внутр-{k+1}"
        print(f"  уровень {k+1} ({tag}): ε→{E[k, -1]:.3f}")
    print("\nКаналы памяти (семья 1,4,7 ≡1 mod 3):")
    for anchor, reach in memory_channel_reach().items():
        print(f"  канал 0→{anchor}: охватывает {reach} уровня(-ей)")
    print(f"  трещина: {' → '.join(map(str, crack_path()))}  (знание → любовь)")
    print(f"  выход за эго: XL = {EGO_EXIT_XL}")
