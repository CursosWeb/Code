import turtle

# Crear una ventana para dibujar
ventana = turtle.Screen()

# Crear una tortuga
tortuga = turtle.Turtle()

# Dibujar un cuadrado
for _ in range(4):  # Repetir 4 veces para dibujar los 4 lados del cuadrado
    tortuga.forward(100)  # Avanzar 100 píxeles
    tortuga.right(90)  # Girar 90 grados hacia la derecha

# Cerrar la ventana al hacer clic
ventana.exitonclick()