# Servidor web sencillo

Programas correspondientes al ejercicio "Servidor sencillo con carrito de la compra". El programa `servidor.py` es la versión más simple, mientras que `servidor2.py` es una versión un poco más completa, que usa enlaces de la forma `/objetos/{id}` para acceder a los objetos, y tiene un formulario para añadir objetos solo en las páginas de los objetos.

Realiza `servidor3.py` que funcione como `servidor2.py`, pero que además:

* permita añadir al carrito de un usuario cualquier número de objetos
* muestre si se hace un GET al recurso `/carrito` el contenido del carrito, un botón para comprar el carrigo, y un enlace para volver a la página
* si se pulsa el botón para comprar el carrito, se debe hacer un POST al recurso `/comprar`, que devolverá un formulario que pedirá un número de tarjeta de crédito, y tendrá un botón para enviar dicho número, y un enlace para volver a la página principal.
* si se pulsa el botón para enviar el número de tarjeta de crédito, se debe hacer un POST al recurso `/comprar`, que devolverá un mensaje de confirmación, y un enlace para volver a la página principal.
* todas las páginas mostarán el valor de las cabeceras `Accept-Language` y `User-Agent`, si estas cabeceras vienen en la petición HTTP.
* todas las respuestas de tu servidor incluirán una cabecera `Server` con el valor `Servidor sencillo 0.0`.

Recuerda que puedes consultar este enunciado en la guía de estudio (programa) de la asignatura.
