# Plataforma MVC

## Especificación funcional

Sistema que permite construir aplicaciones HTTP siguiendo un modelo arquitectural MVC (modelo, vista controlador). Las aplicaciones van a estar definidas por qué estado mantienen, qué recursos y métodos sobre estos recursos ofrecen para consultar o modificar ese estado, y qué semántica (comportamiento) concreto se especifica para esos recursos.

Siguendo MVC, los principales componentes serán:

* Modelo: Gestiona el estado y los datos, que se almacenarán persistentemente. Proporcionará mecanismos para manejar este estado de forma lo más genérica posible, de forma que sirva para diferentes lógicas de aplicación.
* Vista: Presenta la información (páginas HTML, formularios, etc.) al usuario, y atiende a sus peticiones (query strings en POST, por ejemplo). La lógica de aplicación específica se dejará para que la proporcione quien desarrolla la aplicación.
* Controlador: Maneja las peticiones HTTP y coordina modelo y vista. Se encargará de toda la incialización para poder atender peticiones HTTP, y de proporcionar mecanismos para llamar a la lógica de aplicación según las peticiones HTTP recibidas, para acceder al estado (vía el modelo) cuando sea preciso.

Además, crea un módulo cookies.py para gestión de cookies, con métodos:

* Para crear una cookie
* Para extraer las cookies que vengan en una petición HTTP
* Para enviar una cookie en una respuesta HTTP
* Para eliminar una cookie

Además, crea un módulo sessions.py para implementar sesiones. Entenderemos por sesión el conjunto de nteracciones HTTP que tiene un navegdor específico con la aplicación. Proporcionaremos dos funciones:

* get_session: para que, si se llama, se compruebe si ha venido una cookie con un identificador de sesión en la petición HTTP, que devolverá
* start_session: para que, si se llama, se cree una nueva sesión y se envíe una cookie con el identificador de sesión en la respuesta HTTP

# Especificación no funcional

* Utliza sockets.server para la comunicación, incluyendo la inicialización, la recepción de peticiones y emisión de respuestas HTTP. No utilices http.server ni ningún otro módulo por encima del nivel de sockets.
* Utiliza un diccionario Python para almacenar el estado.
* Proporciona persistencia a ese diccionario usando shelve, de la biblioteca estándar de Python.
* Usa solo módulos de la biblioteca estándar de Python.
* No utilices decoradores para indicar a qué recursos o qué operaciones HTTP atiende una vista: usa código explícito para indicar qué función (vista) se invoca cuando se recibe la petición para una familia de recursos con una operación HTTP concreta.
* Asegúrate de que la lógica de aplicación está completamente separada de la del framework. Para comprobarlo, haz dos aplicaciones de ejemplo: todo el código común debería estar en los ficheros de framework.
* Para HTML y CSS usa plantillas separadas del código que las usa, de forma que sea faćil cambiar el aspecto de la aplicación sin tocar el código.
* Para las plantillas, usa solo la sintaxis que entiende "format" en Python. Nada de incluir condicionales o bucles, sólo sustitución de variables, como permite "format"
* Ten en cuenta que la sintaxis {} de las plantillas de Python puede confundirse con {} en CSS. Cuando estes usando {} en CSS, pon doble {{ o }}
