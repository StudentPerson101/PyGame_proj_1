#  base - v2_p18 - music

import pygame 
import random
import sys
import math
import os

# Initialize PyGame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

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

# Load images
# player_image_path = # initially hard-coded
# asteroid_image_path = # initially hard-coded
# background_image_path = # initially hard-coded
# background_image_path = # initially hard-coded
base_path = os.path.dirname(__file__)
player_image_path = os.path.join(base_path, 's_1_assets', 'images', 'ship_1.png')
asteroid_image_path = os.path.join(base_path, 's_1_assets', 'images', 'asteroid_1.png')
background_image_path = os.path.join(base_path, 's_1_assets', 'images', 'background_2.png')
asteroid_explosion_image_path = os.path.join(base_path, 's_1_assets', 'images', 'asteroid_explosion_1.png')
projectile_explosion_image_path = os.path.join(base_path, 's_1_assets', 'images', 'projectile_explosion_2.png')

# Load images
asteroid_image_original = pygame.image.load(asteroid_image_path).convert_alpha()
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
asteroid_explosion_image_original = pygame.image.load(asteroid_explosion_image_path).convert_alpha()
projectile_explosion_image_original = pygame.image.load(projectile_explosion_image_path).convert_alpha()

# Load sounds
# asteroid_explosion_sound_path = # initially hard-coded
# projectile_explosion_sound_path = # initially hard-coded
asteroid_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'meteor_impact_1.mp3')
projectile_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'laser_explosion_1.mp3')

asteroid_explosion_sound = pygame.mixer.Sound(asteroid_explosion_sound_path)
projectile_explosion_sound = pygame.mixer.Sound(projectile_explosion_sound_path)

# Set volume levels (0.0 to 1.0)
asteroid_explosion_volume = 0.5  # Adjust as needed
projectile_explosion_volume = 0.5  # Adjust as needed

asteroid_explosion_sound.set_volume(asteroid_explosion_volume)
projectile_explosion_sound.set_volume(projectile_explosion_volume)

# Music files
# menu_music_path = # initially hard-coded
# gameplay_music_path = # initially hard-coded
# game_over_music_path = # initially hard-coded
menu_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - main menu.mp3')
gameplay_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - gameplay.mp3')
game_over_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - game over.mp3')

# Variable to track current music
current_music = None

# Function to play music
def play_music(music_path):
    global current_music
    if current_music != music_path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        current_music = music_path

# Explosion class
class Explosion:
    def __init__(self, x, y, image, duration, sound=None):
        self.x = x
        self.y = y
        self.image = image
        self.duration = duration  # in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.sound_played = False
        self.sound = sound
        self.sound_channel = None  # Store the channel the sound is playing on
        self.sound_start_time = None  # Store the time the sound started

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.sound_played and self.sound:
            self.sound_channel = self.sound.play()
            self.sound_start_time = current_time
            self.sound_played = True
        elif self.sound_channel and current_time - self.sound_start_time >= 2000:
            self.sound_channel.stop()
            self.sound_channel = None  # Prevent stopping again

    def draw(self, screen):
        screen.blit(self.image, (int(self.x - self.image.get_width() / 2), int(self.y - self.image.get_height() / 2)))

    def is_finished(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.start_time) >= self.duration

# Define the Player1 class
class Player1:
    def __init__(self, image_path, size, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = size
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Start at center
        self.speed = speed  # Speed at which the player moves
        # Scale the image
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        # Keep a copy of the original image for transformations
        self.original_image = self.image.copy()
        self.is_flashing = False
        self.angle = 0  # Angle the player is facing

    def update(self, keys):
        # Handle movement
        move_x = 0
        move_y = 0
        if keys[pygame.K_w]:
            move_y = -self.speed
        if keys[pygame.K_s]:
            move_y = self.speed
        if keys[pygame.K_a]:
            move_x = -self.speed
        if keys[pygame.K_d]:
            move_x = self.speed

        self.pos[0] += move_x
        self.pos[1] += move_y

        # Keep the player within the bounds of the screen
        self.pos[0] = max(0, min(self.pos[0], SCREEN_WIDTH))
        self.pos[1] = max(0, min(self.pos[1], SCREEN_HEIGHT))

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Compute angle to the mouse position
        dx = mouse_x - self.pos[0]
        dy = mouse_y - self.pos[1]
        self.angle = math.degrees(math.atan2(dy, dx))

    def draw(self, screen):
        # Rotate the image to the angle
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(rotated_image, rect)

    def set_flash(self, flash_on):
        self.is_flashing = flash_on
        if flash_on:
            # Create a white image for flashing effect
            self.image = self.original_image.copy()
            self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_ADD)
        else:
            # Reset to original image
            self.image = self.original_image.copy()

# Projectile class
class Projectile:
    def __init__(self, x, y, angle, speed=10, color=(255, 0, 0), radius=5, max_hits=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        # Compute the velocity components
        angle_rad = math.radians(self.angle)
        self.vx = self.speed * math.cos(angle_rad)
        self.vy = self.speed * math.sin(angle_rad)
        self.radius = radius  # Radius of the projectile
        self.color = color
        self.remaining_hits = max_hits

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)

# Asteroid class
class Asteroid:
    def __init__(self, x, y, radius, color, speed_x, speed_y, image):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        # Scale the asteroid image based on radius
        self.image = pygame.transform.scale(image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (int(self.x), int(self.y))

        # Check for collisions with the off-screen square
        if self.x - self.radius <= SQUARE_X or self.x + self.radius >= SQUARE_X + SQUARE_WIDTH:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= SQUARE_Y or self.y + self.radius >= SQUARE_Y + SQUARE_HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
        speed_y=random.choice([-2, -1, 1, 2]),
        image=asteroid_image_original
    )
    return asteroid

# Function to reset the game
def reset_game():
    global game_over, player1, asteroids, invulnerable, invulnerability_start_time, last_flash_time, start_time, projectiles, explosions
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
    # Clear projectiles
    projectiles = []
    # Clear explosions
    explosions = []

# Initialize game variables
running = True
game_over = False
game_state = 'menu'  # Possible states: 'menu', 'playing', 'options', 'game_over', 'paused'
previous_state = None  # To keep track of the previous state
final_score = 0  # To store the final score when game ends
high_score = 0  # Initialize high score to zero

# Invulnerability settings
invulnerable = False  # Will be set to True when the game starts
invulnerability_duration = 5  # in seconds
invulnerability_start_time = None
flash_interval = 200  # milliseconds for flashing effect
last_flash_time = None

# Charging settings
is_charging = False
charge_start_time = None
charge_flash_interval = 300  # milliseconds for flashing effect during charging
last_charge_flash_time = None
charging_flash_visible = True  # To control flashing visibility
max_charge_time = 3  # Maximum charge time in seconds
charge_circle_radius = 80  # Starting radius for charging circle
current_charge_circle_radius = charge_circle_radius  # Current radius during shrinking
charge_circle_shrink_speed = 150  # Pixels per second

# Initialize player and asteroids (will be done in reset_game)
player_size = 60  # Adjust the size as needed
player_speed = 5  # Speed at which the player moves
player1 = Player1(image_path=player_image_path, size=player_size, speed=player_speed)
asteroids = []
projectiles = []
explosions = []  # List to hold explosions

# Main game loop
while running:
    current_time = pygame.time.get_ticks()

    if game_state == 'menu':
        play_music(menu_music_path)  # Play main menu music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 'start_button_rect' in locals() and start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    reset_game()
                elif 'options_button_rect' in locals() and options_button_rect.collidepoint(mouse_pos):
                    previous_state = 'menu'  # Remember we came from the menu
                    game_state = 'options'
                elif 'quit_button_rect' in locals() and quit_button_rect.collidepoint(mouse_pos):
                    running = False

        # Render the start screen
        screen.blit(background_image, (0, 0))  # Use the same background as gameplay
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
        play_music(menu_music_path)  # Play main menu music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the previous state
                    game_state = previous_state
                    previous_state = None  # Reset previous_state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # You can add mouse interactions for options here if needed
                pass

        # Render the options screen
        screen.blit(background_image, (0, 0))  # Use the same background
        options_title = font_large.render("OPTIONS", True, TEXT_COLOR)
        back_text = font_small.render("Press ESC to return", True, TEXT_COLOR)

        # Position the text
        options_title_rect = options_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        back_text_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(options_title, options_title_rect)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the options state

    elif game_state == 'paused':
        # Continue playing gameplay music
        play_music(gameplay_music_path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass  # No key actions in paused state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 'continue_button_rect' in locals() and continue_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                elif 'pause_options_button_rect' in locals() and pause_options_button_rect.collidepoint(mouse_pos):
                    previous_state = 'paused'  # Remember we came from the paused state
                    game_state = 'options'
                elif 'main_menu_button_rect' in locals() and main_menu_button_rect.collidepoint(mouse_pos):
                    game_state = 'menu'

        # Render the pause screen
        screen.blit(background_image, (0, 0))  # Use the same background
        pause_title = font_large.render("PAUSED", True, TEXT_COLOR)
        continue_text = font_medium.render("CONTINUE", True, TEXT_COLOR)
        pause_options_text = font_medium.render("OPTIONS", True, TEXT_COLOR)
        main_menu_text = font_medium.render("MAIN MENU", True, TEXT_COLOR)

        # Position the text
        pause_title_rect = pause_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        continue_button_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        pause_options_button_rect = pause_options_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        main_menu_button_rect = main_menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(pause_title, pause_title_rect)
        screen.blit(continue_text, continue_button_rect)
        screen.blit(pause_options_text, pause_options_button_rect)
        screen.blit(main_menu_text, main_menu_button_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the paused state

    elif game_state == 'playing':
        play_music(gameplay_music_path)  # Play gameplay music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'paused'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    is_charging = True
                    charge_start_time = current_time
                    last_charge_flash_time = current_time
                    charging_flash_visible = True
                    current_charge_circle_radius = charge_circle_radius  # Reset the circle radius
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and is_charging:
                    # Calculate charging duration
                    charge_duration = (current_time - charge_start_time) / 1000  # in seconds
                    if charge_duration >= 2:
                        # Fire a white projectile
                        projectile = Projectile(
                            player1.pos[0], player1.pos[1], player1.angle,
                            speed=10, color=(255, 255, 255), radius=25, max_hits=4
                        )
                    elif charge_duration >= 1:
                        # Fire an orange projectile
                        projectile = Projectile(
                            player1.pos[0], player1.pos[1], player1.angle,
                            speed=10, color=(255, 255, 0), radius=15, max_hits=2
                        )
                    else:
                        # Fire a normal projectile
                        projectile = Projectile(player1.pos[0], player1.pos[1], player1.angle)
                    projectiles.append(projectile)
                    is_charging = False
                    charge_start_time = None

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

            # Get keys
            keys = pygame.key.get_pressed()
            # Update player1 position
            player1.update(keys)

            # Update projectile positions
            for projectile in projectiles[:]:
                projectile.update()
                # Remove projectile if it goes off-screen
                if projectile.is_off_screen():
                    # Create projectile explosion
                    explosion_image = pygame.transform.scale(
                        projectile_explosion_image_original,
                        (projectile.radius * 4, projectile.radius * 4)
                    )
                    explosion = Explosion(
                        projectile.x, projectile.y, explosion_image, 500, projectile_explosion_sound
                    )
                    explosions.append(explosion)
                    projectiles.remove(projectile)
                else:
                    # Check for collisions between projectiles and asteroids
                    for asteroid in asteroids[:]:
                        dist = math.hypot(asteroid.x - projectile.x, asteroid.y - projectile.y)
                        if dist <= asteroid.radius + projectile.radius:
                            # Collision detected
                            asteroid_explosion_image = pygame.transform.scale(
                                asteroid_explosion_image_original,
                                (asteroid.radius * 4, asteroid.radius * 4)
                            )
                            # Create asteroid explosion
                            explosion = Explosion(
                                asteroid.x, asteroid.y, asteroid_explosion_image, 500, asteroid_explosion_sound
                            )
                            explosions.append(explosion)
                            asteroids.remove(asteroid)
                            if projectile.remaining_hits > 1:
                                projectile.remaining_hits -= 1
                            else:
                                # Create projectile explosion
                                explosion_image = pygame.transform.scale(
                                    projectile_explosion_image_original,
                                    (projectile.radius * 4, projectile.radius * 4)
                                )
                                explosion = Explosion(
                                    projectile.x, projectile.y, explosion_image, 500, projectile_explosion_sound
                                )
                                explosions.append(explosion)
                                projectiles.remove(projectile)
                            break  # Break out of the inner loop

            # Update asteroid positions and check for collision with player
            for asteroid in asteroids[:]:
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

            # Update explosions
            for explosion in explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    # Stop the sound if it's still playing
                    if explosion.sound_channel:
                        explosion.sound_channel.stop()
                    explosions.remove(explosion)

        # Draw everything
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (SQUARE_X, SQUARE_Y, SQUARE_WIDTH, SQUARE_HEIGHT), 1)

        # Draw charging indicator before drawing the player
        if is_charging:
            # Update the shrinking circle radius
            delta_time = clock.get_time() / 1000  # Time since last frame in seconds
            current_charge_circle_radius -= charge_circle_shrink_speed * delta_time
            if current_charge_circle_radius <= 0:
                current_charge_circle_radius = charge_circle_radius  # Reset radius when it reaches zero

            if current_charge_circle_radius < player1.size // 2:
                current_charge_circle_radius = player1.size // 2

            # Draw the circle
            circle_surface_size = int(current_charge_circle_radius * 2)
            circle_surface = pygame.Surface((circle_surface_size, circle_surface_size), pygame.SRCALPHA)
            circle_surface.fill((0, 0, 0, 0))  # Make it fully transparent

            # Draw filled circle with 25% transparency (alpha = 64)
            pygame.draw.circle(circle_surface, (255, 255, 255, 64), (int(current_charge_circle_radius), int(current_charge_circle_radius)), int(current_charge_circle_radius))

            # Blit the circle_surface onto the main screen at the correct position
            screen.blit(circle_surface, (int(player1.pos[0] - current_charge_circle_radius), int(player1.pos[1] - current_charge_circle_radius)))

        # Now draw the asteroids, projectiles, explosions, and player
        for asteroid in asteroids:
            asteroid.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
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
            invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
            countdown_time = max(0, invulnerability_duration - invulnerability_elapsed_time)
            countdown_text = font_large.render(f"GAME STARTS IN: {countdown_time:.1f}", True, TEXT_COLOR)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)

        pygame.display.flip()
        clock.tick(60)

    elif game_state == 'game_over':
        play_music(game_over_music_path)  # Play Game Over music

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
        screen.blit(background_image, (0, 0))  # Use the same background

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


