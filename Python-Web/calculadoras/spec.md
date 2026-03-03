# Calculadoras

## Reqisitos funcionales

Aplicación que permite crear calculadoras de varios tipos.
Los usuarios  de la aplicación podrán crear calculadoras.
Cada calculadora tendrá un identificador único, decidido por la aplicación
cuando se crea la calculadora.
Tendremos calculadoras de dos tipos:
* Calculadoras de IVA. Calcula el IVA de la cantidad que le demos
* Calculadoras de sumas. Suma las dos cantidades que le demos.

Para crear una calculadora la aplicación ofrecerá un formulario con
un botón.
Cada calculadora tendrá su propio recurso. Cuando se invoque ese recurso,
devolverá un formulario para que el usuario indique los datos para calcular.
Tras ponerlos y darle a enviar,  el usuario verá la cantidad resultante,
y de nuevo el formulario de la calculadora.

## Requisitos no funcionales

* Utiliza la clase http.server
* Genera un único programa llamado calculadoras.py
* Utiliza el módulo uuid para generar identificadores únicos

## Estado

* Variable compartida calculadoras
  * Es un diccionario
  * Claves: identificadores de calculadoras
  * Valores: diccionario:
    * tipo: tipo de calculadora
    * valor: valor de la calculadora.
      * Para las calculadoras de IVA, un único número (la cantidad)
      * Para las calculadoras de sumas, una tupla con dos números.

## Código de inicialización

* Reconoce un argumento de línea de comandos, que será el puerto en el que
hay que lanzar el servidor HTTP

## Recursos

### / GET

* Petición: nada en particular
* Respuesta:
  * Cuerpo: HTML
    * con formulario para crear una calculadora
    * con listado de todas las calculadoras en el diccionario calculadoras
      * para cada calculadora: enlace a la calculadora, y tipo de la calculadora

### / POST

* Petición:
  * Cuerpo: query string: crear=<tipo>
    * <tipo> puede ser "iva" o "suma"
* Respuesta:
  * Cuerpo: HTML con enlace a la calculadora creada
* Modificación de estado:
  * Nueva clave en diccionario calculadoras:
    * Clave: id de la calculadora
    * Valor: {tipo: <tipo>, valor: None}

### /calcs/<id> GET

* Petición: nada en particular
* Respuesta:
  * Cuerpo: HTML con formulario para la calculadora correspondiente

### /calcs/<id> post

* Petición:
  * Cuerpo: query string:
    * Si tipo es "iva": valor=<valor>
    * Si tipo es "suma": sum1=<sum1>&sum2=<sum2>

* Respuesta:
  * Cuerpo: HTML con el resultado de la operación, y el formulario para poner otra cantidad
* Modificación de estado:
  * Cambio de valor en diccionario calculadoras:
    * Clave: <id>
    * Valor:
      * Clave: valor
      * Valor: <valor> o (<sum1>, <sum2>)












