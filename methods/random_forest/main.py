# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os
import logging
import datetime

# internal dependencies
from methods import constants as c
from methods.random_forest import RF_CONFIG

date = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_words, show_weight):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        file_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")
        with open(file_path, 'r', encoding=RF_CONFIG.ENCODE_FILE_INPUT) as file:
            data = [line.strip().split() for line in file.readlines()]

        max_columns = max(len(row) for row in data)

        data_filled = [row + ['0'] * (max_columns - len(row)) for row in data]

        df = pd.DataFrame(data_filled[1:], columns=data_filled[0])

        df = df.apply(pd.to_numeric, errors='ignore')

        X = df.iloc[:, 1:]
        y = df.iloc[:, 0]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()

        model.fit(X_train, y_train)

        importances = model.feature_importances_

        important_words = pd.DataFrame({
            'Palabra': X.columns,
            'Importancia': importances
        })

        important_words = important_words.sort_values(by='Importancia', ascending=False)

        path_name = get_path_output_file()
        selected_words = []
        if show_weight:
            for i in range(n_words):
                palabra = important_words.iloc[i]['Palabra']
                importancia = important_words.iloc[i]['Importancia']
                selected_words.append(f"{palabra} {importancia}")
        else:
            for i in range(n_words):
                palabra = important_words.iloc[i]['Palabra']
                selected_words.append(f"{palabra}")

        with open(path_name['path'], 'w', encoding=RF_CONFIG.ENCODE_FILE_OUTPUT) as file:
            file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_words
        response_method['message'] = f"RF_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').replace(':', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/RF_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data
