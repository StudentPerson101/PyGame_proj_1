#  base - v2_p8 - game starts in 321

import pygame  
import random
import sys
import math

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
    def __init__(self, color, size, speed):
        self.color = color
        self.size = size
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Start at center
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
player_color_normal = (0, 32, 96)
player1 = Player1(color=player_color_normal, size=20, speed=0.4)  # 0.4 for gradual movement

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

# Function to reset the game
def reset_game():
    global game_over, start_time, final_score, player1, asteroids
    global invulnerable, invulnerability_start_time, last_flash_time  # Add these globals
    game_over = False
    start_time = pygame.time.get_ticks()
    final_score = 0
    # Reset player position
    player1.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    # Reset player's color
    player1.color = player_color_normal
    # Re-create asteroids
    asteroids.clear()
    for _ in range(30):
        asteroid_radius = random.randint(8, 12)
        asteroid = Asteroid(
            x=random.randint(SQUARE_X + asteroid_radius, SQUARE_X + SQUARE_WIDTH - asteroid_radius),
            y=random.randint(SQUARE_Y + asteroid_radius, SQUARE_Y + SQUARE_HEIGHT - asteroid_radius),
            radius=asteroid_radius,
            color=random.choice([(192, 79, 21), (100, 200, 255), (255, 165, 0)]),
            speed_x=random.choice([-2, -1, 1, 2]),
            speed_y=random.choice([-2, -1, 1, 2])
        )
        asteroids.append(asteroid)
    # Reset invulnerability
    invulnerable = True
    invulnerability_start_time = pygame.time.get_ticks()
    last_flash_time = invulnerability_start_time

# Create multiple asteroids
asteroids = []
for _ in range(30):
    asteroid_radius = random.randint(8, 12)
    asteroid = Asteroid(
        x=random.randint(SQUARE_X + asteroid_radius, SQUARE_X + SQUARE_WIDTH - asteroid_radius),
        y=random.randint(SQUARE_Y + asteroid_radius, SQUARE_Y + SQUARE_HEIGHT - asteroid_radius),
        radius=asteroid_radius,
        color=random.choice([(192, 79, 21), (100, 200, 255), (255, 165, 0)]),  # Random colors
        speed_x=random.choice([-2, -1, 1, 2]),
        speed_y=random.choice([-2, -1, 1, 2])
    )
    asteroids.append(asteroid)

# Initialize game variables
running = True
game_over = False
start_time = pygame.time.get_ticks()  # Start the timer
final_score = 0  # To store the final score when game ends
high_score = 0  # Initialize high score to zero

# Invulnerability settings
invulnerable = True
invulnerability_duration = 5  # in seconds
invulnerability_start_time = pygame.time.get_ticks()
flash_interval = 200  # milliseconds for flashing effect
last_flash_time = invulnerability_start_time
player_color_flash = (255, 255, 255)  # Flash color (white)

# Main game loop
while running:
    current_time = pygame.time.get_ticks()  # Move this outside the event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

    # Update game only if not over
    if not game_over:
        invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
        if invulnerable and invulnerability_elapsed_time >= invulnerability_duration:
            invulnerable = False  # Invulnerability period is over
            player1.color = player_color_normal  # Ensure the player is back to normal color

        # Handle flashing effect during invulnerability
        if invulnerable:
            if current_time - last_flash_time >= flash_interval:
                last_flash_time = current_time
                # Toggle the player's color between normal and flash color
                if player1.color == player_color_normal:
                    player1.color = player_color_flash
                else:
                    player1.color = player_color_normal

        # Update player1 position
        player1.update()

        # Update asteroid positions and check for collision with player
        for asteroid in asteroids:
            asteroid.move()

            # Check for collision with player
            dist = math.hypot(asteroid.x - player1.pos[0], asteroid.y - player1.pos[1])
            if dist <= asteroid.radius + player1.size:
                if not invulnerable:
                    print("Collision with player!")
                    game_over = True
                    # Calculate final score
                    final_score = (current_time - start_time) / 1000  # Convert milliseconds to seconds
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
    if not game_over:
        # Calculate elapsed time
        elapsed_time = (current_time - start_time) / 1000  # In seconds
    else:
        elapsed_time = final_score  # Use final score after game over

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

    # If game is over, display "GAME OVER" and final score
    if game_over:
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

    # Control frame rate
    clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
