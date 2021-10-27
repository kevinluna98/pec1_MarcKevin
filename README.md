# pec1_MarcKevin

Autores: Marc Nieto y Kevin Luna

DOI Zenodo: https://doi.org/10.5281/zenodo.5597774

## Español
Este código genera un dataset que proporciona la localización y las características principales (número de habitaciones, baños, metros cuadrados, barrio y precio) de un piso en Barcelona, a fecha 24/10/2021 

Extrae los precios y caracteristicas de diferentes pisos de la página web https://www.pisos.com/viviendas/barcelones.

Para ejecutar el script es necesario instalar la siguientes bibliotecas:
```
pip install pandas
pip install requests
pip install numpy
pip install datetime
pip install beautifulsoup4
```

El script se debe ejecutar de la siguiente manera:
```
python housePriceScraper.py
```

Actualmente solo extrae información de pisos en Barcelona capital. La información extraida es la siguiente:
-  Barrio
-  Contrato
-  Descripción
-  Precio
-  Habitación
-  Baños
-  Metros


