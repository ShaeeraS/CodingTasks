import pygame
import random
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# define font
font = pygame.font.SysFont('Constantia', 30)

# define colours
bg = (234, 218, 184)
# block colours
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
# paddle colours
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
# text colour
text_col = (78, 81, 139)

# define game variables
cols = 6
rows = 8  # Changed to 8 rows of bricks
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = False  # Changed to boolean
lives = 5  # Added variable to track lives
score = 0  # Added variable to track score

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        # define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)

# paddle class
class paddle():
    def __init__(self):
        self.reset()

    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        # define paddle variables
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

# ball class
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        global score  # Need to modify the global score variable
        global lives  # Need to modify the global lives variable

        # collision threshold
        collision_thresh = 5

        # start off with the assumption that the wall has been destroyed completely
        wall_destroyed = True  # Changed to boolean
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                        score += 1  # Increment score when a brick is destroyed
                        # Randomly spawn a power-up when a brick is destroyed
                        if random.random() < 0.1:  # Adjust spawn probability as needed
                            spawn_power_up(item[0].centerx, item[0].centery)

                # check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = False
                # increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed:
            self.game_over = True

        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            lives -= 1  # Decrement lives when the ball touches the bottom
            if lives == 0:
                self.game_over = True

        # look for collision with paddle
        if self.rect.colliderect(player_paddle):
            # check if colliding from the top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = False  # Reset game over status when ball is reset

# Power-up class
class PowerUp:
    def __init__(self, x, y, power_up_type):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 0, 0)  # Red color for demonstration
        self.power_up_type = power_up_type
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Define power-up types and effects
POWERUP_TYPES = ['increase_paddle_width', 'decrease_paddle_width', 'extra_life', 'multi_ball']
POWERUP_EFFECTS = {
    'increase_paddle_width': lambda: increase_paddle_width(),
    'decrease_paddle_width': lambda: decrease_paddle_width(),
    'extra_life': lambda: gain_life(),
    'multi_ball': lambda: spawn_multi_ball()
}

# Function to spawn a power-up
def spawn_power_up(x, y):
    global active_power_up
    power_up_type = random.choice(POWERUP_TYPES)
    active_power_up = PowerUp(x, y, power_up_type)

# Function to activate power-up effects
def activate_power_up():
    global active_power_up
    if active_power_up:
        POWERUP_EFFECTS[active_power_up.power_up_type]()
        active_power_up = None

# Function to increase paddle width
def increase_paddle_width():
    player_paddle.width += 20
    player_paddle.rect.width += 20

# Function to decrease paddle width
def decrease_paddle_width():
    player_paddle.width -= 20
    player_paddle.rect.width -= 20

# Function to gain an extra life
def gain_life():
    global lives
    lives += 1

# Function to spawn multiple balls
def spawn_multi_ball():
    # Implement spawning multiple balls logic here
    pass  # Placeholder for now

# create a wall
wall = wall()
wall.create_wall()

# create paddle
player_paddle = paddle()

# create ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True

# function to display lives and score
def display_stats():
    draw_text(f"Lives: {lives}", font, text_col, 10, 10)
    draw_text(f"Score: {score}", font, text_col, screen_width - 160, 10)

active_power_up = None

while run:
    clock.tick(fps)

    screen.fill(bg)

    # draw all objects
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        # draw paddle
        player_paddle.move()
        # draw ball
        game_over = ball.move()
        if game_over:
            live_ball = False

    # print player instructions
    if not live_ball:
        if game_over:
            draw_text('GAME OVER!', font, text_col, 200, screen_height // 2 - 50)
            draw_text('CLICK ANYWHERE TO PLAY AGAIN', font, text_col, 100, screen_height // 2 + 50)
        else:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)

    display_stats()

    # Draw and check power-up collision
    if active_power_up:
        active_power_up.draw()
        if active_power_up.rect.colliderect(player_paddle.rect):
            activate_power_up()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
            lives = 5

    pygame.display.update()

pygame.quit()
