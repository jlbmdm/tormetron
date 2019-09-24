#Tormetron

Tormetron es un paquete destinado a descargar, guardar y procesar im�genes ofrecidas por AEMET (www.aemet.es) referentes a:
  * Radares de precipitaci�n. Fuente: API de AEMET ([aemet open data](https://opendata.aemet.es/)).
  * Precipitaci�n acumulada de 6 horas. Fuente: web de AEMET ([aemet radar](http://www.aemet.es/es/eltiempo/observacion/radar)).
  
P�gina web ~~en preparaci�n~~

##Descarga e instalaci�n

Se puede descargar e instalar en un solo paso desde [PyPI](https://pypi.org/project/tormetron/):

* Versi�n de prueba en test.pypi.org:

```
$ pip install -i https://test.pypi.org/simple/ tormetron==0.0.1
```

* �ltima versi�n disponible en pypi:

```
$ pip install tormetron
```

Tormetron funciona en Python 2.7 y en Python 3.4 o superior.

Se puede descargar la versi�n en desarrollo disponible en [github](https://github.com/jlbmdm/tormetron) (repositorio provisionalmente privado; se har� p�blico con la versi�n 1.0.0)

Si se descarga el paquete desde github, se puede instalar para que est� disponible para python (en lib/site-packages). Para ello, desde la consola de comandos (cmd en Windows):

```
$ cd ruta_del_proyecto
$ pip install .

```

o bien con el m�todo antiguo (menos recomendable):

```
$ cd ruta_del_proyecto
$ python setup.py install
```
>ruta\_del\_proyecto es la carpeta del proyecto (la que contine el setup.py)

##Uso de tormetron

Para descargar im�genes de radar de la API de AEMET es necesario obtener antes una API_KEY de [AEMET](https://opendata.aemet.es/centrodedescargas/altaUsuario)

###Uso en linea de comandos

    $ python -m radatron [ options ]
    
&nbsp;&nbsp;&nbsp;&nbsp;options:

>--radar n
>>n: &nbsp;&nbsp;&nbsp;&nbsp;1 ultimo radar
>>>2 acum de las ultimas 6 horas

>--estacion nombre
>>nombre: nombre o codigo de la estaci�n radar; por defecto, Palencia

>--modo m
>>m: &nbsp;&nbsp;&nbsp;&nbsp;p descarga puntual
>>>c descarga programada la cada 10 minutos -�ltimo radar- o 24 horas -acum de las �ltimas 6 horas-

>--carpeta dir
>>dir: nombre de la carpeta en la que guardar las im�genes; por defecto, "data"
			
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


## Organizaci�n interna

Tormetron incluye un paquete llamado __tormetron__ con un m�dulo principal, _radares.py_, que tiene tres clases:

- Class EstacionRadar     -> Incluye m�todos para buscar/identificar una estaci�n radar
  
- Class ImagenRadarAEMET  -> Incluye m�todos para descargar im�genes radar de AEMET

- Class ImagenRadarFile   -> Con m�todos para procesar georreferenciar im�genes descargadas

Las clases y sus m�todos se documentar�n pr�ximamente.

El script \_\_main\_\_.py utiliza estas clases para:

 * Obtener imagen(es) r�dar

  o bien:

 * Obtener imagen de precipitaci�n de las �ltimas 6 horas
    
En ambos casos se puede descargar:
		
 * 0 Modo puntual: ultima imagen disponible
			
 * 1 Modo continuo: descarga la imagen disponble cada 10 minutos (tiempo de actualizaci�n)

En el caso del radar, AEMET actualiza la imagen cada 10 minutos. Para la imagen de precipitaci�nde las �ltimas horas, AEMET ofrece las �ltimas 8 imagenes, correspondientes a los 4 momentos de referencia del d�a (AEMET genera estas im�genes a las 00:00, 06:00, 12:00 y 18:00 cada d�a).

