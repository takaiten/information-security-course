from lab2.ansi_x9_17 import generate_sequence, convert_to_bin_and_hex
from lab2.statistical_tests import *

import PySimpleGUI as sg

EMPTY_STR = ''
DEFAULT_KEY1 = '12345678'
DEFAULT_KEY2 = '87654321'
DEFAULT_SEED = 'examples'
DEFAULT_BLOCKS = 2

DEFAULT_FRAME_PAD = (7, 7)
DEFAULT_TEXT_SIZE = (11, 1)
DEFAULT_BUTTON_SIZE = (10, 1)


def create_default_input(text, key, input_type=sg.Input):
    return [sg.Text(text, DEFAULT_TEXT_SIZE), input_type(key=key, disabled=True)]


sg.theme('Reddit')

main_layout = [
    [sg.Text('Key1:', size=(7, 1)), sg.Input(key='key1', default_text=DEFAULT_KEY1)],
    [sg.Text('Key2:', size=(7, 1)), sg.Input(key='key2', default_text=DEFAULT_KEY2)],
    [sg.Text('Seed:', size=(7, 1)), sg.Input(key='seed', default_text=DEFAULT_SEED)],
    [sg.Text('Blocks:', size=(7, 1)), sg.Input(key='blocks', default_text=DEFAULT_BLOCKS)],
    [sg.Text('File:', size=(7, 1)), sg.Input(key='file', default_text=EMPTY_STR, disabled=True),
     sg.FileBrowse(key='browse', file_types=(("TXT", "*.txt"),), size=DEFAULT_BUTTON_SIZE)],
    [sg.Button('Generate', key='generate', size=DEFAULT_BUTTON_SIZE),
     sg.Button('Save', key='save', size=DEFAULT_BUTTON_SIZE)],
]

sequence_layout = [
    [sg.Text('Hex:', size=(4, 1)), sg.Multiline(key='hex', disabled=True)],
    [sg.Text('Bin:', size=(4, 1)), sg.Multiline(key='bin', disabled=True)],
]

quantile_layout = [
    create_default_input('Quantile:', 'quantile')
]

test1_layout = [
    create_default_input('Result:', 'test1_result'),
    create_default_input('Statistics:', 'test1_stat'),
]

test2_layout = [
    create_default_input('Result:', 'test2_result'),
    create_default_input('Pi:', 'test2_pi'),
    create_default_input('V:', 'test2_v'),
    create_default_input('Statistics:', 'test2_stat'),
]

test3_layout = [
    create_default_input('Result:', 'test3_result'),
    create_default_input('L:', 'test3_l'),
    create_default_input('Statistics:', 'test3_s', sg.Multiline),
]

layout1 = [
    [sg.Frame('Generate ANSI X9.17', main_layout, key='frame1', pad=DEFAULT_FRAME_PAD, element_justification='right')],
    [sg.Frame('Sequence', sequence_layout, key='frame2', pad=DEFAULT_FRAME_PAD)],
]

layout2 = [
    [sg.Frame('Constants', quantile_layout, key='frame6', pad=DEFAULT_FRAME_PAD)],
    [sg.Frame('Frequency test', test1_layout, key='frame3', pad=DEFAULT_FRAME_PAD)],
    [sg.Frame('Identical bits test', test2_layout, key='frame4', pad=DEFAULT_FRAME_PAD)],
    [sg.Frame('Arbitrary deviations test', test3_layout, key='frame5', pad=DEFAULT_FRAME_PAD)],
]

layout = [
    [sg.Frame('Generation', layout1, key='generation', pad=DEFAULT_FRAME_PAD, border_width=3),
     sg.Frame('Tests', layout2, key='tests', pad=DEFAULT_FRAME_PAD, border_width=3)]
]

window = sg.Window('ANSI X9.17', layout, size=(1600, 550), font=('Fira Code Retina', 10), finalize=True)


def set_expand_true(keys: List[str]):
    for key in keys:
        window[key].expand(expand_x=True, expand_y=True)


set_expand_true(['key1', 'key2', 'seed', 'blocks', 'file', 'hex', 'bin', 'quantile',
                 'test1_result', 'test1_stat',
                 'test2_result', 'test2_pi', 'test2_v', 'test2_stat',
                 'test3_result', 'test3_s', 'test3_l',
                 'frame1', 'frame2', 'frame3', 'frame4', 'frame5', 'frame6',
                 'generation', 'tests'])


def validate_fields(fields) -> bool:
    errors = []

    for field in ['key1', 'key2', 'seed']:
        if len(fields[field]) != 8:
            errors.append(f'{field} must have 8 chars')

    if fields['key1'] == fields['key2']:
        errors.append('key1 and key2 must be different')

    if len(fields['blocks']) == 0 or not fields['blocks'].isnumeric() or fields['blocks'][0] == '0':
        errors.append('blocks must be positive integer')

    has_errors = len(errors) != 0

    if has_errors:
        sg.popup_error('\n'.join(errors), title='Error', auto_close=True, auto_close_duration=5)

    return has_errors


def format_float_array(arr: List[float]) -> str:
    new_arr = list(map(lambda x: f'{x:.3f}', arr))
    n = int(len(new_arr) / 2)
    return '[' + ', '.join(new_arr[:n]) + '\n ' + ', '.join(new_arr[n:]) + ']'


def update_window(keys: List[str], fields_values: List[any]):
    if len(keys) != len(fields_values):
        return

    for k, v in zip(keys, fields_values):
        window[k].update(str(v))


def save_to_file(filename: str, values_to_save: dict):
    with open(filename, 'w') as f:
        f.writelines([f'{key}: {value}\n' for key, value in values_to_save.items()])


def is_empty_field(field: str) -> bool:
    return len(field) == 0 or field.isspace()


while True:  # Event Loop
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Quit'):  # if all windows were closed
        break
    elif event == 'save':
        if not is_empty_field(values['bin']) and not is_empty_field(values['file']):
            save_to_file(values['file'], {'key1': values['key1'],
                                          'key2': values['key2'],
                                          'seed': values['seed'],
                                          'blocks': values['blocks'],
                                          'bin': values['bin']})
            sg.popup('Sequence successfully saved to file!',
                     title='Success', auto_close=True, auto_close_duration=5)
        else:
            sg.popup_error('You must select file and generate sequence!',
                           title='Error', auto_close=True, auto_close_duration=5)
    elif event == 'generate':
        if validate_fields(values):
            continue
        key1 = values['key1']
        key2 = values['key2']
        seed = values['seed']
        m = int(values['blocks'])

        sequence = generate_sequence(key1, key2, seed, m)
        sequence_bin, sequence_hex = convert_to_bin_and_hex(sequence)

        update_window(['hex', 'bin'], [sequence_hex, sequence_bin])

        update_window(['quantile'], [QUANTILE])

        frequency_test_result = list(frequency_test(sequence_bin))
        update_window(['test1_result', 'test1_stat'], frequency_test_result)

        identical_bits_test_result = list(identical_bits_test(sequence_bin))
        update_window(['test2_result', 'test2_pi', 'test2_v', 'test2_stat'], identical_bits_test_result)

        arbitrary_deviations_test_result = list(arbitrary_deviations_test(sequence_bin))
        arbitrary_deviations_test_result[1] = format_float_array(arbitrary_deviations_test_result[1])
        update_window(['test3_result', 'test3_s', 'test3_l'], arbitrary_deviations_test_result)
