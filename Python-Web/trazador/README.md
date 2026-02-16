# Trazador

Programa y ficheros correspondientes al ejercicio "Traza de historiales de navegación por terceras partes (implementación)". El programa `trazador.py` es una solución parcial que implementa un trazador capaz de trazar el momento en que se pidió un recurso del servidor trazado (incluyendo tanto el momento, como el recurso, como un identificador único para el navegador que lo pidió).

Para probar este trazador, puede usarse la página `hola.html` que está en el directorio `web`, y que incluye un elemento IMG (una imagen) que se obtiene del trazador: esa es la forma en que el trazador "sabe" que el recurso `/hola.html` fue solicitado.

Así pues, el servidor web trazado se lanzará ejecutando el módulo Python que proporciona un servidor web, desde el directorio `web`, y de forma que quede escuchando en el puerto 8002 (que será al que apunte la imagen indicada anteriormente):

```
cd web
python3 -m http.server 8002
```

Luego, se lanza en otro terminal el programa trazador, que escuchará en el puerto 8000:

```
python3 trazador.py
```
