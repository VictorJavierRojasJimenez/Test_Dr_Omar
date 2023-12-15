# Author: Victor Javier Rojas Jimenez
# Date: October 2023

# external dependencies
import logging
import os

# internal dependencies
from methods import constants
from methods.analisis_de_componentes_principales import main as method_pca
from methods.ganancia_de_informacion import main as method_gi
from methods.maxima_relevancia_minima_redundancia import main as method_mrmr
from methods.puntuacion_de_informacion_mutua import main as method_pim
from methods.random_forest import main as method_rf
from methods.regularizacion_L1 import main as method_lasso

logger = logging.getLogger()
logger.setLevel(constants.LOGGER_LEVEL)


def main(name, n_words, file_name, show_values=False):
    response_main = {'success': False, 'message': '', 'data': {}}
    try:
        if name == constants.METHOD_PCA:
            response_main = method_pca.main(file_name, n_words, show_values)
        elif name == constants.METHOD_GI:
            response_main = method_gi.main(file_name, n_words, show_values)
        elif name == constants.METHOD_MRMR:
            response_main = method_mrmr.main(file_name, n_words, show_values)
        elif name == constants.METHOD_PIM:
            response_main = method_pim.main(file_name, n_words, show_values)
        elif name == constants.METHOD_RF:
            response_main = method_rf.main(file_name, n_words, show_values)
        elif name == constants.METHOD_LASSO:
            response_main = method_lasso.main(file_name, n_words, show_values)

    except Exception as e:
        logger.exception(e)
        response_main['message'] = str(e)
    return response_main


if __name__ == '__main__':
    response = {'success': False, 'message': '', 'data': [], 'details': []}
    try:
        print("__________________ HELLO __________________")
        print("############################### IMPORTANTE ###############################")
        print("Los algoritmos programados se estandarizaron con el siguiente criterio:")
        print(" '0' significa ausencia de la palabra y '1' representa presencia de la palabra.")
        print("")
        print(" El formato del documento debera ser:")
        print()
        print(" col1 Este es un texto de prueba")
        print(" arch1.txt 0 1 1 0 1 0")
        print(" arch20.txt 1 0 1 0 1 0")
        print()
        print("=================================== IMPORTANTE ================================")
        print()
        print(" 1) Analisis de componentes principales")
        print(" 2) Ganancia de Información")
        print(" 3) Puntuación de Información Mutua")
        print(" 4) Máxima Relevancia Mínima Redundancia")
        print("")
        print("=================================== Por Modelos  ==============================")
        print(" 5) Random Forest [stable]")
        print(" 6) regularización L1 [stable]")

        method_value = int(input("Selecciona un algoritmo: "))
        words_value = int(input("Selecciona el numero de palabras: "))
        is_show_values = int(input("Digita 1 para ver los valores de los pesos y 0 para no mostrarlos: "))

        boolean_show_values = True if is_show_values == 1 else False
        method_name = ''
        if method_value == 1:
            method_name = constants.METHOD_PCA
        elif method_value == 2:
            method_name = constants.METHOD_GI
        elif method_value == 3:
            method_name = constants.METHOD_PIM
        elif method_value == 4:
            method_name = constants.METHOD_MRMR
        elif method_value == 5:
            method_name = constants.METHOD_RF
        elif method_value == 6:
            method_name = constants.METHOD_LASSO

        files = os.listdir(constants.INPUT_DIRECTORY_NAME)

        for file in files:
            response_method = main(method_name, words_value, file, boolean_show_values)
            if not response_method['success']:
                response['details'].append(
                    {'event': method_name,
                     'message': response_method['message']
                     })
                continue

            response['details'].append({
                'method': method_name,
                'file_name': response_method['message'] + '.' + constants.OUTPUT_DEFAULT_EXT,
                'count_selected_words': response_method['data']['count_selected_words']
            })

        response['message'] = 'successfully'
        response['success'] = True
    except Exception as error:
        logger.exception(error)
    finally:
        print(response)
