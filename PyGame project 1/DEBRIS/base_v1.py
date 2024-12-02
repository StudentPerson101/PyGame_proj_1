# base - v1

import pygame
import sys

# Initialize PyGame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DEBRIS")

# Define the Player1 class


# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player1 position (follow indentation)
    

    # Clear screen (follow indentation)
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw player1 (follow indentation) ()
    

    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

