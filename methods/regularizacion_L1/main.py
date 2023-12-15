# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
import datetime
import logging

# internal dependencies
from methods import constants as c
from methods.regularizacion_L1 import LASSO_CONFIG

date = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

script_directory = os.path.dirname(os.path.abspath(__file__))


def main(file_name, n_words, show_weight):
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        file_path = os.path.join(script_directory, f"../../{c.INPUT_DIRECTORY_NAME}/{file_name}")
        with open(file_path, 'r', encoding=LASSO_CONFIG.ENCODE_FILE_INPUT) as file:
            data = [line.strip().split() for line in file.readlines()]

        max_columns = max(len(row) for row in data)

        data_filled = [row + ['0'] * (max_columns - len(row)) for row in data]

        df = pd.DataFrame(data_filled[1:], columns=data_filled[0])
        df = df.apply(pd.to_numeric, errors='ignore')

        X = df.iloc[:, 1:]
        y = df.iloc[:, 0]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model_l1 = LogisticRegression(penalty='l1', solver='liblinear')
        model_l1.fit(X_train, y_train)

        selected_columns_l1 = X.columns[model_l1.coef_[0] != 0]
        n_words = min(n_words, len(selected_columns_l1))
        coefficients_l1 = model_l1.coef_[0][model_l1.coef_[0] != 0]

        words_coefficients_l1 = pd.DataFrame({
            'Palabra': selected_columns_l1,
            'Coeficiente': coefficients_l1
        })

        words_coefficients_l1 = words_coefficients_l1.sort_values(by='Coeficiente', ascending=False)
        path_name = get_path_output_file()
        selected_words = []

        if show_weight:
            for i in range(n_words):
                palabra = words_coefficients_l1.iloc[i]['Palabra']
                coeficiente = words_coefficients_l1.iloc[i]['Coeficiente']
                selected_words.append(f"{palabra} {coeficiente}")
        else:
            for i in range(n_words):
                palabra = words_coefficients_l1.iloc[i]['Palabra']
                selected_words.append(f"{palabra}")

        with open(path_name['path'], 'w', encoding=LASSO_CONFIG.ENCODE_FILE_OUTPUT) as file:
            file.write('\n'.join(selected_words))

        response_method['data']['count_selected_words'] = n_words
        response_method['message'] = f"LASSO_{path_name['name']}"
        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method


def get_path_output_file():
    data = {'path': '', 'name': '_name_.' + c.OUTPUT_DEFAULT_EXT}
    date_format = str(date).replace(' ', '_').replace(':', '_').split('.')[0]
    path = os.path.join(script_directory,
                        f"../../{c.OUTPUT_DIRECTORY_NAME}/LASSO_{date_format}.{c.OUTPUT_DEFAULT_EXT}")
    data['path'] = path
    data['name'] = data['name'].replace('_name_', date_format)
    return data
