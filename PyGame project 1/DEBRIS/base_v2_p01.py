#  base - v2_p1 - player class

import pygame
import sys

# Initialize PyGame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Follow with Player1 Object")

# Define the Player1 class
class Player1:
    def __init__(self, color, size, speed):
        self.color = color
        self.size = size
        self.pos = [screen_width // 2, screen_height // 2]  # Start at center
        self.speed = speed  # Speed affects how quickly it moves towards the mouse

    def update(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Smoothly interpolate player position towards the mouse
        self.pos[0] += (mouse_x - self.pos[0]) * self.speed
        self.pos[1] += (mouse_y - self.pos[1]) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

# Initialize the Player1 object
player1 = Player1(color=(0, 32, 96), size=20, speed=0.4)  # 0.4 for gradual movement (changed to 0.4)

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player1 position
    player1.update()

    # Clear screen
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw player1
    player1.draw(screen)

    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

