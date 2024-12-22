import re


def parse(filename: str) -> list[tuple[int, int]]:
    with open(filename) as f:
        return [
            tuple(map(int, pair))
            for pair in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', f.read())
        ]


puzzle = parse('input.txt')
print(sum(a * b for a, b in puzzle))


def parse(filename: str) -> list[tuple[int, int]]:
    with open(filename) as f:
        return re.findall(
            r"mul\((\d{1,3}),(\d{1,3})\)|(do|don't)\(\)",
            f.read()
        )


do = True
res = 0
for m1, m2, do_or_dont in parse('input.txt'):
    match do_or_dont:
        case "do":
            do = True
        case "don't":
            do = False
        case _:
            if do:
                res += int(m1) * int(m2)

print(res)
