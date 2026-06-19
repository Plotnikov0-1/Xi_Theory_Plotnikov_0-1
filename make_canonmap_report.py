#!/usr/bin/env python3
"""
Карта канонов DIALOG QMT — верхний, картографический слой (синхронизация 3·7·12).
Жанр: картография уже доказанного + защита от искажения источника.
Запуск:  python make_canonmap_report.py  →  report/DIALOG_QMT_CanonMap.pdf
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

from qmt import synchronization as S

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
TEAL = colors.HexColor("#2f6f6d")
GREEN = colors.HexColor("#2e7d32")
AMBER = colors.HexColor("#f9a825")
RED = colors.HexColor("#c62828")
HEAD = colors.HexColor("#d9d2c2")


def st(name, **kw):
    base = dict(fontName="DV", textColor=INK, fontSize=10.5, leading=15.5)
    base.update(kw)
    return ParagraphStyle(name, **base)


S_TITLE = st("t", fontName="DV-Bold", fontSize=23, leading=27, textColor=CLAY, alignment=TA_CENTER)
S_SUB = st("s", fontSize=12.5, leading=17, textColor=GRAY, alignment=TA_CENTER)
S_H1 = st("h1", fontName="DV-Bold", fontSize=15.5, leading=20, textColor=CLAY, spaceBefore=15, spaceAfter=5)
S_H2 = st("h2", fontName="DV-Bold", fontSize=12.5, leading=17, textColor=TEAL, spaceBefore=10, spaceAfter=3)
S_BODY = st("b", alignment=TA_JUSTIFY, spaceAfter=5)
S_NOTE = st("n", fontSize=9.7, leading=14, textColor=GRAY)
S_CAP = st("c", fontSize=9, leading=12.5, textColor=GRAY, alignment=TA_CENTER, spaceBefore=2, spaceAfter=9)
S_TD = st("td", fontSize=9.3, leading=12)
S_TDC = st("tdc", fontSize=9.3, leading=12, alignment=TA_CENTER)
S_TH = st("th", fontName="DV-Bold", fontSize=9.3, leading=12, textColor=INK)

W = A4[0] - 4 * cm


def P(t, s=S_BODY):
    return Paragraph(t, s)


def note(t):
    tab = Table([[Paragraph(t, S_NOTE)]], colWidths=[W])
    tab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBEFORE", (0, 0), (0, -1), 3, CLAY),
    ]))
    return tab


def fig(name, caption, max_h=9.5 * cm):
    path = os.path.join(FIG, name)
    iw, ih = ImageReader(path).getSize()
    scale = min(W / iw, max_h / ih)
    im = Image(path, width=iw * scale, height=ih * scale)
    im.hAlign = "CENTER"
    return [Spacer(1, 4), KeepTogether([im, P(caption, S_CAP)])]


def table(headers, rows, widths, style_extra=None):
    data = [[Paragraph(h, S_TH) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, S_TDC if i else S_TD) for i, c in enumerate(r)])
    tab = Table(data, colWidths=widths, repeatRows=1)
    base = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bdb6a6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if style_extra:
        base += style_extra
    tab.setStyle(TableStyle(base))
    return [Spacer(1, 3), tab, Spacer(1, 6)]


def build():
    s = []

    def A(x):
        s.extend(x) if isinstance(x, list) else s.append(x)

    # ===== Титул =====
    A(Spacer(1, 3.0 * cm))
    A(P("КАРТА КАНОНОВ", S_TITLE))
    A(P("Синхронизация структуры 3 · 7 · 12", S_SUB))
    A(Spacer(1, 0.4 * cm))
    A(P("Картография уже доказанного — с защитой от искажения источника.", S_SUB))
    A(Spacer(1, 1.8 * cm))
    A(note("Это <b>верхний слой</b> модели, не физический. Его задача — не "
           "предсказать новое, а показать, что независимые канонические системы "
           "несут одну и ту же структурную разметку. Критерий успеха — полнота "
           "охвата и непротиворечивость связей, а не предсказательная сила."))
    A(PageBreak())

    # ===== 1. Жанр =====
    A(P("1. Жанр: картография, а не предсказание", S_H1))
    A(P("Когда теория претендует <b>предсказать новое</b>, подбор постфактум — "
        "слабость (cherry-picking). Но синхронизация канонов — другой жанр: взять "
        "уже доказанное человечеством и показать, что оно укладывается в одну "
        "структуру. У этого жанра есть законные научные прецеденты:"))
    A(table(
        ["Работа", "Что сделано", "Предсказание?"],
        [["Менделеев (1869)", "классификация известных элементов", "нет (потом)"],
         ["Линней (1735)", "7 уровней систематики живого", "нет"],
         ["ADE — Дынкин (1947)", "группы Ли, особенности, тела — одна схема", "синтез"],
         ["Теория категорий", "язык алгебры, топологии, логики, физики", "синтез"]],
        [3.6 * cm, 8.0 * cm, 3.2 * cm]))
    A(P("Критика cherry-picking применима только к нижнему (физическому) слою. "
        "На верхних слоях критерий другой — встаёт ли гипотеза в общую сеть связей."))

    # ===== 2. Защита от искажения =====
    A(P("2. Защита от искажения источника", S_H1))
    A(P("Эзотерические каноны (каббала и др.) за века переписывались вручную и "
        "переинтерпретировались — их структура <b>могла быть искажена</b>. "
        "Поэтому им нельзя доверять как первоисточнику. Правило:"))
    A(note("Каждое число проверяется не по эзотерике, а по структурам, которые "
           "можно <b>вывести заново</b> (математика, физика, кристаллография). Их "
           "исказить нельзя: теорема Эйлера и 7 кристаллических систем сегодня те "
           "же, что и всегда.<br/><br/>"
           "<b>Доверие = жёсткость × устойчивость к искажению</b>, где жёсткость = "
           "независимость + точность + полнота разметки, а устойчивость убывает от "
           "«выводимо заново» (низкий риск) к «эзотерическая передача» (высокий)."))

    # ===== 3. Карта канонов (из модуля) =====
    A(P("3. Карта канонов 3·7·12", S_H1))
    mark = lambda v: "✓" if v else "—"
    rows = []
    color_rows = []
    ordered = sorted(S.CANONS, key=lambda c: -c.trust())
    for i, c in enumerate(ordered, start=1):
        rows.append([c.name, c.distortion, c.grade(),
                     mark(c.three), mark(c.seven), mark(c.twelve)])
        col = {"низкий": GREEN, "средний": AMBER, "высокий": RED}[c.distortion]
        color_rows.append(("TEXTCOLOR", (1, i), (1, i), col))
    A(table(
        ["Канон", "риск иск.", "доверие", "3", "7", "12"], rows,
        [5.2 * cm, 2.2 * cm, 2.6 * cm, 1.4 * cm, 1.4 * cm, 1.4 * cm],
        style_extra=color_rows))
    A(P("Каббала даёт <b>полную</b> разметку 3+7+12, но из-за высокого риска "
        "искажения принимается лишь как вспомогательная корроборация, а не опора."))

    A(fig("21_canon_map.png",
          "Рис. 1. Разметка 3·7·12 по канонам (цвет = риск искажения). Справа — "
          "каждое число закреплено в неискажаемом источнике."))

    # ===== 4. Главный результат =====
    A(P("4. Главный результат: карта выживает без эзотерики", S_H1))
    A(P("Каждое число независимо закреплено в <b>неискажаемых (выводимых заново)</b> "
        "источниках. Если выбросить всю эзотерику — разметка 3+7+12 держится:"))
    for n in (3, 7, 12):
        items = "; ".join(S.corroboration(n))
        A(P(f"<b>{n}:</b> {items}"))
    A(note("Семёрку, которой нет в счёте вершин/рёбер/граней платоновых тел, "
           "поставляет <b>не каббала, а кристаллография</b> (7 кристаллических "
           "систем) — независимый, выводимый заново источник. Эзотерика лишь "
           "подтверждает то, что уже закреплено математикой и физикой."))

    # ===== 5. Геометрия =====
    A(P("5. Геометрия: теорема Эйлера и где живут числа", S_H1))
    A(P(f"Тождество V − E + F = 2 выполняется для всех пяти тел "
        f"(проверено символьно, Q0): {S.euler_check()}."))
    A(table(
        ["Тело", "V", "E", "F", "V−E+F"],
        [[s.name, str(s.V), str(s.E), str(s.F), str(s.euler())] for s in S.SOLIDS],
        [4.6 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 3.0 * cm]))
    A(P("<b>12</b> живёт в геометрии (рёбра куба, грани додекаэдра, вершины "
        "икосаэдра). <b>3</b> — оси симметрии. <b>7</b> в счёте V/E/F отсутствует — "
        "берётся из кристаллографии. Это граница карты, и её надо держать открыто."))

    # ===== 6. Проверяемые направления =====
    A(P("6. Проверяемые направления (статус Q3)", S_H1))
    A(P("<b>V-E-F как три силы.</b> Формально проверяемо: у каждого тела три "
        "числа, связанных двойственностью (куб↔октаэдр, додекаэдр↔икосаэдр). Но "
        "сопоставление «элемент → взаимодействие» требует физического обоснования. "
        "Пока гипотеза."))
    A(P("<b>Внутренние точки как туннели.</b> Переводится на готовый язык "
        "замечательных точек многогранников (центроид, точки Жергонна, Нагеля, "
        "Торричелли — у треугольника их каталогизировано более тысячи, есть "
        "аналоги для тетраэдра). Каждая задаёт траектории грань→грань. Это "
        "измеримая геометрия, не спекуляция."))

    # ===== 7. Лестница и статус =====
    A(P("7. Лестница допустимости и статус карты", S_H1))
    A(P("Построение сверху вниз: фантастика → религия → психология → химия → "
        "физика. Каждый шаг вниз — ужесточение и согласование с экспериментом. "
        "Гипотеза, прошедшая все пять слоёв без поломки, — сильное свидетельство "
        "(не «доказательство» по Попперу, а узел карты)."))
    A(note("<b>Статус.</b> Разметка 3+7+12 — Q4 (подтверждение независимыми "
           "источниками), причём опорные источники неискажаемы (кристаллография, "
           "физика, геометрия, теорема Эйлера). Эзотерические каноны — "
           "вспомогательная корроборация с явной пометкой риска искажения. "
           "Сопоставления «сила↔элемент» и «точка↔туннель» — Q3 (проверяемые "
           "направления). Воспроизводимо: модуль qmt/synchronization.py."))

    return s


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm,
                             f"DIALOG QMT · карта канонов · стр. {doc.page}")
    canvas.restoreState()


def main():
    out = os.path.join(OUT, "DIALOG_QMT_CanonMap.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=1.8 * cm,
                            title="DIALOG QMT — Карта канонов")
    doc.build(build(), onFirstPage=footer, onLaterPages=footer)
    print("Готово:", out)


if __name__ == "__main__":
    main()
