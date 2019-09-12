# Tormetron

Tormetron es un paquete destinado a descargar y procesar imágenes del radar de precipitación o de imágenes con la precipitación de 6 horas de [AEMET](www.aemet.es) usando la API de AEMET ([aemet open data](https://opendata.aemet.es/).)

Para más información consultar: [tormetron](https://tormetron.com/).

## Installation

Se puede descargar tormetron de [PyPI](https://pypi.org/project/tormetron/):

    pip install tormetron

Tormetron funciona en Python 2.7 y en Python 3.5 y superior.

## Uso de tormetron

Uso en linea de comandos:
  $ python -m radatron [ops]
    ops:
    --radar n
      Donde n: 1-> ultimo radar; 2-> acum de las ultimas 6 horas
    --estacion nombre
      Donde Nombre: Nombre o codigo de la estacón radar; por defecto, Palencia
    --modo m
      Donde m: p-> descarga puntual; c-> descarga programada la cada 10 minutos (último radar) o 24 horas (acum de las últimas 6 horas)
    --carpeta dir
      Donde dir: nombre de la carpeta en la que guardar las imágenes; por defecto, "data"
  Los comandos se puede abreviar respectivamente: -r, -e, -m, -c

  Ejemplos:
    $ python -m radatron --radar 1 --estacion Madrid
    $ python -m radatron -r 2 -e Palencia -m c --carpeta radarPalencia

Uso desde un script:
>>> import radatron
>>> imagen_radar = radatron.ImagenRadarAEMET({'nombre':'Palencia'}, verbose=True)
>>> imagen_radar.descargar_mapa_radar_regional()

TODO: completar las instrucciones

## Organización interna

Tormetron incluye un paquete llamado __radatron__ con un módulo principal, _radares.py_, que tiene tres clases:

  Class EstacionRadar     -> Lista de estaciones radar de AEMET. Tiene el método para localizar una estación a partir de su nombre o código:
  
    buscar_estacion(nombre_o_codigo)

  Class ImagenRadarAEMET  -> Con métodos para descargar imágenes radar:
  
    descargar_mapa_radar_nacional(archivo_salida)
    descargar_mapa_radar_regional(ruta_orig, cod_est, nombre_est)
    descargar_mapa_radar_regional_6h(ruta_orig, cod_est', nombre_est, urlRadarAcum6h, urlRadarAcum6h_ref1, urlRadarAcum6h_ref2)

  Class ImagenRadarFile   -> Con métodos para procesar georreferenciar imágenes descargadas:
  
    georeferenciarImagenRadar()
    guardar_raster_asc(nBandas)

El script __main__.py utiliza estas clases para:

    $ Obtener imagen rádar
    $ Obtener imagen de precipitación de las últimas 6 horas
    
    En ambos casos se puede descargar:
      0 Modo puntual: ultima imagen disponible
      1 Modo continuo: descarga la imagen disponble cada 10 minutos (tiempo de actualización)

En el caso del radar, AEMET actualiza la imagen cada 10 minutos. Para la imagen de precipitaciónde las últimas horas, AEMET ofrece las últimas 8 imagenes, correspondientes a los 4 momentos de referencia del día (AEMET genera estas imágenes a las 00:00, 06:00, 12:00 y 18:00 cada día).

