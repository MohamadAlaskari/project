import pygame
import random
import sys

# Fenstergröße
WIDTH = 800
HEIGHT = 600


# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Geschwindigkeit des Spielers
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Größe und Geschwindigkeit der Hindernisse
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 3

# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hindernisvermeidungsspiel")

clock = pygame.time.Clock()

# Klasse für den Spieler
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH ,PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        #koordinaten des spieler
        self.rect.x = 50
        self.rect.y = HEIGHT // 2


    def update(self):
        # Spielerbewegung
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= PLAYER_SPEED
            
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - 50:
            self.rect.y += PLAYER_SPEED

# Klasse für Hindernisse
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - OBSTACLE_HEIGHT)

    def update(self):
        # Hindernisbewegung
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - OBSTACLE_HEIGHT)

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Erzeugung der Hindernisse
for i in range(5):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

def show_game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Kollisionserkennung
    if pygame.sprite.spritecollide(player, obstacles, True):
        show_game_over()
        running = False

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
