# external dependencies
import logging
import os
# internal dependencies
from utils import constants

logger = logging.getLogger()
logger.setLevel(constants.LOGGER_LEVEL)


def get_categories_data():
    response_method = {'success': False, 'message': '', 'data': {}}
    try:
        data = {}
        with open('TEST_BOOL.txt', 'r') as file:
            lines = file.readlines()
            headers = lines[0].strip().split()

            # Iterar a través de las líneas de datos
            for line in lines[1:]:
                # Dividir la línea en elementos
                elements = line.strip().split()

                # Obtener el nombre del archivo y la categoría
                file_name = elements[0]
                category = file_name.split('_')[0]

                # Obtener los valores binarios como una lista
                values = [int(value) for value in elements[1:]]

                # Agregar los datos a la categoría correspondiente en el diccionario
                if category not in data:
                    data[category] = []

                data[category].append(values)

        response_method['success'] = True
    except Exception as error:
        logger.exception(error)
        response_method['message'] = str(error)
    return response_method
