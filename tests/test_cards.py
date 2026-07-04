import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import cards as C

def test_ten_number_cards_closed():
    assert len(C.NUMBER_CARDS) == 10
    assert C.pipeline_is_closed()

def test_each_card_one_function():
    fns = C.functions()
    assert len(fns) == 10
    assert fns["5"].startswith("ВЫБОР")          # центр = выбор
    assert fns["0"].startswith("ПАМЯТЬ")

def test_center_is_choice():
    assert C.center_is_choice()

def test_card_lookup_and_modules():
    c5 = C.card("5")
    assert "node5" in c5.module and "0.5" in c5.physics
    c1 = C.card("1")
    assert c1.hydrogen.startswith("n=1")         # водород Лайман

def test_letter_cards():
    assert {c.symbol for c in C.LETTER_CARDS} == {"А", "Л", "Д", "Х"}

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
