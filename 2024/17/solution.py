import re
from typing import Self, Iterable
from itertools import islice
from collections import defaultdict

Program = list[int]


class Computer:
    A = 4
    B = 5
    C = 6

    def __init__(self, regs: dict, ip: int = 0):
        self.regs = regs
        self.ip = 0
        self.instructions: list = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv
        ]

    def v(self: Self, operand: int) -> int:
        if operand >= 7:
            raise ValueError(f'{operand=} is not an acceptable value.')
        return (
            {i: i for i in range(4)} | self.regs
        )[operand]

    def adv(self: Self, operand: int) -> None:
        self.regs[self.A] = (
            self.regs[self.A] //
            2 ** self.v(operand)
        )

    def bxl(self: Self, operand: int) -> None:
        self.regs[self.B] = (
            self.regs[self.B] ^ operand
        )

    def bst(self: Self, operand: int) -> None:
        self.regs[self.B] = self.v(operand) % 8

    def jnz(self: Self, operand: int) -> None:
        if self.regs[self.A] != 0:
            self.ip = operand - 2

    def bxc(self: Self, operand: int) -> None:
        self.bxl(self.regs[self.C])

    def out(self: Self, operand: int) -> int:
        return self.v(operand) % 8

    def bdv(self: Self, operand: int) -> None:
        self.regs[self.B] = (
            self.regs[self.A] //
            2 ** self.v(operand)
        )

    def cdv(self: Self, operand: int) -> None:
        self.regs[self.C] = (
            self.regs[self.A] //
            2 ** self.v(operand)
        )

    def run(self: Self, program: Program) -> Iterable[int]:
        while self.ip < len(program):
            opcode, operand = program[self.ip], program[self.ip + 1]
            result = self.instructions[opcode](operand)
            if result is not None:
                yield result
            self.ip += 2


def load(filename: str) -> tuple[Computer, Program]:
    with open(filename) as f:
        A, B, C, _, program = f.read().splitlines()
    A, B, C = map(lambda x: int(re.search(r'\d+', x).group(0)), (A, B, C))
    program = [int(s) for s in program.split()[1].split(',')]

    return Computer({4: A, 5: B, 6: C}), program


computer, program = load('input.txt')
print(
    ','.join(map(str, list(computer.run(program))))
)


def equal_program(computer: Computer, program: Program) -> bool:
    return list(islice(computer.run(program), len(program))) == program


val_to_bits = defaultdict(list)
for i in range(2 ** 11):
    c = Computer({4: i, 5: 0, 6: 0})
    val = next(c.run(program))
    val_to_bits[val].append(i)

d_val_to_bits = {}
for val, l_bits in val_to_bits.items():
    for bits in l_bits:
        top_7_bits = bits // 2**3
        if top_7_bits not in d_val_to_bits:
            d_val_to_bits[top_7_bits] = defaultdict(list)
        d_val_to_bits[top_7_bits][val].append(bits)

for top_7_bits, sub_d in d_val_to_bits.items():
    for val, l_bits in sub_d.items():
        d_val_to_bits[top_7_bits][val] = sorted(l_bits)


def possible_10_bits(
    program: list[int],
    val_to_bits: dict[int, int],
) -> Iterable[tuple[int]]:

    if len(program) == 1:
        yield from map(lambda x: (x,), val_to_bits[program[0]])
        return

    *program, output = program

    for v in val_to_bits[output]:
        last_7_bits = (v % 2**8)
        for bits in possible_10_bits(program, d_val_to_bits[last_7_bits]):
            msb, *lsb = bits
            yield (v, msb, *lsb)


best_bits = next(possible_10_bits(program, val_to_bits))

result = sum(
    (bits % 8) * 2**(3*i)
    for i, bits in enumerate(reversed(best_bits))
)
print(result)

print(
    list(
        Computer({
            4: result,
            5: 0,
            6: 0
        }).
        run(program)
    )
)
