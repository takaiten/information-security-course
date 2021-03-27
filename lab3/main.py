import PySimpleGUI as sg
from utils import *

sg.theme('Reddit')

ALLOWED_FILE_TYPES = (('Text files', '*.txt'),)
SYMMETRIC = {'DES': handle_des, 'AES': handle_aes, 'Blowfish': handle_blowfish}
DEFAULT_SYMMETRIC = list(SYMMETRIC.keys())[0]


def error_popup(text: str, *args, **kwargs):
    sg.popup_error(text, auto_close=True, auto_close_duration=5, *args, **kwargs)


## Define layouts ##
symmetric_layout = [
    # [sg.Text('Choose symmetric algorithm')],
    # [sg.Radio(x, 'algorithm', key=x, default=x == 'DES') for x in ['DES', 'AES', 'Blowfish']],
    [sg.Frame('Choose symmetric algorithm',
              [[sg.Radio(x, 'algorithm', key=x, default=x == DEFAULT_SYMMETRIC) for x in SYMMETRIC.keys()]])],
    [sg.Input(key='-KEY_PATH-'), sg.FileBrowse('Select file with key', file_types=ALLOWED_FILE_TYPES)],
    [sg.Input(key='-CIPHERTEXT_PATH-'), sg.FileSaveAs('Select file with ciphertext', file_types=ALLOWED_FILE_TYPES)],
    [sg.Input(key='-PLAINTEXT_PATH-'), sg.FileSaveAs('Select file with plaintext', file_types=ALLOWED_FILE_TYPES)],
    [sg.Button('Encrypt plaintext file', key='-ENCRYPT-', button_color=('white', 'red')),
     sg.Button('Decrypt ciphertext file', key='-DECRYPT-', button_color=('white', 'red'))]
]

asymmetric_layout = [
    [sg.FileSaveAs('Select file with ciphertext')],
    [sg.FileSaveAs('Select file with plaintext')]
]

signature_layout = [

]

hash_layout = [

]

## Define tab layouts ##
tab_group_layout = [[
    sg.Tab('Symmetric', symmetric_layout, key='-TAB1-'),
    sg.Tab('Asymmetric', asymmetric_layout, key='-TAB2-'),
    sg.Tab('Signature', signature_layout, key='-TAB3-'),
    sg.Tab('Hash', hash_layout, key='-TAB4-'),
]]

layout = [[
    sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')
]]

window = sg.Window('LAB3', layout, no_titlebar=False)


def read_from_file(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except IOError as error:
        error_popup(error, title='IO Error')


def write_to_file(filepath: str, data: str):
    if data is None: return
    try:
        with open(filepath, 'w+') as f:
            f.write(data)
    except IOError as error:
        error_popup(error, title='IO Error')


def validate_fields(values_dict: dict, required_fields=[]):
    return [key for key in required_fields if len(values_dict[key].strip())] != required_fields


def handle_symmetric(event_key: str, values_dict: dict):
    if event_key == '-ENCRYPT-':
        input_path = values_dict['-PLAINTEXT_PATH-']
        save_path = values_dict['-CIPHERTEXT_PATH-']
        mode = 'encrypt'
    elif event_key == '-DECRYPT-':
        input_path = values_dict['-CIPHERTEXT_PATH-']
        save_path = values_dict['-PLAINTEXT_PATH-']
        mode = 'decrypt'
    else:
        return

    [algorithm] = [k for k in SYMMETRIC.keys() if values_dict[k]]

    key = read_from_file(values_dict['-KEY_PATH-']).encode('UTF-8')
    data = read_from_file(input_path)

    try:
        result = SYMMETRIC[algorithm](data.encode('UTF-8') if mode == 'encrypt' else bytes.fromhex(data), key, mode)
        write_to_file(save_path, result.hex() if mode == 'encrypt' else result.decode('UTF-8'))
    except TypeError or ValueError as error:
        error_popup(error, title='Symmetric error')


while True:
    event, values = window.read()  # type: str, dict
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event in ['-ENCRYPT-', '-DECRYPT-']:
        if validate_fields(values, ['-PLAINTEXT_PATH-', '-CIPHERTEXT_PATH-', '-KEY_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        handle_symmetric(event, values)

window.close()
