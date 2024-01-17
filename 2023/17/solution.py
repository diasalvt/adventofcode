def load(filename: str) -> dict[complex, int]:
    return {
        complex(i, j): c
        for i, row in enumerate(open(filename))
        for j, c in enumerate(row.strip())
    }


test = load('test.txt')
print(test)
