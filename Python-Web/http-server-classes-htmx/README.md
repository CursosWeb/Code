## ContentApp usando HTMX

Demos simples de uso de HTMX en combinación con ContentApp:

* webapp.py: Clase base WebApp
* contentapp.py: Ejemplo sencillo de uso de HTMX. La aplicación sirve en el recurso principal (`/`) una página HTML que incluye elementos HTMX. En particular, cuando se pulsa el botón, se realiza un GET sobre el recurso `/hola`, y se recibe su valor (que sirve la aplicación). Ambos recursos se almacenan en el diccionario `self.contents`, y la aplicación simplemente sirve lo que hay en ese diccionario cuando se le pide con `GET`.
* contentapp-post.py: Ejemplo de HTMX, incluyendo `GET` y `POST`. En cualquier recurso que no comience por `/content/`, la aplicación sirve una página HTML para ese recurso. Esa página incluye elementos HTMX para hacer un `GET` o un `POST` a `/content/<recurso>`, y un campo para escribir texto. Por ejemplo, si el recurso es `/hola`, el `GET` y el `POST` se hacen sobre `/content/hola`. El `GET` obtiene el contenido del diccionario para ese recurso (si lo hay) y el `POST` pone lo que haya en el campo para escribir texto como contenido del diccionario para ese recurso.