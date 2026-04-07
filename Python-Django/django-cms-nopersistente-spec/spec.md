# Servidor de Contenidos Django

## Requisitos funcionales / Descripción

* Aplicación web en Django que sirve contenidos almacenados en un diccionario.
* El diccionario se define directamente en `views.py` y contiene pares clave-valor donde la clave es el nombre del recurso y el valor es el contenido HTML o texto asociado.
* La página principal lista todos los recursos disponibles como enlaces.
* Al acceder a un recurso, se muestra su contenido.
* Si se accede a un recurso que no existe en el diccionario, se devuelve un error 404 con un mensaje informativo.

## Requisitos NO funcionales

* Usa Django como framework web.
* Nombre del proyecto Django: `contenidos_project`
* Nombre de la app Django: `contenidos`
* No uses plantillas (templates) de Django. Devuelve el HTML directamente desde las vistas con `HttpResponse`.
* No uses modelos ni base de datos.
* No uses JavaScript.
* El diccionario de contenidos debe estar definido como variable global en `views.py`.
* Usa el conversor `<str:recurso>` en las URLs de Django para capturar el nombre del recurso.

## Estado

* Diccionario `CONTENIDOS` definido en `views.py`:
  ```python
  CONTENIDOS = {
      "python": "Python es un lenguaje de programación de alto nivel, interpretado y multiparadigma.",
      "html": "HTML (HyperText Markup Language) es el lenguaje de marcado estándar para crear páginas web.",
      "css": "CSS (Cascading Style Sheets) es un lenguaje de diseño para definir la presentación de documentos HTML.",
      "django": "Django es un framework web de alto nivel escrito en Python que fomenta el desarrollo rápido.",
      "http": "HTTP (HyperText Transfer Protocol) es el protocolo de comunicación utilizado en la World Wide Web.",
  }
  ```

## Recursos

* `/` : Página principal
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Servidor de Contenidos"
    * Párrafo `<p>`: "Recursos disponibles:"
    * Lista `<ul>` con todos los recursos del diccionario, donde cada elemento es un enlace `<a>` a `/<nombre_recurso>/`

* `/<str:recurso>/` : Página de un recurso
  * GET: 
    * Si el recurso **existe** en el diccionario, devuelve una página HTML con:
      * Título `<h1>`: el nombre del recurso (capitalizado)
      * Párrafo `<p>`: el contenido asociado en el diccionario
      * Enlace para volver a `/`
    * Si el recurso **no existe** en el diccionario, devuelve un error HTTP 404 con:
      * Título `<h1>`: "Error 404"
      * Párrafo `<p>`: "El recurso '`<nombre_recurso>`' no fue encontrado"
      * Enlace para volver a `/`

## Estructura de archivos esperada

```
contenidos_project/
├── manage.py
├── contenidos_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── contenidos/
    ├── __init__.py
    ├── views.py
    └── urls.py
```
