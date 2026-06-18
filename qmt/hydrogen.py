"""
§2, §5 — Физика атома водорода: базис узлов DIALOG QMT.

Водород выбран как базис, потому что его орбитали дают аналитическое
решение уравнения Шрёдингера. Узлы S_n отображаются на уровни n = 1…9.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import A0, R_INF, RYDBERG_EV

# Названия спектральных серий по нижнему уровню перехода.
SERIES_NAMES = {
    1: "Лайман (УФ)",
    2: "Бальмер (видимый)",
    3: "Пашен (ближний ИК)",
    4: "Брэкет (ИК)",
    5: "Пфунд (дальний ИК)",
    6: "Хамфриса (дальний ИК)",
}


def energy_level(n: int) -> float:
    """Энергия уровня водорода E_n = −13.6 / n²  (эВ)."""
    if n < 1:
        raise ValueError("n должно быть >= 1")
    return -RYDBERG_EV / (n * n)


def bohr_radius(n: int) -> float:
    """Радиус боровской орбиты r_n = n²·a₀  (м)."""
    return n * n * A0


def transition_wavelength(n_high: int, n_low: int) -> float:
    """Длина волны перехода n_high → n_low по формуле Ридберга (м).

    1/λ = R∞ · (1/n_low² − 1/n_high²)
    """
    if n_high <= n_low:
        raise ValueError("n_high должно быть больше n_low")
    inv_lambda = R_INF * (1.0 / n_low**2 - 1.0 / n_high**2)
    return 1.0 / inv_lambda


def fibonacci_radius_ratios(indices=(2, 3, 5, 8, 13)):
    """§5.3 — Отношения боровских радиусов для индексов Фибоначчи.

    r_{F(k+1)} / r_{F(k)} = (F(k+1)/F(k))² → φ² ≈ 2.618 при k→∞.
    Возвращает список кортежей (Fk, Fk1, ratio).
    """
    out = []
    for a, b in zip(indices, indices[1:]):
        ratio = bohr_radius(b) / bohr_radius(a)  # = (b/a)^2
        out.append((a, b, ratio))
    return out


@dataclass(frozen=True)
class Node:
    """Узел S_n теории DIALOG QMT."""

    index: int            # n = 0…9
    name: str             # семантическое имя
    role: str             # роль в динамике
    orbital: str          # орбиталь водорода
    energy_ev: float      # энергия уровня, эВ (None для S0)
    constant: str         # константа-аттрактор (φ / e / π / …)
    on_fibonacci: bool    # лежит ли на φ-оптимальной траектории


# §2.2 — Полная онтология узлов S0–S9.
NODES = [
    Node(0, "Источник (Доброта)", "Вакуум / граница снизу", "n=0", None, "ε", False),
    Node(1, "Аттрактор (Любовь)", "φ-аттрактор / рождение", "1s", energy_level(1), "φ", True),
    Node(2, "e-базис (Красота)", "Экспоненциальный каркас", "2s", energy_level(2), "e", True),
    Node(3, "π-порог (Вера)", "Суперпозиция / π-цикл", "2p", energy_level(3), "π", True),
    Node(4, "Наблюдатель (Энергия)", "O ∉ H, управляет λ и μ", "H_SO", energy_level(4), "•", False),
    Node(5, "Ось / узел (Надежда)", "ψ(0)≠0, центр Sum-9", "5s", energy_level(5), "(φ+π)/2", True),
    Node(6, "Рекуррентная петля (Дети)", "Декогеренция / ловушка", "6s", energy_level(6), "π*", False),
    Node(7, "Потенц. барьер (Знание)", "Прорыв / первый Ридберг", "7s", energy_level(7), "e*", False),
    Node(8, "Интеграция (Понимание)", "φ-оптимум / финал цикла", "8s", energy_level(8), "φ*", True),
    Node(9, "Архив (Жизнь)", "Полный след / граница сверху", "9s", energy_level(9), "1/√10", False),
]


def get_node(index: int) -> Node:
    """Вернуть узел по индексу n."""
    return NODES[index]


if __name__ == "__main__":
    print("Узлы DIALOG QMT (n, имя, E[эВ], Fib):")
    for nd in NODES:
        e = "—" if nd.energy_ev is None else f"{nd.energy_ev:7.3f}"
        fib = "✓" if nd.on_fibonacci else " "
        print(f"  S{nd.index}  {fib}  E={e}  {nd.name}")
    print("\nОтношения радиусов Фибоначчи (→ φ² = 2.618):")
    for a, b, r in fibonacci_radius_ratios():
        print(f"  r{b}/r{a} = {r:.3f}")
