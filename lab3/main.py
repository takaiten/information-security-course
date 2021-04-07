import PySimpleGUI as sg
from functools import reduce

from lab3.bytes_utils import *
from lab3.crypto_utils import *

sg.theme('Reddit')

ALLOWED_FILE_TYPES = (('Text files', '*.txt'), ('Key files', '*.key'),)
DEFAULT_FRAME_PAD = (7, 7)
DEFAULT_BUTTON_SIZE = (19, 1)

SYMMETRIC = {'DES': handle_des, 'AES': handle_aes, 'Blowfish': handle_blowfish}
ASYMMETRIC = {'PKCS1 OAEP': handle_pkcs1_oaep}
CIPHERING = reduce(lambda x, y: dict(x, **y), (SYMMETRIC, ASYMMETRIC))
HASH = {'SHA256': hash_sha256, 'MD5': hash_md5, 'Ripemd160': hash_ripemd160}
SIGNATURE = {'PSS': signature_pss}


def get_default_algorithm(algorithms: dict):
    return list(algorithms.keys())[0]


def create_file_button(title: str, button_type=sg.FileBrowse):
    return button_type(title, file_types=ALLOWED_FILE_TYPES, size=DEFAULT_BUTTON_SIZE)


#  ### DEFINE LAYOUTS ### #

symmetric_layout = [
    [sg.Radio(x, 'ciphering', key=x, default=x == get_default_algorithm(CIPHERING)) for x in SYMMETRIC.keys()]
]

asymmetric_layout = [
    [sg.Radio(x, 'ciphering', key=x) for x in ASYMMETRIC.keys()]
]

ciphering_layout = [
    [sg.Frame('Symmetric', symmetric_layout, pad=DEFAULT_FRAME_PAD),
     sg.Frame('Asymmetric', asymmetric_layout, pad=DEFAULT_FRAME_PAD)],
    [sg.Input(key='-KEY_PATH-'), create_file_button('Select file with key')],
    [sg.Input(key='-CIPHERTEXT_PATH-'), create_file_button('Select file with ciphertext', sg.FileSaveAs)],
    [sg.Input(key='-PLAINTEXT_PATH-'), create_file_button('Select file with plaintext', sg.FileSaveAs)],
    [sg.Button('Encrypt plaintext file', key='-ENCRYPT-', button_color=('white', 'darkred'), size=DEFAULT_BUTTON_SIZE),
     sg.Button('Decrypt ciphertext file', key='-DECRYPT-', button_color=('white', 'green'), size=DEFAULT_BUTTON_SIZE)]
]

hash_layout = [
    [sg.Frame('Hash algorithm',
              [[sg.Radio(x, 'hash', key=x, default=x == get_default_algorithm(HASH)) for x in HASH.keys()]],
              border_width=3)],
    [sg.Input(key='-HASH_MESSAGE_PATH-'), create_file_button('Select file with message')],
    [sg.Input(key='-HASH_PATH-'), create_file_button('Select file with hash', sg.FileSaveAs)],
    [sg.Button('Hash message', key='-HASH-', button_color=('white', 'darkred'), size=DEFAULT_BUTTON_SIZE)]
]

signature_layout = [
    [sg.Text('Signature PKCS#1 PSS (RSA)')],
    [sg.Input(key='-RSA_KEY_PATH-'), create_file_button('Select file with key')],
    [sg.Input(key='-SIGN_MESSAGE_PATH-'), create_file_button('Select file with message')],
    [sg.Input(key='-SIGN_PATH-'), create_file_button('Select file with signature', sg.FileSaveAs)],
    [sg.Button('Sign message', key='-SIGN-', button_color=('white', 'darkred'), size=DEFAULT_BUTTON_SIZE),
     sg.Button('Verify', key='-VERIFY-', button_color=('white', 'green'), size=DEFAULT_BUTTON_SIZE)]
]

# ### DEFINE TAB LAYOUTS ### #

tab_group_layout = [[
    sg.Tab('Ciphering', ciphering_layout, key='-TAB1-'),
    sg.Tab('Hash', hash_layout, key='-TAB2-'),
    sg.Tab('Signature', signature_layout, key='-TAB3-'),
]]

layout = [[
    sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')
]]

window = sg.Window('LAB3', layout, no_titlebar=False)

# ### METHODS ### #


def error_popup(text: str, *args, **kwargs):
    sg.popup_error(text, auto_close=True, auto_close_duration=5, *args, **kwargs)


def popup(text: str, *args, **kwargs):
    sg.popup(text, auto_close=True, auto_close_duration=5, *args, **kwargs)


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
    return reduce(lambda acc, key: acc & (len(values_dict[key].strip()) > 0), required_fields, True)


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
    key = read_from_file(values_dict['-KEY_PATH-'])

    try:
        result = CIPHERING[algorithm](convert_input(data), encode_utf8(key), mode)
        write_to_file(save_path, convert_output(result))
        popup(f'Successfully {mode}ed', title='Success')
    except TypeError or ValueError as error:
        error_popup(error, title='Ciphering error')


# ### SIGNATURE ### #

def handle_signature(values_dict: dict):
    data = read_from_file(values_dict['-SIGN_MESSAGE_PATH-'])
    key = read_from_file(values_dict['-RSA_KEY_PATH-'])

    try:
        result = signature_pss(encode_utf8(data), encode_utf8(key))
        write_to_file(values_dict['-SIGN_PATH-'], bytes_to_hex(result))
        popup('Successfully created signature', title='Success')
    except TypeError or ValueError as error:
        error_popup(error, title='Signature error')


def verify_signature(values_dict: dict):
    data = read_from_file(values_dict['-SIGN_MESSAGE_PATH-'])
    key = read_from_file(values_dict['-RSA_KEY_PATH-'])
    signature = read_from_file(values_dict['-SIGN_PATH-'])

    try:
        verify_signature_pss(encode_utf8(data), encode_utf8(key), bytes_from_hex(signature))
        popup('Signature verified', title='Success')
    except ValueError as error:
        error_popup(error, title="Couldn't verify signature")


# ### HASH ### #

def handle_hash(values_dict: dict):
    [algorithm] = [k for k in HASH.keys() if values_dict[k]]

    data = read_from_file(values_dict['-HASH_MESSAGE_PATH-'])

    try:
        result = HASH[algorithm](encode_utf8(data))
        write_to_file(values_dict['-HASH_PATH-'], result)
        popup('Successfully hashed', title='Success')
    except TypeError or ValueError as error:
        error_popup(error, title='Hash error')


# ### EVENT LOOP ### #

while True:
    event, values = window.read()  # type: str, dict

    if event == sg.WIN_CLOSED:
        break
    elif event in ['-ENCRYPT-', '-DECRYPT-']:
        if not validate_fields(values, ['-PLAINTEXT_PATH-', '-CIPHERTEXT_PATH-', '-KEY_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        handle_ciphering(event, values)
    elif event == '-HASH-':
        if not validate_fields(values, ['-HASH_MESSAGE_PATH-', '-HASH_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        handle_hash(values)
    elif event == '-SIGN-':
        if not validate_fields(values, ['-RSA_KEY_PATH-', '-SIGN_MESSAGE_PATH-', '-SIGN_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        handle_signature(values)
    elif event == '-VERIFY-':
        if not validate_fields(values, ['-RSA_KEY_PATH-', '-SIGN_MESSAGE_PATH-', '-SIGN_PATH-']):
            error_popup('Please select all the files', title='Validation error')
            continue

        verify_signature(values)

window.close()
