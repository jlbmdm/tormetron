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
    print('Import -> Intentando carga del paquete radatron desde __main__.py: import radatron')
    import radatron
    print('Import radatron ok from __main__.py (loading as package %s)' % __name__)
    #REMOVE:\>
except:
    #REMOVE: quitar los comentarios y los print() al cargar los módulos
    #Esto funciona cuando este módulo se ejecuta de forma no ortodoxa:
    #    $ python __main__.py
    print('Como ha fallado import radatron, cargo el módulo radares con import radares as radatron')
    import radares as radatron
    print('Import radares as radatron ok from __init__.py (loading as package %s)' % __name__)
    #REMOVE:\>

VERBOSE = False
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.abspath(os.path.join(FILE_DIR, '..')) #Equivale a FILE_DIR = pathlib.Path(__file__).parent
TRON_DIR = os.path.join(WORK_DIR, 'radatron')
if FILE_DIR != TRON_DIR:
    print('\nSe está trabajando en una versión reubicada del paquete radatron')
if not os.path.exists(TRON_DIR):
    print('\nFalta el directorio {os.path.join(WORK_DIR, "radatron"")}; revisar nombre del paquete')
    #sys.exit(0)

#REMOVE: quitar este chequeo de directorios
def chequear_directorios():
    HOME_DIR = str(pathlib.Path.home())
    BASE_DIR = os.path.abspath('.')
    SUPR_DIR = os.path.abspath('..') #Equivale a SUPR_DIR = os.path.abspath(r'../')
    print('Fichero que se esta ejecutando:', __file__)
    print('\nDirectorios de la aplicación:')
    print('  Directorio en el que esta el fichero en ejecución     (FILE_DIR):', FILE_DIR)
    print('  Directorio del proyecto y del repositorio             (WORK_DIR):', WORK_DIR)
    print('Directorios desde el que se llama a la aplicación:')
    print('  Directorio base desde el que se lanza la ejecucion    (BASE_DIR):', BASE_DIR)
    print('  Directorio padre del BASE_DIR                         (SUPR_DIR):', SUPR_DIR)
    print('Directorio HOME del usuario                             (HOME_DIR):', HOME_DIR)
    print('\nDirectorio de trabajo -> RAIZ_DIR                       (WORK_DIR):', WORK_DIR)
chequear_directorios()
#REMOVE:\>

config = RawConfigParser()
config.optionxform = str #Avoid change to lowercase
config_dict = {}
configFileName = '%s%s' % (FILE_DIR, '/config.cfg')
if os.path.exists(configFileName):
    try:
        config.read(configFileName)
        cfg_secciones = config.sections()
        if VERBOSE:
            print('Configuracion ({}):'.format(configFileName))
        for cfg_seccion in cfg_secciones:
            cfg_opciones = config.options(cfg_seccion)
            for cfg_opcion in cfg_opciones:
                cfg_valores = config.get(cfg_seccion, cfg_opcion).split(',')
                config_dict[cfg_opcion] = cfg_valores
                if VERBOSE:
                    print('\t', cfg_opcion, cfg_valores)
        if not 'tipodescarga' in config_dict.keys():
            print('Falta propiedad "tipodescarga" en el fichero de configuración', configFileName)
            print('Se usa valor por defecto ("1" -> radar)')
            config_dict['tipodescarga'] = ['1']
        if not 'estaciones' in config_dict.keys():
            print('Falta propiedad "estacion" en el fichero de configuración', configFileName)
            print('Se usa valor por defecto ("Palencia")')
            config_dict['estaciones'] = ['Palencia']
        if not 'modo' in config_dict.keys():
            print('Falta propiedad "modo" en el fichero de configuración', configFileName)
            print('Se usa valor por defecto ("p" -> descarga puntual)')
            config_dict['modo'] = ['p']
        if not 'urlRadarAcum6h' in config_dict.keys():
            config_dict['urlRadarAcum6h'] = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'
        if not 'urlRadarAcum6h_ref1' in config_dict.keys():
            config_dict['urlRadarAcum6h_ref1'] = '<div id="imagen%i" class="item">'
        if not 'urlRadarAcum6h_ref2' in config_dict.keys():
            config_dict['urlRadarAcum6h_ref2'] = '<img class="lazyOwl" data-src="'
        config_ok = True
    except:
        print('\nError al leer la configuracion del fichero:', configFileName)
        config_ok = False
else:
    print('\nFichero de configuracion no encontrado:', configFileName)
    config_ok = False
if not config_ok:
    print('Se usan valores por defecto')
    config_dict['tipodescarga'] = ['1']
    config_dict['estaciones'] = ['Palencia']
    config_dict['modo'] = ['p']
    config_dict['urlRadarAcum6h'] = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'
    config_dict['urlRadarAcum6h_ref1'] = '<div id="imagen%i" class="item">'
    config_dict['urlRadarAcum6h_ref2'] = '<img class="lazyOwl" data-src="'


def descargarRadar(tipo_radar, estacion_radar, modo, carpeta):
    '''
    Lanza la descarga de las imagenes radar o acum6h usando el paquete radatron 
    :param tipo_radar:     "1": ultimo radar; "2" acum de las ultimas 6 horas
    :param estacion_radar: Instancia de la clase EstacionRadar (del paquete radatron)
    :param modo:           "c": para descarga continua; "p" (resto): descarga puntual
    :param carpeta:        Nombre de la carpeta en la que guardar las imágenes
    '''
    ruta_imagenes_radar = os.path.join(WORK_DIR, carpeta)
    ruta_orig, ruta_tif, ruta_asc = radatron.ImagenRadarAEMET.habilitar_rutas(ruta_imagenes_radar)
    descargas_exitosas = 0
    descargas_fallidas = 0
    imagen_radar = radatron.ImagenRadarAEMET(estacion_radar, verbose=VERBOSE)
    while True:
        if tipo_radar == 'radar':
            rpta = imagen_radar.descargar_mapa_radar_regional(ruta_orig=ruta_orig)
        elif tipo_radar == 'acum6h':
            rpta = imagen_radar.descargar_mapa_radar_regional_6h(ruta_orig=ruta_orig,
                                                                 urlRadarAcum6h=config_dict['urlRadarAcum6h'][0],
                                                                 urlRadarAcum6h_ref1=config_dict['urlRadarAcum6h_ref1'][0],
                                                                 urlRadarAcum6h_ref2=config_dict['urlRadarAcum6h_ref2'][0])
        if rpta['status'] == 200:
            descargas_exitosas += 1
            out_file = rpta["out_file"][0].replace("\\", "/")
            print(f'{descargas_exitosas} de {descargas_fallidas + descargas_exitosas}', end=' ->')
            for nombre_imagen_radar_orig_con_ruta in rpta['out_file']:
                out_file = nombre_imagen_radar_orig_con_ruta.replace("\\", "/")
                print(f'\tDescarga radar {estacion_radar.nombre_raw} ok. Fichero: {out_file}')
        else:
            numero_error = rpta['status']
            nombre_imagen_radar_orig_con_ruta = rpta['out_file']
            print('Error {} descargando o guardando: {}'.format(numero_error, nombre_imagen_radar_orig_con_ruta))
            print('\tRevisar el API_KEY, el codigo o la conexión a Internet')
            descargas_fallidas += 1
            if descargas_fallidas > 10 and float(descargas_fallidas) / (descargas_fallidas + descargas_exitosas) >= 0.9:
                sys.exit(4)
            continue

        # La imagen se ha descargado y guardado como nombre_imagen_radar_orig_con_ruta
        # Siguiente paso: abrir el fichero, georreferenciarlo y guardarlo como ASC
        for nombre_imagen_radar_orig_con_ruta in rpta['out_file']:
            nombre_imagen_radar_tif_con_ruta = nombre_imagen_radar_orig_con_ruta.replace(ruta_orig, ruta_tif).replace('.gif', '.tif').replace('.png', '.tif')
            nombre_imagen_radar_asc_con_ruta = nombre_imagen_radar_orig_con_ruta.replace(ruta_orig, ruta_asc).replace('.gif', '.asc').replace('.png', '.asc')
            if estacion_radar.nombre == 'Palencia':
                imagen_radar_file = radatron.ImagenRadarFile(nombre_imagen_radar_orig_con_ruta=nombre_imagen_radar_orig_con_ruta,
                                                             nombre_imagen_radar_tif_con_ruta=nombre_imagen_radar_tif_con_ruta,
                                                             nombre_imagen_radar_asc_con_ruta=nombre_imagen_radar_asc_con_ruta,
                                                             tipo_imagen=tipo_radar,
                                                             verbose=VERBOSE)
                if not imagen_radar_file.ok:
                    #print('\tHa ocurrido algún error al grabar la imagen', nombre_imagen_radar_orig_con_ruta, '(no existe)')
                    break

                imagen_radar_file.georeferenciar_imagen_radar()
                if not imagen_radar_file.ok:
                    #print('\tHa ocurrido algun error al georreferenciar', nombre_imagen_radar_orig_con_ruta, '-> src_dataset is None')
                    break

                imagen_radar_file.guardar_raster_asc()
                if not imagen_radar_file.ok:
                    #print('\tHa ocurrido algún error al guardar la imagen', nombre_imagen_radar_orig_con_ruta, 'como asc:', nombre_imagen_radar_asc_con_ruta)
                    break

                if tipo_radar == 'radar':
                    print('\tProceso ok: imagen descargada, georreferenciada y guardada como png, tif y asc (%s)' % nombre_imagen_radar_orig_con_ruta.replace('.png', '.*'))
                elif tipo_radar == 'acum6h':
                    print('\tProceso ok: imagen descargada, georreferenciada y guardada como gif, tif y asc (%s)' % nombre_imagen_radar_orig_con_ruta.replace('.gif', '.*'))
            else:
                #TODO: habilitar la georreferenciación de otras estaciones
                print('\tNo se georreferencia la imagen por no ser la de Palencia')

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
            print('\tEsperando para la siguiente descarga a las', siguiente_descarga)
            time.sleep(tiempo_espera)
        else:
            break


@click.command()
@click.option('-r', '--radar', default='1', prompt='Elige: (1): ultimo radar; (2) acum de las ultimas 6 horas', help='Descarga la última imagen del radar de AEMET')
@click.option('-e', '--estacion', default='', help='Indica el nombre o codigo de la estacón radar. Por defecto, Palencia')
@click.option('-m', '--modo', default='', prompt='Escribe "c" para descarga continua', help='Escribe "c" (sin comillas) si se quieres programar la descarga cada 10 minutos (último radar) o 1 día (acum de las últimas 6 horas)')
#@click.option('-m', '--modo', default='', help='Escribe "c" (sin comillas) si se quieres programar la descarga cada 10 minutos (último radar) o 1 día (acum de las últimas 6 horas)')
@click.option('-d', '--carpeta', default='data', help='Indica el nombre de la carpeta en la que guardar las imágenes. Por defecto, "data"')
def main(estacion='', radar='', modo='', carpeta=''):
    '''
    Realiza tres acciones:
        Lee los parametros que se pasan en linea de comandos y los que no se pasan los extrae del config.cfg
        Crea una instancia de la clase EstacionRadar (del paquete radatron) correspondiente a la estación solicitada (estacion)
        Llama a la función descargarRadar() para lanzar la descarga
    :param tipo_radar:     "1": ultimo radar; "2" acum de las ultimas 6 horas
    :param estacion_radar: Nombre o codigo de la estacón radar
    :param modo:           "c": para descarga continua; "p" (resto): descarga puntual
    :param carpeta:        Nombre de la carpeta en la que guardar las imágenes
    '''

    #Lee los parametros que se pasan en linea de comandos y los que no se pasan los extrae del config.cfg
    if radar == '1':
        tipo_radar = 'radar'
    elif radar == '2':
        tipo_radar = 'acum6h'
    else:
        print('Valor de la opcion --radar no permitida. Elegir 1 o 2; se usa opción por defecto: 1->Ultima imagen de radar')
        tipo_radar = 'radar'
        time.sleep(0.1)

    estacion_solicitada = estacion
    if estacion_solicitada == '':
        #print('No se ha solicitado ninguna estación en linea de comandos: se usa la del fichero de configuración', configFileName)
        if 'estaciones' in config_dict.keys():
            if len(config_dict['estaciones']) > 0:
                estacion_solicitada = config_dict['estaciones'][0]
            else:
                print('Falta valor de la propiedad estacion (nombre de la estación) en el fichero de configuración', configFileName)
                estacion_solicitada = 'Palencia'
        else:
            print('Falta propiedad estacion en el fichero de configuración', configFileName)
            estacion_solicitada = 'Palencia'

    modo = modo.lower()
    if modo == '':
        modo = config_dict['modo'][0].lower()
    if modo == 'c':
        if tipo_radar == 'radar':
            modo_solicitado = 'Se deja que la aplicación descargue las imágenes cada 10 minutos'
        elif tipo_radar == 'acum6h':
            modo_solicitado = 'Se deja que la aplicación descargue las imágenes cada 24 horas (a las 8:00 a.m.)'
        else:
            modo_solicitado = 'Opcion no disponible'
    else:
        modo_solicitado = 'Descarga puntual'
    print('Información solicitada:', tipo_radar, '-', estacion_solicitada, '-', modo_solicitado)

    if carpeta == '':
        carpeta = config_dict['carpeta'][0]

    #Crea una instancia de la clase EstacionRadar (del paquete radatron) correspondiente a la estación solicitada (estacion)
    MODO_JB = True
    if MODO_JB:
        estacion_radar = radatron.EstacionRadar(estacion_solicitada) #<class EstacionRadar'>
    else:
        #Esta es otra forma de instanciar la clase EstacionRadar) la del ejemplo de AEMET)
        lista_radares = radatron.EstacionRadar.buscar_estacion(estacion_solicitada, instanciar=True) #<class 'list'>
        #print('lista_radares', lista_radares)
        if lista_radares is None or len(lista_radares) == 0:
            print('Radar de %s no encontrado. Escribe el nombre o codigo corecto. Nombres validos:' % estacion_solicitada)
            for mi_lista_radar in radatron.EstacionRadar.LISTA_RADAR:
                #TODO: arreglar para que muestre bien los acentos -> decode()
                print('\t', mi_lista_radar['nombre'])
            sys.exit(1)
        #Proceso solo el primero de la lista
        estacion_radar = lista_radares[0]
    print('estacion_radar', type(estacion_radar)) #<class '__main__.EstacionRadar'>
    print('Radar encontrado:', estacion_radar.nombre)

    #Llama a la función descargarRadar() para lanzar la descarga
    descargarRadar(tipo_radar, estacion_radar, modo, carpeta)


if __name__ == '__main__':
    main()
