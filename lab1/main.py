from hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

import numpy as np
import matplotlib.pyplot as plt


def plot_avalanche_effect(changed_bits, **kwargs):
    x = np.arange(1, len(changed_bits) + 1)
    plt.plot(x, changed_bits, **kwargs)


def main():
    message = 'a'

    # Change first bit
    bit_to_change = 0
    md, bits = py_ripemd320_with_shift(message, bit_to_change)
    plot_avalanche_effect(bits, color='r', label=f'bit {bit_to_change}')

    # Change first middle bit
    bit_to_change = len(message) << 2
    md, bits = py_ripemd320_with_shift(message, bit_to_change)
    plot_avalanche_effect(bits, color='b', label=f'bit {bit_to_change}')

    # Change last bit
    bit_to_change = len(message) << 3
    md, bits = py_ripemd320_with_shift(message, bit_to_change)
    plot_avalanche_effect(bits, color='g', label=f'bit {bit_to_change}')

    # Setup plot
    plt.title(f'Message: "{message}"\nLength: {len(message) << 3} bits')
    plt.ylabel('Changed bits')
    plt.xlabel('Round')

    plt.legend(loc=1, shadow=True, ncol=1)

    plt.show()


if __name__ == '__main__':
    main()
