# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import math
import numpy as np
import os
import datetime
import logging

# internal dependencies
from methods import constants as c
from methods.maxima_relevancia_minima_redundancia import MRMR_CONFIG

date = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_words, show_weight):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        file_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")
        with open(file_path, 'r', encoding=MRMR_CONFIG.ENCODE_FILE_INPUT) as file:
            lines = file.readlines()

        words = lines[0].strip().split()
        words = words[1:]

        data = [line.strip().split() for line in lines[1:]]

        max_num_words = len(data[0])
        for fila in data:
            while len(fila) < max_num_words:
                fila.append('0')

        X = np.array([[int(valor) for valor in fila[1:]] for fila in data])

        num_examples, num_words = X.shape

        pmi_words = []
        for i in range(num_words):
            p_word = np.sum(X[:, i]) / num_examples
            p_not_word = 1 - p_word
            p_word_not_present = np.sum(X[:, i] == 0) / num_examples
            pmi = calculate_pmi(p_word, p_not_word, p_word_not_present)
            pmi_words.append(pmi)

        ordered_indexes = np.argsort(pmi_words)[::-1]

        num_desired_features = n_words
        selected_words = [words[i] for i in ordered_indexes[:num_desired_features]]
        selected_weights = [pmi_words[i] for i in ordered_indexes[:num_desired_features]]

        path_name = get_path_output_file()

        if show_weight:
            new_selected_words = []
            for palabra, peso in zip(selected_words, selected_weights):
                new_selected_words.append(f"{palabra} {peso}")
            with open(path_name['path'], 'w', encoding=MRMR_CONFIG.ENCODE_FILE_OUTPUT) as file:
                file.write('\n'.join(new_selected_words))

        else:
            with open(path_name['path'], 'w', encoding=MRMR_CONFIG.ENCODE_FILE_OUTPUT) as file:
                file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_words
        response_method['data']['all_words_in_file'] = len(words)
        response_method['message'] = f"MRMR_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def calculate_pmi(p_word, p_not_word, p_word_not_present):
    if p_word == 0 or p_not_word == 0 or p_word_not_present == 0:
        return 0
    return math.log2(p_word / (p_not_word * p_word_not_present))


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/MRMR_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data
