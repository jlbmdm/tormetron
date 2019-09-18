#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
# -*- coding: UTF8 -*-
# -*- coding: cp1252 -*-
'''
import os, sys
import pathlib
import time, datetime
import click

try:
    from configparser import RawConfigParser
except ImportError:    # Python 2
    from ConfigParser import RawConfigParser

try:
    #REMOVE: quitar los comentarios y los print() al cargar los módulos
    #Esto funciona cuando el módulo se carga al importar el paquete radatron:
    #Este es el modo normal para cargar el package:
    #    >>> import radatron     # importo el paquete (sus clases) desde el interpreta de python
    #    $ python -m radatron    # ejecuto el paquete con la opción -m (ejecuta su __main__.py)
    #REMOVE:\>
    print('\nImport -> Intentando carga del paquete radatron desde __main__.py: import radatron')
    import radatron
    print('Import radatron ok from __main__.py (loading as package %s)' % __name__)
except:
    #REMOVE: quitar los comentarios y los print() al cargar los módulos
    #Esto funciona cuando este módulo se ejecuta de forma no ortodoxa:
    #    $ python __main__.py
    #REMOVE:\>
    print('Como ha fallado import radatron, cargo el módulo radares con import radares as radatron')
    import radares as radatron
    print('Import radares as radatron ok from __init__.py (loading as package %s)' % __name__)

FILE_DIR = os.path.dirname(os.path.abspath(__file__)) #Equivale a FILE_DIR = pathlib.Path(__file__).parent
WORK_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))
VERBOSE = False

#REMOVE: quitar este chequeo de directorios
HOME_DIR = str(pathlib.Path.home())
RAIZ_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))
BASE_DIR = os.path.abspath('.')
PADRE_DIR = os.path.abspath('..') #Equivale a PADRE_DIR = os.path.abspath(r'../')
if VERBOSE:
    print('Fichero que se esta ejecutando:', __file__)
    print('\nDirectorios de la aplicación (no cambian):')
    print('  Directorio en el que esta el fichero en ejecución     (FILE_DIR):', FILE_DIR)
    print('  Directorio raiz de la aplicacion                      (RAIZ_DIR):', RAIZ_DIR)
    print('Directorios desde el que se llama a la aplicación (si cambian):')
    print('  Directorio base desde el que se lanza la ejecucion    (BASE_DIR):', BASE_DIR)
    print('  Directorio padre del BASE_DIR                        (PADRE_DIR):', PADRE_DIR)
    print('Directorio HOME del usuario                             (HOME_DIR):', HOME_DIR)
    print('\nDirectorio de trabajo -> RAIZ_DIR                       (WORK_DIR):', WORK_DIR)
if not os.path.exists(os.path.join(WORK_DIR, 'radatron')):
    #Esto no deberia ocurrir: significaria que se ha cambiado el nombre al paquete
    print('\nFalta el directorio /radatron; revisar nombre del paquete')
    sys.exit(0)
#REMOVE:\>

config = RawConfigParser()
config.optionxform = str #Avoid change to lowercase
config_dict = {}
configFileName = '%s%s' % (FILE_DIR, '/config.cfg')
if os.path.exists(configFileName):
    try:
        config.read(configFileName)
        trm_secciones = config.sections()
        if VERBOSE:
            print('Configuracion ({}):'.format(configFileName))
        for trm_seccion in trm_secciones:
            trm_opciones = config.options(trm_seccion)
            for trm_opcion in trm_opciones:
                trm_valores = config.get(trm_seccion, trm_opcion).split(',')
                config_dict[trm_opcion] = trm_valores
                if VERBOSE:
                    print('\t', trm_opcion, trm_valores)
        if not 'tipodescarga' in config_dict.keys():
            config_dict['tipodescarga'] = ['1']
        if not 'estaciones' in config_dict.keys():
            print('Falta propiedad estacion en el fichero de configuración', configFileName)
            print('Se usa valor por defecto (Palencia)')
            config_dict['estaciones'] = ['Palencia']
        if not 'modo' in config_dict.keys():
            config_dict['modo'] = ['p']
        if not 'urlRadarAcum6h' in config_dict.keys():
            config_dict['urlRadarAcum6h'] = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'
        if not 'urlRadarAcum6h_ref1' in config_dict.keys():
            config_dict['urlRadarAcum6h_ref1'] = '<div id="imagen%i" class="item">'
        if not 'urlRadarAcum6h_ref2' in config_dict.keys():
            config_dict['urlRadarAcum6h_ref2'] = '<img class="lazyOwl" data-src="'
    except:
        print('Error en fichero de configuracion:', configFileName)
        print('Se usan valores por defecto')
        config_dict['tipodescarga'] = ['1']
        config_dict['estaciones'] = ['Palencia']
        config_dict['modo'] = ['p']
        config_dict['urlRadarAcum6h'] = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'
        config_dict['urlRadarAcum6h_ref1'] = '<div id="imagen%i" class="item">'
        config_dict['urlRadarAcum6h_ref2'] = '<img class="lazyOwl" data-src="'
else:
    print('Fichero de configuracion no encontrado:', configFileName)
    print('Se usan valores por defecto')
    config_dict['tipodescarga'] = ['1']
    config_dict['estaciones'] = ['Palencia']
    config_dict['modo'] = ['p']
    config_dict['urlRadarAcum6h'] = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'
    config_dict['urlRadarAcum6h_ref1'] = '<div id="imagen%i" class="item">'
    config_dict['urlRadarAcum6h_ref2'] = '<img class="lazyOwl" data-src="'


def habilitar_rutas(carpeta):
    ruta_imagenes_radar = os.path.join(WORK_DIR, carpeta)
    if not os.path.exists(ruta_imagenes_radar):
        #print( 'No existe el directorio %s -> Se crea automaticamente' % (ruta_imagenes_radar) )
        try:
            os.makedirs(ruta_imagenes_radar)
        except:
            print( 'No se ha podido crear el directorio %s' % (ruta_imagenes_radar) )
            sys.exit(0)
    ruta_orig = os.path.join(ruta_imagenes_radar, 'orig')
    if not os.path.exists(ruta_orig):
        os.makedirs(ruta_orig)
    ruta_tif = os.path.join(ruta_imagenes_radar, 'tif')
    if not os.path.exists(ruta_tif):
        os.makedirs(ruta_tif)
    ruta_asc = os.path.join(ruta_imagenes_radar, 'asc')
    if not os.path.exists(ruta_asc):
        os.makedirs(ruta_asc)
    return ruta_orig, ruta_tif, ruta_asc


def descargarRadar(tipo_radar, dict_radar, modo, carpeta):
    ruta_orig, ruta_tif, ruta_asc = habilitar_rutas(carpeta)
    cod_estacion = dict_radar.cod
    nombre_raw_estacion = dict_radar.nombre_raw

    imagen_radar = radatron.ImagenRadarAEMET(dict_radar, verbose=VERBOSE)
    while True:
        if tipo_radar == 'radar':
            rpta = imagen_radar.descargar_mapa_radar_regional(ruta_orig=ruta_orig,
                                                              cod_est=cod_estacion,
                                                              nombre_est=nombre_raw_estacion)
        elif tipo_radar == 'acum6h':
            rpta = imagen_radar.descargar_mapa_radar_regional_6h(ruta_orig=ruta_orig,
                                                                 cod_est=cod_estacion,
                                                                 nombre_est=nombre_raw_estacion,
                                                                 urlRadarAcum6h=config_dict['urlRadarAcum6h'][0],
                                                                 urlRadarAcum6h_ref1=config_dict['urlRadarAcum6h_ref1'][0],
                                                                 urlRadarAcum6h_ref2=config_dict['urlRadarAcum6h_ref2'][0])
        if rpta['status'] == 200:
            out_file = rpta["out_file"][0].replace("\\", "/")
            print(f'Descarga radar {nombre_raw_estacion} ok. Fichero: {out_file}')
            descargaOk = True
        else:
            numero_error = rpta['status']
            nombre_imagen_radar_orig_con_ruta = rpta['out_file']
            print('Error {} descargando o guardando: {}'.format(numero_error, nombre_imagen_radar_orig_con_ruta))
            print('Revisar el API_KEY, el codigo o la conexión a Internet')
            descargaOk = False
            #sys.exit(4)

        for nombre_imagen_radar_orig_con_ruta in rpta['out_file']:
            nombre_imagen_radar_tif_con_ruta = nombre_imagen_radar_orig_con_ruta.replace(ruta_orig, ruta_tif).replace('.gif', '.tif').replace('.png', '.tif')
            nombre_imagen_radar_asc_con_ruta = nombre_imagen_radar_orig_con_ruta.replace(ruta_orig, ruta_asc).replace('.gif', '.asc').replace('.png', '.asc')
            if descargaOk:
                if dict_radar.nombre == 'Palencia':
                    imagen_radar_file = radatron.ImagenRadarFile(nombre_imagen_radar_orig_con_ruta=nombre_imagen_radar_orig_con_ruta,
                                                                 nombre_imagen_radar_tif_con_ruta=nombre_imagen_radar_tif_con_ruta,
                                                                 nombre_imagen_radar_asc_con_ruta=nombre_imagen_radar_asc_con_ruta,
                                                                 tipo_imagen=tipo_radar,
                                                                 verbose=VERBOSE)
                    imagen_radar_file.georeferenciarImagenRadar()
                    imagen_radar_file.guardar_raster_asc()
                    if tipo_radar == 'radar':
                        print('Proceso ok: imagen descargada, georreferenciada y guardada como png, tif y asc (%s)' % nombre_imagen_radar_orig_con_ruta.replace('.png', '.*'))
                    elif tipo_radar == 'acum6h':
                        print('Proceso ok: imagen descargada, georreferenciada y guardada como gif, tif y asc (%s)' % nombre_imagen_radar_orig_con_ruta.replace('.gif', '.*'))
                else:
                    #TODO: habilitar la georreferenciación de otras estaciones
                    print('No se georreferencia la imagen por no ser la de Palencia')

        if modo == 'c':
            #time1 = time.time()
            fechahora1 = datetime.datetime.now()
            if tipo_radar == 'radar':
                tiempo_espera = 10 * 60
                fechahora2 = fechahora1 + datetime.timedelta(minutes = 10)
            elif tipo_radar == 'acum6h':
                tiempo_espera = 60 * 60 * 24
                fechahora2 = fechahora1 + datetime.timedelta(days = 1)
            #time2 = time1 + tiempo_espera
            #siguiente_descarga = time.asctime(time.localtime(time2))
            if '{:%d}'.format(fechahora1) == '{:%d}'.format(fechahora2):
                siguiente_descarga = '{:%H:%M:%S}'.format(fechahora2)
            else:
                siguiente_descarga = '{:%H:%M:%S de mañana dia %d}'.format(fechahora2)
            print('Esperando para la siguiente descarga a las', siguiente_descarga)
            time.sleep(tiempo_espera)
        else:
            break

#@click.option('-m', '--modo', default='', prompt='Escribe "c" para descarga continua', help='Escribe "c" (sin comillas) si se quieres programar la descarga cada 10 minutos (último radar) o 1 día (acum de las últimas 6 horas)')

@click.command()
@click.option('-r', '--radar', default='1', prompt='Elige: (1): ultimo radar; (2) acum de las ultimas 6 horas', help='Descarga la última imagen del radar de AEMET')
@click.option('-e', '--estacion', default='', help='Indica el nombre o codigo de la estacón radar. Por defecto, Palencia')
@click.option('-m', '--modo', default='', help='Escribe "c" (sin comillas) si se quieres programar la descarga cada 10 minutos (último radar) o 1 día (acum de las últimas 6 horas)')
@click.option('-d', '--carpeta', default='data', help='Indica el nombre de la carpeta en la que guardar las imágenes. Por defecto, "data"')
def main(estacion='', radar='', modo='', carpeta=''):
    estacion_solicitada = estacion
    modo = modo.lower()
    if radar == '1':
        tipo_radar = 'radar'
    elif radar == '2':
        tipo_radar = 'acum6h'
    else:
        print('Valor de la opcion --radar no permitida. Elegir 1 o 2; se usa opción por defecto: Ultima imagen de radar')
        tipo_radar = 'radar'
        time.sleep(0.1)

    if estacion_solicitada == '':
        print('No se ha solicitado ninguna estación en linea de comandos: se usa la del fichero de configuración', configFileName)
        if 'estaciones' in config_dict.keys():
            if len(config_dict['estaciones']) > 0:
                estacion_solicitada = config_dict['estaciones'][0]
            else:
                print('Falta valor de la propiedad estacion (nombre de la estación) en el fichero de configuración', configFileName)
                estacion_solicitada = config_dict['estaciones'][0]
        else:
            print('Falta propiedad estacion en el fichero de configuración', configFileName)
            estacion_solicitada = config_dict['estaciones'][0]

    if modo == '':
        modo = config_dict['modo'][0].lower()
    if modo == 'c':
        if tipo_radar == 'radar':
            modo_solicitado = 'Se deja que la aplicación descargue las imágenes cada 10 minutos'
        elif tipo_radar == 'acum6h':
            modo_solicitado = 'Se deja que la aplicación descargue las imágenes cada 24 horas (a las 8:00 a.m.)'
        else:
            modo_solicitado = 'Opcion imposible'
    else:
        modo_solicitado = 'Descarga puntual'
    print('Radar solicitado:', estacion_solicitada, '-', tipo_radar, '-', modo_solicitado, end=' -> ')

    lista_radares = radatron.EstacionRadar.buscar_estacion(estacion_solicitada) #<class 'list'>
    #print('lista_radares', lista_radares)
    if lista_radares is None or len(lista_radares) == 0:
        print('Radar de %s no encontrado. Escribe el nombre o codigo corecto. Nombres validos:' % estacion_solicitada)
        for mi_lista_radar in radatron.EstacionRadar.LISTA_RADAR:
            #TODO: arreglar para que muestre bien los acentos -> decode()
            print('\t', mi_lista_radar['nombre'])
        quit()
    #Proceso solo el primero de la lista
    dict_radar = lista_radares[0] #<class '__main__.EstacionRadar'>
    print('Radar encontrado:', dict_radar.nombre) #<class '__main__.EstacionRadar'>

    if carpeta == '':
        carpeta = config_dict['carpeta'][0]

    descargarRadar(tipo_radar, dict_radar, modo, carpeta)


if __name__ == '__main__':
    main()
