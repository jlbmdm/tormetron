# Tormetron

Tormetron es un paquete destinado a descargar y procesar imágenes ofrecidas por AEMET (www.aemet.es) referentes a:

  * Radares de precipitación. Fuente: API de AEMET ([aemet open data](https://opendata.aemet.es/)).

  * Precipitación acumulada de 6 horas. Fuente: web de AEMET ([aemet radar](http://www.aemet.es/es/eltiempo/observacion/radar)).
  
Página web en preparación: [tormetron](https://tormetron.com/).


## Descarga e instalación

Se puede descargar tormetron de [PyPI](https://pypi.org/project/tormetron/):

    pip install tormetron

Tormetron funciona en Python 2.7 y en Python 3.5 y superior.

Versión en desarrollo en github ([repositorio provisionalmente privado; se hará público con la versión 1.0.1](https://github.com/jlbmdm/tormetron))

Si se descarga el paquete desde github, se puede instalar en el site-packages de python desde el cmd, ubicandose en carpeta del proyecto en la que está el setup.py ($ cd ruta_del_proyecto), mediante:

    $ pip install .

o bien con el método antiguo (menos recomendable):

    $ python setup.py install

## Uso de tormetron

Para descargar imágenes de radar de la API de AEMET es necesario obtener antes una API_KEY de [AEMET](https://opendata.aemet.es/centrodedescargas/altaUsuario)

# Uso en linea de comandos:

    $ python -m radatron [ options ]
    
options:

 --radar n
 		 (n: 1-> ultimo radar; 2-> acum de las ultimas 6 horas)

 --estacion nombre
 		 (nombre: nombre o codigo de la estacón radar; por defecto, Palencia)
		
 --modo m
 		 (m: p-> descarga puntual; c-> descarga programada la cada 10 minutos -último radar- o 24 horas -acum de las últimas 6 horas-)
		
 --carpeta dir
 		 (dir: nombre de la carpeta en la que guardar las imágenes; por defecto, "data")
			
Los comandos se puede abreviar respectivamente: -r, -e, -m, -c

  Ejemplos:
  
		$ python -m radatron --radar 1 --estacion Madrid
    
		$ python -m radatron -r 2 -e Palencia -m c --carpeta radarPalencia


Para usarlo desde un script el paquete debe estar instalado en site-packages o estar disponible para el script:

	>>> import radatron

	>>> estacion_radar = radatron.EstacionRadar('Palencia')

	>>> imagen_radar = radatron.ImagenRadarAEMET(estacion_radar)

	>>> imagen_radar.descargar_mapa_radar_regional()


TODO: Pendiente completar las instrucciones


## Organización interna

Tormetron incluye un paquete llamado __radatron__ con un módulo principal, _radares.py_, que tiene tres clases:

  Class EstacionRadar     -> Incluye métodos para buscar/identificar una estación radar
  
  Class ImagenRadarAEMET  -> Incluye métodos para descargar imágenes radar de AEMET

  Class ImagenRadarFile   -> Con métodos para procesar georreferenciar imágenes descargadas

Las clases y sus métodos se documentarán próximamente.

El script \_\_main\_\_.py utiliza estas clases para:

 * Obtener imagen(es) rádar

  o bien:

 * Obtener imagen de precipitación de las últimas 6 horas
    
En ambos casos se puede descargar:
		
 * 0 Modo puntual: ultima imagen disponible
			
 * 1 Modo continuo: descarga la imagen disponble cada 10 minutos (tiempo de actualización)

En el caso del radar, AEMET actualiza la imagen cada 10 minutos. Para la imagen de precipitaciónde las últimas horas, AEMET ofrece las últimas 8 imagenes, correspondientes a los 4 momentos de referencia del día (AEMET genera estas imágenes a las 00:00, 06:00, 12:00 y 18:00 cada día).

