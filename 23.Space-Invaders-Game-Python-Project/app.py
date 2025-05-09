import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship_icon.png")  # Optional: Add your own icon
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship.png")  # Add your spaceship image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")  # Add your enemy image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, screen_width - self.rect.width)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png")  # Add your bullet image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Game loop
def game_loop():
    running = True
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Spawn enemies
    for i in range(5):  # Number of enemies
        enemy = Enemy()
        enemies.add(enemy)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        # Update
        all_sprites.update()

        # Collision detection
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if hits:
                bullet.kill()

        # Draw everything
        all_sprites.draw(screen)
        bullets.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Start the game
game_loop()
