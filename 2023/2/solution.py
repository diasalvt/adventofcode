from collections import Counter, defaultdict


def load(filename: str) -> list[list[dict]]:
    games = []
    with open(filename) as f:
        for line in f.read().splitlines():
            game, results = line.split(": ")
            games.append([
                Counter({
                    color: int(count)
                    for count, color in map(lambda x: x.split(" "), draw.split(", "))
                })
                for draw in results.split("; ")
            ])
    return games


games = load("input.txt")
constraint = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def game_is_valid(game: list[dict], constraint: dict) -> bool:

    def draw_is_valid(draw: dict, constraint: dict) -> bool:
        return all(draw[color] <= count for color, count in constraint.items())

    return all(draw_is_valid(draw, constraint) for draw in game)


print(sum(i + 1 for i, game in enumerate(games) if game_is_valid(game, constraint)))


def power(game: list[dict]) -> dict:
    d = defaultdict(int)
    for draw in game:
        for color, count in draw.items():
            d[color] = max(d[color], count)
    return d['red']*d['green']*d['blue']


print(sum(power(game) for game in games))
