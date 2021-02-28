import matplotlib
matplotlib.use('TkAgg')

import PySimpleGUI as sg
import matplotlib.pyplot as plt

from hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

sg.theme('Reddit')

layout = [
    [sg.Text('Message:', size=(14, 1)), sg.InputText(key='message'), sg.Button('Hash', key='generate')],
    [sg.Text('Hash:', size=(14, 1)), sg.InputText(key='hash', readonly=True)],
    [sg.Text('Bit to change:', size=(14, 1)), sg.Input(key='bit', default_text='0'), sg.Button('Graph', key='graph')],
]

window = sg.Window('RIPEMD-320', layout, size=(800, 150), font=('Fira Code Retina', 10), finalize=True)
window['bit'].expand(expand_x=True)
window['hash'].expand(expand_x=True)
window['message'].expand(expand_x=True)

# Event Loop
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Quit'):  # if all windows were closed
        break
    elif event == 'graph':
        message = values['message']
        bit_to_change = int(values['bit'])

        md, bits = py_ripemd320_with_shift(message, bit_to_change)

        x = range(1, len(bits) + 1)
        p1 = plt.plot(x, bits, color='b', label=f'bit {bit_to_change}')

        plt.ylabel('Changed bits')
        plt.xlabel('Round')
        plt.title(f'Message: "{message}"\nLength: {len(message) << 3} bits')

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True)
        plt.show()
    elif event == 'generate':
        hash_val = py_ripemd320(values['message'])
        window['hash'].update(hash_val)
