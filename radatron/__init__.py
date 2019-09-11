#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
# -*- coding: UTF8 -*-
# -*- coding: cp1252 -*-
'''

#REMOVE: quitar los comentarios y los print() al cargar los módulos
try:
    #Esto funciona cuando el módulo se carga al importar el paquete radatron:
    #Este es el modo normal para cargar el package:
    #    >>> import radatron     # importo el paquete (sus clases) desde el interpreta de python
    #    $ python -m radatron    # ejecuto el paquete con la opción -m (ejecuta su __main__.py)
    from radatron.radares import EstacionRadar
    from radatron.radares import ImagenRadarAEMET
    from radatron.radares import ImagenRadarFile
    print('Import classes of radatron.radares ok (loading %s package)' % __name__)
except:
    #Esto funciona cuando este módulo se ejecuta de forma no ortodoxa:
    #    $ python __init__.py
    from radares import EstacionRadar
    from radares import ImagenRadarAEMET
    from radares import ImagenRadarFile
    print('Import classes of radares ok (loading %s package)' % __name__)
#REMOVE:\>

def main():
    #REMOVE: quitar los comentarios y los print(). Sustituir por pass
    #Estos mensajes solo se muestran si se llama directamente __ini__.py
    #Cuando el módulo se carga al importar el paquete radatron, este mensaje no se muestra
    print('Se esta ejecutando /radatron/__init__.py -> main()')
    print('EstacionRadar.LISTA_RADAR:')
    for estacion_radar in EstacionRadar.LISTA_RADAR:
        #TODO: arreglar para que muestre bien los acentos -> decode()
        print('\t', estacion_radar['cod'], '->', estacion_radar['nombre'])
    #REMOVE:\>

if __name__ == '__main__':
    main()
