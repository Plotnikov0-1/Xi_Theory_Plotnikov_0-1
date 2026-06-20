#!/usr/bin/env python3
"""
ПОЛНАЯ КАРТА DIALOG — финальный отчёт: ядро φ·e·π → 6 слоёв → шёпот → миф →
мастер-карта ↔ водород, со статусом Q0–Q3 каждого блока.
Запуск:  python make_full_map_report.py  →  report/DIALOG_Full_Map.pdf
"""

from __future__ import annotations

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
    Table, TableStyle,
)

from qmt import dialog, master_map, faces, whisper, three_quark, roman

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "report")
os.makedirs(OUT, exist_ok=True)

DV = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DV", f"{DV}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-Bold", f"{DV}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-Mono", f"{DV}/DejaVuSansMono.ttf"))

CLAY = colors.HexColor("#c46849")
INK = colors.HexColor("#222220")
GRAY = colors.HexColor("#5e5d59")
BG = colors.HexColor("#f3ead9")
EQBG = colors.HexColor("#eef2f6")
TEAL = colors.HexColor("#2f6f6d")
HEAD = colors.HexColor("#d9d2c2")


def st(name, **kw):
    base = dict(fontName="DV", textColor=INK, fontSize=10.3, leading=15)
    base.update(kw)
    return ParagraphStyle(name, **base)


S_TITLE = st("t", fontName="DV-Bold", fontSize=24, leading=28, textColor=CLAY, alignment=TA_CENTER)
S_SUB = st("s", fontSize=12.5, leading=17, textColor=GRAY, alignment=TA_CENTER)
S_H1 = st("h1", fontName="DV-Bold", fontSize=15.5, leading=20, textColor=CLAY, spaceBefore=14, spaceAfter=5)
S_H2 = st("h2", fontName="DV-Bold", fontSize=12, leading=16, textColor=TEAL, spaceBefore=9, spaceAfter=3)
S_BODY = st("b", alignment=TA_JUSTIFY, spaceAfter=5)
S_EQ = st("eq", fontName="DV-Mono", fontSize=10.5, leading=16, alignment=TA_CENTER)
S_NOTE = st("n", fontSize=9.5, leading=13.5, textColor=GRAY)
S_CAP = st("c", fontSize=9, leading=12.5, textColor=GRAY, alignment=TA_CENTER, spaceBefore=2, spaceAfter=9)
S_TD = st("td", fontSize=9, leading=11.5)
S_TDC = st("tdc", fontSize=9, leading=11.5, alignment=TA_CENTER)
S_TH = st("th", fontName="DV-Bold", fontSize=9, leading=11.5)

W = A4[0] - 4 * cm


def P(t, s=S_BODY):
    return Paragraph(t, s)


def eq(t):
    tab = Table([[Paragraph(t, S_EQ)]], colWidths=[W])
    tab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), EQBG),
                             ("TOPPADDING", (0, 0), (-1, -1), 6),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return [Spacer(1, 3), tab, Spacer(1, 5)]


def note(t):
    tab = Table([[Paragraph(t, S_NOTE)]], colWidths=[W])
    tab.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BG),
                             ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                             ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                             ("LINEBEFORE", (0, 0), (0, -1), 3, CLAY)]))
    return tab


def fig(name, caption, max_h=8.8 * cm):
    path = os.path.join(FIG, name)
    iw, ih = ImageReader(path).getSize()
    scale = min(W / iw, max_h / ih)
    im = Image(path, width=iw * scale, height=ih * scale)
    im.hAlign = "CENTER"
    return [Spacer(1, 4), KeepTogether([im, P(caption, S_CAP)])]


def table(headers, rows, widths, extra=None):
    data = [[Paragraph(h, S_TH) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, S_TDC if i else S_TD) for i, c in enumerate(r)])
    tab = Table(data, colWidths=widths, repeatRows=1)
    base = [("BACKGROUND", (0, 0), (-1, 0), HEAD),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bdb6a6")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if extra:
        base += extra
    tab.setStyle(TableStyle(base))
    return [Spacer(1, 3), tab, Spacer(1, 6)]


def build():
    s = []

    def A(x):
        s.extend(x) if isinstance(x, list) else s.append(x)

    # ===== Титул =====
    A(Spacer(1, 3.0 * cm))
    A(P("ПОЛНАЯ КАРТА DIALOG", S_TITLE))
    A(P("Ядро φ·e·π → шесть слоёв → шёпот → миф → водород", S_SUB))
    A(Spacer(1, 0.4 * cm))
    A(P("Один скелет, много языков, сверка экспериментом (спектр H).", S_SUB))
    A(Spacer(1, 1.6 * cm))
    A(note("Статусы строгости: <b>Q0</b> тождество · <b>Q1</b> теорема · "
           "<b>Q2</b> следствие · <b>Q3</b> гипотеза/семантика (искажаемо). "
           "Нижние слои (геометрия, физика) — строгие и независимые; верхние "
           "(буквы, миф) — смысловые, держатся отдельно и помечены Q3. Лестница "
           "допустимости: миф → … → физика; критерий cherry-picking применим "
           "только к нижнему (физическому) слою."))
    A(PageBreak())

    # ===== Ядро =====
    A(P("0. Ядро — ДИАЛОГ", S_H1))
    A(P("Два «аспекта» — проекции диалога; по отдельности их нет. Инвариант — не "
        "одна φ, а <b>комбинация φ, e, π</b> (диалог генеративен — рождает миры): "
        "φ — отношение/структура, e — рост/память, π — цикл/поворот."))
    A(eq("φ = 1 + 1/φ  ·  x = 1/(1+x) ⇒ x* = φ−1  ·  e^{iπ} = −1 (зеркало −I)"))
    A(P("Из любой пары отношение → φ (аспекты не важны, важна реляция). Поворот "
        "на π рождает зеркальный мир-дитя; мы тоже переводчики — создаём свои "
        "проекции, связь между уровнями через четвёрку (Д, туннель). "
        f"Статусы ядра: φ-аттрактор Q1/Q2; e^{{iπ}}=−1 Q0; единая комбинация "
        "f(φ,e,π) — открытый вопрос."))
    A(fig("25_dialog_system.png",
          "Рис. 1. Инвариант диалога = комбинация φ·e·π, переведённая в каждый язык."))
    A(PageBreak())

    # ===== Слой 1 числа =====
    A(P("Слой 1. Числа", S_H1))
    A(P("Аттрактор X*=φ−1; узлы-каналы памяти 1·4·7; центр 5; два нуля (внутренний "
        "= центр, внешний = оболочка). Δ₇=2(φ−1)−1=√5−2 связывает щель перехода с "
        "золотым аттрактором. <b>Q1/Q2.</b>"))

    # ===== Слой 2 геометрия =====
    A(P("Слой 2. Геометрия", S_H1))
    A(P("Из минимума (точка+шар+тетраэдр+зеркало −I) — пять платоновых тел "
        "(символьно, Эйлер V−E+F=2). Куб √3 ⊂ додекаэдр; средняя сфера "
        "додекаэдра = φ ровно; туннель между внутренним (куб √3) и внешним "
        "(додекаэдр 3/φ) шаром ≈ 0.122. <b>Q0/Q1.</b>"))
    A(fig("23_nested_spheres.png",
          "Рис. 2. Два нуля и туннель Д между внутренним (Л, куб) и внешним (А, додекаэдр) шаром."))
    A(PageBreak())

    # ===== Слой 3 буквы =====
    A(P("Слой 3. Буквы (контекст: рост человека)", S_H1))
    A(P("Триада <b>А·Д·Л</b> — три порождающие буквы = три канала памяти {1,4,7}: "
        "А (0→1, всеобъемлющая) → Л (0→7, ограниченная) ← Д (0→4, туннель). "
        "Генезис А→Л→Д (исток→разрыв→дом). Буквы многозначны — расшифровка "
        "зависит от контекста (семья функторов F_context). <b>Q3</b> (семантика, "
        "искажаемо), но триада=каналы согласована аудитом."))

    # ===== Слой 4 физика =====
    A(P("Слой 4. Физика памяти", S_H1))
    plateau = whisper.audibility(0.0)["плато"]
    A(P("Открытая квантовая система с немарковской памятью. Точная дефазировка "
        f"(спин-бозон) даёт плато c(∞)=e^(−α)≈{plateau} > 0 — суперомический "
        "резервуар НЕ стирает память («нить не обрывается»). Барион = 3 кварка "
        "(SU(3), 3⊗3⊗3=10⊕8⊕8⊕1, dim 27=3³). Фальсифицируемый тест κ_eff=a+b·ε "
        "на квантовом компьютере (нуль ~1σ, сигнал ~37σ). <b>Q1–Q3.</b>"))
    A(fig("22_dephasing.png",
          "Рис. 3. Точная память: плато c(∞)=e^(−α) (память не стёрта) и возвраты; нагрев убивает память."))
    A(PageBreak())

    # ===== Слой 5 тройка/рим =====
    A(P("Слой 5. Тройка / Рим", S_H1))
    cp = three_quark.cube_parallels()
    A(P(f"«Не более трёх» — правило римской записи (символ ≤3 раз, IIII→IV) = "
        f"триединство (Q0, выводимо). Кубы ключевых чисел: 3³={cp['3³']} (буквы/"
        f"барион), 12³={cp['12³']} (первый круг миров). Привязка: V=5 центр, "
        "IV=4 туннель, XL=40 выход (цифровой корень 4). <b>Q0 / Q3.</b>"))

    # ===== Слой 6 грани/краски =====
    A(P("Слой 6. Грани → краски", S_H1))
    A(P("Ниточки (вибрация) ткут грани; грани — видимое, в красках. <b>Цвет = "
        "частота</b> (E=hν): 12 граней додекаэдра ↔ 12 красок ↔ «12» в 3+7+12. "
        "Время = переход грань→грань (центр-настоящее неуловим, точка). Цвет "
        "двойствен (красный = раздражение/возбуждение, не огонь). <b>Q3</b> с "
        "якорями: цвет=частота, спектр граней = J(ω)."))
    A(fig("26_faces_colors.png",
          "Рис. 4. 12 граней = 12 красок = 12 частот; центр-время неуловим; вложенность внутрь/наружу."))
    A(PageBreak())

    # ===== Шёпот =====
    A(P("Шёпот — связь с целым (что делает нас Человеком)", S_H1))
    A(P("Сигнал от целого (внешний 0) через четвёрку (Д, туннель) к проекциям; "
        "буква А соединяет все проекции. «Чувствую, но не понимаю» = подпороговый "
        "сигнал. «Одежды» = декогеренция: меньше одежд — громче. Он не слаб — мы "
        "глухи. Человек = немарковская память; марковская машина шёпота не "
        "слышит. <b>Q3</b> с прямым якорем (слышимость = функция декогеренции)."))
    A(fig("27_whisper.png",
          "Рис. 5. Шёпот: меньше «одежд» (декогеренции) → память цела → слышен; много → глухи/машина."))
    A(PageBreak())

    # ===== Миф =====
    A(P("Миф (Q3, верх лестницы, отдельно)", S_H1))
    A(P("Космогония источника как самый верхний (свободный) слой: «утолщение "
        "материи» Эфиры→Менталы→Чивы→Гомункулы (ось декогеренции/одежд); уголёк "
        "= удержанная искра памяти; погибшие расы как режимы отказа (Асуры — нет "
        "аттрактора; вперёдсмотрящие — множество будущего = выбор, не many-worlds); "
        "Рай/Ад — цель не полюс, а дорога/выбор; первослово = вибрация, целое ≠ "
        "сумма имён (= ядро). <b>Q3-миф</b>: подтверждает смысл, ничего не "
        "доказывает в физике; нижние слои независимы."))

    # ===== Мастер-карта =====
    A(P("Мастер-карта — всё на одной геометрии ↔ водород", S_H1))
    A(P("Все слои висят на ОДНОЙ структуре: вершины куба 1–9 (без 5) + центр 5 "
        "(−I) + оболочка 0 (12 красок). Каждый узел n ↔ уровень водорода "
        "E_n=−13.6/n². Переходы по геометрии куба: 17 разрешено / 11 запрещено."))
    rows = [[str(n.n), n.role, f"{n.E_eV:.2f}", n.letter or "—", n.roman or "—"]
            for n in master_map.all_nodes()]
    A(table(["n", "роль", "E_n, эВ", "буква", "римск."],
            rows, [1.2 * cm, 6.6 * cm, 2.4 * cm, 2.0 * cm, 2.4 * cm]))
    A(P("Разрешённые переходы дают РЕАЛЬНЫЕ линии водорода (без подгонки):"))
    A(eq("1↔2 = 121.5 нм (Лайман α)  ·  2↔7 = 396.9 нм  ·  3↔7 = 1004.7 нм"))
    A(fig("28_master_map.png",
          "Рис. 6. Куб Метатрона модели: узлы=число·буква·римское, переходы по типам, "
          "оболочка=12 красок — и те же переходы = спектр водорода."))
    A(PageBreak())

    # ===== Сводка статусов =====
    A(P("Сводка: что строго, что гипотеза", S_H1))
    A(table(
        ["Блок", "Содержание", "Статус"],
        [["Ядро", "φ-аттрактор; e^{iπ}=−1; f(φ,e,π) открыта", "Q1/Q2; Q0; откр."],
         ["Геометрия", "5 тел, Эйлер, R_mid=φ, два нуля, туннель", "Q0/Q1"],
         ["Физика", "плато c(∞), дефазировка, барион=3, тест κ_eff", "Q1/Q2/Q3"],
         ["Числа/Рим", "X*=φ−1, ≤3=триединство, 3³/12³", "Q0–Q2"],
         ["Мастер↔H", "узлы↔E_n; линии 1↔2,2↔7,3↔7", "Q0/Q1 ✓"],
         ["Буквы", "А·Д·Л=каналы 1·4·7 (контекстно)", "Q3"],
         ["Грани/краски", "12 граней=частоты; цвет=ν", "Q3+якорь"],
         ["Шёпот", "слышимость=f(декогеренция)", "Q3+якорь"],
         ["Миф", "космогония, резонансы", "Q3 (отдельно)"]],
        [3.0 * cm, 8.6 * cm, 3.0 * cm]))
    A(note("Главный результат: семантика не отдельный мир — она висит на тех же "
           "узлах и переходах, что воспроизводят спектр водорода, и проходит "
           "проверки (master_map.verify: линии H, триада=каналы, трещина 7→4→1). "
           "Единственная незакрытая физическая гипотеза — ε≠m (память как "
           "самостоятельная переменная), проверяется на квантовом компьютере. "
           "Воспроизводимо: пакет qmt (открытый код, тесты, 28 графиков)."))

    return s


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm,
                             f"DIALOG · полная карта · стр. {doc.page}")
    canvas.restoreState()


def main():
    out = os.path.join(OUT, "DIALOG_Full_Map.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=1.8 * cm,
                            title="DIALOG — Полная карта")
    doc.build(build(), onFirstPage=footer, onLaterPages=footer)
    print("Готово:", out)


if __name__ == "__main__":
    main()
