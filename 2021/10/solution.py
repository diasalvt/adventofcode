from collections import defaultdict
from itertools import islice, chain
from collections import deque
from functools import reduce
from statistics import median

test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
scores = {
    '(': 3,
    '[': 57,
    '{': 1197,
    '<': 25137
}

open_to_close = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

scores2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

close_to_open = {v: k for k, v in open_to_close.items()}

characters_types = dict(close_to_open)
characters_types.update({k: k for k in open_to_close})


def is_opened(character):
    return character in open_to_close


def is_closed(character):
    return not is_opened(character)


def check_corruption(row):
    stack_opened_character = deque()

    for character in row:
        if is_opened(character):
            stack_opened_character.append(character)
        else:
            if not (stack_opened_character.pop() == close_to_open[character]):
                return character

    return None

def get_completion(lines):
    for row in lines:
        stack_opened_character = deque()
        is_corrupted = False
        for character in row:
            if is_opened(character):
                stack_opened_character.append(character)
            else:
                if not (stack_opened_character.pop() == close_to_open[character]):
                    is_corrupted = True
                    break

        if not is_corrupted:
            stack_opened_character.reverse()
            yield stack_opened_character



def sol1():
    with open("input10.txt") as f:
        lines = [row.strip() for row in f]
        print(sum([scores[characters_types[default]] for default in filter(
            lambda x: x is not None,
            map(check_corruption, lines))]))

def sol2():
    with open("input10.txt") as f:
        lines = [row.strip() for row in f]

        def score(characters):
            return reduce(lambda x, y: x*5 + scores2[y], characters, 0)
        uncomplete = median(map(score, get_completion(lines)))
        print(uncomplete)

sol2()