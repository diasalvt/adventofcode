import re
from collections import defaultdict


Card = tuple[list[int], list[int]]  # Winning numbers, Numbers we have


def load(filename: str) -> list[Card]:
    cards = []
    with open(filename) as f:
        for line in f:
            _, game = re.split(r':\s+', line)
            winning_numbers, numbers = re.split(r'\s+\|\s+', game)
            cards.append(
                (
                    list(map(int, winning_numbers.split())),
                    list(map(int, numbers.split()))
                )
            )
    return cards


cards = load('input.txt')
cards_test = load('test.txt')
print(cards_test)


def nb_wins(winning_numbers: list[int], numbers: list[int]) -> int:
    return sum(n in winning_numbers for n in numbers)


def points(winning_numbers: list[int], numbers: list[int]) -> int:
    wins = nb_wins(winning_numbers, numbers)
    return 0 if wins == 0 else 2**(wins - 1)


def score(cards: list[Card]) -> int:
    return sum(points(*card) for card in cards)


def test_score():
    assert score(cards_test) == 13


print([nb_wins(*card) for card in cards_test])
print(score(cards))


GameState = dict[int, int]


def step(
    cards: list[Card], card_number: int, game_state: GameState
) -> GameState:
    wins = nb_wins(*cards[card_number])
    for i in range(card_number + 1, card_number + 1 + wins):
        game_state[i] += game_state[card_number]

    return game_state


def play(cards: list[Card]) -> GameState:
    game_state = {
        i: 1
        for i in range(len(cards))
    }

    for i, _ in enumerate(cards):
        game_state = step(cards, i, game_state)

    return game_state


def test_play():
    assert sum(play(cards_test).values()) == 30


print(sum(play(cards).values()))
