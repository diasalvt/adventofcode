from dataclasses import dataclass, field
from typing import Any, Self


Pos = tuple[int, int]
Dir = str  # N, S, E, W

DIRS: dict[Dir, tuple[int, int]] = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}


@dataclass
class Array:
    arr: list[list[Any]]

    height = property(lambda self: len(self.arr))
    width = property(lambda self: len(self.arr[0]))

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls([list(line) for line in s.splitlines()])

    def is_valid_pos(self, pos: Pos) -> bool:
        i, j = pos
        return (0 <= i <= self.height) & (0 <= j <= self.width)

    def __getitem__(self, key: tuple[int, int]) -> Any:
        i, j = key
        if (i < 0) or (j < 0):
            raise IndexError
        return self.arr[key[0]][key[1]]


@dataclass(frozen=True)
class PlayerState:
    pos: Pos = (0, -1)
    dir: Dir = 'E'


@dataclass
class GameState:
    array: Array
    players: list[PlayerState] = field(default_factory=lambda: [PlayerState()])
    past_players_states: set[PlayerState] = field(
        default_factory=set
    )

    def _move_player(self, player: PlayerState) -> list[PlayerState]:
        """
            Return True if GameState changed.
        """
        i, j = player.pos
        shift_i, shift_j = DIRS[player.dir]
        next_pos = i + shift_i, j + shift_j
        try:
            next_val = self.array[next_pos]

        except IndexError:
            return []

        match (next_val, player.dir):
            case ('.', _):
                return [PlayerState(next_pos, player.dir)]
            case ('|', dir) if dir in ['N', 'S']:
                return [PlayerState(next_pos, player.dir)]
            case ('|', dir) if dir in ['E', 'W']:
                return [
                    PlayerState(next_pos, 'N'),
                    PlayerState(next_pos, 'S')
                ]
            case ('-', dir) if dir in ['N', 'S']:
                return [
                    PlayerState(next_pos, 'W'),
                    PlayerState(next_pos, 'E')
                ]
            case ('-', dir) if dir in ['W', 'E']:
                return [PlayerState(next_pos, player.dir)]
            case ('/', 'N'):
                return [PlayerState(next_pos, 'E')]
            case ('/', 'S'):
                return [PlayerState(next_pos, 'W')]
            case ('/', 'W'):
                return [PlayerState(next_pos, 'S')]
            case ('/', 'E'):
                return [PlayerState(next_pos, 'N')]
            case ('\\', 'N'):
                return [PlayerState(next_pos, 'W')]
            case ('\\', 'S'):
                return [PlayerState(next_pos, 'E')]
            case ('\\', 'W'):
                return [PlayerState(next_pos, 'N')]
            case ('\\', 'E'):
                return [PlayerState(next_pos, 'S')]
            case other:
                raise ValueError(f'{other} is not a valid state')

    def move_players(self) -> bool:
        self.players = [
            new_player
            for player in self.players
            for new_player in self._move_player(player)
        ]
        next_players = set(self.players) - self.past_players_states
        self.players = list(next_players)
        self.past_players_states |= set(self.players)
        return len(next_players) > 0


def score(game: GameState) -> int:
    while game.move_players():
        pass
    return len({s.pos for s in game.past_players_states})


terrain = Array.from_str(open('input.txt').read())
print(score(GameState(terrain)))


def score_2(terrain: Array) -> int:
    max_south = max(
        score(GameState(terrain, [PlayerState((-1, i), 'S')]))
        for i in range(terrain.width)
    )
    max_north = max(
        score(GameState(terrain, [PlayerState((terrain.height, i), 'N')]))
        for i in range(terrain.width)
    )
    max_east = max(
        score(GameState(terrain, [PlayerState((i, -1), 'E')]))
        for i in range(terrain.height)
    )
    max_west = max(
        score(GameState(terrain, [PlayerState((i, terrain.width), 'W')]))
        for i in range(terrain.height)
    )
    return max(max_south, max_north, max_east, max_west)

print(score_2(terrain))
