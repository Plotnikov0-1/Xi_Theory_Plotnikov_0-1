import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qmt import chemistry as C

def test_shell_2n2():
    assert [C.shell_capacity(n) for n in range(1,5)] == [2,8,18,32]

def test_period_lengths_doubled():
    assert C.period_lengths() == [8,8,18,18,32]
    assert C.each_length_doubled()

def test_d_block_18():
    assert C.d_block_is_18()

def test_magic_numbers():
    assert C.is_magic(2) and C.is_magic(82) and not C.is_magic(30)

def test_octet():
    assert C.OCTET == 8

def _run_all():
    fns=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for fn in fns: fn(); print(f'  OK  {fn.__name__}')
    print(f'\nВсе {len(fns)} тестов пройдены.')
if __name__=='__main__': _run_all()
