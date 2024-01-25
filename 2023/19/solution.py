from operator import lt, gt
from dataclasses import dataclass
from typing import Self, Callable, Optional, ClassVar
import re


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
VarsRange = dict[str, set[Range]]


def split_range(r: Range, cond: Callable, val: int) -> Optional[Range]:
    r1, r2 = r
    match cond(r1, val), cond(r2, val):
        case True, True:
            return (r1, r2)
        case False, True:
            return (val + 1, r2)
        case True, False:
            return (r1, val - 1)
        case _:
            return None


def split_set_range(
    s_range: set[Range], cond: Callable, val: int
) -> set[Range]:
    return {split_range(r, cond, val) for r in s_range}


class InstructionRange(Instruction):
    def run(self, vars_range: VarsRange) -> tuple[VarsRange, str | bool]:

        if self.cond:
            vars_range_true, vars_range_false = dict(vars_range), dict(vars_range)
            vars_range_true[self.var] = split_set_range(
                vars_range[self.var], self.cond, self.val
            )

            vars_range_false[self.var] = split_set_range(
                vars_range[self.var], lambda x, y: not self.cond(x, y), self.val
            )
            return [(vars_range_true, self.ret), (vars_range_false, None)]
        else:
            return [(vars_range, self.ret)]


@dataclass
class NamedWorkflowsRange(NamedWorkflows):
    instruction_constructor: ClassVar = InstructionRange

    def _run_workflow(self, vars_range: VarsRange, name: str) -> bool:
        res = set()
        for instruction in self.workflows[name]:
            vars_range_ret = instruction.run(vars)
            for vars_range, ret in vars_range_ret:
                match ret:
                    case True:
                        res.update(vars_range)
                    case False:
                        pass
                    case str():
                        res |= self._run_workflow(vars_range, ret)
        return res

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
    return NamedWorkflowsRange.from_str(workflows), parts


instructions = NamedWorkflowsRange.from_str(instructions_str)
print(instructions.run(parts[0]))
# print(sum(sum(p.values()) for p in parts if instructions.run(p)))
