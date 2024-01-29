from operator import lt, gt
from dataclasses import dataclass
from typing import Self, Callable, Optional, ClassVar
import re
from math import prod


_COND = {'<': lt, '>': gt}
_RETURN = {'R': False, 'A': True}


Vars = dict[str, int]


@dataclass
class Instruction:
    var: str
    cond: Callable
    val: int
    ret: str | bool

    @classmethod
    def from_str(cls, s: str) -> Self:
        m = re.fullmatch(
            r'(?:(?P<var>[a-z])(?P<cond>[\<\>])(?P<val>\d+):)?(?P<return>\w+)',
            s
        )
        var, cond, val, do = m.groups()
        ret = _RETURN.get(do, do)

        if cond:
            return cls(var, _COND[cond], int(val), ret)
        return cls(None, None, None, ret)

    def run(self, vars: Vars) -> Optional[str | bool]:
        if self.cond:
            return self.ret if self.cond(vars[self.var], self.val) else None
        else:
            return self.ret


@dataclass
class NamedWorkflows:
    workflows: dict[str, list[Instruction]]
    instruction_constructor: ClassVar = Instruction

    @classmethod
    def from_str(cls, s: str) -> Self:
        named_workflows = {}
        for line in s.splitlines():
            name, _workflow = line.split('{')
            workflow = _workflow[:-1]
            named_workflows[name] = [
                cls.instruction_constructor.from_str(inst)
                for inst in workflow.split(',')
            ]
        return cls(named_workflows)

    def _run_workflow(self, vars: Vars, name: str) -> bool:
        for instruction in self.workflows[name]:
            if (ret := instruction.run(vars)) is not None:
                if ret in [True, False]:
                    return ret
                return self._run_workflow(vars, ret)

    def run(self, vars: Vars) -> bool:
        return self._run_workflow(vars, 'in')


def load(filename: str) -> tuple[NamedWorkflows, list[dict[str, int]]]:
    workflows, parts_str = open(filename).read().split('\n\n')
    parts = []
    for line in parts_str.splitlines():
        line = line[1:-1]
        parts.append(
            {
                key_val[0]: int(key_val[2:])
                for key_val in line.split(',')
            }
        )
    return workflows, parts


instructions_str, parts = load('input.txt')
instructions = NamedWorkflows.from_str(instructions_str)
print(sum(sum(p.values()) for p in parts if instructions.run(p)))


Range = tuple[int, int]
VarsRange = dict[str, Range]


def split_range(r: Range, cond: Callable, val: int) -> Optional[Range]:
    r1, r2 = r
    match cond(r1, val), cond(r2, val):
        case True, True:
            return (r1, r2)
        case False, True:
            return (val + (0 if cond(val, val) else 1), r2)
        case True, False:
            return (r1, val - (0 if cond(val, val) else 1))
        case _:
            return None


class InstructionRange(Instruction):
    def run(self, vars_range: VarsRange) -> list[tuple[VarsRange, str | bool]]:

        if self.cond:
            vars_range_true, vars_range_false = dict(vars_range), dict(vars_range)
            vars_range_true[self.var] = split_range(
                vars_range[self.var], self.cond, self.val
            )

            vars_range_false[self.var] = split_range(
                vars_range[self.var], lambda x, y: not self.cond(x, y), self.val
            )
            return [(vars_range_true, self.ret), (vars_range_false, None)]
        else:
            return [(vars_range, self.ret)]


def count(vars_range: VarsRange) -> int:
    return prod(y - x + 1 if x <= y else 0 for x, y in vars_range.values())


# def intersection_range(
#     a: tuple[int, int], b: tuple[int, int]
# ) -> tuple[int, int]:
#     return (max(a[0], b[0]), min(a[1], b[1]))


# def intersection_v1_v2(v1: VarsRange, v2: VarsRange) -> VarsRange:
#     return {
#         var: intersection_range(v_range_1, v_range_2)
#         for var, (v_range_1, v_range_2) in zip(
#             v1.keys(), zip(v1.values(), v2.values())
#         )
#     }


# def intersection(l_v: list[VarsRange]) -> VarsRange:
#     return reduce(intersection_v1_v2, l_v)


# def count_union(l_v_ranges: list[VarsRange]) -> int:
#     match l_v_ranges:
#         case []:
#             return 0
#         case [v_range, *tail]:
#             return count(v_range) + count_union(tail) - count_union(
#                 [intersection_v1_v2(v_range, v) for v in tail]
#             )

def dummy_count_union(l_v_ranges):
    return sum(count(v) for v in l_v_ranges)


@dataclass
class NamedWorkflowsRange(NamedWorkflows):
    instruction_constructor: ClassVar = InstructionRange

    def _run_workflow(self, vars_range: VarsRange, name: str) -> list[VarsRange]:
        res = []
        for instruction in self.workflows[name]:
            vars_range_ret = instruction.run(vars_range)
            for vars_range, ret in vars_range_ret:
                match ret:
                    case True:
                        res += [vars_range]
                    case str():
                        res += self._run_workflow(vars_range, ret)
        return res

    def run(self, vars_range: VarsRange) -> bool:
        return dummy_count_union(self._run_workflow(vars_range, 'in'))


instructions_test_str, parts = load('test.txt')
instructions_test = NamedWorkflowsRange.from_str(instructions_test_str)
instructions = NamedWorkflowsRange.from_str(instructions_str)
print(instructions.run({
    'x': (1, 4000),
    'm': (1, 4000),
    'a': (1, 4000),
    's': (1, 4000)
}))
# print(sum(sum(p.values()) for p in parts if instructions.run(p)))
