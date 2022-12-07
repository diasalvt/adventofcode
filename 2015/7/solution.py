'''
    Going mad on testing and OOP
    TODO: create another solution with minimal amount of code
'''

from dataclasses import dataclass
from operator import not_
from typing import Self, Union
import re
from collections import defaultdict
from functools import reduce
from itertools import product


@dataclass
class Hextet:

    bits: list[bool]

    @classmethod
    def from_int(cls, val: int) -> Self:
        bits = []
        for i in reversed(range(16)):
            bit, val = divmod(val, 2**i)
            bits.append(bit == 1)

        return cls(bits)

    def __and__(self, other: Self) -> Self:
        return self.__class__([a & b for a, b in zip(self.bits, other.bits)])

    def __or__(self, other: Self) -> Self:
        return self.__class__([a | b for a, b in zip(self.bits, other.bits)])

    def __rshift__(self, other: Self) -> Self:
        if other.val == 0:
            return self.__class__(self.bits)
        return self.__class__([False]*other.val + self.bits[:-other.val])

    def __lshift__(self, other: Self) -> Self:
        return self.__class__(self.bits[other.val:] + [False]*other.val)

    def __invert__(self) -> Self:
        return self.__class__(list(map(not_, self.bits)))

    @property
    def val(self):
        return reduce(lambda x, y: 2*int(x) + int(y), self.bits)

    def __repr__(self):
        return f'H.{self.val}'


def test_hextet():
    def h(i: int) -> Hextet:
        return Hextet.from_int(i)

    def val(hextet: Hextet) -> int:
        return hextet.val

    def cap(i: int) -> int:
        return i % (2**16)

    assert h(1) << h(15) == h(32768)
    assert h(8) & h(7) == h(0)
    assert h(8) & h(9) == h(8)
    assert h(8) | h(9) == h(9)
    assert h(65535) & h(742) == h(742)
    assert h(569) & h(65535) == h(569)
    assert h(324) | h(65535) == h(65535)
    assert ~ h(65535) == h(0)
    assert ~ h(0) == h(65535)
    assert ~ h(8) == h(65535 - 8)
    assert h(8) << h(2) == h(32)
    assert h(1) << h(16) == h(0)
    assert h(9) << h(3) == h(72)
    assert h(72) >> h(3) == h(9)
    assert h(65535) >> h(16) == h(0)
    assert h(9) >> h(3) << h(3) == h(8)
    for a, b in product(range(2**4), repeat=2):
        assert h(a) & h(b) == h(b) & h(a)
        assert val(h(a) & h(b)) == a & b
        assert h(a) | h(b) == h(b) | h(a)
        assert val(h(a) | h(b)) == a | b
        assert val(h(a) >> h(b)) == a >> b
        assert val(h(a) << h(b)) == cap(a << b)
        assert val(~ h(a)) == (0b1111_1111_1111_1111 - a)


Register = str
Value = int

operations = {
    'NOT': lambda x: ~ x,
    'AND': lambda x, y: x & y,
    'OR': lambda x, y: x | y,
    'LSHIFT': lambda x, y: x << y,
    'RSHIFT': lambda x, y: x >> y,
    'LOAD': lambda x: x
}


def to_int_if_possible(x: str) -> Union[str, int]:
    try:
        return int(x)
    except ValueError:
        return x


Registers = defaultdict


def get_reg_inputs(inputs: list[Union[Register, Value]]) -> list[Register]:
    return [input_op for input_op in inputs if isinstance(input_op, Register)]


def test_get_reg_inputs():
    assert get_reg_inputs(['a', 1]) == ['a']
    assert get_reg_inputs([1, 'b']) == ['b']
    assert get_reg_inputs([2, 1]) == []
    assert get_reg_inputs([1]) == []
    assert get_reg_inputs(['a']) == ['a']
    assert get_reg_inputs(['a', 'b']) == ['a', 'b']


def get_val_inputs(inputs: list[Union[Register, Value]]) -> list[Value]:
    return [input_op for input_op in inputs if isinstance(input_op, Value)]


def test_get_val_inputs():
    assert get_val_inputs(['a', 1]) == [1]
    assert get_val_inputs([1, 'b']) == [1]
    assert get_val_inputs([2, 1]) == [2, 1]
    assert get_val_inputs([1]) == [1]
    assert get_val_inputs(['a']) == []
    assert get_val_inputs(['a', 'b']) == []


@dataclass(frozen=True)
class Op:

    output: Register
    inputs: list[Union[Register, Value]]
    operation: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        lhs, rhs = s.split(' -> ')
        matches = re.match(
            r'(\d+|[a-z]+)?\s*(?P<op>[A-Z]+)?\s*(\d+|[a-z]+)?', lhs
        ).groups()

        matches = (t for t in matches if t)
        cleaned_matches = tuple(map(to_int_if_possible, matches))

        match cleaned_matches:
            case (a, op, b):
                return cls(rhs, [a, b], op)
            case (op, a):
                return cls(rhs, [a], op)
            case (a,):
                return cls(rhs, [a], 'LOAD')

    def process(self, regs: Registers) -> Registers:
        regs[self.output] = operations[self.operation](
            *[
                (Hextet.from_int(i) if isinstance(i, int) else regs[i])
                for i in self.inputs
            ]
        )
        return regs


str_to_op = Op.from_str


def order_op(ops: list[Op]) -> list[Op]:

    # add Load op
    not_processed = ops
    processed = []

    def is_processed(op, processed):
        reg_inputs = get_reg_inputs(op.inputs)
        reg_processed = [o.output for o in processed]

        return len(set(reg_inputs) - set(reg_processed)) == 0

    while len(not_processed) > 0:
        not_processed_stage = []
        processed_stage = []
        for op in not_processed:
            if is_processed(op, processed):
                processed_stage += [op]
            else:
                not_processed_stage += [op]
        if len(processed_stage) == 0:
            raise ValueError("wrong dag")
        processed += processed_stage
        not_processed = not_processed_stage

    return processed


def run(ops: list[Op]) -> dict:
    reg = {}
    ops_ordered = order_op(ops)
    for op in ops_ordered:
        reg = op.process(reg)

    return reg


def test_run():
    with open('test.txt') as f:
        ops = [str_to_op(row) for row in f.read().splitlines()]

    reg = run(ops)
    assert reg == {
        'd': Hextet.from_int(72),
        'e': Hextet.from_int(507),
        'f': Hextet.from_int(492),
        'g': Hextet.from_int(114),
        'h': Hextet.from_int(65412),
        'i': Hextet.from_int(65079),
        'x': Hextet.from_int(123),
        'y': Hextet.from_int(456),
    }


def test_order():
    op1 = str_to_op('a OR b -> c')
    op2 = str_to_op('NOT e -> f')
    op3 = str_to_op('c OR d -> e')
    op4 = str_to_op('8 -> a')
    op5 = str_to_op('9 -> d')
    op6 = str_to_op('10 -> b')
    op7 = str_to_op('NOT f -> aa')
    op8 = str_to_op('aa OR b -> ab')

    reg = run([op1, op2, op3, op4, op5, op6, op7, op8])
    assert reg['f'] == Hextet.from_int(65535 - 11)
    assert reg['aa'] == Hextet.from_int(11)
    assert reg['ab'] == Hextet.from_int(11)


with open('input.txt') as f:
    ops = [str_to_op(line) for line in f.read().splitlines()]

    # print(*ops, sep='\n')
    reg = run(ops)


print(reg['a'].val)

with open('input.txt') as f:
    ops = [str_to_op(line) for line in f.read().splitlines()]
    op_a = next(filter(lambda x: x.output == 'a', ops))
    ops_modified = [
        op if op.output != 'b' else Op('b', [reg['a'].val], 'LOAD')
        for op in ops
    ]
    print([op for op in ops_modified if op.output == 'b'])

    # print(*ops, sep='\n')
    reg = run(ops_modified)


print(reg['a'].val)
