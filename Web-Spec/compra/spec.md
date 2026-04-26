# Lista de la compra

## Especificación funcional

Aplicación que mantiene una lista de la compra.
Cada elemento de la lista tendrá un nombre (por ejemplo, "leche")
y una cantidad (por ejemplo 5).

La aplicación me permitirá ver los elementos de la lista y
la cantidad de cada elemento. También me permitirá incluir
nuevos elementos en la lista, darles una cantidad, y cambiar
la cantidad de un elemento que ya tenía en la lista.

## Especificación no funcional

* Usa http.server.
* Guarda las plantillas de páginas HTML, CSS, etc. en un fichero
aparte, plantillas.py
* No usa JavaScript, sólo HTML y CSS.
* Escribe el programa principal en compra.py

## Estado

* Diccionario "compra". Variable donde se almacenará la lista de la
  compra. Las claves serán los elementos, y los valores, las
  cantitades

## Recursos

* /: Recurso principal. Actuará como colección de elementos.
  * GET: Página HTML con la lista de elementos, y un formulario
    para introducir un nuevo elemento. Cada elemento de la lista
    será un enlace al recurso de ese elemento.
    El formulario hará POST sobre el mismo recurso.
  * POST: Creación de un nuevo elemento en la lista.
    * Query string: nombre=<elemento>
    * Resultado: misma página que se envía con un GET para este recurso
* /<elemento>. Recurso para cada uno de los elementos.
  * GET: Página HTML con el nombre y la cantidad del elemento.
    Si aún no se le ha dado un valor, tendría 0.
    Formulario para poder introducir la cantidad del elemento.
    El formulario hará POST sobre el mismo recurso.
  * POST: Nueva cantidad para el elemento.
    * Query string: valor=<cantidad>
    * Resultado: misma página que se envía con un GET para este recurso

## Notas de implementación

* Cuando se recibe un POST, la query string viene en el cuerpo de la petición.
* Cuando se usan plantillas que se interpretan (render) con "format" hay que
  tener cuidado si hay { o } en el texto de la plantilla, pues se identificará
  como una variable a interpretar. En estos casos, hay que "escaparlas" como
  }} o {{.