from dataclasses import dataclass
from operator import not_
from typing import Self, Union
import re
from collections import defaultdict
from functools import reduce


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

    def __rshift__(self, count: int) -> Self:
        return self.__class__([False]*count + self.bits[:-count])

    def __lshift__(self, count: int) -> Self:
        return self.__class__(self.bits[count:] + [False]*count)

    def __invert__(self) -> Self:
        return self.__class__(list(map(not_, self.bits)))

    def __repr__(self):
        return str(reduce(lambda x, y: 2*int(x) + int(y), self.bits))


val1 = Hextet.from_int(9)
val2 = Hextet.from_int(3)

print(
    f'{val1=}',
    f'{val2=}',
    val1 & val2,
    val1 | val2,
    val1 << 2,
    val1 >> 2,
    0 << 1,
    ~ val1,
    sep='\n'
)

Register = str
Value = int

operations = {
    'NOT': lambda x: ~ x,
    'AND': lambda x, y: x & y,
    'OR': lambda x, y: x | y,
    'LSHIFT': lambda x, y: x << 2,
    'RSHIFT': lambda x, y: x >> 2,
    'LOAD': lambda x: x
}

def to_int_if_possible(x: str) -> Union[str, int]:
    try:
        return int(x)
    except ValueError:
        return x

Registers = defaultdict

@dataclass
class Op:

    output: Register
    inputs: list[Union[Register, Value]]
    operation: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        lhs, rhs = s.split(' -> ')
        matches = re.match(
            r'(\d+|[a-z]+)?\s*(?P<op>[A-Z]+)?\s*(\d|[a-z]+)?', lhs
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

print(Op.from_str('da LSHIFT 1 -> du'))
print(Op.from_str('d OR j -> k'))

reg = defaultdict(lambda: Hextet.from_int(0))

with open('input.txt') as f:
    for line in f.read().splitlines():
        print(line)
        op = Op.from_str(line)
        print(op)
        reg = op.process(reg)
        print(reg)
