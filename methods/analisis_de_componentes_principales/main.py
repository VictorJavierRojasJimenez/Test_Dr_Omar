# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import numpy as np
from sklearn.decomposition import PCA
import os
import datetime
import hashlib
import logging

# internal dependencies
from methods.analisis_de_componentes_principales import PCA_CONFIG
from methods import constants as c

logger = logging.getLogger()
logger.setLevel(c.LOGGER_LEVEL)

date = datetime.datetime.now()

script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_components, show_values):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        archivo_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")

        with open(archivo_path, 'r', encoding=PCA_CONFIG.ENCODE_FILE_INPUT) as file:
            lines = file.readlines()

        words = lines[0].split()[1:]

        data = [line.split()[1:] for line in lines[1:]]

        matrix = np.array([[int(val) for val in line] for line in data])

        # pca = PCA(n_components=n_components)
        pca = PCA()
        pca.fit(matrix)
        # principal_components = pca.fit_transform(matrix)
        principal_components = pca.components_

        important_words_indices = np.argsort(np.abs(pca.components_))[0, :n_components]
        weights = principal_components[0]
        path_name = get_path_output_file()

        selected_words_dict = []
        for word, weight in zip(words, weights):
            selected_words_dict.append({'word': word, 'weight': weight})

        clean_selected_words = sorted(selected_words_dict, key=lambda x: x['weight'], reverse=True)

        if show_values:
            selected_words = []
            for item in clean_selected_words[:n_components]:
                selected_words.append(f"{item['word']} {item['weight']}")

        else:
            selected_words = [item['word'] for item in clean_selected_words[:n_components]]

        with open(path_name['path'], 'w', encoding=PCA_CONFIG.ENCODE_FILE_OUTPUT) as file:
            file.write('\n'.join(selected_words))

        # selected_words = [words[i + 1] for i in important_words_indices]

        # with open(path_name['path'], 'w', encoding=PCA_CONFIG.ENCODE_FILE_OUTPUT) as file:
        #    file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_components
        response_method['data']['all_words_in_file'] = len(words)
        response_method['message'] = f"PCA_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/PCA_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data
