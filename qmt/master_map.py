"""
МАСТЕР-КАРТА — сведение всех слоёв в ОДНУ геометрию узлов и переходов,
синхронизированную с квантовой динамикой атома водорода (как куб Метатрона:
одна фигура держит всё).

Идея: у каждого узла 0–9 — единое «досье» из всех слоёв (число, уровень
водорода, буква-триада, канал памяти, римское, цвет/роль), а переходы между
узлами классифицированы геометрией куба и дают РЕАЛЬНЫЕ линии водорода.
Всё висит на одной структуре: вершины куба (1–9 без 5) + центр 5 + оболочка 0.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import hydrogen as H
from . import roman as R
from . import scaling as SC
from . import sync as S
from . import letters as L

# Буквы-триада на узлах-каналах (ведущая читка из semantic_audit).
TRIAD_NODE = {1: "А", 4: "Д", 7: "Л"}
REACH = SC.memory_channel_reach()                      # {1:3, 4:2, 7:1}


@dataclass
class Node:
    n: int
    role: str
    E_eV: float                      # уровень водорода E_n = −13.6/n²
    letter: str = ""                 # буква-триада (1/4/7)
    channel_reach: int = 0           # охват канала памяти (1/4/7)
    roman: str = ""
    note: str = ""


def node_dossier(n: int) -> Node:
    """Единое досье узла из всех слоёв."""
    if n == S.SHELL:                                   # 0
        return Node(0, "оболочка / внешний 0", 0.0, roman="",
                    note="вакуум, ионизация n→∞; целое за кругом (источник шёпота)")
    if n == S.CENTER:                                  # 5
        return Node(5, "центр / внутренний 0", H.energy_level(5),
                    roman=R.to_roman(5),
                    note="зеркало −I, ψ(0)≠0; V=чаша-оценка, точка выбора")
    letter = TRIAD_NODE.get(n, "")
    reach = REACH.get(n, 0)
    role = "канал памяти (триада)" if n in TRIAD_NODE else "узел-состояние (вершина)"
    note = ""
    if n in TRIAD_NODE:
        note = {1: "всеобъемлющая память (0→1)",
                4: "туннель Д (0→4); IV; через 4 идёт шёпот",
                7: "ограниченная память (0→7); трещина 7→4→1"}[n]
    if n == 6:
        note = "VI — «число Дьявола» (мнимое всезнание)"
    return Node(n, role, H.energy_level(n), letter=letter,
                channel_reach=reach, roman=R.to_roman(n), note=note)


def all_nodes() -> list[Node]:
    return [node_dossier(n) for n in range(10)]


# --- Проверки правильности (что всё сходится на одной геометрии) -----------
def verify() -> dict:
    """Сводные проверки: водород, триада, каналы, переходы."""
    lines = {(1, 2): 121.6, (2, 7): 397.0, (3, 7): 1005.0}   # реперные линии
    line_ok = {}
    for t in S.allowed_transitions():
        key = (min(t.a, t.b), max(t.a, t.b))
        if key in lines:
            line_ok[key] = abs(t.wavelength_nm - lines[key]) / lines[key] < 0.01
    cnt = S.selection_counts()
    return {
        "узлов_всего": len(all_nodes()),
        "вершин": len(S.VERTICES),
        "линии_водорода_сходятся": all(line_ok.values()) and len(line_ok) == 3,
        "триада_1_4_7_вершины": all(n in S.VERTICES for n in TRIAD_NODE),
        "триада_каналы": set(TRIAD_NODE) == set(SC.MOD3_ANCHORS),
        "переходы": cnt,
        "разрешено": cnt["прямой"] + cnt["резонанс"] + cnt["зеркало"],
        "запрещено": cnt["запрещён"],
        "трещина_7_4_1": tuple(SC.crack_path()) == (7, 4, 1),
    }


def print_report() -> None:
    print("МАСТЕР-КАРТА — все слои на одной геометрии ↔ водород")
    print("=" * 72)
    print(f"{'n':>2} {'роль':<26} {'E_n,эВ':>8} {'бкв':>3} {'охв':>3} "
          f"{'рим':>4}  заметка")
    for nd in all_nodes():
        print(f"{nd.n:>2} {nd.role:<26} {nd.E_eV:>8.3f} {nd.letter:>3} "
              f"{nd.channel_reach or '':>3} {nd.roman:>4}  {nd.note}")
    v = verify()
    print("\nПРОВЕРКИ:")
    for k in ("линии_водорода_сходятся", "триада_1_4_7_вершины", "триада_каналы",
              "трещина_7_4_1"):
        print(f"  [{'✓' if v[k] else '✗'}] {k}")
    print(f"  переходы: разрешено {v['разрешено']} / запрещено {v['запрещено']} "
          f"({v['переходы']})")
    print("=" * 72)
    print("Всё на одной фигуре: вершины 1–9 (без 5) + центр 5 + оболочка 0;")
    print("переходы дают реальные линии водорода (1↔2 Лайман α, 2↔7, 3↔7).")


if __name__ == "__main__":
    print_report()
