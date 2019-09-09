#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
# -*- coding: UTF8 -*-
# -*- coding: cp1252 -*-
'''

try:
    from radatron.radares import EstacionRadar
    from radatron.radares import ImagenRadarAEMET
    from radatron.radares import ImagenRadarFile
except:
    from radares import EstacionRadar
    from radares import ImagenRadarAEMET
    from radares import ImagenRadarFile

def main():
    print('Se esta ejecutando radatron/__init__.py -> main()')
    print('EstacionRadar.LISTA_RADAR:')
    for estacion_radar in EstacionRadar.LISTA_RADAR:
        print('\t', estacion_radar['cod'], '->', estacion_radar['nombre'])

if __name__ == '__main__':
    main()
