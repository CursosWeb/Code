import turtle
import math

# Crear una ventana para dibujar
ventana = turtle.Screen()
ventana.bgcolor("white")  # Establecer el color de fondo de la ventana

# Crear una tortuga
tortuga = turtle.Turtle()
tortuga.speed(0)  # Establecer la máxima velocidad de dibujo

# Definir la amplitud y la frecuencia de las funciones seno y coseno
amplitud_seno = 100
frecuencia_seno = 5
amplitud_coseno = 100
frecuencia_coseno = 7

# Dibujar una curva utilizando senos y cosenos
for x in range(-180, 181, 5):
    y = amplitud_seno * math.sin(math.radians(x) * frecuencia_seno) + amplitud_coseno * math.cos(math.radians(x) * frecuencia_coseno)
    tortuga.goto(x, y)

# Ocultar la tortuga al finalizar el dibujo
tortuga.hideturtle()

# Cerrar la ventana al hacer clic
ventana.exitonclick()