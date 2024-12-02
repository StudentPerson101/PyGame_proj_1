#  base - v2_p20 - new enemy logic

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
CHARGING_FLASH_COLOR = (17, 255, 255)

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_timer = pygame.font.SysFont(None, 24)  # Font for the timer

# Clock
clock = pygame.time.Clock()

# Left boundary rectangle (used to detect when asteroids are destroyed)
LEFT_RECT_WIDTH = 200
LEFT_RECT_HEIGHT = 1200
LEFT_RECT_X = -200  # 200 pixels to the left of the screen
LEFT_RECT_Y = -300  # Centered vertically around the screen

# Right spawn rectangle (where asteroids spawn)
RIGHT_RECT_WIDTH = 200
RIGHT_RECT_HEIGHT = 1200
RIGHT_RECT_X = SCREEN_WIDTH  # Right edge of the screen
RIGHT_RECT_Y = -300  # Centered vertically around the screen

# Load images
# Use relative paths
base_path = os.path.dirname(__file__)
player_image_path = os.path.join(base_path, 's_1_assets', 'images', 'ship_1.png')
asteroid_image_path = os.path.join(base_path, 's_1_assets', 'images', 'enemy_t1.png')
background_image_path = os.path.join(base_path, 's_1_assets', 'images', 'background_1.png')
asteroid_explosion_image_path = os.path.join(base_path, 's_1_assets', 'images', 'asteroid_explosion_1.png')

# Projectile images and explosion images
projectile_1_image_path = os.path.join(base_path, 's_1_assets', 'images', 'projectile_explosion_2.png')
projectile_explosion_1_image_path = os.path.join(base_path, 's_1_assets', 'images', 'projectile_explosion_6.png')
projectile_2_image_path = os.path.join(base_path, 's_1_assets', 'images', 'player_shot_2.png')
projectile_explosion_2_image_path = os.path.join(base_path, 's_1_assets', 'images', 'projectile_explosion_1.png')
projectile_3_image_path = os.path.join(base_path, 's_1_assets', 'images', 'player_shot_3.png')
projectile_explosion_3_image_path = os.path.join(base_path, 's_1_assets', 'images', 'projectile_explosion_3.png')

# Load images
try:
    asteroid_image_original = pygame.image.load(asteroid_image_path).convert_alpha()
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    asteroid_explosion_image_original = pygame.image.load(asteroid_explosion_image_path).convert_alpha()
except pygame.error as e:
    print(f"Failed to load image: {e}")
    sys.wxit()

# Load projectile images
try:
    projectile_1_image = pygame.image.load(projectile_1_image_path).convert_alpha()
    projectile_explosion_1_image = pygame.image.load(projectile_explosion_1_image_path).convert_alpha()
    projectile_2_image = pygame.image.load(projectile_2_image_path).convert_alpha()
    projectile_explosion_2_image = pygame.image.load(projectile_explosion_2_image_path).convert_alpha()
    projectile_3_image = pygame.image.load(projectile_3_image_path).convert_alpha()
    projectile_explosion_3_image = pygame.image.load(projectile_explosion_3_image_path).convert_alpha()
except pygame.error as e:
    print(f"Failed to load projectile image: {e}")
    sys.exit()

# Load sounds
asteroid_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'meteor_impact_1.mp3')
projectile_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'laser_explosion_1.mp3')

try:
    asteroid_explosion_sound = pygame.mixer.Sound(asteroid_explosion_sound_path)
    projectile_explosion_sound = pygame.mixer.Sound(projectile_explosion_sound_path)
except pygame.error as e:
    print(f"Failed to load sound: {e}")
    sys.exit()

# Set volume levels (0.0 to 1.0)
asteroid_explosion_volume = 0.5  # Adjust as needed
projectile_explosion_volume = 0.5  # Adjust as needed

asteroid_explosion_sound.set_volume(asteroid_explosion_volume)
projectile_explosion_sound.set_volume(projectile_explosion_volume)

# Music files
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
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            current_music = music_path
        except pygame.error as e:
            print(f"Failed to load music: {e}")
            current_music = None

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
        self.flash_color = None
        self.flash_interval = 200  # milliseconds
        self.last_flash_time = 0
        self.angle = 0  # Angle the player is facing

    def update(self, keys, current_time):
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

        # Update flashing
        self.update_flash(current_time)

    def update_flash(self, current_time):
        if self.is_flashing and self.flash_color:
            if current_time - self.last_flash_time >= self.flash_interval:
                self.last_flash_time = current_time
                # Toggle the flashing effect
                if self.image == self.original_image:
                    # Create flashed image
                    flashed_image = self.original_image.copy()
                    overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                    overlay.fill((*self.flash_color, 0))
                    flashed_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    self.image = flashed_image
                else:
                    self.image = self.original_image.copy()

    def set_flash(self, flash_on, flash_color=None):
        self.is_flashing = flash_on
        self.flash_color = flash_color
        self.last_flash_time = pygame.time.get_ticks()
        if not flash_on:
            # Reset to original image
            self.image = self.original_image.copy()

    def draw(self, screen):
        # Rotate the image to the angle
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        screen.blit(rotated_image, rect)

# Projectile sizes
projectile_1_size = 40  # Normal shot size
projectile_explosion_1_size = 60  # Explosion size for projectile 1

projectile_2_size = 60  # Charged shot size
projectile_explosion_2_size = 80  # Explosion size for projectile 2

projectile_3_size = 80  # Super charged shot size
projectile_explosion_3_size = 100  # Explosion size for projectile 3

# Projectile class
class Projectile:
    def __init__(self, x, y, angle, image, size, speed=10, max_hits=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        # Compute the velocity components
        angle_rad = math.radians(self.angle)
        self.vx = self.speed * math.cos(angle_rad)
        self.vy = self.speed * math.sin(angle_rad)
        self.size = size
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.remaining_hits = max_hits
        self.explosion_image = None  # Will be set when projectile is created
        self.explosion_size = None

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        # Rotate the image to the angle
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rect)

    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)

# Asteroid class
class Asteroid:
    def __init__(self, player, image):
        self.player = player  # Reference to the player object
        self.x = random.randint(RIGHT_RECT_X, RIGHT_RECT_X + RIGHT_RECT_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = random.randint(10, 20)
        self.image = pygame.transform.scale(image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.speed_x = -random.uniform(2, 5)  # Move left at a random speed
        self.max_vertical_speed = random.uniform(1, 2)

    def move(self):
        # Move left
        self.x += self.speed_x

        # Adjust Y position to follow the player
        dy = self.player.pos[1] - self.y
        if dy > 0:
            self.y += min(self.max_vertical_speed, dy)
        elif dy < 0:
            self.y -= min(self.max_vertical_speed, -dy)

        # Keep asteroid within vertical screen bounds
        self.y = max(0, min(self.y, SCREEN_HEIGHT))

        # Update rectangle position
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        # Check if the asteroid has moved past the left boundary
        return self.x + self.radius < LEFT_RECT_X + LEFT_RECT_WIDTH

# Function to spawn a group of asteroids
def spawn_asteroid_group():
    num_asteroids = random.randint(6, 20)
    for _ in range(num_asteroids):
        if len(asteroids) < 30:
            asteroid = Asteroid(player1, asteroid_image_original)
            asteroids.append(asteroid)
        else:
            break  # Do not exceed 30 asteroids

# Function to reset the game
def reset_game():
    global game_over, player1, asteroids, invulnerable, invulnerability_start_time, start_time, projectiles, explosions, last_asteroid_group_spawn_time
    game_over = False
    # Reset player position
    player1.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    # Reset player's image and flashing state
    player1.set_flash(False)
    # Clear asteroids list; they will be spawned by the spawning logic
    asteroids = []
    # Reset invulnerability
    invulnerable = True
    invulnerability_start_time = pygame.time.get_ticks()
    # Reset start_time (will be set after invulnerability wears off)
    start_time = None
    # Clear projectiles
    projectiles = []
    # Clear explosions
    explosions = []
    # Reset asteroid group spawn timer
    last_asteroid_group_spawn_time = pygame.time.get_ticks()

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

# Charging settings
is_charging = False
charge_start_time = None

# Initialize player and asteroids (will be done in reset_game)
player_size = 60  # Adjust the size as needed
player_speed = 5  # Speed at which the player moves
player1 = Player1(image_path=player_image_path, size=player_size, speed=player_speed)
asteroids = []
projectiles = []
explosions = []  # List to hold explosions

# Asteroid group spawn settings
ASTEROID_GROUP_SPAWN_INTERVAL = 5000  # Spawn every 5 seconds
last_asteroid_group_spawn_time = pygame.time.get_ticks()

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
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and is_charging:
                    # Calculate charging duration
                    charge_duration = (current_time - charge_start_time) / 1000  # in seconds
                    if charge_duration >= 2:
                        # Super charged shot
                        projectile = Projectile(
                            player1.pos[0], player1.pos[1], player1.angle,
                            image=projectile_3_image,
                            size=projectile_3_size,
                            speed=10,
                            max_hits=4
                        )
                        projectile.explosion_image = projectile_explosion_3_image
                        projectile.explosion_size = projectile_explosion_3_size
                    elif charge_duration >= 1:
                        # Charged shot
                        projectile = Projectile(
                            player1.pos[0], player1.pos[1], player1.angle,
                            image=projectile_2_image,
                            size=projectile_2_size,
                            speed=10,
                            max_hits=2
                        )
                        projectile.explosion_image = projectile_explosion_2_image
                        projectile.explosion_size = projectile_explosion_2_size
                    else:
                        # Normal shot
                        projectile = Projectile(
                            player1.pos[0], player1.pos[1], player1.angle,
                            image=projectile_1_image,
                            size=projectile_1_size,
                            speed=10,
                            max_hits=1
                        )
                        projectile.explosion_image = projectile_explosion_1_image
                        projectile.explosion_size = projectile_explosion_1_size
                    projectiles.append(projectile)
                    is_charging = False
                    charge_start_time = None

        if not game_over:
            # Handle invulnerability timing
            if invulnerable:
                invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
                if invulnerability_elapsed_time >= invulnerability_duration:
                    invulnerable = False  # Invulnerability period is over
                    player1.set_flash(False)
                    start_time = pygame.time.get_ticks()  # Start the timer now

            # Determine player flashing state
            if is_charging:
                player1.set_flash(True, CHARGING_FLASH_COLOR)
            elif invulnerable:
                player1.set_flash(True, (255, 255, 255))
            else:
                player1.set_flash(False)

            # Get keys
            keys = pygame.key.get_pressed()
            # Update player1 position
            player1.update(keys, current_time)

            # Update projectile positions
            for projectile in projectiles[:]:
                projectile.update()
                # Remove projectile if it goes off-screen
                if projectile.is_off_screen():
                    # Create projectile explosion
                    explosion_image = pygame.transform.scale(
                        projectile.explosion_image,
                        (projectile.explosion_size, projectile.explosion_size)
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
                        if dist <= asteroid.radius + projectile.size / 2:
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
                                    projectile.explosion_image,
                                    (projectile.explosion_size, projectile.explosion_size)
                                )
                                explosion = Explosion(
                                    projectile.x, projectile.y, explosion_image, 500, projectile_explosion_sound
                                )
                                explosions.append(explosion)
                                projectiles.remove(projectile)
                            break  # Break out of the inner loop

            # Spawn asteroid groups periodically
            if current_time - last_asteroid_group_spawn_time >= ASTEROID_GROUP_SPAWN_INTERVAL:
                spawn_asteroid_group()
                last_asteroid_group_spawn_time = current_time

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

                # Check if asteroid has moved past the left boundary
                if asteroid.is_off_screen():
                    asteroids.remove(asteroid)

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


