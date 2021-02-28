from hashpkg.ripemd320 import py_ripemd320_with_shift, py_ripemd320

import PySimpleGUI as sg


layout = [
    [sg.Text('Message:', size=(8, 1)), sg.InputText(key='message'), sg.Button('Hash', key='generate')],
    [sg.Text('Hash:', size=(8, 1)), sg.InputText(key='hash', readonly=True)],
]

window = sg.Window('RIPEMD-320...', layout, size=(770, 80), font=('Fira Code Retina', 10), finalize=True)
window['hash'].expand(expand_x=True)
window['message'].expand(expand_x=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Quit'):
        break
    elif event == 'generate':
        hash_val = py_ripemd320(values['message'])
        print(len(hash_val) << 3)
        window['hash'].update(hash_val)

window.close()
