#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 31 ago. 2019

@author: joseb
API de AEMET: https://opendata.aemet.es/centrodedescargas/AEMETApi
'''
import os, sys
import pathlib
import json
import datetime
import math
import numpy as np
import requests #Ver https://realpython.com/python-requests/
#import urllib3
#urllib3.disable_warnings()
try:
    from osgeo import gdal, osr
    from osgeo import gdalconst
except:
    pass
    #import gdal, osr, gdalconst

try:
    from radatron import constants
    #from radarAEMET.constants import BASE_DIR, API_KEY, API_KEY_FILE1, API_KEY_FILE2, RADAR_NACIONAL_API_URL, RADAR_REGIONAL_API_URL
except:
    import constants
    #from constants import BASE_DIR, API_KEY, API_KEY_FILE1, API_KEY_FILE2, RADAR_NACIONAL_API_URL, RADAR_REGIONAL_API_URL

HOME_DIR = str(pathlib.Path.home())
FILE_DIR = os.path.dirname(os.path.abspath(__file__)) #Equivale a FILE_DIR = pathlib.Path(__file__).parent
RAIZ_DIR = os.path.abspath(os.path.join(FILE_DIR, '..'))
BASE_DIR = os.path.abspath('.')
PADRE_DIR = os.path.abspath('..') #Equivale a PADRE_DIR = os.path.abspath(r'../')
WORK_DIR = RAIZ_DIR
NODATA = -1
DATA_DIR = 'radardata'
LISTA_RADARES_FILE_NAME = 'cod_radar_regional.json'

'''
En principio no instancio directamente ningún objeto de esta clase
con miEstacion = EstacionRadar(...). En su lugar lo hago desde el metodo
buscar_estacion(...) que crea un objeto de la clase EstacionRadar
usando la funcion estacionRadar_from_jsonData(...)
Estas dos funciones son metodos de la propia clase EstacionRadar
pero podrian estar fuera de la clase
'''
class EstacionRadar:
    '''
    Esta clase sirve para localizar un radar regional y solo tiene
    tres propiedades que son el cod, nombre y nombre_raw del radar
    '''
    lista_radares_file_name = os.path.join(FILE_DIR, DATA_DIR, LISTA_RADARES_FILE_NAME)
    if not os.path.exists(lista_radares_file_name):
        print('Falta el fichero de codigos de radar:', lista_radares_file_name)
        print('Reinstala la aplicación')
        sys.exit(1)
    with open(lista_radares_file_name) as lista_radares_file:
        LISTA_RADAR = json.loads(lista_radares_file.read())
        #LISTA_RADAR es una lista de dicts; cada dict es un radar
        #con tres claves: cod, nombre y nombre_raw

    def __init__(self, cod='', nombre='', buscar=True):
        '''
        Se puede instanciar la clase sin pasarle ningun argumento
        o pasando una de estas tres kwargs:
            cod        Codigo de una estacion radar
            nombre:    Nombre de una estación radar
                        Se admite nombre real y nombre siplificado (sin acentos ni mayusculas)
        Si se instancia la clase sin argumentos, hay que usar el metodo
            .buscar_estacion() para asignar la estación.
        Si se instancia la clase con algún argumento indicativ de la estación,
            se llama automáticamente al método .buscar_estacion() para verificar que existe.
            Orden de prioridad de argumento a usar en la busqueda: cod, nombre
        '''
        if buscar and cod != '':
            radares_localizados = self.buscar_estacion(cod)
            if radares_localizados is None:
                print('Revsar código porque radares_localizados es None')
                sys.exit(1)
            radar_buscado = True
            #Esto siguiente es un poco raro, porque creo un objeto de la clase
            #desde dentr de la clase y lo asigno luego a self.
            #Está copiado de lo que hace AEMET; yo no lo haría así:
            #dejaría el método .buscar_estación() fuera de la clase
            if nombre != '':
                if not nombre in radares_localizados.nombre and\
                    not nombre in radares_localizados.nombre_raw:
                    print('Atención: el código no coincide con el nombre; se usa el código e ignra el nombre')
        elif buscar and nombre != '':
            radares_localizados = self.buscar_estacion(nombre)
            radar_buscado = True
        else:
            radar_buscado = False
            self.cod = cod
            self.nombre = nombre
            nombre_raw = nombre.lower().replace('á', 'a').replace('í', 'i')
            self.nombre_raw = nombre_raw

        if radar_buscado:
            if radares_localizados is None or len(radares_localizados) == 0:
                print('Radar no encontrado. Escribe el nombre o codigo corecto. Nombres validos:')
                for mi_lista_radar in EstacionRadar.LISTA_RADAR:
                    #TODO: arreglar para que muestre bien los acentos -> decode()
                    print('\t', mi_lista_radar['nombre'])
                quit()
            #Proceso solo el primero de la lista
            if len(radares_localizados) > 1:
                print('Lista de radares localizados:', end='\n')
            else:
                print('Radar localizados:', end=' ')
            for radar_localizado in radares_localizados:
                self = radares_localizados[0] #<class '__main__.EstacionRadar'>
                print(f'\tRadar localizado: {self.nombre} {self.cod}')
            #print('self.nombre_raw', self.nombre_raw)

    def __str__(self):
        return 'Estacion radar de {}: {} ({})'.format(self.nombre, self.cod, self.nombre_raw)

    @staticmethod
    def buscar_estacion(nombre_o_codigo):
        """
        Devuelve una lista con los resultados de la busqueda de radares
        :param nombre_o_codigo: Nombre o código del radar
        """
        nombre_o_codigo_raw = nombre_o_codigo.lower().replace('á', 'a').replace('í', 'i')
        #print('nombre_raw', nombre_raw)
        #Esto está copiado del ejemplo de AEMET: busqueda del radar de forma compacta
        try:
            #Primero chequeo si coincide con algún oambre_raw
            radares_raw = list(filter(lambda t: nombre_o_codigo_raw in t.get('nombre_raw'), EstacionRadar.LISTA_RADAR))
            if len(radares_raw) == 0:
                #Si eso falla, chequeso si coincide con algún codigo
                radares_raw = list(filter(lambda t: nombre_o_codigo_raw in t.get('cod'), EstacionRadar.LISTA_RADAR))
                if len(radares_raw) == 0:
                    return None
            # radares_raw es una lista de 
            #print('EstacionRadar.LISTA_RADAR ->', type(EstacionRadar.LISTA_RADAR), type(EstacionRadar.LISTA_RADAR[0]), EstacionRadar.LISTA_RADAR)
            print('radar encontrado: radares_raw ->', type(radares_raw), type(radares_raw[0]), radares_raw)
        except:
            return None
        #Esto esta copiado del ejemplo de AEMET: llama al metodo estacionRadar_from_jsonData() de esta clase
        lista_radares = list(map(lambda m: EstacionRadar.estacionRadar_from_jsonData(m), radares_raw))
        #Versión multilinea, sin lambda ni map()
        #lista_radares = []
        #for radar_raw in radares_raw:
        #    lista_radares.append(EstacionRadar.estacionRadar_from_jsonData(radar_raw))
        #print('lista_radares                 ->', type(lista_radares), type(lista_radares[0]), lista_radares)
        return lista_radares

    @staticmethod
    def estacionRadar_from_jsonData(jsonData):
        #print('jsonData:', type(jsonData), jsonData)
        #print('cod    ->', jsonData.get('cod', ''))
        #print('nombre ->', jsonData.get('nombre', ''))
        return EstacionRadar(
            cod=jsonData.get('cod', ''),
            nombre=jsonData.get('nombre', ''),
            buscar=False
        )

#Metodos del script de AEMET que no utilizo:
#     @staticmethod
#     def get_estacion(id):
#         estacion = list(filter(lambda m: id == '{}{}{}'.format(m.get('cod'), m.get('nombre'), m.get('nombre_raw')), EstacionRadar.LISTA_RADAR))[0]
#         return EstacionRadar.estacionRadar_from_jsonData(estacion)
# 
#     @staticmethod
#     def get_estacion_cod(id):
#         estacion = list(filter(lambda m: id == '{}'.format(m.get('cod')), EstacionRadar.LISTA_RADAR))[0]
#         return EstacionRadar.estacionRadar_from_jsonData(estacion)
# 
#     @staticmethod
#     def get_estacion_nombre(id):
#         estacion = list(filter(lambda m: id == '{}'.format(m.get('nombre')), EstacionRadar.LISTA_RADAR))[0]
#         return EstacionRadar.estacionRadar_from_jsonData(estacion)
# 
#     @staticmethod
#     def get_estacion_nombre_raw(id):
#         estacion = list(filter(lambda m: id == '{}'.format(m.get('nombre_raw')), EstacionRadar.LISTA_RADAR))[0]
#         return EstacionRadar.estacionRadar_from_jsonData(estacion)


class ImagenRadarAEMET:
    def __init__(self, mi_radar, api_key=constants.API_KEY, api_key_file=constants.API_KEY_FILE, verbose=False):
        if not api_key and not api_key_file:
            print('Tienes que añadir una clave de API')
            api_key = self.guardar_clave_api()
        elif api_key_file:
            if not os.path.exists(api_key_file):
                print('No se encuentra', api_key_file, '-> revisar código')
            with open(api_key_file) as f:
                api_key = f.read().strip()
        self.api_key = api_key
        self.api_key_file = api_key_file
        self.querystring = {
            'api_key': self.api_key
        }
        self.mi_radar = mi_radar
        self.headers = {}
        self.verbose = verbose
        #print('api_key', self.api_key)

    @staticmethod
    def guardar_clave_api():
        api_key = input('Escriba su clave de API: ')
        if not api_key:
            raise Exception('La clave de API no puede estar vacía')
        try:
            with open(constants.API_KEY_FILE1, 'w') as f:
                f.write(api_key)
            print('Clave de API almacenada en {}'.format(constants.API_KEY_FILE1))
        except:
            with open(constants.API_KEY_FILE2, 'w') as f:
                f.write(api_key)
            print('No se puede escribir en {}. Clave de API almacenada en {}'.format(constants.API_KEY_FILE1, constants.API_KEY_FILE2))
        return api_key

    def get_request_data(self, url, todos=False):
        """
        Returns the JSON formatted request data
        """
        if self.verbose:
            print(url)
        r = requests.get(
            url,
            headers=self.headers,
            params=self.querystring,
            verify=False  # Avoid SSL Verification .__.
        )
        #print('url solicitado:', url,
        #      'headers->', self.headers,
        #      'params->', self.querystring,
        #      'verify=False')
        if r.status_code == 200:
            url = r.json().get('datos')
            if self.verbose:
                print(url)
            r = requests.get(url, verify=False)
            if todos:
                data = r.json()
            else:
                try:
                    data = r.json()[0]
                except IndexError:
                    return r.json()
            return data
        else:
            raise Exception('Error: {}'.format(r.json()))

    def get_request_normalized_data(self, url):
        """
        Return the request raw content data
        """
        if self.verbose:
            print(url)
        r = requests.get(
            url,
            headers=self.headers,
            params=self.querystring,
            verify=False  # Avoid SSL Verification .__.
        )
        #print('url normalizado solicitado:', url,
        #      'headers->', self.headers,
        #      'params->', self.querystring,
        #      'verify=False')
 
        if r.status_code == 200:
            r = requests.get(r.json().get('datos'), verify=False)
            data = r.text
            return data
        return {
            'error': r.status_code
        }

    def get_fecha_hoy(self):
        """
        Devuelve la fecha formateada en el formato que acepta AEMET
        """
        #print(datetime.datetime.now())  #<class 'datetime.datetime'>
        return '{:%Y-%m-%d}'.format(datetime.datetime.now())

    def download_file_from_url(self, url, out_file):
        """
        Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename
        """
        if self.verbose:
            print('Downloading from {}...'.format(url))
        r = requests.get(
            url,
            params=self.querystring,
            headers=self.headers,
            verify=False
        )
        #print('url descargado:', url,
        #      'headers->', self.headers,
        #      'params->', self.querystring,
        #      'verify=False')
 
        try:
            error = r.json().get('estado')
            return {
                'error': error,
                'status': 400,
                'out_file': [out_file]
            }
        except KeyError:
            data = r.content
            with open(out_file, 'wb') as f:
                f.write(data)
            return {
                'status': 200,
                'out_file': [out_file]
            }

    def download_image_from_url(self, url, out_file):
        """
        Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename
        """
        if self.verbose:
            print('Downloading from {}'.format(url))
        try:
            r = requests.get(
                url,
                params=self.querystring,
                headers=self.headers,
                verify=False
            )
            #Esto lanza este requests:
            #   requests.get('https://opendata.aemet.es/opendata/api/red/radar/regional/vd', headers={}, params={'api_key': APY_KEY}, verify=False)
            #Alternativa que me funciona: poner el AI_KEY en headers:
            #   requests.get('https://opendata.aemet.es/opendata/api/red/radar/regional/vd', headers={'Accept': 'application/json', 'api_key': APY_KEY})
            if self.verbose:
                print('url imagen:', url,
                      'headers->', self.headers,
                      'params->', self.querystring,
                      'verify=False')

            if r.json()['descripcion'] =="exito" or r.json()["estado"] == 200:
                ahora = datetime.datetime.now() #<class 'datetime.datetime'>
                if self.verbose:
                    print(ahora, 'Respuesta de la API de opendata.aemet.es: API KEY ok')
                img_url_ = r.json()['datos']
            elif r.json()['descripcion'] =="datos expirados" or\
                 r.json()['descripcion'] == 'API key invalido' or\
                 r.json()["estado"] == 404:
                print('La API KEY es incorrecta')
                if os.path.exists(self.api_key_file):
                    print('Eliminar o modificar el fichero', self.api_key_file)
                    sys.exit(2)
            else:
                print('descripcion:', r.json()['descripcion'], 'estado:', r.json()["estado"])
                print('Revisar http')
                quit()

            error = ''
            img_url = r.json().get('datos')
            if self.verbose:
                print('img_url:', img_url, img_url_)
                #print(img_url)
            r = requests.get(img_url, verify=False)
            try:
                error = r.json()
            except:
                pass
            if error:
                raise Exception(error)
            if self.verbose:
                print('Contenido devuelto por AEMET:', r.headers['Content-Type'], 'tamaño:', r.headers['Content-Length'], type(r.content))
                print('Consulta:', r.headers['aemet_num'], 'Consultas restantes:', r.headers['Remaining-request-count'])

            if r.headers['Content-Type'][:9] == 'image/gif':
                data = r.content
                with open(out_file, 'wb') as f:
                    f.write(data)
                if self.verbose:
                    print('    Se ha creado una nueva imagen', out_file, 'de', os.path.getsize(out_file), 'bytes') 
            elif r.headers['Content-Type'][:16] == 'application/json':
                print('Imagen no disponible')
            else:
                print('-->', r.headers['Content-Type'][:16])
        except:
            if r.json()['descripcion'] =="datos expirados" or\
                 r.json()['descripcion'] == 'API key invalido' or\
                 r.json()["estado"] == 404:
                sys.exit(2)
            print('Error al descargar o guardar la imagen', out_file)
            return {
                'status': r.json().get('estado', 'error'),
                'out_file': [out_file]
                }
        return {
            'status': 200,
            'out_file': [out_file]
        }

    def download_image_from_web_page(self, urlRadarAcum6hCompleto, nombre_Imagen_acum6h_con_ruta,
                                     urlRadarAcum6h_ref1='',
                                     urlRadarAcum6h_ref2=''):
        """
        Crea un nuevo fichero con la imagen de preciptacion 6h del url de AEMET:
        Es un apaño porque la API de AEMET no ofrece esta imagen:
            la extraigo leyendo descargando la pagina web
            y buscando donde guarda la ruta de la imagen que me interesa
        :param urlRadarAcum6hCompleto: Url de la paginweb en la que esta la imagen radar
        :param nombre_Imagen_acum6h: Nombre del archivo en el que se va a guardar
        """
        if self.verbose:
            print('Downloading from {}'.format(urlRadarAcum6hCompleto))
        try:
            rpta1 = requests.get(urlRadarAcum6hCompleto)
            rpta1.raise_for_status()
#         except HTTPError as http_err:
#             print('\nError en requests accediendo:', urlRadarAcum6hCompleto)
#             print(f'HTTP error occurred: {http_err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
#             return {'status': 400, 'out_file': [nombre_Imagen_acum6h_con_ruta]}
        except Exception as err:
            print('\nError en requests accediendo:', urlRadarAcum6hCompleto)
            print(f'Other error occurred: {err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
            return {'status': 400, 'out_file': [nombre_Imagen_acum6h_con_ruta]}

        if self.verbose:
            print(urlRadarAcum6hCompleto, '.header:')
            for header in rpta1.headers:
                print('\t', header, '\t->', rpta1.headers[header])

        posicion0 = 0
        lista_nombre_ficheros = []
        for nImagen in range(9):
            if nImagen == 8:
                break
            textoPreImagen = urlRadarAcum6h_ref1 % nImagen
            #print(textoPreImagen)
            posicion1 = rpta1.text[posicion0:].find(textoPreImagen)
            #print('posicion1:', posicion1)
            if posicion1 == -1:
                if nImagen >= 1:
                    break
                print(f'No se ha localizado el texo {textoPreImagen} en la web {urlRadarAcum6hCompleto}')
                return {'status': 500, 'out_file': [nombre_Imagen_acum6h_con_ruta]}
            textoDeReferencia = urlRadarAcum6h_ref2
            posicion2 = posicion1 + rpta1.text[posicion1:].find(textoDeReferencia)
            avance2 = len(textoDeReferencia) #31
            #print('posicion2:', posicion2)
            if posicion2 == -1:
                if nImagen >= 1:
                    break
                print(f'No se ha localizado el texo {textoDeReferencia} en la web {urlRadarAcum6hCompleto}')
                return {'status': 500, 'out_file': [nombre_Imagen_acum6h_con_ruta]}
            posicion3 = posicion2 + rpta1.text[posicion2:].find('.gif')
            avance3 = 4
            urlImagen = 'http://www.aemet.es%s' % rpta1.text[posicion2 + avance2: posicion3 + avance3]
            idImagen = urlImagen[-21:-4].replace('\\', '_').replace('/', '_')
            nombre_Imagen_acum6h_con_ruta_fechado = nombre_Imagen_acum6h_con_ruta.replace('.gif', f'_{idImagen}.gif')
            if os.path.exists(nombre_Imagen_acum6h_con_ruta_fechado):
                continue
                #print('La imagen', nombre_Imagen_acum6h_con_ruta_fechado, 'ya existe: se sobreescribe')
                #try:
                #    os.remove(nombre_Imagen_acum6h_con_ruta_fechado)
                #except:
                #    return {'status': 600, 'out_file': lista_nombre_ficheros}
            lista_nombre_ficheros.append(nombre_Imagen_acum6h_con_ruta_fechado)
            if self.verbose:
                print('Se ha encontrado el url de la imagen buscada (acum 6h): {} (num {})'.format(urlImagen, nImagen))

            try:
                rpta2 = requests.get(urlImagen)
                rpta2.raise_for_status()
#             except HTTPError as http_err:
#                 print('\nError en requests accediendo:', urlImagen)
#                 print(f'HTTP error occurred: {http_err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
#                 return {'status': 401, 'out_file': [urlImagen]}
            except Exception as err:
                print(f'\nError en requests accediendo: {urlImagen}')
                print(f'Other error occurred: {err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
                return {'status': 401, 'out_file': [urlImagen]}

            if self.verbose:
                print(urlImagen, '.header:')
                for header in rpta2.headers:
                    print('\t', header, '\t->', rpta2.headers[header])
                #print('\nrpta2.cookies:\t',rpta2.cookies)
                print('    Contenido devuelto por AEMET:', rpta2.headers['Content-Type'], 'tamaño:', rpta2.headers['Content-Length'], type(rpta2.content))

            if rpta2.headers['Content-Type'][:9] != 'image/gif':
                print('No se ha encontrado la imagen en', urlImagen)
                return {'status': 700, 'out_file': lista_nombre_ficheros}

#             try:
            if True:
                myImage = open(nombre_Imagen_acum6h_con_ruta_fechado, 'wb')
                myImage.write(rpta2.content)
                myImage.close()
                if self.verbose:
                    print('    Se ha creado una nueva imagen', nombre_Imagen_acum6h_con_ruta_fechado, 'de', os.path.getsize(nombre_Imagen_acum6h_con_ruta_fechado), 'bytes')
#             except:
#                 print('    Error 1 - imagen no guardada', nombre_Imagen_acum6h_con_ruta_fechado)
#                 return {'status': 800, 'out_file': lista_nombre_ficheros}

        return {'status': 200, 'out_file': lista_nombre_ficheros}

    def descargar_mapa_radar_nacional(self, archivo_salida):
        """
        Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url_imagen_radar = constants.RADAR_NACIONAL_API_URL
        if os.path.exists(archivo_salida):
            print('La imagen', archivo_salida, 'ya existe: se sobreescribe')
            try:
                os.remove(archivo_salida)
            except:
                return {'status': 600, 'out_file': archivo_salida}
        return self.download_image_from_url(url_imagen_radar, archivo_salida)

    def descargar_mapa_radar_regional(self, ruta_orig='', cod_est='vd', nombre_est=''):
        """
        Descarga una imagen con el mapa del radar por región
        :param ruta_orig: Ruta en la que se guardan las imagenes
        :param cod_estacion: Codigo de estacion regional consultada
        :param nombre_raw_estacion: Nombre de estacion regional consultada (sin mayusculas, espacios ni acentos)
        """
        url_imagen_radar = constants.RADAR_REGIONAL_API_URL.format(cod_est)
        if nombre_est == '':
            nombre_est = cod_est
        ahora = str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h')[:16]
        nombre_imagen_radar_orig = f'AEMET_radar_{nombre_est}_{ahora}.png'
        nombre_imagen_radar_orig_con_ruta = os.path.join(ruta_orig, nombre_imagen_radar_orig)
        if os.path.exists(nombre_imagen_radar_orig_con_ruta):
            print('La imagen', nombre_imagen_radar_orig_con_ruta, 'ya existe: se sobreescribe')
            try:
                os.remove(nombre_imagen_radar_orig_con_ruta)
            except:
                return {'status': 600, 'out_file': [nombre_imagen_radar_orig_con_ruta]}
        return self.download_image_from_url(url_imagen_radar, nombre_imagen_radar_orig_con_ruta)

    def descargar_mapa_radar_regional_6h(self, ruta_orig='', cod_est='vd', nombre_est='',
                                         urlRadarAcum6h='', urlRadarAcum6h_ref1='', urlRadarAcum6h_ref2=''):

        """
        Descarga las imagenes de un dia determinado de precipitacion acumulada en 6 h
        :param ruta_orig: Ruta en la que se guardan las imagenes
        :param cod_est: Código de dos letras de la estacion radar
        :param nombre_est: Nombre de la estacion sin acentos ni mayusculas
        """
        if nombre_est == '':
            nombre_est = cod_est

        if urlRadarAcum6h != '':
            urlRadarAcum6hCompleto = urlRadarAcum6h.format(cod_est)
        else:
            urlRadarAcum6hCompleto = 'http://www.aemet.es/es/eltiempo/observacion/radar?w=1&p={}&opc1=3'.format(cod_est)
        if urlRadarAcum6h_ref1 == '':
            urlRadarAcum6h_ref1 = '<div id="imagen%i" class="item">'
        if urlRadarAcum6h_ref2 == '':
            urlRadarAcum6h_ref2 = '<img class="lazyOwl" data-src="'

        nombre_Imagen_acum6h = f'AEMET_radarAcum6h_{nombre_est}.gif'
        nombre_Imagen_acum6h_con_ruta = os.path.join(ruta_orig, nombre_Imagen_acum6h)
        return self.download_image_from_web_page(urlRadarAcum6hCompleto, nombre_Imagen_acum6h_con_ruta,
                                                 urlRadarAcum6h_ref1=urlRadarAcum6h_ref1,
                                                 urlRadarAcum6h_ref2=urlRadarAcum6h_ref2)


class ImagenRadarFile:
    def __init__(self,
                 nombre_imagen_radar_orig_con_ruta='',
                 nombre_imagen_radar_tif_con_ruta='',
                 nombre_imagen_radar_asc_con_ruta='',
                 tipo_imagen='radar',
                 verbose=False):
        '''
        Clase para referenciar la imagen descargada y guardada en nombre_imagen_radar_orig_con_ruta
        :param nombre_imagen_radar_orig_con_ruta: Nombre de la imagen a georeferenciar
        :param tipo_imagen: Tipo de imagen: (1) ultimo radar (2) acumulado de 6 horas
        :param verbose: Mensajes informativos durante el procesado
        '''
        self.nombre_imagen_radar_orig_con_ruta = nombre_imagen_radar_orig_con_ruta
        self.nombre_imagen_radar_tif_con_ruta = nombre_imagen_radar_tif_con_ruta
        self.nombre_imagen_radar_asc_con_ruta = nombre_imagen_radar_asc_con_ruta
        self.tipo_imagen = tipo_imagen
        self.verbose = verbose

    def georeferenciarImagenRadar(self):
        '''
        Georreferencia una imagen radar (implementado solo para el radar de Palencia)
        '''
        if self.tipo_imagen != 'radar' and self.tipo_imagen != 'acum6h':
            print('\nAplicacion no preparada para interpretar otras imagenes que no sean de radar y precipitacion acumlada de 6 horas')
            sys.exit(9)
        formato = "GTiff"
        driver = gdal.GetDriverByName( formato )
        if os.path.exists(self.nombre_imagen_radar_tif_con_ruta):
            print('La imagen', self.nombre_imagen_radar_tif_con_ruta, 'ya existe: se sobreescribe')
            try:
                os.remove(self.nombre_imagen_radar_tif_con_ruta)
            except:
                print('No se ha posido eliminar la imagen', self.nombre_imagen_radar_tif_con_ruta, 'revisar si esta bloqueada por el sistema operativo')
                sys.exit(5)
        try:
            self.src_dataset = gdal.Open(self.nombre_imagen_radar_orig_con_ruta)
            if self.src_dataset is None:
                print('Error abriendo', self.nombre_imagen_radar_orig_con_ruta)
        except:
                print('Error abriendo', self.nombre_imagen_radar_orig_con_ruta)
                sys.exit(4)

        nCeldasX = self.src_dataset.RasterXSize
        nCeldasY = self.src_dataset.RasterYSize
        #nBandas = self.src_dataset.RasterCount
        ancho_pixel = 1000
        SesgoEnX = (15000) / nCeldasY
        SesgoEnY = (15000) / nCeldasX
        alto_pixel = -1000
        XsupIzda = 125000 - 5000
        YsupIzda = 4890000 - 6000

        outputOptions = ['COMPRESS=LZW']
        try:
            outputDataset = driver.CreateCopy(self.nombre_imagen_radar_tif_con_ruta, self.src_dataset, 0, outputOptions)
        except:
            print('No se ha podido crear la imagen', self.nombre_imagen_radar_tif_con_ruta, 'revisar si hay restricciones para escribir en la ruta de destino')
            sys.exit(5)
        outputDataset.SetGeoTransform( [XsupIzda, ancho_pixel, SesgoEnX, YsupIzda, SesgoEnY, alto_pixel ] )
        #Nota:
        # Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
        # Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)

        #Creacion y asignacion del sistema de referencia espacial (SRS)
        targetSR = osr.SpatialReference() #Por el momento targetSR.ExportToWkt() es ''
        targetSR.SetWellKnownGeogCS( 'EPSG:25830' ) #ETRS89 / UTM zone 30N
        targetSR.SetUTM(30, True)
        outputDataset.SetProjection( targetSR.ExportToWkt() )
        #agregarNoData = "gdal_translate -of GTiff -a_nodata 0 " + self.nombre_imagen_radar_tif_con_ruta1 + ' ' + self.nombre_imagen_radar_tif_con_ruta2
        #print(agregarNoData)
        #os.system(agregarNoData)
        if self.verbose:
            print('Imagen reproyectada ok')

    def guardar_raster_asc(self, nBandas=0):
        '''
        :param nBandas: Numero de bandas que se quiere procesar: indicar 0 si se quieren procesar todas las que tenga el raster. 
        '''
        reading_filename = self.nombre_imagen_radar_tif_con_ruta
        reading_dataset = gdal.Open( reading_filename, gdalconst.GA_ReadOnly )
        if reading_dataset is None:
            print('Error abriendo raster', reading_filename)
            sys.exit(5)
        nCeldasX = reading_dataset.RasterXSize
        nCeldasY = reading_dataset.RasterYSize
        if nBandas == 0:
            nBandas = reading_dataset.RasterCount
        geotransform = reading_dataset.GetGeoTransform()
        if geotransform is None:
            print('La imagen no esta georreferenciada:')
            origenX_Imagen, origenY_Imagen = 0, 0
            ancho_pixel, alto_pixel = 1, 1
            sesgoX, sesgoY = 0, 0
        else:
            origenX_Imagen, origenY_Imagen = geotransform[0], geotransform[3] #Esquina exterior del pixel arriba izda
            ancho_pixel, alto_pixel = geotransform[1], geotransform[5]
            sesgoX = geotransform[2] #Modifica la coordenada X georreferenciada conforme nos movemos en la Y de la imagen
            sesgoY = geotransform[4] #Modifica la coordenada Y georreferenciada conforme nos movemos en la X de la imagen
            #sesgoX -> metros que hay que sumar a la X por cada pixel en Y desde la esquina sup izda (hacia abajo)
            #sesgoY -> metros que hay que sumar a la Y por cada pixel en X desde la esquina sup izda (hacia la dcha)
        #Xgeo = geotransform(0) + Ximg*geotransform(1) + Yimg*geotransform(2)
        #Ygeo = geotransform(3) + Ximg*geotransform(4) + Yimg*geotransform(5)
        #TODO: revisar por qué hay que hacer estas correcciones y hacerlo correctamente 
        origenX_raster = origenX_Imagen + (0.8 * ancho_pixel)
        #origenY_Imagen es la coordenada Y exterior del pixel de la esquina superior izda (antes de deformar la imagen con sesgoX y sesgoY)
        origenY_raster = origenY_Imagen - ( ((nCeldasY + 0.7) * abs(alto_pixel)) + (sesgoY * nCeldasX) )

        #TODO: seleccionar el trozo de la imagen a grabar (solo mapa, sin leyenda ni texto del margen)
        #Para eso usar los valores adecuados de xOffsetLectura, yOffsetLectura, xPixelsLectura, yPixelsLectura
        #y/o guardar solo los pixeles del circulo central de la imagen
        #Por el momento leo toda la imagen y la guardo como asc 
        xOffsetLectura, yOffsetLectura = 0, 0
        xPixelsLectura, yPixelsLectura = nCeldasX, nCeldasY

        reading_band_asArrayIntDictOld = {} #Incluto este array por si hubiera varias bandas (no es el caso)
        reading_band_asArrayIntDictNew = {} #Incluto este array por si hubiera varias bandas (no es el caso)
        for nBand in range(nBandas):
            try:
                reading_band = reading_dataset.GetRasterBand(nBand+1)
            except:
                print('Este raster no tiene la banda %i' % nBand)
                sys.exit(7)
            reading_band_asArrayInt = reading_band.ReadAsArray(xOffsetLectura,
                                                               yOffsetLectura, 
                                                               xPixelsLectura,
                                                               yPixelsLectura).astype(np.int8)
            #El nuevo array tiene:
            nRows = reading_band_asArrayInt.shape[0] #-> yPixelsLectura
            nCols = reading_band_asArrayInt.shape[1] #-> xPixelsLectura
            #Aplico la deformación (sesgo en x e y
            xPixelsNew = xPixelsLectura + math.ceil(sesgoX * yPixelsLectura / ancho_pixel) + 1
            yPixelsNew = yPixelsLectura + math.ceil(sesgoY * xPixelsLectura / abs(alto_pixel)) + 1
            nRowsNew = yPixelsNew
            nColsNew = xPixelsNew
            reading_band_asArrayIntNew = np.zeros((nRowsNew, nColsNew), dtype = np.int8)
            for row in range(nRows):
                for col in range(nCols):
                    coordX = origenX_Imagen + (col * ancho_pixel) + (row * sesgoX)
                    coordY = origenY_Imagen + (row * alto_pixel) + (col * sesgoY)
                    new_col = int( (coordX - origenX_Imagen) / ancho_pixel )
                    new_row = int( (coordY - origenY_Imagen) / alto_pixel )
                    reading_band_asArrayIntNew[new_row, new_col] = reading_band_asArrayInt[row, col]
            reading_band_asArrayIntDictOld[nBand] = reading_band_asArrayInt
            reading_band_asArrayIntDictNew[nBand] = reading_band_asArrayIntNew

        if self.tipo_imagen == 'radar':
            listaValoresPrecipitacion = [12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72] #En realidad son valores de reflectividad
            colInicial = 506
            colFinal = 518
            celdaInicial = 144
            nCeldasPorColor = 24
            if self.verbose:
                print('\nGuardo la útima imagen de radar en un fichero ASC')
        elif self.tipo_imagen == 'acum6h':
            listaValoresPrecipitacion = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
            colInicial = 501
            colFinal = 513
            celdaInicial = 150
            nCeldasPorColor = 32
            if self.verbose:
                print('\nGuardo la precipitacion en las ultimas 6 horas en un fichero ASC')
        else:
            print('\nAplicacion no preparada para interpretar otras imagenes que no sean de radar y precipitacion acumlada de 6 horas')
            sys.exit(9)

        dictRangoCeldasPorValorPrecipitacion = {}
        dictListaColoresPorValorPrecipitacion = {}
        for valorPrecipitacion in listaValoresPrecipitacion:
            celdaFinal = celdaInicial + nCeldasPorColor
            dictRangoCeldasPorValorPrecipitacion[valorPrecipitacion] = [celdaInicial, celdaFinal]
            dictListaColoresPorValorPrecipitacion[valorPrecipitacion] = []
            celdaInicial = celdaFinal
        for valorPrecipitacion in listaValoresPrecipitacion:
            for row in range(colInicial, colFinal):
                for col in range(*dictRangoCeldasPorValorPrecipitacion[valorPrecipitacion]):
                    codigoColor = reading_band_asArrayIntDictOld[nBand][row, col]
                    if not codigoColor in dictListaColoresPorValorPrecipitacion[valorPrecipitacion]:
                        dictListaColoresPorValorPrecipitacion[valorPrecipitacion].append(codigoColor)
                        if self.verbose:
                            print('Precipitacion/Reflectividad', valorPrecipitacion, 'Color', codigoColor)

        for nBand in range(nBandas):
            if False:
                #Lineas de uso interno para ver las celdas con los codigos de coor en la imagen original
                target_ascfile_name_orginal = self.nombre_imagen_radar_asc_con_ruta.replace('.asc', '_banda%i_original.txt' % nBand)
                target_ascfile_opened = open(target_ascfile_name_orginal, 'w+')
                for row in range(nRows):
                    for col in range(nCols):
                        valor = reading_band_asArrayIntDictOld[nBand][row, col]
                        target_ascfile_opened.write('%03i ' % valor)
                    target_ascfile_opened.write('\n')
                target_ascfile_opened.close

            if nBandas <= 1:
                target_ascfile_name_georef = self.nombre_imagen_radar_asc_con_ruta
            else:
                target_ascfile_name_georef = self.nombre_imagen_radar_asc_con_ruta.replace('.asc', '_banda%i.asc' % nBand)
            if os.path.exists(target_ascfile_name_georef):
                print('La imagen', target_ascfile_name_georef, 'ya existe: se sobreescribe')
                try:
                    os.remove(target_ascfile_name_georef)
                except:
                    print('No se ha posido eliminar la imagen', target_ascfile_name_georef, 'revisar si esta bloqueada por el sistema operativo')
                    sys.exit(5)
            target_ascfile_opened = open(target_ascfile_name_georef, 'w+')
            target_ascfile_opened.write('ncols %i \n' % (xPixelsNew))
            target_ascfile_opened.write('nrows %i \n' % (yPixelsNew))
            target_ascfile_opened.write('xllcenter %0.3f \n' % (int(origenX_raster + (ancho_pixel / 2)))) #Centro del pixel abajo izda
            target_ascfile_opened.write('yllcenter %0.3f \n' % (int(origenY_raster + (alto_pixel / 2)))) #Centro del pixel abajo izda
            target_ascfile_opened.write('cellsize %0.3f \n' % (ancho_pixel))
            target_ascfile_opened.write('nodata_value %i \n' % (NODATA))
            for row in range(yPixelsNew):
                for col in range(xPixelsNew):
                    codigoColor = reading_band_asArrayIntDictNew[nBand][row, col]
                    valor = NODATA
                    for valorPrecipitacion in listaValoresPrecipitacion:
                        if codigoColor in dictListaColoresPorValorPrecipitacion[valorPrecipitacion]:
                            valor = valorPrecipitacion
                    target_ascfile_opened.write('%03i ' % valor)
                target_ascfile_opened.write('\n')
            target_ascfile_opened.close
    

if __name__ == '__main__':
    pass

