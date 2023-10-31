# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import math
import logging
import os
import datetime

# internal dependencies
from methods import constants as c
from methods.puntuacion_de_informacion_mutua import PIM_CONFIG

date = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_words, show_weight):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:

        file_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")
        with open(file_path, 'r', encoding=PIM_CONFIG.ENCODE_FILE_INPUT) as file:
            lines = file.readlines()

        words = lines[0].strip().split()
        words = words[1:]

        data = [line.strip().split() for line in lines[1:]]

        max_num_words = len(words)
        for fila in data:
            while len(fila) < max_num_words:
                fila.append('0')

        num_examples = len(data)

        documents_with_word = [sum(1 for fila in data if fila[i] == '1') for i in range(max_num_words)]

        pmi = {}
        for i, word in enumerate(words):
            p_word = documents_with_word[i] / num_examples
            p_not_word = 1 - p_word
            p_word_not_present = sum(1 for fila in data if fila[i] == '0') / num_examples

            if p_word == 0 or p_not_word == 0 or p_word_not_present == 0:
                pmi[word] = 0
            else:
                pmi[word] = math.log2(p_word / (p_not_word * p_word_not_present))

        ordered_words = sorted(pmi, key=pmi.get, reverse=True)

        n = n_words
        path_name = get_path_output_file()
        if show_weight:
            new_selected_words = []
            for word in ordered_words[:n]:
                new_selected_words.append(f"{word} {pmi[word]}")
            with open(path_name['path'], 'w', encoding=PIM_CONFIG.ENCODE_FILE_OUTPUT) as file:
                file.write('\n'.join(new_selected_words))

        else:
            selected_words = [word_s for word_s in ordered_words[:n]]
            with open(path_name['path'], 'w', encoding=PIM_CONFIG.ENCODE_FILE_OUTPUT) as file:
                file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_words
        response_method['data']['all_words_in_file'] = len(words)
        response_method['message'] = f"PIM_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/PIM_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data