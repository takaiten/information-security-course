from lab1.hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

import matplotlib.pyplot as plt
import yaml


def read_data():
    try:
        with open(r'./cli/data.yml') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except IOError:
        exit('No data file')


def plot_avalanche_effect(changed_bits, ax, **kwargs):
    x = range(1, len(changed_bits) + 1)
    ax.plot(x, changed_bits, **kwargs)


def generate_hash_and_plot(message, bit_to_change, ax, cmap):
    md, bits = py_ripemd320_with_shift(message=message, bit_pos=bit_to_change)
    plot_avalanche_effect(changed_bits=bits, ax=ax, color=cmap(bit_to_change), label=f'bit {bit_to_change}')
    print(f'Changed bit: {bit_to_change}')
    print(f'Hash: {md}\n')


def main():
    # read messages and bits from file
    data = read_data()

    # loop for each message
    for index, item in enumerate(data, start=1):
        # if no message then use empty
        message = item['message'] if 'message' in item else ''
        print('_' * 100)
        print(f'Message: {message}')
        print(f'Default hash: {py_ripemd320(message)}\n')

        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)

        # set parameters: bits to change and colors
        bits_to_change = item['bits'] if 'bits' in item else [0, len(message) << 2, len(message) << 3]
        if len(bits_to_change) > 5:
            bits_to_change = bits_to_change[:5]

        cmap = plt.cm.get_cmap('Set1', len(message) << 3)

        # generate hashes with different parameters
        for bit in bits_to_change:
            generate_hash_and_plot(message=message, bit_to_change=bit, ax=ax, cmap=cmap)

        # Setup plot
        ax.set_title(f'Message: "{message}"\nLength: {len(message) << 3} bits')
        ax.set_ylabel('Changed bits')
        ax.set_xlabel('Round')

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=5)

        fig.savefig(f'./cli/output/avalanche_effect_{index}.png')


if __name__ == '__main__':
    main()
