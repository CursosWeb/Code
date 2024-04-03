import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH = 600
HEIGHT = 400
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración del jugador
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Configuración del obstáculo
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 3

# Función para generar un nuevo obstáculo
def create_obstacle():
    x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    y = 0
    return pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquiva los obstáculos")
clock = pygame.time.Clock()

# Inicializar jugador
player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

# Lista de obstáculos
obstacles = []

# Tiempo entre generación de obstáculos
obstacle_timer = 0
OBSTACLE_INTERVAL = 50

# Puntuación
score = 0

# Loop principal del juego
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += PLAYER_SPEED

    # Generar obstáculos
    obstacle_timer += 1
    if obstacle_timer >= OBSTACLE_INTERVAL:
        obstacles.append(create_obstacle())
        obstacle_timer = 0

    # Mover obstáculos
    for obstacle in obstacles:
        obstacle.y += OBSTACLE_SPEED
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)
            score += 1

    # Colisiones con obstáculos
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            running = False

    # Limpiar pantalla
    screen.fill(BLACK)

    # Dibujar jugador
    pygame.draw.rect(screen, WHITE, player)

    # Dibujar obstáculos
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

    # Mostrar puntuación
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar velocidad de cuadros por segundo
    clock.tick(FPS)

# Mostrar mensaje de fin de juego
font = pygame.font.SysFont(None, 72)
text = font.render("¡Game Over!", True, WHITE)
text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
screen.blit(text, text_rect)
pygame.display.flip()

# Esperar un momento antes de salir
pygame.time.wait(2000)

# Salir del juego
pygame.quit()
sys.exit()