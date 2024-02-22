# Código

Código fuente utilizado en las asignaturas apoyadas en [CursosWeb](http://cursosweb.github.io "CursosWeb").

## Problemas comunes en los laboratorios Linux de la EIF

Estas son las soluciones a algunos problemas comunes en los laboratorios. Si no ves tu problema aquí, o la solución que ves aquí no te funciona, díselo a un profesor, a ver si te puede ayudar. Si consigues resolver un problema que no está aquí, o de una forma diferente o mejor a la que está aquí, dile a un profesor, para que lo pueda reflejar. O, mejor, si sabes, haz un pull request con el texto que cambiarías en este fichero, y avisa algún profesor para que lo mire y en su caso lo acepte.

### No arranca Chrome

**Síntoma:** Pulso el icono de Chrome en el escritorio, y no arranca (no llega a salir la ventana de Chrome)

**Solución:** Es muy posible que lo que ocurre es que en algún momento (quizás en una sesión VNC), un navegador se ha quedado abierto, sin eliminar un fichero que indica que está funcionando. Si ha ocurrido esto, al arrancar el nuevo chrome, busca ese fichero, ve que está, y piensa que el otro chrome sigue funcionando (aunque no sea ya el caso). La solución es eliminar ese fichero (primero nos cambiamos al directorio principal del usuario, y luego borramos el fichero):

```shell
cd
rm .config/google-chrome/SingletonLock
```

Si el problema era ese, ahora debería aparecer ya cuando le des al icono en el escritorio. Si no pueda así, prueba a lanzarlo desde un terminal, para ver si escribe algo en consola que nos de alguna pista:

```shell
/opt/google/chrome/chrome
```

Si lo que escriba en pantalla no te diera ninguna pista, díselo al profesor, o a un técnico del laboratorio, a ver si a ellos sí se la da, y te pueden ayudar.