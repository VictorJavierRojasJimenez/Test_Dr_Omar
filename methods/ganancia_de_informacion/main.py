# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import math
import logging
import os
import datetime

# internal dependencies
from methods import constants as c
from methods.ganancia_de_informacion import GI_CONFIG

date = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_words, show_weight):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        file_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")
        with open(file_path, 'r', encoding=GI_CONFIG.ENCODE_FILE_INPUT) as file:
            lines = file.readlines()

        words = lines[0].strip().split()
        words = words[1:]

        data = [line.strip().split() for line in lines[1:]]

        for fila in data:
            while len(fila) < len(words):
                fila.append('0')

        num_examples = len(data)

        total_ones = sum(1 for fila in data for valor in fila if valor == '1')
        total_zeros = num_examples * len(words) - total_ones
        prob_uno = total_ones / (num_examples * len(words))
        prob_cero = total_zeros / (num_examples * len(words))
        entropy_h = -prob_uno * math.log2(prob_uno) - prob_cero * math.log2(
            prob_cero) if prob_uno > 0 and prob_cero > 0 else 0

        information_gain = {}

        for i, word in enumerate(words):
            count_ones = sum(1 for fila in data if fila[i] == '1')
            zero_count = num_examples - count_ones

            prob_present_word = count_ones / num_examples
            prob_absent_word = zero_count / num_examples

            present_word_entropy = -prob_present_word * math.log2(prob_present_word) if prob_present_word > 0 else 0
            entropy_absent_word = -prob_absent_word * math.log2(prob_absent_word) if prob_absent_word > 0 else 0

            gain = entropy_h - (prob_present_word * present_word_entropy + prob_absent_word * entropy_absent_word)

            information_gain[word] = gain

        ordered_words = sorted(information_gain, key=information_gain.get, reverse=True)

        n = n_words
        path_name = get_path_output_file()
        if show_weight:
            selected_words = [f"{word} {information_gain[word]}" for word in ordered_words[:n]]
        else:
            selected_words = [word for word in ordered_words[:n]]

        with open(path_name['path'], 'w', encoding=GI_CONFIG.ENCODE_FILE_OUTPUT) as file:
            file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_words
        response_method['data']['all_words_in_file'] = len(words)
        response_method['message'] = f"GI_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/GI_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data
