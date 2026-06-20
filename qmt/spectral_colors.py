"""
Грани → конкретные линии спектра водорода (цвет = реальная частота).

Замыкает слой «грани/краски» на ту же физику, что и узлы: видимая часть спектра
водорода — это РЕАЛЬНЫЕ цвета. Серия Бальмера (n→2) лежит в видимом диапазоне:
    Hα 656 нм (красный) · Hβ 486 нм (голубой) · Hγ 434 нм (синий) · Hδ 410 нм (фиол.)
Значит «краски граней» — не произвольные оттенки, а цвета спектральных линий.

Связь со слоями: переходы модели (sync) дают спектр; его видимая часть = цвета
(faces). Так грани/краски привязаны к водороду так же строго, как узлы.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import hydrogen as H
from . import sync as S

VISIBLE_LO, VISIBLE_HI = 380.0, 750.0   # нм


def wavelength_to_rgb(wl_nm: float):
    """Приближённый цвет (RGB 0–255) для длины волны видимого света."""
    wl = wl_nm
    if wl < VISIBLE_LO or wl > VISIBLE_HI:
        return None
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    return tuple(round(255 * max(0.0, min(1.0, c))) for c in (r, g, b))


@dataclass
class Line:
    name: str
    n_hi: int
    n_lo: int
    wavelength_nm: float
    rgb: tuple


def balmer_visible() -> list[Line]:
    """Серия Бальмера (n→2): видимые линии = реальные цвета."""
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ"}
    out = []
    for n in (3, 4, 5, 6):
        lam = H.transition_wavelength(n, 2) * 1e9
        out.append(Line(names[n], n, 2, round(lam, 1), wavelength_to_rgb(lam)))
    return out


def model_visible_transitions() -> list[dict]:
    """Переходы модели (sync), попадающие в ВИДИМЫЙ диапазон → их цвет."""
    out = []
    for t in S.all_transitions():
        lam = t.wavelength_nm
        rgb = wavelength_to_rgb(lam)
        if rgb is not None:
            out.append({"a": t.a, "b": t.b, "kind": t.kind,
                        "allowed": t.allowed, "λ_нм": round(lam, 1), "rgb": rgb})
    return sorted(out, key=lambda d: d["λ_нм"])


def print_report() -> None:
    print("ГРАНИ → ЛИНИИ СПЕКТРА: цвет = реальная частота водорода")
    print("=" * 64)
    print("Серия Бальмера (n→2) — видимые линии = реальные цвета:")
    for L in balmer_visible():
        print(f"  {L.name} ({L.n_hi}→{L.n_lo}): λ={L.wavelength_nm:6.1f} нм  RGB={L.rgb}")
    print("\nПереходы МОДЕЛИ (sync), видимые глазом, и их цвет:")
    for d in model_visible_transitions():
        mark = "разреш." if d["allowed"] else "запрещ."
        print(f"  {d['a']}↔{d['b']}  {d['kind']:<9} {mark}  "
              f"λ={d['λ_нм']:6.1f} нм  RGB={d['rgb']}")
    print("=" * 64)
    print("Краски граней — не произвольны: это цвета спектральных линий водорода.")
    print("Грани привязаны к водороду так же строго, как узлы и переходы.")


if __name__ == "__main__":
    print_report()
