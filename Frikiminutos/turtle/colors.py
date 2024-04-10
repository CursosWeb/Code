import turtle

# Crear una ventana para dibujar
ventana = turtle.Screen()

# Crear una tortuga
tortuga = turtle.Turtle()

# Definir los colores para los lados de la espiral
colores = ['red', 'blue', 'green', 'purple']

# Dibujar una espiral cuadrada
lado = 10
for i in range(100):
    tortuga.color(colores[i % 4])  # Seleccionar un color de la lista en cada iteración
    tortuga.forward(lado)
    tortuga.right(90)
    lado += 10  # Incrementar el tamaño del lado para aumentar el tamaño de la espiral

# Cerrar la ventana al hacer clic
ventana.exitonclick()