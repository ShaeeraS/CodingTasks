import pygame
import random
from pygame.locals import *

pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 600

# Colors
bg_color = (234, 218, 184)
block_colors = [(69, 177, 232), (86, 174, 87), (242, 85, 96)]
paddle_color = (142, 135, 123)
text_color = (0, 0, 0)  # Black

# Fonts
font = pygame.font.SysFont('Constantia', 30)

# Game variables
cols = 6
rows = 8
fps = 60
clock = pygame.time.Clock()
score = 0
lives = 5

# Create the screen surface
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30
        self.blocks = []

    def create_wall(self):
        for row in range(rows):
            block_row = []
            for col in range(cols):
                rect = pygame.Rect(col * self.width, row * self.height, self.width, self.height)
                strength = random.randint(1, 3)
                block_row.append([rect, strength])
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                pygame.draw.rect(screen, block_colors[block[1]-1], block[0])
                pygame.draw.rect(screen, bg_color, block[0], 2)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - self.height * 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, text_color, self.rect, 3)

class Ball:
    def __init__(self):
        self.radius = 10
        self.reset()

    def reset(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.dx = random.choice([-1, 1])
        self.dy = -1
        self.speed = 5

    def move(self):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy

        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.dx *= -1
        if self.y - self.radius <= 0:
            self.dy *= -1
        if self.y + self.radius >= screen_height:
            self.reset()
            lives -= 1

    def draw(self):
        pygame.draw.circle(screen, text_color, (self.x, self.y), self.radius)

wall = Wall()
wall.create_wall()
paddle = Paddle()
ball = Ball()

running = True
while running:
    screen.fill(bg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    wall.draw_wall()
    paddle.move()
    paddle.draw()
    ball.move()
    ball.draw()

    # Draw lives and score
    lives_text = font.render(f'Lives: {lives}', True, text_color)
    screen.blit(lives_text, (10, 10))
    score_text = font.render(f'Score: {score}', True, text_color)
    screen.blit(score_text, (screen_width - 140, 10))

    if lives == 0:
        game_over_text = font.render('Game Over', True, text_color)
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
