Cmd = str
Result = str
Session = list[tuple[Cmd, Result]]


def parse_file(filename: str) -> Session:
    with open(filename) as f:
        return [
            (cmd.split(' '), result)
            for cmd, *result in map(lambda x: x.split('\n'),
                                    f.read().split('$ '))
        ][2:]


session = parse_file('input.txt')


def filesystem(session: Session) -> dict:
    fs = {}
    current_folder = fs
    parent_folder = {}
    for cmd, result in session:
        match cmd:
            case ['cd', next_folder]:
                parent_folder = current_folder
                current_folder = current_folder[next_folder]
            case ['ls', *_]:
                current_folder['..'] = parent_folder
                for file in result:
                    match file.split(' '):
                        case ['dir', dirname]:
                            current_folder[dirname] = {}
                        case [size, name]:
                            current_folder[name] = int(size)
            case _:
                raise ValueError(f'Unexpected {cmd=}')

    return fs


def fs_str(fs: dict, indent_size: int = 0) -> None:
    result = ''
    indent = '  '*indent_size

    for name, value in fs.items():
        if name != '..':
            match value:
                case int(size):
                    result += f'{indent}- {name} {{file, {size=}}}\n'
                case _:
                    result += f'{indent}- {name} (dir)\n'
                    result += fs_str(value, indent_size + 1)
    return result


def print_fs(fs: dict) -> None:
    print(fs_str(fs))


fs = filesystem(session)
# print_fs(fs)


def fs_folder_size(fs: dict) -> list[int]:
    total_size = 0
    folder_sizes = []
    for name, value in fs.items():
        if name != '..':
            match value:
                case int(size):
                    total_size += size
                case _:
                    subfolder_sizes = fs_folder_size(value)
                    total_size += subfolder_sizes[0]
                    folder_sizes += subfolder_sizes

    return [total_size] + folder_sizes


print(fs_folder_size(filesystem(parse_file('test.txt'))))


def test_fs_folder_size():
    fs = filesystem(parse_file('test.txt'))
    assert sum(filter(lambda x: x <= 100_000, fs_folder_size(fs))) == 95437


print(sum(filter(lambda x: x <= 100_000, fs_folder_size(fs))))


def to_delete(fs: dict) -> int:
    sizes = fs_folder_size(fs)
    needed = 3e7 - (7e7 - sizes[0])
    return min(filter(lambda x: x >= needed, sizes))


def test_fs_folder_size_part2():
    fs = filesystem(parse_file('test.txt'))
    assert to_delete(fs) == 24933642


print(to_delete(fs))
