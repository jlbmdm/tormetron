#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
# -*- coding: UTF8 -*-
# -*- coding: cp1252 -*-
'''

#REMOVE: quitar este chequeo de directorios
import os, sys
import pathlib
FILE_DIR = os.path.dirname(os.path.abspath(__file__)) #Equivale a FILE_DIR = pathlib.Path(__file__).parent
WORK_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))

if __name__ == '__main__':
    VERBOSE = True
    HOME_DIR = str(pathlib.Path.home())
    RAIZ_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))
    BASE_DIR = os.path.abspath('.')
    PADRE_DIR = os.path.abspath('..') #Equivale a PADRE_DIR = os.path.abspath(r'../')
    if VERBOSE:
        print('Fichero que se esta ejecutando:', __file__)
        print('\nDirectorios en los que est� la aplicaci�n:')
        print('  Directorio en el que esta el fichero en ejecuci�n     (FILE_DIR):', FILE_DIR)
        print('  Directorio raiz de la aplicacion                      (RAIZ_DIR):', RAIZ_DIR)
        print('Directorio desde el que se llama a la aplicaci�n y su padre:')
        print('  Directorio base desde el que se lanza la ejecucion    (BASE_DIR):', BASE_DIR)
        print('  Directorio padre del BASE_DIR                        (PADRE_DIR):', PADRE_DIR)
        print('Directorio HOME del usuario                             (HOME_DIR):', HOME_DIR)
        print('Directorio de trabajo -> RAIZ_DIR                       (WORK_DIR):', WORK_DIR)
#REMOVE:\>

VERBOSE = False

#REMOVE: quitar los comentarios y los print() al cargar los m�dulos
try:
    #Esto funciona cuando el m�dulo se carga al importar el paquete radatron:
    #    Este es el modo normal para cargar el package:
    #        >>> import radatron     # importo el paquete (sus clases) desde el interpreta de python
    #        $ python -m radatron    # ejecuto el paquete con la opci�n -m (ejecuta su __main__.py)
    print('\nImport -> Intentando carga de clases del modulo radatron desde __init__.py: from radatron.radares import EstacionRadar')
    #print('Como ha fallado from radares import EstacionRadar, cargo from radatron.radares import EstacionRadar')
    from radatron.radares import EstacionRadar
    from radatron.radares import ImagenRadarAEMET
    from radatron.radares import ImagenRadarFile
    print('Import classes of radatron.radares ok from __init__.py (loading as package %s)' % __name__)
except:
    #Esto funciona cuando este m�dulo se ejecuta de forma no ortodoxa:
    #    $ python __init__.py
    #print('\nImport -> Intentando carga de clases del modulo radares: from radares import EstacionRadar')
    print('Como ha fallado from radatron.radares import EstacionRadar, cargo directamente from radares import EstacionRadar')
    from radares import EstacionRadar
    from radares import ImagenRadarAEMET
    from radares import ImagenRadarFile
    print('Import classes of radares ok from __init__.py (loading as package %s)' % __name__)
#REMOVE:\>

def main():
    #REMOVE: quitar los comentarios y los print(). Sustituir por pass
    #Estos mensajes solo se muestran si se llama directamente __ini__.py
    #Cuando el m�dulo se carga al importar el paquete radatron, este mensaje no se muestra
    print('\nSe ha llamado especificamente a /radatron/__init__.py como main(): modo de prueba de carga de clases')
    print('Simplemente se prueba la carga de paquetes y no se ejecuta busqueda de estaci�n ni descarga de im�genes')
    print('Lista de estaciones (EstacionRadar.LISTA_RADAR):')
    for estacion_radar in EstacionRadar.LISTA_RADAR:
        #TODO: arreglar para que muestre bien los acentos -> decode()
        print('\t', estacion_radar['cod'], '->', estacion_radar['nombre'])
    #REMOVE:\>

if __name__ == '__main__':
    main()
