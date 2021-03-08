from lab2.ansi_x9_17 import generate_sequence, convert_to_dec_and_bin
from lab2.statistical_tests import *


def main():
    key1, key2 = '12345678', '87654321'
    seed = 'examples'
    m = 2

    sequence = generate_sequence(key1, key2, seed, m)
    sequence_dec, sequence_bin = convert_to_dec_and_bin(sequence)

    print(f'Sequence dec:\n{sequence_dec}\n')
    print(f'Sequence bin:\n{sequence_bin}\n')

    results = frequency_test(sequence_bin), identical_bits_test(sequence_bin), arbitrary_deviations_test(sequence_bin)
    print(f'Tests results: {results}')


if __name__ == '__main__':
    main()
