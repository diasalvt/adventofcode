Pos = complex
Terrain = dict[Pos, str]


def load(filename: str) -> Terrain:
    with open(filename) as f:
        return {
            x + y * 1j: c
            for y, row in enumerate(f.read().splitlines())
            for x, c in enumerate(row)
        }
