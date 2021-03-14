from typing import List
from numpy import sqrt, count_nonzero, array

QUANTILE = 1.82138636


def frequency_test(bit_sequence: str) -> (bool, float):
    n = len(bit_sequence)
    s = (bit_sequence.count('1') - bit_sequence.count('0')) / sqrt(n)

    return s <= QUANTILE, s


def identical_bits_test(bit_sequence: str) -> (bool, float, float, float):
    n = len(bit_sequence)
    p = bit_sequence.count('1') / n

    v = 1 + sum([bit_sequence[k] != bit_sequence[k + 1] for k in range(n - 1)])

    s = abs(v - 2 * n * p * (1 - p)) / (2 * p * (1 - p) * sqrt(2 * n))

    return s <= QUANTILE, p, v, s


def arbitrary_deviations_test(bit_sequence: str) -> (bool, List[int], List[float], int):
    n = len(bit_sequence)
    sequence = [2 * int(x) - 1 for x in bit_sequence]

    s = [0, sequence[0]]
    for i in range(1, n):
        s.append(s[i] + sequence[i])
    s.append(0)

    l = count_nonzero(array(s) == 0) - 1

    e, y = [], []
    for j in range(-9, 10):
        if j == 0:
            continue
        e.append(s.count(j))
        y.append(abs(e[-1] - l) / sqrt(2 * l * (abs(j) * 4 - 2)))

    return count_nonzero(array(y) > QUANTILE) == 0, e, y, l
