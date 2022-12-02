from typing import Iterator, List, Tuple, Union, DefaultDict
from collections import defaultdict
from itertools import chain

Column = Tuple[int, ...]
Row = Tuple[int, ...]
Vector = Union[Column, Row]
Board= Union[Tuple[Column], Tuple[Row]]

def parse_boards(iterator: Iterator) -> Iterator[Board]:
    res = []
    for row in iterator:
        if len(row) <= 1:
            if len(res) > 0:
                yield tuple(res)
            res = []
        else:
            res.append(tuple(map(int, row.split())))
    yield tuple(res)

def sol1():
    with open("input4.txt") as f:
        iter_f = iter(f)
        draw_numbers = [int(value) for value in next(iter_f).split(',')]

        # row
        boards: List[Board] = list(parse_boards(iter_f))
        # columns
        transposed_boards: List[Board] = [tuple(zip(*board)) for board in boards]

        number_in_vectors: DefaultDict[int, List[Vector]] = defaultdict(list)
        for row in chain.from_iterable(boards):
            for number in row:
                number_in_vectors[number].append(row)

        for col in chain.from_iterable(transposed_boards):
            for number in col:
                number_in_vectors[number].append(col)

        vector_to_boards: DefaultDict[Vector, List[Board]] = defaultdict(list)
        for board, transposed_board in zip(boards, transposed_boards):
            for vector in chain(board, transposed_board):
                vector_to_boards[vector].append(board)

        def find_board() -> Tuple[int, Vector, Board]:
            # Filling of each vector is incremented by 1 when we see a number, Stop at 5
            vector_filling: DefaultDict[Vector, int] = defaultdict(int)
            for i, number in enumerate(draw_numbers):
                vectors_with_number: List[Vector] = number_in_vectors[number]
                for vector in vectors_with_number:
                    vector_filling[vector] += 1
                    if vector_filling[vector] == len(boards[0][0]):
                        print(vector_filling[vector])
                        return i, vector, vector_to_boards[vector][0]

            raise ValueError("No selected board")

        i, v, result = find_board()
        last_number = draw_numbers[i]
        sum_not_draw = sum(set(chain.from_iterable(result)) - set(draw_numbers[:i+1]))
        print(v)
        print(draw_numbers[:i+1])
        print(result)
        print(sum_not_draw * last_number)

def sol2():
    with open("input4.txt") as f:
        iter_f = iter(f)
        draw_numbers = [int(value) for value in next(iter_f).split(',')]
    
        # row
        boards: List[Board] = list(parse_boards(iter_f))
        # columns
        transposed_boards: List[Board] = [tuple(zip(*board)) for board in boards]
    
        number_in_vectors: DefaultDict[int, List[Vector]] = defaultdict(list)
        for row in chain.from_iterable(boards):
            for number in row:
                number_in_vectors[number].append(row)
    
        for col in chain.from_iterable(transposed_boards):
            for number in col:
                number_in_vectors[number].append(col)
            
        vector_to_boards: DefaultDict[Vector, List[Board]] = defaultdict(list)
        for board, transposed_board in zip(boards, transposed_boards):
            for vector in chain(board, transposed_board):
                vector_to_boards[vector].append(board)
    
        def find_board() -> Tuple[int, Vector, Board]:
            # Filling of each vector is incremented by 1 when we see a number, Stop at 5
            # Remove board from the set
            unselected_boards = set(boards)
            vector_filling: DefaultDict[Vector, int] = defaultdict(int)
            for i, number in enumerate(draw_numbers):
                vectors_with_number: List[Vector] = number_in_vectors[number]
                for vector in vectors_with_number:
                    vector_filling[vector] += 1
                    if vector_filling[vector] == len(boards[0][0]):
                        selected_boards = set(vector_to_boards[vector])
                        unselected_boards -= selected_boards
                        if len(unselected_boards) == 0:
                            return i, selected_boards.pop()

                    
            raise ValueError("No selected board")
            
        i, result = find_board()
        last_number = draw_numbers[i]
        sum_not_draw = sum(set(chain.from_iterable(result)) - set(draw_numbers[:i+1]))
        print(draw_numbers[:i+1])
        print(result)
        print(sum_not_draw * last_number)


sol1()
sol2()