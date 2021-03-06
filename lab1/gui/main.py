import matplotlib
matplotlib.use('TkAgg')

import PySimpleGUI as sg
import matplotlib.pyplot as plt

from lab1.hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

# Read file
initial_message = ''

try:
    with open('./gui/message.txt', 'r+') as file:
        initial_message = file.readline()
except IOError:
    initial_message = ''


# Configure GUI
sg.theme('Reddit')

main_layout = [
    [sg.Text('Message:', size=(8, 1)), sg.Input(key='message', default_text=initial_message), sg.Button('Hash', key='generate')],
    [sg.Text('Hash:', size=(8, 1)), sg.Multiline(key='hash', disabled=True)],
]

graph_layout = [
    [sg.Text('Bit to change:'), sg.Input(key='bit', default_text='0'), sg.Button('Graph', key='graph')],
    [sg.Text('Hash:', size=(8, 1)), sg.Multiline(key='hash_changed', disabled=True)],
]

layout = [
    [sg.Frame('Generate RIPEMD-320', main_layout, key='frame1')],
    [sg.Frame('Avalanche Effect', graph_layout, key='frame2')],
]

window = sg.Window('RIPEMD-320', layout, size=(600, 250), font=('Fira Code Retina', 10), finalize=True)
window['bit'].expand(expand_x=True)
window['hash'].expand(expand_x=True)
window['hash_changed'].expand(expand_x=True)
window['message'].expand(expand_x=True)
window['frame1'].expand(expand_x=True)
window['frame2'].expand(expand_x=True)

while True:         # Event Loop
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Quit'):     # if all windows were closed
        break
    elif event == 'graph':                      # if 'graph' button was pressed
        # Read values from inputs
        message = values['message'] if values['message'] else ''
        # Try to parse string as int
        try:
            bit_to_change = int(values['bit'])
        except ValueError:
            window['bit'].update('0')
            continue

        # Clamp bit_to_change from 0 to len(message) in bits
        bit_to_change = max(0, min(bit_to_change, (len(message) << 3) - 1))
        # Calculate hash and number of changed bits on each round
        hash_val, bits = py_ripemd320_with_shift(message, bit_to_change)

        window['hash_changed'].update(hash_val)

        # Clear and setup figure
        plt.subplots_adjust(bottom=0.2)
        plt.clf()

        # Plot avalanche effect
        x = range(1, len(bits) + 1)
        plt.plot(x, bits, color='tab:red', label=f'bit {bit_to_change}')

        # Plot changed bits when on default hash
        x = range(1, len(bits) + 1)
        bits = py_ripemd320(message)[1]
        plt.plot(x, bits, color='black', label=f'default')

        plt.ylabel('Changed bits')
        plt.xlabel('Round')
        plt.title(f'Message: "{message}"\nLength: {len(message) << 3} bits')

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=5)
        plt.show(block=False)
    elif event == 'generate':                   # if 'hash' button was pressed
        # Generate hash from 'message' input and put it in 'hash' input
        hash_val = py_ripemd320(values['message'])[0]
        window['hash'].update(hash_val)
