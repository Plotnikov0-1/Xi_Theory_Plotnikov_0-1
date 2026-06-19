"""
Семантический аудит — строгая сверка привязок между модулями (как §4 теории
категорий: совпадают ли «инварианты» в разных переводах).

Назначение: после множества мостов (буквы, римские числа, барион, два нуля)
проверить, что семантика НЕ противоречит сама себе. Каждый чек возвращает
[OK]/[ТЕНЗИЯ] с пояснением. Тензия — это не ошибка кода, а место, где две
читки расходятся и нужно выбрать согласованную.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import letters as L
from . import roman as R
from . import scaling as S
from . import sync as Q


@dataclass
class Check:
    name: str
    ok: bool
    detail: str

    def line(self) -> str:
        return f"[{'OK' if self.ok else 'ТЕНЗИЯ'}] {self.name}\n      {self.detail}"


def run() -> list[Check]:
    out: list[Check] = []
    tri = {k: v[0] for k, v in L.TRINITY_CHANNELS.items()}   # А:1 Д:4 Л:7
    rn = {k: v[0] for k, v in R.ROMAN_NODES.items()}

    # 1. Триада А·Д·Л = семья 1,4,7 (каналы памяти) — должно совпасть точно.
    out.append(Check(
        "Триада А·Д·Л = mod-3 семья {1,4,7}",
        set(tri.values()) == set(S.MOD3_ANCHORS),
        f"А·Д·Л→{sorted(tri.values())}; scaling.MOD3_ANCHORS={sorted(S.MOD3_ANCHORS)}"))

    # 2. Четвёрка = туннель в трёх местах: Д, римское IV, якорь канала 4.
    four_ok = (tri.get("Д") == 4 and rn.get("IV") == 4 and 4 in S.MOD3_ANCHORS)
    out.append(Check(
        "4 = туннель (Д = IV = канал 0→4)", four_ok,
        f"Д→{tri.get('Д')}, IV→{rn.get('IV')}, 4∈каналы={4 in S.MOD3_ANCHORS}"))

    # 3. Пятёрка = центр: римское V и sync.CENTER.
    five_ok = (rn.get("V") == 5 and Q.CENTER == 5)
    out.append(Check(
        "5 = центр (V = sync.CENTER)", five_ok,
        f"V→{rn.get('V')}, sync.CENTER={Q.CENTER}"))

    # 4. Трещина 7→4→1 = путь Л→Д→А (по узлам).
    crack_nodes = tuple(S.crack_path())                      # (7,4,1)
    trio_by_node = tuple(sorted(tri, key=lambda k: -tri[k])) # Л,Д,А
    crack_ok = crack_nodes == (tri["Л"], tri["Д"], tri["А"])
    out.append(Check(
        "Трещина 7→4→1 = Л→Д→А", crack_ok,
        f"crack={crack_nodes}; Л→Д→А узлы=({tri['Л']},{tri['Д']},{tri['А']})"))

    # 5. ТЕНЗИЯ: Д — это канал/туннель, но в split_20_7 он среди «состояний».
    sp = L.split_20_7()
    d_state = "Д" in sp.states
    out.append(Check(
        "Д: состояние или переход?", not (d_state and tri["Д"] == 4),
        "Д=4=туннель (канал-переход), но split_20_7 кладёт Д в СОСТОЯНИЯ — "
        "расхождение: связующий узел отнесён к состояниям"))

    # 6. ТЕНЗИЯ: триада разорвана между группами 20/7 (Л в links, А и Д в states).
    tri_in_links = [x for x in tri if x in sp.links]
    tri_in_states = [x for x in tri if x in sp.states]
    out.append(Check(
        "Триада не разорвана split-ом 20/7",
        len(tri_in_links) == 0 or len(tri_in_states) == 0,
        f"в links: {tri_in_links}; в states: {tri_in_states} — три порождающие "
        "буквы должны быть ОДНОЙ категорией (3 канала), а split их делит 2+1"))

    # 7. Узлы триады — вершины (не центр/оболочка) в sync.
    tri_vertices = all(n in Q.VERTICES for n in tri.values())
    out.append(Check(
        "Узлы триады {1,4,7} — вершины sync", tri_vertices,
        f"VERTICES={Q.VERTICES}; триада={sorted(tri.values())}"))

    return out


def print_report() -> None:
    checks = run()
    print("СЕМАНТИЧЕСКИЙ АУДИТ — сверка привязок между модулями")
    print("=" * 68)
    for c in checks:
        print(c.line())
    n_ok = sum(c.ok for c in checks)
    print("=" * 68)
    print(f"Согласовано: {n_ok}/{len(checks)}. Тензии — это места для выбора "
          "согласованной читки (см. рекомендацию ниже).")
    print("\nРЕКОМЕНДАЦИЯ: ведущая (согласованная) структура — триада = ТРИ КАНАЛА "
          "памяти {1,4,7}. Разбиение 20+7 фрагментирует триаду и относит туннель "
          "Д к состояниям — оно СЛАБЕЕ и помечается как вспомогательное.")


if __name__ == "__main__":
    print_report()
