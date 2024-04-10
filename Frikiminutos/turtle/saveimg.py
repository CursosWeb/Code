import turtle
from PIL import Image
import random

# Crear una ventana para dibujar
ventana = turtle.Screen()

# Crear una tortuga
tortuga = turtle.Turtle()
tortuga.speed(0)  # Establecer la máxima velocidad de dibujo

# Definir una función para dibujar una estrella de n lados
def dibujar_estrella(tortuga, tamaño, n, color):
    tortuga.color(color)
    tortuga.begin_fill()
    for _ in range(n):
        tortuga.forward(tamaño)
        tortuga.right(180 - 180 / n)
    tortuga.end_fill()

# Dibujar un patrón colorido y complejo
for _ in range(36):
    color = random.choice(["red", "orange", "yellow", "green", "blue", "purple"])
    tortuga.penup()
    tortuga.goto(random.randint(-200, 200), random.randint(-200, 200))
    tortuga.pendown()
    dibujar_estrella(tortuga, random.randint(50, 150), random.randint(5, 12), color)

# Ocultar la tortuga al finalizar el dibujo
tortuga.hideturtle()

# Guardar la imagen en un archivo
nombre_archivo = "logo.png"
canvas = ventana.getcanvas()
canvas.postscript(file="temp.eps")
imagen = Image.open("temp.eps")
imagen.save(nombre_archivo)

# Cerrar la ventana al hacer clic
ventana.exitonclick()