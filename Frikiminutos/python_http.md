## Servidor web con una línea

Servidor HTTP (sí, un servidor web), usando Python:

```
python3 -m http.server
```

El módulo `http.server` de Python incluye un servidor HTTP bastante completo. Puedes ver más detalles en la [documentación del módulo http.server de Python](https://docs.python.org/3/library/http.server.html). Especialmente, hacia el final de ese documento, puedes ver varios ejemplos sobre cómo lanzarlo desde la línea de comandos en varios escenarios. Por ejemplo:

* Para servir un directorio concreto: 
```commandline
python -m http.server --directory /tmp/
```

* Para servir en una dirección IP y un puerto concretos:
```commandline
python -m http.server 9000 --bind 127.0.0.1
```
