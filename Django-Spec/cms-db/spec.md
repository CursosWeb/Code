# Servidor de Contenidos Django

## Requisitos funcionales / Descripción

* Aplicación web en Django que permite decidir qué contenidos se almacenan en una base de datos.
* Cada contenido irá asociado a un nombre de recurso, y se mostrará cuando el navegador solicite ese recurso.
* La página principal permite crear, editar y eliminar contenidos asociados a cada recurso. También mostrará todos los recursos disponibles, como enlaces.
* Si se accede a un recurso para el que no hay contenido, se devuelve un error 404 con un mensaje informativo.

## Requisitos NO funcionales

* Trabaja en este directorio, donde estás leyendo este fichero spec.md.
* Usa Django como framework web
* Usa el entorno virtual venv-django, en el directorio padre, para ejecutar Python (y los comandos de Django)
* Nombre del proyecto Django: `cms_db`.
* Crea el proyecto en este mismo directorio, usando `django-admin startproject cms_db .`
* Nombre de la app Django: `contenidos`
* No uses plantillas (templates) de Django. Devuelve el HTML directamente desde las vistas con `HttpResponse`
* Usa modelos (models.py) para acceder a la base de datos
* No uses JavaScript.
* Usa el conversor `<str:recurso>` en las URLs de Django para capturar el nombre del recurso.


## Estado

* Tabla `Contenido`:
  * `id` (int, primary key, auto increment)
  * `recurso` (str, unique)
  * `contenido` (str)

## Recursos

* `/` : Página principal
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Servidor de Contenidos"
    * Párrafo `<p>`: "Recursos disponibles:"
    * Lista `<ul>` con todos los recursos del diccionario, donde cada elemento es un enlace `<a>` a `/<nombre_recurso>/`
    * Formulario para crear un nuevo recurso con su contenido. El formulario debe tener un campo para el nombre del recurso y otro para el contenido.
  * POST: Crea un nuevo recurso con el nombre y el contenido proporcionados en el formulario. Para ello, lo almacenará en la tabla Contenido de la base de datos.
* `/<str:recurso>/` : Página de un recurso
  * GET: 
    * Si el recurso existe en la tabla `Contenido`, devuelve una página HTML con:
      * Título `<h1>`: el nombre del recurso (capitalizado)
      * Párrafo `<p>`: el contenido asociado en el diccionario, extraido de la tabla `Contenido`
      * Enlace para volver a `/`
    * Si el recurso no existe en la tabla `Contenido`, devuelve un error HTTP 404 con:
      * Título `<h1>`: "Error 404"
      * Párrafo `<p>`: "El recurso '`<nombre_recurso>`' no fue encontrado"
      * Enlace para volver a `/`

