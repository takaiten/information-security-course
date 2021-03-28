import PySimpleGUI as sg
from functools import reduce
from lab3.bytes_utils import *
from lab3.crypto_utils import *

sg.theme('Reddit')

ALLOWED_FILE_TYPES = (('Text files', '*.txt'),)
DEFAULT_FRAME_PAD = (7, 7)

SYMMETRIC = {'DES': handle_des, 'AES': handle_aes, 'Blowfish': handle_blowfish}
DEFAULT_SYMMETRIC = list(SYMMETRIC.keys())[0]

ASYMMETRIC = {'PKCS1 OAEP': handle_pkcs1_oaep}
DEFAULT_ASYMMETRIC = list(SYMMETRIC.keys())[0]

CIPHERING = reduce(lambda x, y: dict(x, **y), (SYMMETRIC, ASYMMETRIC))


#  ### DEFINE LAYOUTS ### #

symmetric_layout = [
    [sg.Radio(x, 'algorithm', key=x, default=x == DEFAULT_SYMMETRIC) for x in SYMMETRIC.keys()]
]

asymmetric_layout = [
    [sg.Radio(x, 'algorithm', key=x, default=x == DEFAULT_ASYMMETRIC) for x in ASYMMETRIC.keys()]
]

ciphering_layout = [
    [sg.Frame('Choose ciphering algorithm',
              [[sg.Frame('Symmetric', symmetric_layout, key='generation', pad=DEFAULT_FRAME_PAD),
                sg.Frame('Asymmetric', asymmetric_layout, key='tests', pad=DEFAULT_FRAME_PAD)]],
              border_width=3)],

    [sg.Input(key='-KEY_PATH-'), sg.FileBrowse('Select file with key', file_types=ALLOWED_FILE_TYPES)],
    [sg.Input(key='-CIPHERTEXT_PATH-'), sg.FileSaveAs('Select file with ciphertext', file_types=ALLOWED_FILE_TYPES)],
    [sg.Input(key='-PLAINTEXT_PATH-'), sg.FileSaveAs('Select file with plaintext', file_types=ALLOWED_FILE_TYPES)],
    [sg.Button('Encrypt plaintext file', key='-ENCRYPT-', button_color=('white', 'red')),
     sg.Button('Decrypt ciphertext file', key='-DECRYPT-', button_color=('white', 'red'))]
]

signature_layout = [

]

hash_layout = [

]

# ### DEFINE TAB LAYOUTS ### #

tab_group_layout = [[
    sg.Tab('Ciphering', ciphering_layout, key='-TAB1-'),
    sg.Tab('Signature', signature_layout, key='-TAB2-'),
    sg.Tab('Hash', hash_layout, key='-TAB3-'),
]]

layout = [[
    sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')
]]

window = sg.Window('LAB3', layout, no_titlebar=False)


# ### METHODS ### #

def error_popup(text: str, *args, **kwargs):
    sg.popup_error(text, auto_close=True, auto_close_duration=5, *args, **kwargs)


def read_from_file(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except IOError as error:
        error_popup(error, title='IO Error')


def write_to_file(filepath: str, data: str):
    if data is None:
        return
    try:
        with open(filepath, 'w+') as f:
            f.write(data)
    except IOError as error:
        error_popup(error, title='IO Error')


def validate_fields(values_dict: dict, required_fields=[]):
    return [key for key in required_fields if len(values_dict[key].strip())] != required_fields


# ### CIPHERING ### #

def config_ciphering_params(event_key: str, values_dict: dict):
    """
    Configure parameters for ciphering
    :param event_key: name of GUI event
    :param values_dict: GUI values dictionary
    :return: input data file path,
             output data file path,
             mode (encrypt or decrypt),
             function to convert input data,
             function to convert output data
    """
    if event_key == '-ENCRYPT-':
        return (values_dict['-PLAINTEXT_PATH-'], values_dict['-CIPHERTEXT_PATH-'],
                'encrypt', encode_utf8, bytes_to_hex)
    elif event_key == '-DECRYPT-':
        return (values_dict['-CIPHERTEXT_PATH-'], values_dict['-PLAINTEXT_PATH-'],
                'decrypt', bytes_from_hex, decode_utf8)
    else:
        raise ValueError(f'main.config_ciphering_params: Unable to handle event: {event_key}')


def handle_ciphering(event_key: str, values_dict: dict):
    input_path, save_path, mode, convert_input, convert_output = config_ciphering_params(event_key, values_dict)
    [algorithm] = [k for k in CIPHERING.keys() if values_dict[k]]

    data = read_from_file(input_path)
    key = encode_utf8(read_from_file(values_dict['-KEY_PATH-']))

    try:
        result = CIPHERING[algorithm](convert_input(data), key, mode)
        write_to_file(save_path, convert_output(result))
    except TypeError or ValueError as error:
        error_popup(error, title='Ciphering error')


while True:
    event, values = window.read()  # type: str, dict
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event in ['-ENCRYPT-', '-DECRYPT-']:
        if validate_fields(values, ['-PLAINTEXT_PATH-', '-CIPHERTEXT_PATH-', '-KEY_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        handle_ciphering(event, values)

window.close()
