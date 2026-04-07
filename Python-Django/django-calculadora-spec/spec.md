# Calculadora Django

## Requisitos funcionales / Descripción

* Aplicación web en Django que funciona como una calculadora.
* Las operaciones se realizan a través de la URL, pasando la operación y los dos operandos como partes del recurso.
* La página principal muestra las instrucciones de uso con ejemplos de cada operación.
* Al realizar una operación, se muestra el resultado en una página HTML.
* Si se intenta dividir entre cero, se mostrará un mensaje de error.

## Requisitos NO funcionales

* Usa Django como framework web.
* Nombre del proyecto Django: `calculadora_project`
* Nombre de la app Django: `calculadora`
* No uses plantillas (templates) de Django. Devuelve el HTML directamente desde las vistas con `HttpResponse`.
* No uses modelos ni base de datos.
* No uses JavaScript.
* Usa los conversores de tipo `<int:a>` y `<int:b>` en las URLs de Django para capturar los operandos.

## Estado

* No se necesita estado. No hay datos persistentes.

## Recursos

* `/` : Página principal
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Calculadora Django"
    * Lista de operaciones disponibles, donde cada una sea un enlace de ejemplo:
      * `/sumar/10/5/` → Suma
      * `/restar/10/5/` → Resta
      * `/multiplicar/10/5/` → Multiplicación
      * `/dividir/10/5/` → División

* `/sumar/<int:a>/<int:b>/` : Suma
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Resultado de la suma"
    * Párrafo `<p>`: "`a` + `b` = `resultado`"
    * Enlace para volver a `/`

* `/restar/<int:a>/<int:b>/` : Resta
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Resultado de la resta"
    * Párrafo `<p>`: "`a` - `b` = `resultado`"
    * Enlace para volver a `/`

* `/multiplicar/<int:a>/<int:b>/` : Multiplicación
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Resultado de la multiplicación"
    * Párrafo `<p>`: "`a` × `b` = `resultado`"
    * Enlace para volver a `/`

* `/dividir/<int:a>/<int:b>/` : División
  * GET: Devuelve una página HTML con:
    * Título `<h1>`: "Resultado de la división"
    * Párrafo `<p>`: "`a` / `b` = `resultado`"
    * Enlace para volver a `/`
    * Si `b` es 0, en lugar del resultado mostrar: "Error: no se puede dividir entre cero"

## Estructura de archivos esperada

```
calculadora_project/
├── manage.py
├── calculadora_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── calculadora/
    ├── __init__.py
    ├── views.py
    └── urls.py
```
