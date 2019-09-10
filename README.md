# Tormetron

Tormetron es un paquete destinado a descargar y procesar imágenes del radar de precipitación o de imágenes con la precipitación de 6 horas de [AEMET](www.aemet.es) usando la API de AEMET ([aemet open data](https://opendata.aemet.es/).)

Para más información consultar: [tormetron](https://tormetron.com/).

## Installation

Se puede descargar tormetron de [PyPI](https://pypi.org/project/tormetron/):

    pip install tormetron

Tormetron funciona en Python 2.7 y en Python 3.5 y superior.

## Uso de tormetron

Tormetron incluye un paquete llamado radatron con el módodulo radares.py que tiene tres clases:
  EstacionRadar     -> Lista de estaciones radar de AEMET. Tiene el metodo:
    buscar_estacion(nombre_o_codigo) para identificar la estación
  ImagenRadarAEMET  -> Con métodos para la descarga de imágenes radar:
    descargar_mapa_radar_nacional(archivo_salida)
    descargar_mapa_radar_regional(ruta_orig, cod_est, nombre_est)
    descargar_mapa_radar_regional_6h(ruta_orig, cod_est', nombre_est, urlRadarAcum6h, urlRadarAcum6h_ref1, urlRadarAcum6h_ref2)
  ImagenRadarFile   -> Con métodos para procesar georreferenciar imágenes descargadas:
    georeferenciarImagenRadar()
    guardar_raster_asc(nBandas)

El script __main__.py utiliza estas clases

TODO:

    $ tormetron 10 cada minutos
    Ver tutorial en (https://tormetron.com/)
     0 Cómo descargar
     1 Cómo buscar datos del último mes

    $ tormetrom 6 horas
    # Como descargar imágenes de precipitación en las últimas 6 horas

