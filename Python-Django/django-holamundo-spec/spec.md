# Hola Mundo en Django

## Requisitos funcionales / Descripción

* Aplicación web mínima en Django que muestra un mensaje de bienvenida.
* Al acceder al recurso raíz (`/`), se mostrará una página HTML con el título "Hola Mundo" y un mensaje de bienvenida.
* Al acceder al recurso `/about/`, se mostrará una página con información sobre la aplicación.

## Requisitos NO funcionales

* Usa Django como framework web.
* Nombre del proyecto Django: `holamundo_project`
* Nombre de la app Django: `holamundo`
* No uses plantillas (templates) de Django. Devuelve el HTML directamente desde las vistas con `HttpResponse`.
* No uses modelos ni base de datos.
* No uses JavaScript.
* El HTML devuelto debe incluir una estructura básica válida (`<html>`, `<head>`, `<body>`).

## Estado

* No se necesita estado. No hay datos persistentes.

## Recursos

* `/` : Página principal
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "¡Hola Mundo!"
    * Párrafo `<p>`: "Bienvenido a mi primera aplicación Django"
    * Un enlace `<a>` a `/about/`

* `/about/` : Página "Acerca de"
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Acerca de"
    * Párrafo `<p>`: "Esta es mi primera aplicación web con Django"
    * Un enlace `<a>` a `/` para volver a la página principal

## Estructura de archivos esperada

```
holamundo_project/
├── manage.py
├── holamundo_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── holamundo/
    ├── __init__.py
    ├── views.py
    └── urls.py
```
