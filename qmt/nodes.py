"""
§3 — Топология Sum-9: резонансные пары и матрица взаимодействий.

Принцип Sum-9: сумма индексов каждой резонансной пары равна 9.
Пять пар покрывают все 10 узлов S0–S9 без остатка.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import E, PHI, PI

# §3.1 — Пять резонансных пар (A, B, сумма = 9, константа канала).
RESONANCE_PAIRS = [
    (0, 9, "∞", "Вакуум ↔ полный след"),
    (1, 8, "φ", "Оба на Фибоначчи-пути, гармонический резонанс"),
    (2, 7, "e", "Геометрическая симметрия (видимый канал)"),
    (3, 6, "π", "Туннельный канал (невидимый, ИК)"),
    (4, 5, "•", "Наблюдатель ↔ ось (связь, не туннель)"),
]


@dataclass(frozen=True)
class Sum9Check:
    pairs_ok: bool         # все ли пары дают сумму 9
    covers_all: bool       # покрыты ли все узлы 0–9
    pair_count: int        # число пар


def verify_sum9() -> Sum9Check:
    """Проверить топологический инвариант Sum-9."""
    covered = set()
    pairs_ok = True
    for a, b, _const, _desc in RESONANCE_PAIRS:
        if a + b != 9:
            pairs_ok = False
        covered.add(a)
        covered.add(b)
    return Sum9Check(
        pairs_ok=pairs_ok,
        covers_all=covered == set(range(10)),
        pair_count=len(RESONANCE_PAIRS),
    )


# Активное ядро — 7 узлов (S4 ∉ H исключён).
ACTIVE_NODES = [1, 2, 3, 5, 6, 7, 8]


def interaction_matrix_7x7() -> tuple[np.ndarray, list[int]]:
    """§3.3 — Симметричная матрица взаимодействий 7×7 активного ядра.

    Свойства модели:
      * вся строка и столбец узла S5 равны π (универсальный фазовый мост);
      * туннельные элементы M[1,8]=φ, M[2,7]=e, M[3,6]=π.

    Возвращает (матрицу, список индексов узлов-строк).
    """
    idx = ACTIVE_NODES
    pos = {node: i for i, node in enumerate(idx)}
    n = len(idx)
    M = np.zeros((n, n))

    # Ось S5 — фазовый мост: вся строка/столбец = π.
    if 5 in pos:
        M[pos[5], :] = PI
        M[:, pos[5]] = PI

    # Туннельные резонансные элементы Sum-9.
    tunnels = {(1, 8): PHI, (2, 7): E, (3, 6): PI}
    for (a, b), val in tunnels.items():
        if a in pos and b in pos:
            M[pos[a], pos[b]] = val
            M[pos[b], pos[a]] = val

    return M, idx


if __name__ == "__main__":
    chk = verify_sum9()
    print(f"Sum-9: пары=9? {chk.pairs_ok}; покрыты все узлы? {chk.covers_all}; пар: {chk.pair_count}")
    M, idx = interaction_matrix_7x7()
    print(f"Матрица 7×7 симметрична? {np.allclose(M, M.T)}")
    print("Узлы:", idx)
    np.set_printoptions(precision=3, suppress=True)
    print(M)
