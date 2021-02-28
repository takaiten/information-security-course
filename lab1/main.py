from hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

import matplotlib.pyplot as plt
import yaml


def read_data():
    with open(r'data.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def plot_avalanche_effect(changed_bits, ax, **kwargs):
    x = range(1, len(changed_bits) + 1)
    ax.plot(x, changed_bits, **kwargs)


def generate_hash_and_plot(message, bit_to_change, ax, color):
    md, bits = py_ripemd320_with_shift(message, bit_to_change)
    plot_avalanche_effect(bits, ax, color=color, label=f'bit {bit_to_change}')
    print(f'Changed bit: {bit_to_change}')
    print(f'Hash: {md}\n')


def main():
    data = read_data()

    for index, message in enumerate(data['messages'], start=1):
        print('_' * 100)
        print(f'Message: {message}')
        print(f'Default hash: {py_ripemd320(message)}\n')

        fig, ax = plt.subplots()

        # set parameters
        bits_to_change = [0, len(message) << 2, len(message) << 3]
        colors = ['r', 'b', 'g']

        # generate hashes with different parameters
        for bit_to_change, color in zip(bits_to_change, colors):
            generate_hash_and_plot(message, bit_to_change, ax, color)

        # Setup plot
        ax.set_title(f'Message: "{message}"\nLength: {len(message) << 3} bits')
        ax.set_ylabel('Changed bits')
        ax.set_xlabel('Round')

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=len(bits_to_change))

        fig.savefig(f'./output/avalanche_effect_{index}.png')
        # fig.show()


if __name__ == '__main__':
    main()
