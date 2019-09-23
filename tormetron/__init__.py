#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
# -*- coding: UTF8 -*-
# -*- coding: cp1252 -*-
'''

__version__ = '0.0.1'

try:
    from radares import EstacionRadar
    from radares import ImagenRadarAEMET
    from radares import ImagenRadarFile
    #print(f'Import classes of radares ok from __init__.py (__name__ = {__name__}')
except:
    from tormetron.radares import EstacionRadar
    from tormetron.radares import ImagenRadarAEMET
    from tormetron.radares import ImagenRadarFile
    print(f'Import classes of tormetron.radares ok from __init__.py (__name__ = {__name__}')

def main():
    #REMOVE: quitar los comentarios y los print(). Sustituir por pass
    #Estos mensajes solo se muestran si se llama directamente __ini__.py
    #Cuando el módulo se carga al importar el paquete tormetron, este mensaje no se muestra
    print('\nSe ha llamado especificamente a /tormetron/__init__.py como main(): modo de prueba de carga de clases')
    print('Simplemente se prueba la carga de paquetes y no se ejecuta busqueda de estación ni descarga de imágenes')
    print('Lista de estaciones (EstacionRadar.LISTA_RADAR):')
    for estacion_radar in EstacionRadar.LISTA_RADAR:
        #TODO: arreglar para que muestre bien los acentos -> decode()
        print('\t', estacion_radar['cod'], '->', estacion_radar['nombre'])
    #REMOVE:\>

if __name__ == '__main__':
    main()
