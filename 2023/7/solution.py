from string import ascii_uppercase
from collections import Counter
from functools import cmp_to_key
from typing import Callable


CARDS = ''.join(map(str, range(2, 10))) + 'TJQKA'
replacement = {card: letter for card, letter in zip(CARDS, ascii_uppercase)}


def load(filename: str) -> list[tuple[int, int]]:
    return [
        (cards, int(bid))
        for cards, bid in map(lambda x: x.split(), open(filename))
    ]


game = load('input.txt')
game_test = load('test.txt')


def hand_type(hand: str) -> int:
    match sorted(Counter(hand).values()):
        case [_]:
            return 7
        case [1, 4]:
            return 6
        case [2, 3]:
            return 5
        case [1, 1, 3]:
            return 4
        case [1, 2, 2]:
            return 3
        case [1, 1, 1, 2]:
            return 2
        case _:
            return 1


def comp(
    cards_bid1: tuple[str, int], cards_bid2: tuple[str, int],
    hand_type: Callable, replacement: dict
) -> float:
    hand1, bid1 = cards_bid1
    hand2, bid2 = cards_bid2

    def repl(x): return ''.join(replacement[c] for c in x)

    if hand1 == hand2:
        return 0

    if diff_hand_type := (hand_type(hand1) - hand_type(hand2)):
        return diff_hand_type

    hand1, hand2 = repl(hand1), repl(hand2)
    return (hand1 > hand2) - 0.5


comp_1 = lambda x, y: comp(x, y, hand_type, replacement)


print(
    sum(
        i * bid
        for i, (cards, bid) in enumerate(sorted(game, key=cmp_to_key(comp_1)), start = 1)
    )
)


CARDS_2 = 'J' + ''.join(map(str, range(2, 10))) + 'TQKA'
replacement_2 = {card: letter for card, letter in zip(CARDS_2, ascii_uppercase)}


def hand_type_joker(hand: str) -> int:
    if hand == 'JJJJJ':
        return hand_type(hand)
    most_common_card, _ = Counter(c for c in hand if c != 'J').most_common(1)[0]

    return hand_type(
        ''.join(card if card != 'J' else most_common_card for card in hand)
    )



comp_2 = lambda x, y: comp(x, y, hand_type_joker, replacement_2)


print(
    sum(
        i * bid
        for i, (cards, bid) in enumerate(sorted(game, key=cmp_to_key(comp_2)), start = 1)
    )
)


