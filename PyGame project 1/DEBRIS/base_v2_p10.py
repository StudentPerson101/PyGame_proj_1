#  base - v2_p10 - start screen + delayed timer

import pygame
import random
import sys
import math
import os

# Initialize PyGame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DEBRIS")

# Colors
ASTEROID_COLOR = (192, 79, 21)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_timer = pygame.font.SysFont(None, 24)  # Font for the timer

# Clock
clock = pygame.time.Clock()

# Square dimensions (off-screen)
SQUARE_WIDTH = 900
SQUARE_HEIGHT = 700
SQUARE_X = (SCREEN_WIDTH - SQUARE_WIDTH) // 2
SQUARE_Y = (SCREEN_HEIGHT - SQUARE_HEIGHT) // 2

# Define the Player1 class
class Player1:
    def __init__(self, image_path, size, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = size
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Start at center
        self.speed = speed  # Speed affects how quickly it moves towards the mouse
        # Scale the image
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        # Keep a copy of the original image for transformations
        self.original_image = self.image.copy()
        self.is_flashing = False

    def update(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Smoothly interpolate player position towards the mouse
        self.pos[0] += (mouse_x - self.pos[0]) * self.speed
        self.pos[1] += (mouse_y - self.pos[1]) * self.speed

    def draw(self, screen):
        # Blit the image at the player's position
        rect = self.image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(self.image, rect)

    def set_flash(self, flash_on):
        self.is_flashing = flash_on
        if flash_on:
            # Create a white image for flashing effect
            self.image = self.original_image.copy()
            self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_ADD)
        else:
            # Reset to original image
            self.image = self.original_image.copy()

# Asteroid class
class Asteroid:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Check for collisions with the off-screen square
        if self.x - self.radius <= SQUARE_X or self.x + self.radius >= SQUARE_X + SQUARE_WIDTH:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= SQUARE_Y or self.y + self.radius >= SQUARE_Y + SQUARE_HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, other):
        # Calculate distance between the two asteroids
        dist = math.hypot(self.x - other.x, self.y - other.y)
        if dist <= self.radius + other.radius:  # Collision condition
            # Bounce logic: Swap velocities for simplicity
            self.speed_x, other.speed_x = other.speed_x, self.speed_x
            self.speed_y, other.speed_y = other.speed_y, self.speed_y

# Function to create an asteroid
def create_asteroid():
    asteroid_radius = random.randint(8, 12)
    asteroid = Asteroid(
        x=random.randint(SQUARE_X + asteroid_radius, SQUARE_X + SQUARE_WIDTH - asteroid_radius),
        y=random.randint(SQUARE_Y + asteroid_radius, SQUARE_Y + SQUARE_HEIGHT - asteroid_radius),
        radius=asteroid_radius,
        color=ASTEROID_COLOR,
        speed_x=random.choice([-2, -1, 1, 2]),
        speed_y=random.choice([-2, -1, 1, 2])
    )
    return asteroid

# Function to reset the game
def reset_game():
    global game_over, player1, asteroids, invulnerable, invulnerability_start_time, last_flash_time, start_time
    game_over = False
    # Reset player position
    player1.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    # Reset player's image and flashing state
    player1.set_flash(False)
    # Re-create asteroids
    asteroids = [create_asteroid() for _ in range(30)]
    # Reset invulnerability
    invulnerable = True
    invulnerability_start_time = pygame.time.get_ticks()
    last_flash_time = invulnerability_start_time
    # Reset start_time (will be set after invulnerability wears off)
    start_time = None

# Initialize game variables
running = True
game_over = False
game_state = 'menu'  # Possible states: 'menu', 'playing', 'options', 'game_over'
final_score = 0  # To store the final score when game ends
high_score = 0  # Initialize high score to zero

# Invulnerability settings
invulnerable = False  # Will be set to True when the game starts
invulnerability_duration = 5  # in seconds
invulnerability_start_time = None
flash_interval = 200  # milliseconds for flashing effect
last_flash_time = None

# Initialize player and asteroids (will be done in reset_game)
# player_image_path = # initially hard-coded
base_path = os.path.dirname(__file__)
player_image_path = os.path.join(base_path, 's_1_assets', 'images', 'ship_1.png')
player_size = 70  # Adjust the size as needed
player1 = Player1(image_path=player_image_path, size=player_size, speed=0.4)  # 0.4 for gradual movement
asteroids = []

# Main game loop
while running:
    current_time = pygame.time.get_ticks()

    if game_state == 'menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 'start_button_rect' in locals() and start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    reset_game()
                elif 'options_button_rect' in locals() and options_button_rect.collidepoint(mouse_pos):
                    game_state = 'options'
                elif 'quit_button_rect' in locals() and quit_button_rect.collidepoint(mouse_pos):
                    running = False

        # Render the start screen
        screen.fill(BACKGROUND_COLOR)
        title_text = font_large.render("DEBRIS", True, TEXT_COLOR)
        start_text = font_medium.render("START", True, TEXT_COLOR)
        options_text = font_medium.render("OPTIONS", True, TEXT_COLOR)
        quit_text = font_medium.render("QUIT", True, TEXT_COLOR)

        # Position the text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        start_button_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        options_button_rect = options_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_button_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_button_rect)
        screen.blit(options_text, options_button_rect)
        screen.blit(quit_text, quit_button_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the menu state

    elif game_state == 'options':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'

        # Render the options screen
        screen.fill(BACKGROUND_COLOR)
        options_title = font_large.render("OPTIONS", True, TEXT_COLOR)
        back_text = font_small.render("Press ESC to return to the menu", True, TEXT_COLOR)

        # Position the text
        options_title_rect = options_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        back_text_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(options_title, options_title_rect)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the options state

    elif game_state == 'playing':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'

        if not game_over:
            # Handle invulnerability timing
            if invulnerable:
                invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
                if invulnerability_elapsed_time >= invulnerability_duration:
                    invulnerable = False  # Invulnerability period is over
                    player1.set_flash(False)  # Ensure the player is back to normal image
                    start_time = pygame.time.get_ticks()  # Start the timer now

                # Handle flashing effect during invulnerability
                else:
                    if current_time - last_flash_time >= flash_interval:
                        last_flash_time = current_time
                        # Toggle the player's flash effect
                        player1.set_flash(not player1.is_flashing)

            # Update player1 position
            player1.update()

            # Update asteroid positions and check for collision with player
            for asteroid in asteroids:
                asteroid.move()

                # Check for collision with player
                dist = math.hypot(asteroid.x - player1.pos[0], asteroid.y - player1.pos[1])
                if dist <= asteroid.radius + player1.size / 2:
                    if not invulnerable:
                        print("Collision with player!")
                        game_over = True
                        game_state = 'game_over'
                        # Calculate final score
                        if start_time is not None:
                            final_score = (current_time - start_time) / 1000  # Convert milliseconds to seconds
                        else:
                            final_score = 0
                        # Update high score if necessary
                        if final_score > high_score:
                            high_score = final_score
                        break  # Exit the loop since game is over
                    else:
                        # During invulnerability, do not end the game
                        pass

            # Check for collisions between all asteroids
            for i in range(len(asteroids)):
                for j in range(i + 1, len(asteroids)):
                    asteroids[i].check_collision(asteroids[j])

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, (255, 255, 255), (SQUARE_X, SQUARE_Y, SQUARE_WIDTH, SQUARE_HEIGHT), 1)

        for asteroid in asteroids:
            asteroid.draw(screen)
        player1.draw(screen)

        # Display timer in the top-left corner
        if not game_over and start_time is not None:
            # Calculate elapsed time
            elapsed_time = (current_time - start_time) / 1000  # In seconds
        else:
            elapsed_time = 0

        # Render the timer text
        timer_text = font_timer.render(f"Time: {elapsed_time:.2f}s", True, TEXT_COLOR)
        screen.blit(timer_text, (10, 10))  # Position at top-left corner

        # Render the high score text
        high_score_text = font_timer.render(f"High Score: {high_score:.2f}s", True, TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(high_score_text, high_score_rect)

        # Display countdown during invulnerability
        if invulnerable:
            countdown_time = max(0, invulnerability_duration - invulnerability_elapsed_time)
            countdown_text = font_large.render(f"GAME STARTS IN: {countdown_time:.1f}", True, TEXT_COLOR)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)

        pygame.display.flip()
        clock.tick(60)

    elif game_state == 'game_over':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = 'playing'
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # Draw game over screen
        screen.fill(BACKGROUND_COLOR)

        # Create text surfaces
        game_over_text = font_large.render("GAME OVER", True, TEXT_COLOR)
        score_text = font_small.render(f"Final Score: {final_score:.2f} seconds", True, TEXT_COLOR)
        restart_text = font_small.render("Press 'R' to Replay or 'Q' to Quit", True, TEXT_COLOR)

        # Calculate positions to center the text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Blit text onto the screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
