from typing import *
from operator import eq
from itertools import starmap, pairwise

def check_rule(s: str, rules: List[Callable]) -> bool:
    return all(map(lambda x: x(s), rules))

rules: List[Callable] = [
    lambda x: len([e for e in x if e in 'aeiou']) >= 3,
    lambda x: any(starmap(eq, zip(x, x[1:]))),
    lambda x: not any(map(lambda e: e in x, ['ab', 'cd', 'pq', 'xy']))
]

def test_vowel():
    assert rules[0]('ugknbfddgicrmopn') == True
    assert rules[0]('aaa') == True
    assert rules[0]('dvszwmarrgswjxmb') == False

def test_double_char():
    assert rules[1]('ugknbfddgicrmopn') == True
    assert rules[1]('aaa') == True
    assert rules[1]('jchzalrnumimnmhp') == False

def test_forbidden():
    assert rules[2]('ugknbfddgicrmopn') == True
    assert rules[2]('aaa') == True
    assert rules[2]('haegwjzuvuyypxyu') == False

def count_valid_str(strings: List[str], rules: List[Callable]) -> int:
    def _check_rule(s: str) -> bool:
        return check_rule(s, rules)
    return len(list(filter(_check_rule, strings)))

with open('input.txt') as f:
    strings = [s.replace('\n', '') for s in f.readlines()]

def starfilter(fn: Callable, it: Iterable) -> Iterator:
    def _fn(x):
        return fn(*x)
    return filter(_fn, it)

def rm_consecutive(it: Iterable) -> Generator:
    it = iter(it)
    try:
        yield (prev := next(it))
    except StopIteration:
        return

    has_reset = False
    for e in it:
        if e != prev:
            yield e
            has_reset = False
        else:
            if has_reset:
                yield e
                has_reset = False
            has_reset = True
        prev = e

def test_rm_consecutive():
    assert len(list(rm_consecutive([]))) == 0
    assert ''.join(rm_consecutive('aabcdda')) == 'abcda'
    assert ''.join(rm_consecutive('aabcddaa')) == 'abcda'

def has_double_bigram(s: str) -> bool:
    pw = pairwise
    max_count_bigram = max(Counter(rm_consecutive(pw(s))).values(), default=0)
    return max_count_bigram > 1

def test_has_double_bigram():
    assert has_double_bigram('aaa') == False
    assert has_double_bigram('ableubabe') == True
    assert has_double_bigram('aableubabe') == True
    assert has_double_bigram('sknufchjdvccccta') == True

rules2: List[Callable] = [
    has_double_bigram,
    lambda x: any(starmap(eq, zip(x, x[2:])))
]

def test_double_char_separated():
    assert rules2[1]('xyx')
    assert rules2[1]('abcdefeghi')
    assert rules2[1]('aaa')
    assert rules2[1]('sknufchjdvccccta')


def test_rules2():
    assert check_rule('uurcxstgmygtbstg', rules2) == False
    assert check_rule('qjhvhtzxzqqjkmpb', rules2) == True
    assert check_rule('xxyxx', rules2) == True
    assert check_rule('ieodomkazucvgmuy', rules2) == False
    assert check_rule('', rules2) == False
    assert check_rule('sknufchjdvccccta', rules2) == True

print(count_valid_str(strings, rules2))