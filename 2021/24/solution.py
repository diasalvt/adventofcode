from __future__ import annotations
from typing import *
from itertools import product
from dataclasses import dataclass
from abc import ABC
from enum import Enum
from collections import defaultdict
from operator import mul
from tqdm import tqdm

class Op(Enum):
    add = 1
    mul = 2
    div = 3
    mod = 4
    eql = 5
    inp = 6

ops = {
    Op.add: lambda x, y: x + y,
    Op.mul: lambda x, y: x * y,
    Op.div: lambda x, y: int(x / y),
    Op.mod: lambda x, y: x % y,
    Op.eql: lambda x, y: int(x == y),
    Op.inp: lambda model_number: (model_number[0], model_number[1:])
}

ops_repr = {
    Op.add: '+',
    Op.mul: '*',
    Op.div: '/',
    Op.mod: '%',
    Op.eql: '=',
}

def op_set(op: Op, a: Set, b: Set):
    return {ops[op](x, y) for x in a for y in b}

State = Union['FunctionState', 'UnknownState', 'ValueState']

@dataclass
class ValueState:
    val: int
    vals: Set[int]

    def __init__(self, val: Union[str, int]):
        self.val = int(val)
        self.vals = {self.val}

    def __repr__(self):
        return f'{self.val}'
    
@dataclass
class FunctionState:
    previous_states: Tuple[State, State]
    op: Op
    vals: Set[int]

    def __init__(self, previous_states, op):
        self.previous_states = previous_states
        self.op = op

        state_a, state_b = previous_states
        self.vals = op_set(op, state_a.vals, state_b.vals)

    def simplify(self) -> State:
        a, b = self.previous_states
        if len(self.vals) == 1:
            return ValueState(list(self.vals)[0])
        if (len(a.vals) == 1) and (len(b.vals) == 1):
            return ValueState(ops[self.op](list(a.vals)[0], list(b.vals)[0]))
        if (self.op == Op.eql) and not (a.vals & b.vals):
            return ValueState(0)
        if (self.op == Op.add) and (a.vals == {0}):
            return b
        if (self.op == Op.add) and (b.vals == {0}):
            return a
        if (self.op == Op.mul) and (a.vals == {1}):
            return b
        if (self.op == Op.mul) and (b.vals == {1}):
            return a
        if (self.op == Op.div) and (a.vals == {1}):
            return a
        if (self.op == Op.div) and (b.vals == {1}):
            return a
        else:
            return self

    def __repr__(self):
        a, b = self.previous_states
        return f'({a} {ops_repr[self.op]} {b})'


@dataclass
class UnknownState:
    unknown: int
    vals: Set
    d_vals: Dict[str, ]

    def __init__(self, unknown: int, range_v = (1, 9)):
        self.unknown = unknown
        self.range = range_v
        a, b = range_v
        self.vals = set(range(a, b + 1))

    def __repr__(self):
        return f'w{self.unknown}'

def state_from_str(s: str, variables_states: Dict[str, State], inp_number=0, force_range=(1, 9)):
    op_str, a, *b = s.split()

    if Op[op_str] == Op.inp:
        new_state = UnknownState(inp_number, force_range)
    else:
        b = b[0]
        if b in ['w', 'x', 'y', 'z']:
            new_state =  FunctionState((variables_states[a], variables_states[b]), Op[op_str]).simplify()
        else:
            new_state = FunctionState((variables_states[a], ValueState(b)), Op[op_str]).simplify()

    variables_states[a] = new_state

    return variables_states


with open('input24.txt') as f:
    instructions = [row.strip() for row in f]

def play(min_numbers='1'*14, max_numbers='9'*14):
    variables: Dict[str, State] = defaultdict(lambda: ValueState(0))
    i = -1

    for instruction in instructions:
        op_str, *_ = instruction.split()
        if op_str == 'inp':
            i += 1
        variables = state_from_str(instruction, variables, i, (int(min_numbers[i]), int(max_numbers[i])))

    return variables

def bruteforce(model_number):
    model_number = list(map(int, str(model_number)))
    vars = {'x': 0, 'y': 0, 'w': 0, 'z': 0}
    for instruction in instructions:
        op_str, *params = instruction.split()
        op = Op[op_str]

        if op == Op.inp:
            v = params[0]
            vars[v], model_number = ops[op](model_number)
        else:
            a, b = params
            if b in ['x', 'y', 'w', 'z']:
                vars[a] = ops[op](vars[a], vars[b])
            else:
                vars[a] = ops[op](vars[a], int(b))

    return 0 == vars['z']

#highest_model_number = '9'*14
#while not bruteforce(highest_model_number):
#    print(highest_model_number)
#    highest_digits = ''
#    for h in highest_model_number:
#        for nb in reversed(range(1, int(h)+1)):
#            model_number = highest_digits + str(nb) + 50*'1'
#            if 0 in play(model_number, highest_model_number)['z'].vals:
#                print(model_number)
#                highest_digits += str(nb)
#                break
#        
#    highest_model_number = highest_digits
#
#print(highest_digits)

#print(0 in play('99999897811111', '99999897899999')['z'].vals)
#for i in tqdm(reversed(range(int(1e15)))):
#    if bruteforce(i):
#        print(i)
#        break

print(play()['y'].vals)