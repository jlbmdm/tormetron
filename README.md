# Tormetron

Tormetron es un paquete destinado a descargar, guardar y procesar imágenes ofrecidas por AEMET (www.aemet.es) referentes a:
  * Radares de precipitación. Fuente: API de AEMET ([aemet open data](https://opendata.aemet.es/)).
  * Precipitación acumulada de 6 horas. Fuente: web de AEMET ([aemet radar](http://www.aemet.es/es/eltiempo/observacion/radar)).
  
Página web ~~en preparación~~

## Descarga e instalación

Se puede descargar e instalar en un solo paso desde [PyPI](https://pypi.org/project/tormetron/):

* Versión de prueba en test.pypi.org:

```
$ pip install -i https://test.pypi.org/simple/ tormetron==0.0.1
```

* Última versión disponible en pypi:

```
$ pip install tormetron
```

Tormetron funciona en Python 2.7 y en Python 3.4 o superior.

Se puede descargar la versión en desarrollo disponible en [github](https://github.com/jlbmdm/tormetron) (repositorio provisionalmente privado; se hará público con la versión 1.0.0)

Si se descarga el paquete desde github, se puede instalar para que esté disponible para python (en lib/site-packages). Para ello, desde la consola de comandos (cmd en Windows):

```
$ cd ruta_del_proyecto
$ pip install .

```

o bien con el método antiguo (menos recomendable):

```
$ cd ruta_del_proyecto
$ python setup.py install
```
>ruta\_del\_proyecto es la carpeta del proyecto (la que contine el setup.py)

## Uso de tormetron

Para descargar imágenes de radar de la API de AEMET es necesario obtener antes una API_KEY de [AEMET](https://opendata.aemet.es/centrodedescargas/altaUsuario)

### Uso en linea de comandos

    $ python -m radatron [ options ]
    
&nbsp;&nbsp;&nbsp;&nbsp;options:

--radar n
&nbsp;&nbsp;n: &nbsp;&nbsp;1 ultimo radar
&nbsp;&nbsp;2 acum de las ultimas 6 horas

--estacion nombre
&nbsp;&nbsp;nombre: nombre o codigo de la estación radar; por defecto, Palencia

--modo m
&nbsp;&nbsp;m: &nbsp;&nbsp;p descarga puntual
&nbsp;&nbsp;c descarga programada la cada 10 minutos -último radar- o 24 horas -acum de las últimas 6 horas-

--carpeta dir
&nbsp;&nbsp;dir: nombre de la carpeta en la que guardar las imágenes; por defecto, "data"
			
Los comandos se puede abreviar respectivamente: -r, -e, -m, -c

Ejemplos:

```  
$ python -m radatron -r 2 -e Palencia -m c --carpeta radarPalencia

$ python -m radatron --radar 1 --estacion Madrid
```

### Uso desde un script de python:

Para usarlo desde un script el paquete debe estar instalado en site-packages o estar disponible para el script de forma que pueda importarse el paquete radatron:

```
	>>> import radatron

	>>> estacion_radar = radatron.EstacionRadar('Palencia')

	>>> imagen_radar = radatron.ImagenRadarAEMET(estacion_radar)

	>>> imagen_radar.descargar_mapa_radar_regional()
```

TODO: Pendiente completar las instrucciones


## Organización interna

Tormetron incluye un paquete llamado __tormetron__ con un módulo principal, _radares.py_, que tiene tres clases:

- Class EstacionRadar     -> Incluye métodos para buscar/identificar una estación radar
  
- Class ImagenRadarAEMET  -> Incluye métodos para descargar imágenes radar de AEMET

- Class ImagenRadarFile   -> Con métodos para procesar georreferenciar imágenes descargadas

Las clases y sus métodos se documentarán próximamente.

El script \_\_main\_\_.py utiliza estas clases para:

 * Obtener imagen(es) rádar

  o bien:

 * Obtener imagen de precipitación de las últimas 6 horas
    
En ambos casos se puede descargar:
		
 * 0 Modo puntual: ultima imagen disponible
			
 * 1 Modo continuo: descarga la imagen disponble cada 10 minutos (tiempo de actualización)

En el caso del radar, AEMET actualiza la imagen cada 10 minutos. Para la imagen de precipitaciónde las últimas horas, AEMET ofrece las últimas 8 imagenes, correspondientes a los 4 momentos de referencia del día (AEMET genera estas imágenes a las 00:00, 06:00, 12:00 y 18:00 cada día).

