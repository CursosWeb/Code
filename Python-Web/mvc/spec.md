# Plataforma MVC

## Especificación funcional

Sistema que permite construir aplicaciones HTTP siguiendo un modelo arquitectural MVC (modelo, vista controlador). Las aplicaciones van a estar definidas por qué estado mantienen, qué recursos y métodos sobre estos recursos ofrecen para consultar o modificar ese estado, y qué semántica (comportamiento) concreto se especifica para esos recursos.

Siguendo MVC, los principales componentes serán:

* Modelo: Gestiona el estado y los datos, que se almacenarán persistentemente. Proporcionará mecanismos para manejar este estado de forma lo más genérica posible, de forma que sirva para diferentes lógicas de aplicación.
* Vista: Presenta la información (páginas HTML, formularios, etc.) al usuario, y atiende a sus peticiones (query strings en POST, por ejemplo). La lógica de aplicación específica se dejará para que la proporcione quien desarrolla la aplicación.
* Controlador: Maneja las peticiones HTTP y coordina modelo y vista. Se encargará de toda la incialización para poder atender peticiones HTTP, y de proporcionar mecanismos para llamar a la lógica de aplicación según las peticiones HTTP recibidas, para acceder al estado (vía el modelo) cuando sea preciso.

# Especificación no funcional

* Utliza sockets.server para la comunicación, incluyendo la inicialización, la recepción de peticiones y emisión de respuestas HTTP.
* Utiliza un diccionario Python para almacenar el estado.
* Proporciona persistencia a ese diccionario usando algún módulo de la biblioteca estándar de Python.
* Usa solo módulos de la biblioteca estándar de Python.
* No utilices decoradores para indicar a qué recursos o qué operaciones HTTP atiende una vista: usa código explícito para indicar qué función (vista) se invoca cuando se recibe la petición para una familia de recursos con una operación HTTP concreta.
* Asegúrate de que la lógica de aplicación está completamente separada de la del framework. Para comprobarlo, haz dos aplicaciones de ejemplo: todo el código común debería estar en los ficheros de framework.
* Para HTML y CSS usa plantillas (templates de Python) separadas del código que las usa, de forma que sea faćil cambiar el aspecto de la aplicación sin tocar el código.
