"""
═══════════════════════════════════════════════════════════════════════════
  HYDROGEN_TEMPERATURE — у каждого узла (уровня n) есть своя температура.
═══════════════════════════════════════════════════════════════════════════

«Точная температура на каждом повороте реально существует.» Да — но честно:
это точка ВСТРЕЧИ узла и среды, а не чистая константа атома.

Механизм: видимость линии серии, стартующей с уровня n, есть произведение
  • Больцмана  — заселён ли нижний уровень n (∝ 2n²·exp(−E_n/kT)), и
  • Саха       — не ионизован ли ещё атом (нейтральная доля падает с T).
Произведение имеет ПИК при некоторой T_n — «температура максимальной видимости».

✓ ЧТО ВШИТО В АТОМ (не зависит от среды) — ФОРМА кривой:
  • пик существует (не монотонна): холодно — нет заселения, горячо — ионизация;
  • пик АСИММЕТРИЧЕН (смещён от середины полумаксимумов) — «середина ложна»;
  • T_n РАСТЁТ с n и СХОДИТСЯ к пределу ионизации (шаги сжимаются);
  • ~9000 К для Бальмера = реальный «бальмеровский максимум» звёзд класса A.

⚠️ ЧТО ЗАДАЁТ МИР (не атом): АБСОЛЮТНОЕ значение T_n зависит от электронной
  плотности n_e (давления плазмы). n_e=10¹⁹→T₂≈8.6кК; 10²⁰→9.8кК; 10²¹→11.2кК.
  Поэтому T_n подаём как «узел × среда» (Больцман×Саха), не как число атома.

✓ ДОПЛЕР: тепловой хаос скоростей размывает линию, Δλ ∝ √T. Своя скорость у
  каждого атома → размытие перехода. Hα: 3000 К→25.6 пм, 30000 К→81.1 пм.
  Незнание точной T на повороте = буквально уширение линии (менее точная геометрия).

Запуск:  python -m qmt.hydrogen_temperature
"""

from __future__ import annotations

import math

K_B = 1.380649e-23        # Дж/К
H_PL = 6.62607015e-34
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
EV = 1.602176634e-19
C = 2.99792458e8
CHI_H = 13.6 * EV         # энергия ионизации водорода


def neutral_fraction(T: float, n_e: float) -> float:
    """Доля нейтрального H (уравнение Саха): падает с T (ионизация)."""
    U_I, U_II = 2.0, 1.0
    fac = (2 * U_II / U_I) * (2 * math.pi * M_E * K_B * T / H_PL**2) ** 1.5 \
        * math.exp(-CHI_H / (K_B * T))
    ratio_II_over_I = fac / n_e
    return 1.0 / (1.0 + ratio_II_over_I)


def level_fraction(T: float, n: int) -> float:
    """Доля нейтральных атомов на уровне n (Больцман), E_n=13.6(1−1/n²)."""
    g = 2 * n * n
    E_n = 13.6 * (1 - 1 / n**2) * EV
    return g * math.exp(-E_n / (K_B * T)) / 2.0


def visibility(T: float, n: int, n_e: float = 1e19) -> float:
    """Видимость серии с уровня n = Больцман × Саха (имеет пик по T)."""
    return neutral_fraction(T, n_e) * level_fraction(T, n)


def peak_temperature(n: int, n_e: float = 1e19,
                     lo: float = 2000.0, hi: float = 40000.0) -> float:
    """T_n — температура максимальной видимости узла n (аргмаксимум по T)."""
    best_T, best_v = lo, -1.0
    T = lo
    while T <= hi:
        v = visibility(T, n, n_e)
        if v > best_v:
            best_v, best_T = v, T
        T += 1.0
    return best_T


def node_temperatures(n_e: float = 1e19) -> dict:
    """Карта T_n для узлов n=2..7 (серии Бальмер…)."""
    return {n: peak_temperature(n, n_e) for n in range(2, 8)}


def temperatures_increase_and_converge(n_e: float = 1e19) -> bool:
    """✓ ФОРМА: T_n растёт с n, а шаги сжимаются (сходимость к ионизации)."""
    T = node_temperatures(n_e)
    ns = sorted(T)
    vals = [T[n] for n in ns]
    increasing = all(vals[i + 1] > vals[i] for i in range(len(vals) - 1))
    steps = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    converging = all(steps[i + 1] < steps[i] for i in range(len(steps) - 1))
    return increasing and converging


def doppler_width(T: float, lam: float = 656.3e-9, mass: float = M_P) -> float:
    """Тепловое доплеровское уширение (FWHM), Δλ = (λ/c)·√(8ln2·kT/m) ∝ √T."""
    return (lam / C) * math.sqrt(8 * math.log(2) * K_B * T / mass)


def _half_crossing(n: int, n_e: float, lo: float, hi: float, target: float) -> float:
    """Бисекция точки, где visibility = target на монотонном отрезке [lo,hi]."""
    v_lo = visibility(lo, n, n_e)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        v_mid = visibility(mid, n, n_e)
        # держим target между концами по знаку разности с v_lo
        if (v_mid - target) * (v_lo - target) <= 0:
            hi = mid
        else:
            lo, v_lo = mid, v_mid
    return 0.5 * (lo + hi)


def peak_is_asymmetric(n: int = 2, n_e: float = 1e19) -> bool:
    """✓ «Середина ложна»: пик смещён от середины полумаксимумов (FWHM)."""
    Tp = peak_temperature(n, n_e)
    vmax = visibility(Tp, n, n_e)
    left = _half_crossing(n, n_e, 2000.0, Tp, vmax / 2)        # возрастающая ветвь
    right = _half_crossing(n, n_e, 40000.0, Tp, vmax / 2)      # убывающая ветвь
    mid_of_fwhm = 0.5 * (left + right)
    return abs(Tp - mid_of_fwhm) > 50.0    # пик заметно смещён от середины


def print_report() -> None:
    print("═" * 74)
    print("  ТЕМПЕРАТУРА ВОДОРОДА ПО УЗЛАМ: Больцман × Саха (узел × среда)")
    print("═" * 74)
    series = {2: "Бальмер(видимый)", 3: "Пашен(ИК)", 4: "Брэкет",
              5: "Пфунд", 6: "Хамфрис", 7: "n=7"}
    print("\n  ✓ ФОРМА (вшита в атом) при n_e=10¹⁹ м⁻³:")
    T = node_temperatures(1e19)
    prev = None
    for n in range(2, 8):
        step = f"  (+{T[n]-prev:.0f})" if prev else ""
        print(f"     узел {n} · {series[n]:16} T_n = {T[n]:6.0f} К{step}")
        prev = T[n]
    print(f"     растёт и сходится: {temperatures_increase_and_converge()}"
          f"  ·  пик асимметричен: {peak_is_asymmetric()}")

    print("\n  ⚠️ АБСОЛЮТ задаёт МИР (n_e), не атом:")
    for ne in (1e19, 1e20, 1e21):
        Tne = node_temperatures(ne)
        print(f"     n_e={ne:.0e}: T₂={Tne[2]:.0f} К … T₇={Tne[7]:.0f} К")

    print("\n  ✓ ДОПЛЕР (Δλ ∝ √T): точная T теряется в хаосе скоростей →")
    for Tk in (3000, 30000):
        print(f"     Hα при {Tk:5} К: Δλ = {doppler_width(Tk)/1e-12:5.1f} пм")
    print(f"     √(30000/3000)=√10≈3.16 → 25.6·3.16≈81 пм ✓ (незнание T = уширение)")
    print("═" * 74)
    print("  Реально: ФОРМА T_n(рост, сходимость, ~9кК бальмер-макс, асимметрия) —")
    print("  атомная; АБСОЛЮТ — от среды (n_e). Доплер ∝√T. T_n = узел×мир.")
    print("═" * 74)


if __name__ == "__main__":
    print_report()
