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
import PCA_CONFIG
from utils import constants

logger = logging.getLogger()
logger.setLevel(constants.LOGGER_LEVEL)

date = datetime.datetime.now()
md5 = hashlib.md5()
md5.update(str(date).encode())
hash_md5 = md5.hexdigest()

script_directory = os.path.dirname(os.path.abspath(__file__))
archivo_path_out = os.path.join(script_directory, f"../../outputs/PCA_{hash_md5}.txt")


def main(file_name, n_components):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        archivo_path = os.path.join(script_directory, f"../../inputs/{file_name}")

        with open(archivo_path, 'r', encoding=PCA_CONFIG.ENCODE_FILE_INPUT) as file:
            lines = file.readlines()

        words = lines[0].split()[1:]

        data = [line.split()[1:] for line in lines[1:]]

        matrix = np.array([[int(val) for val in line] for line in data])

        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(matrix)

        important_words_indices = np.argsort(np.abs(pca.components_))[0, :n_components]

        selected_words = [words[i + 1] for i in important_words_indices]

        with open(archivo_path_out, 'w', encoding=PCA_CONFIG.ENCODE_FILE_OUTPUT) as file:
            file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_components
        response_method['data']['all_words_in_file'] = len(words)
        response_method['message'] = f"file name: PCA_{hash_md5}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method
