from typing import TypeAlias, Union, Self, Type
from collections import defaultdict
from dataclasses import dataclass
import re
from itertools import chain, zip_longest


Pos: TypeAlias = complex
Dir: TypeAlias = complex
Board: TypeAlias = dict[Pos, bool]  # True if available, False if wall
Move: TypeAlias = int
Turn: TypeAlias = str
Path: TypeAlias = list[Union[Move, Turn]]


class Grid:
    def __init__(self, board: Board) -> Self:
        self.board = board
        self.height = int(max(pos.imag for pos in self.board)) + 1
        self.width = int(max(pos.real for pos in self.board)) + 1

    def move_until_border(self, pos: Pos, dir: Dir) -> Pos:
        while pos in self.board:
            pos += dir
        return pos - dir

    def next_pos(self, pos: Pos, shift: Dir) -> tuple[Pos, Dir]:
        if (pos + shift) in self.board:
            return pos + shift, shift
        else:
            return self.move_until_border(pos, -shift), shift

    def __repr__(self) -> str:
        def pos_to_char(pos: Pos) -> str:
            if pos not in self.board:
                return ' '
            else:
                return '.' if self.board[pos] else '#'

        cum_str = ''
        for y in range(self.height):
            cum_str += ''.join(
                pos_to_char(x + y * 1j) for x in range(self.width)
            )
            cum_str += '\n'
        return cum_str


def parse_file(
    filename: str, cls_grid: type[Grid] = Grid
) -> tuple[Grid, Path]:
    with open(filename) as f:
        str_board, str_path = f.read().split('\n\n')
        board = {}
        for y, row in enumerate(str_board.splitlines()):
            for x, character in enumerate(row):
                if character != ' ':
                    board[x + y * 1j] = (character == '.')

        path_moves = map(int, re.findall(r'\d+', str_path))
        path_turns = re.findall(r'[LR]', str_path)
        path = list(filter(lambda x: x is not None,
                           chain.from_iterable(
                               zip_longest(path_moves, path_turns))
                           ))
        return cls_grid(board), path


test = parse_file('test.txt')
# print(*test, sep='\n')
print(test[0])


@dataclass
class State:
    pos: Pos
    dir: Dir

    def move(self, steps: int, grid: Grid) -> Self:
        for _ in range(steps):
            # if next pos in not a wall update
            new_pos, new_dir = grid.next_pos(self.pos, self.dir)
            if grid.board[new_pos]:
                self.pos, self.dir = new_pos, new_dir
            else:
                return self
        return self

    def turn(self, right_or_left: Turn) -> Self:
        self.dir *= (1j if right_or_left == 'R' else -1j)
        return self


def part_1(filename: str, cls_grid: Type[Grid] = Grid) -> int:
    grid, path = parse_file(filename, cls_grid)
    state = State(
        min((pos for pos in grid.board if pos.imag == 0), key=lambda x: x.real),
        1
    )

    for cmd in path:
        print(f'{state=} {cmd=}')
        match cmd:
            case int(steps):
                state.move(steps, grid)
            case str():
                state.turn(cmd)

    def dir_score(dir: Dir) -> int:
        match (dir.real, dir.imag):
            case (1, 0):
                return 0
            case (0, 1):
                return 1
            case (-1, 0):
                return 2
            case (0, -1):
                return 3
            case _:
                raise ValueError("Unvalid dir")

    score = int(
        1000 * (state.pos.imag + 1) +
        4 * (state.pos.real + 1) +
        dir_score(state.dir)
    )
    return score


# print(part_1('test.txt'))
# print(part_1('input.txt'))


def keep_side(positions: set, side: str):
    match side:
        case 'N':
            min_imag = min(p.imag for p in positions)
            return {p for p in positions if p.imag == min_imag}
        case 'S':
            max_imag = max(p.imag for p in positions)
            return {p for p in positions if p.imag == max_imag}
        case 'W':
            min_real = min(p.real for p in positions)
            return {p for p in positions if p.real == min_real}
        case 'E':
            max_real = max(p.real for p in positions)
            return {p for p in positions if p.real == max_real}
        case _:
            raise ValueError(f'{side=} is not a valid side')


def get_matching_pos(
    pos: Pos, side1: list[Pos], side2: list[Pos], reverse=False
) -> Pos:
    for p1, p2 in zip(side1, side2[::-1] if reverse else side2):
        if p1 == pos:
            return p2

    raise ValueError(f'{pos=} is not in {side1=}')


class CubeGrid(Grid):
    def __init__(self, board: Board) -> Self:
        super().__init__(board)
        self._cube_size = self.width // 3
        self.cube_pos_to_face = {
            p: int(3 * (p.imag // self._cube_size) + (p.real // self._cube_size) + 1)
            for p in self.board
        }
        self.cube_face_to_pos = defaultdict(set)
        for p, face in self.cube_pos_to_face.items():
            self.cube_face_to_pos[face].add(p)

        self.cube_face_NSEW = {}
        for face, positions in self.cube_face_to_pos.items():
            for side in ['N', 'S', 'E', 'W']:
                self.cube_face_NSEW[(face, side)] = sorted(
                    keep_side(positions, side),
                    key=lambda x: (x.real, x.imag)
                )

    def next_pos(self, pos: Pos, shift: Dir) -> tuple[Pos, Dir]:
        """
            ....____..
            .11|22 33|
            .11|22 33|
            ...|   __|
            .44|55|66.
            .44|55|66.
            .__   |  .
            |77 88|99.
            |77 88|99.
            |   __|...
            |aa|bb cc.
            |aa|bb cc.
            .__.......

        For each face we note
            ......
            ..N...
            .W.E..
            ..s...
            ......

            case 2 -> 10
            case 2 -> 7
            case 4 -> 3
        """
        if (pos + shift) in self.board:
            return (pos + shift, shift)
        else:
            match self.cube_pos_to_face[pos], (shift.real, shift.imag):
                # case 2 -> 10
                case 2, (0, -1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(2, 'N')],
                        self.cube_face_NSEW[(10, 'W')],
                    ), shift * 1j
                # case 10 -> 2
                case 10, (-1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(10, 'W')],
                        self.cube_face_NSEW[(2, 'N')],
                    ), - shift * 1j
                # case 2 -> 7
                case 2, (-1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(2, 'W')],
                        self.cube_face_NSEW[(7, 'W')],
                        reverse=True
                    ), - shift
                # case 7 -> 2
                case 7, (-1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(7, 'W')],
                        self.cube_face_NSEW[(2, 'W')],
                        reverse=True
                    ), - shift
                # case 3 -> 10
                case 3, (0, -1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(3, 'N')],
                        self.cube_face_NSEW[(10, 'S')]
                    ), shift
                # case 10 -> 3
                case 10, (0, 1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(10, 'S')],
                        self.cube_face_NSEW[(3, 'N')]
                    ), shift
                # case 3 -> 8
                case 3, (1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(3, 'E')],
                        self.cube_face_NSEW[(8, 'E')],
                        reverse=True
                    ), - shift
                # case 8 -> 3
                case 8, (1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(8, 'E')],
                        self.cube_face_NSEW[(3, 'E')],
                        reverse=True
                    ), - shift
                # case 3 -> 5
                case 3, (0, 1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(3, 'S')],
                        self.cube_face_NSEW[(5, 'E')]
                    ), shift * 1j
                # case 5 -> 3
                case 5, (1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(5, 'E')],
                        self.cube_face_NSEW[(3, 'S')]
                    ), - shift * 1j
                # case 5 -> 7
                case 5, (-1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(5, 'W')],
                        self.cube_face_NSEW[(7, 'N')],
                    ), - shift * 1j
                # case 7 -> 5
                case 7, (0, -1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(7, 'N')],
                        self.cube_face_NSEW[(5, 'W')],
                    ), shift * 1j
                # case 8 -> 10
                case 8, (0, 1):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(8, 'S')],
                        self.cube_face_NSEW[(10, 'E')]
                    ), shift * 1j
                # case 10 -> 8
                case 10, (1, 0):
                    return get_matching_pos(
                        pos,
                        self.cube_face_NSEW[(10, 'E')],
                        self.cube_face_NSEW[(8, 'S')]
                    ), - shift * 1j
                case _:
                    raise ValueError(
                        f'{pos=}, {self.cube_pos_to_face[pos]=}, {shift=} is unvalid'
                    )


def part_2(filename: str) -> int:
    return part_1(filename, CubeGrid)


print(part_2('input.txt'))
