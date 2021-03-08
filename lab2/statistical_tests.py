from numpy import sqrt, count_nonzero


QUANTILE = 1.82138636


def frequency_test(bit_sequence: str) -> bool:
    n = len(bit_sequence)
    s = (bit_sequence.count('1') - bit_sequence.count('0')) / sqrt(n)

    return s <= QUANTILE


def identical_bits_test(bit_sequence: str) -> bool:
    n = len(bit_sequence)
    p = bit_sequence.count('1') / n
    v = 1 + count_nonzero([lambda k: bit_sequence[k] != bit_sequence[k + 1] for i in range(n - 1)])

    s = abs(v - 2 * n * p * (1 - p)) / (2 * p * (1 - p) * sqrt(2 * n))

    return s <= QUANTILE


def arbitrary_deviations_test(bit_sequence: str) -> bool:
    n = len(bit_sequence)
    sequence = [2 * int(x) - 1 for x in bit_sequence]

    s = [0, sequence[0]]
    for i in range(1, n):
        s.append(s[i] + sequence[i])
    s.append(0)

    l = n + 2 - count_nonzero(s)

    y = []
    for j in range(-9, 10):
        if j == 0:
            continue
        e = s.count(j)
        y.append(abs(e - l) / sqrt(2 * l * (abs(j) * 4 - 2)))

    return count_nonzero([x <= QUANTILE for x in y]) == 18
