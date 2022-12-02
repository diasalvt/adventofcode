from functools import reduce
from itertools import islice
from collections import deque, defaultdict
from typing import *
from math import prod

test = """D2FE28"""
test2 = "38006F45291200"
test3 = "EE00D40C823060"

tests_sum_version = {
    '8A004A801A8002F478': 16,
    '620080001611562C8802118E34': 12,
    'C0015000016115A2E0802F182340': 23,
    'A0016C880162017C3686B18A3D4780': 31
}

Character = str
ID = int
Bits =str

def int_to_nbits(value: int, n: int = 4) -> Bits:
    res = ''
    for i in range(n):
        res += str(value % 2)
        value = value // 2

    return res[::-1]

hex_to_bits:Dict[Character, Bits] = {c: int_to_nbits(i) for i, c in enumerate('0123456789ABCDEF')}

def str_to_bits(code: str) -> Iterator[Bits]:
    return (hex_to_bits[c] for c in code)

cat = ''.join

class BitStream:
    def __init__(self, code):
        self.bit_code = str_to_bits(code)
        self.buffer = deque([])

    def __iter__(self):
        return self

    def __next__(self):
        if not self.buffer:
            self.buffer.extend(next(self.bit_code))
        return self.buffer.popleft()

    def next_bits(self, n: int) -> Bits:
        return cat(islice(self, n))
        
    def __repr__(self):
        return f'BitsReader: \nBuffer {self.buffer}\n Rest: {list(self.bit_code)}'

class PacketInfo:
    def __init__(self, version, id, bit_consumed):
        self.version = version
        self.id = id
        self.bit_consumed = bit_consumed
        
    def __repr__(self):
        return f'PacketInfo: version{self.version}, id={self.id}, bit_consumed={self.bit_consumed}'

class Operator:
    def __init__(self, packetinfo: PacketInfo, * , max_packet=None, length=None):
        self.packets: List['Packet'] = []
        self.max_packet = max_packet
        self.max_bitlen = length
        self.packetinfo = packetinfo

    def add_packet(self, packet):
        self.packets.append(packet)
        self.packetinfo.bit_consumed += packet.packetinfo.bit_consumed

    def sum_version(self):
        return self.packetinfo.version + sum(p.sum_version() for p in self.packets)

    def val(self) -> int:

        ops = {
            0: sum,
            1: prod,
            2: min,
            3: max,
            5: lambda x: int(x[0] > x[1]),
            6: lambda x: int(x[0] < x[1]),
            7: lambda x: int(x[0] == x[1]),
        }
        return ops[self.packetinfo.id]([p.val() for p in self.packets])

    def __repr__(self):
        if self.max_packet is not None:
            return f'Operator[max_packet={self.max_packet}] id={self.packetinfo.id} {self.packets}'
        else:
            return f'Operator[max_bits={self.max_bitlen}] id={self.packetinfo.id} {self.packets}'


class Value:
    def __init__(self, value, packetinfo: PacketInfo) -> None:
        self.value = value
        self.packetinfo = packetinfo

    def __repr__(self):
        return f'Value: {self.value}'

    def sum_version(self):
        return self.packetinfo.version

    def val(self) -> int:
        return self.value

Packet = Union[Value, Operator]

def next_bits(bit_stream, n, packetinfo):
    r = bit_stream.next_bits(n)
    packetinfo.bit_consumed += len(r)

    return r

def read_litteral(bit_stream: BitStream, packetinfo) -> Packet:
    bits = next_bits(bit_stream, 5, packetinfo)
    res = ''
    while bits[0] != '0':
        res += bits[1:]
        bits = next_bits(bit_stream, 5, packetinfo)
    res += bits[1:]

    return Value(int(res, 2), packetinfo)

def read_operator(bit_stream: BitStream, packetinfo) -> Packet:
    # Read mode
    b = next_bits(bit_stream, 1, packetinfo)
    if b == '0':
        len_sub_packet = int(next_bits(bit_stream, 15, packetinfo), 2)
        op = Operator(packetinfo, length=len_sub_packet)
        bit_consumed = op.packetinfo.bit_consumed
        while op.packetinfo.bit_consumed < (bit_consumed + op.max_bitlen):
            op.add_packet(read_packet(bit_stream))
    else:
        nb_sub_packet = int(next_bits(bit_stream, 11, packetinfo), 2)
        op = Operator(packetinfo, max_packet=nb_sub_packet)
        for i in range(op.max_packet):
            op.add_packet(read_packet(bit_stream))
    
    return op

packet_reader: DefaultDict[ID, Callable] = defaultdict(lambda: read_operator)

packet_reader[4] = read_litteral

def read_packet(bit_stream: BitStream) -> Packet:
    # Read Header
    version, id = int(bit_stream.next_bits(3), 2), int(bit_stream.next_bits(3), 2)

    packetinfo = PacketInfo(version, id, 6)
    return packet_reader[id](bit_stream, packetinfo)

def code_to_packet(code: str) -> Packet:
    b = BitStream(code)
    return read_packet(b)

test_code = "D8005AC2A8F0"
print(code_to_packet(test2))

#for code, res in tests_sum_version.items():
#    p = code_to_packet(code)
#    print(f'{p.sum_version()} == {res}')

with open("input16.txt") as f:
    code = list(f)[0].strip()
    
print(code_to_packet(code).val())