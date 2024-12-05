# base - v3 - arrow keys + boss health reduced

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
font_health = pygame.font.SysFont(None, 36)  # Font for player health

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
import sys

# If __file__ is not defined, use sys.argv[0]
if getattr(sys, 'frozen', False):
    # If the application is frozen, use sys.executable
    base_path = os.path.dirname(sys.executable)
else:
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # If __file__ is not defined, use the current working directory
        base_path = os.getcwd()

player_image_path = os.path.join('s_1_assets', 'images', 'ship_1.png')
asteroid_image_path = os.path.join('s_1_assets', 'images', 'enemy_t1.png')
background_image_path = os.path.join('s_1_assets', 'images', 'background_1.png')
asteroid_explosion_image_path = os.path.join('s_1_assets', 'images', 'asteroid_explosion_1.png')

# Projectile images and explosion images
projectile_1_image_path = os.path.join('s_1_assets', 'images', 'projectile_explosion_2.png')
projectile_explosion_1_image_path = os.path.join('s_1_assets', 'images', 'projectile_explosion_6.png')
projectile_2_image_path = os.path.join('s_1_assets', 'images', 'player_shot_2.png')
projectile_explosion_2_image_path = os.path.join('s_1_assets', 'images', 'projectile_explosion_1.png')
projectile_3_image_path = os.path.join('s_1_assets', 'images', 'player_shot_3.png')
projectile_explosion_3_image_path = os.path.join('s_1_assets', 'images', 'projectile_explosion_3.png')

# Right-click weapon image
right_click_weapon_image_path = os.path.join('s_1_assets', 'images', 'player_shot_1.png')

# Life image path
life_image_path = os.path.join('s_1_assets', 'images', 'life_1.png')

# Boss assets
boss_image_path = os.path.join('s_1_assets', 'images', 'enemy_t3.png')
boss_attack_image_path = os.path.join('s_1_assets', 'images', 'boss_attack_1.png')

# Define the path to the high score file
high_score_file_path = os.path.join('s_1_assets', 'score', 'all_time_highest_score.txt')

# Volume Settings
# Set volume levels for all audio components (0.0 to 1.0)
# Music volumes
menu_music_volume = 0.5  # Volume for menu music
gameplay_music_volume = 0.2  # Volume for gameplay music
game_over_music_volume = 0.5  # Volume for game over music
boss_music_volume = 0.5  # Volume for boss fight music

# Sound effect volumes
asteroid_explosion_volume = 0.5  # Volume for asteroid explosion sound
projectile_explosion_volume = 0.5  # Volume for projectile explosion sound

# Weapon sound volumes
left_click_charging_volume = 0.5  # Volume for left-click charging sound
left_click_shot_volume = 0.5  # Volume for left-click shot sound
right_click_fire_volume = 0.5  # Volume for right-click automatic fire sound

# Boss sound volumes
boss_attack_sound_volume = 0.5
boss_attack_explosion_sound_volume = 0.5

# Load images
try:
    asteroid_image_original = pygame.image.load(os.path.join(base_path, asteroid_image_path)).convert_alpha()
    background_image = pygame.image.load(os.path.join(base_path, background_image_path)).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    asteroid_explosion_image_original = pygame.image.load(os.path.join(base_path, asteroid_explosion_image_path)).convert_alpha()
except pygame.error as e:
    print(f"Failed to load image: {e}")
    sys.exit()

# Load projectile images
try:
    projectile_1_image = pygame.image.load(os.path.join(base_path, projectile_1_image_path)).convert_alpha()
    projectile_explosion_1_image = pygame.image.load(os.path.join(base_path, projectile_explosion_1_image_path)).convert_alpha()
    projectile_2_image = pygame.image.load(os.path.join(base_path, projectile_2_image_path)).convert_alpha()
    projectile_explosion_2_image = pygame.image.load(os.path.join(base_path, projectile_explosion_2_image_path)).convert_alpha()
    projectile_3_image = pygame.image.load(os.path.join(base_path, projectile_3_image_path)).convert_alpha()
    projectile_explosion_3_image = pygame.image.load(os.path.join(base_path, projectile_explosion_3_image_path)).convert_alpha()
except pygame.error as e:
    print(f"Failed to load projectile image: {e}")
    sys.exit()

# Load right-click weapon image
try:
    right_click_weapon_image = pygame.image.load(os.path.join(base_path, right_click_weapon_image_path)).convert_alpha()
except pygame.error as e:
    print(f"Failed to load right-click weapon image: {e}")
    sys.exit()

# Load life image
try:
    life_image_original = pygame.image.load(os.path.join(base_path, life_image_path)).convert_alpha()
    life_image = pygame.transform.scale(life_image_original, (30, 30))  # Scale to desired size
    boss_life_image = life_image  # Use the same image for boss health display
except pygame.error as e:
    print(f"Failed to load life image: {e}")
    sys.exit()

# Load boss images
try:
    boss_image_original = pygame.image.load(os.path.join(base_path, boss_image_path)).convert_alpha()
    boss_attack_image_original = pygame.image.load(os.path.join(base_path, boss_attack_image_path)).convert_alpha()
except pygame.error as e:
    print(f"Failed to load boss image: {e}")
    sys.exit()

# Load sounds
asteroid_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'meteor_impact_1.mp3')
projectile_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - explosions', 'laser_explosion_1.mp3')
boss_attack_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - weapons', 'laser_gun_1.mp3')
boss_attack_explosion_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - weapons', 'laser_gun_1.mp3')

try:
    asteroid_explosion_sound = pygame.mixer.Sound(asteroid_explosion_sound_path)
    projectile_explosion_sound = pygame.mixer.Sound(projectile_explosion_sound_path)
    boss_attack_sound = pygame.mixer.Sound(boss_attack_sound_path)
    boss_attack_explosion_sound = pygame.mixer.Sound(boss_attack_explosion_sound_path)
except pygame.error as e:
    print(f"Failed to load sound: {e}")
    sys.exit()

# Set volume levels for sound effects
asteroid_explosion_sound.set_volume(asteroid_explosion_volume)
projectile_explosion_sound.set_volume(projectile_explosion_volume)
boss_attack_sound.set_volume(boss_attack_sound_volume)
boss_attack_explosion_sound.set_volume(boss_attack_explosion_sound_volume)

# Music files
menu_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - main menu.mp3')
gameplay_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - gameplay.mp3')
game_over_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - game over.mp3')
boss_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - boss fight.mp3')
victory_music_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - music', 'music - victory.mp3')  # Victory music

# Load weapon sounds
left_click_charging_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - weapons', 'charging_sound_2.mp3')
left_click_shot_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - weapons', 'laser_blaster_1.mp3')
right_click_fire_sound_path = os.path.join(base_path, 's_1_assets', 'audio', 'audio - sound fx', 'sound fx - weapons', 'machine_gun_1 (edited).mp3')

try:
    left_click_charging_sound = pygame.mixer.Sound(left_click_charging_sound_path)
    left_click_shot_sound = pygame.mixer.Sound(left_click_shot_sound_path)
    right_click_fire_sound = pygame.mixer.Sound(right_click_fire_sound_path)
except pygame.error as e:
    print(f"Failed to load weapon sound: {e}")
    sys.exit()

# Set volume levels for weapon sounds
left_click_charging_sound.set_volume(left_click_charging_volume)
left_click_shot_sound.set_volume(left_click_shot_volume)
right_click_fire_sound.set_volume(right_click_fire_volume)

# Initialize sound channels for weapon sounds
left_click_channel = pygame.mixer.Channel(1)
right_click_channel = pygame.mixer.Channel(2)

# Variable to track current music
current_music = None

# Function to play music
def play_music(music_path, volume=0.5):
    global current_music
    if current_music != music_path:
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
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
        self.image = pygame.image.load(os.path.join(base_path, image_path)).convert_alpha()
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
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # Up movement
            move_y = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Down movement
            move_y = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Left movement
            move_x = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Right movement
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

# Right-click weapon properties
right_click_weapon_size = 40  # Adjust as needed
right_click_weapon_explosion_image = projectile_explosion_1_image  # Or use a different image
right_click_weapon_explosion_size = 60  # Adjust as needed

# Projectile class
class Projectile:
    def __init__(self, x, y, angle, image, size, speed=10, max_hits=1, damage=1):
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
        self.damage = damage  # Add damage attribute

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

# Function to set invulnerability
def set_invulnerability(duration):
    global invulnerable, invulnerability_start_time, invulnerability_duration
    invulnerable = True
    invulnerability_start_time = pygame.time.get_ticks()
    invulnerability_duration = duration

# Boss class
class Boss:
    def __init__(self, player, screen_width, screen_height):
        self.player = player  # Reference to the player object
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = 110
        self.health = 450
        self.max_health = 850
        self.image = pygame.transform.scale(boss_image_original, (self.size, self.size))
        self.x = screen_width + self.size  # Start off-screen to the right
        self.y = screen_height // 2  # Start at vertical center
        self.speed_x = -2  # Move left towards the screen
        self.max_vertical_speed = 1.5
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 2000  # Time between attacks in milliseconds
        self.projectiles = []  # List to hold boss projectiles

    def move(self):
        # Move left until fully on-screen
        if self.x > self.screen_width - self.size:
            self.x += self.speed_x
        else:
            # Adjust Y position to follow the player
            dy = self.player.pos[1] - self.y
            if dy > 0:
                self.y += min(self.max_vertical_speed, dy)
            elif dy < 0:
                self.y -= min(self.max_vertical_speed, -dy)

            # Keep boss within vertical screen bounds
            self.y = max(0, min(self.y, self.screen_height))

        # Update rectangle position
        self.rect.center = (int(self.x), int(self.y))

    def attack(self, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            # Fire a projectile towards the player
            projectile = BossProjectile(
                self.x, self.y, self.player.pos[0], self.player.pos[1],
                boss_attack_image_original, boss_attack_sound
            )
            self.projectiles.append(projectile)
            self.last_attack_time = current_time

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)

    def draw_projectiles(self, surface):
        for projectile in self.projectiles:
            projectile.draw(surface)

    def is_defeated(self):
        return self.health <= 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# BossProjectile class
class BossProjectile:
    def __init__(self, x, y, target_x, target_y, image, sound):
        self.x = x
        self.y = y
        self.speed = 7  # Speed of the projectile
        self.image = pygame.transform.scale(image, (30, 30))  # Adjust size as needed
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.sound = sound
        self.sound.play()
        # Calculate angle towards the player
        dx = target_x - self.x
        dy = target_y - self.y
        angle = math.atan2(dy, dx)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)

# Function to reset the game
def reset_game():
    global game_over, player1, asteroids, invulnerable, invulnerability_start_time, projectiles, explosions, last_asteroid_group_spawn_time, score, player_health, boss_fight_active, boss, game_state
    game_over = False
    # Reset player position
    player1.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    # Reset player's image and flashing state
    player1.set_flash(False)
    # Clear asteroids list; they will be spawned by the spawning logic
    asteroids = []
    # Reset invulnerability
    set_invulnerability(initial_invulnerability_duration)
    # Clear projectiles
    projectiles = []
    # Clear explosions
    explosions = []
    # Reset asteroid group spawn timer
    last_asteroid_group_spawn_time = pygame.time.get_ticks()
    # Reset score
    score = 0
    # Reset player health
    player_health = 5
    # Stop any ongoing weapon sounds
    left_click_channel.stop()
    right_click_channel.stop()
    # Reset boss fight variables
    boss_fight_active = False
    boss = None
    game_state = 'playing'  # Ensure the game state is set to playing
    # Reset speech messages
    global speech_message_active, speech_message_start_time, displayed_speech_messages
    speech_message_active = None
    speech_message_start_time = None
    displayed_speech_messages = set()

# Function to reset practice mode
def reset_practice_mode():
    global player1, projectiles, explosions, invulnerable, invulnerability_start_time, invulnerability_duration, is_charging, is_right_clicking, charge_start_time, right_click_start_time, last_auto_fire_time
    # Reset player position
    player1.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    # Reset player's image and flashing state
    player1.set_flash(False)
    # Clear projectiles and explosions
    projectiles = []
    explosions = []
    # Reset invulnerability
    set_invulnerability(initial_invulnerability_duration)
    # Stop any ongoing weapon sounds
    left_click_channel.stop()
    right_click_channel.stop()
    # Reset charging and firing variables
    is_charging = False
    is_right_clicking = False
    charge_start_time = None
    right_click_start_time = None
    last_auto_fire_time = pygame.time.get_ticks()

# Initialize game variables
running = True
game_over = False
game_state = 'menu'  # Possible states: 'menu', 'playing', 'rules', 'game_over', 'paused', 'victory', 'practice'
previous_state = None  # To keep track of the previous state
score = 0  # Initialize score to zero
player_health = 5  # Initialize player health to 5

# Invulnerability settings
invulnerable = False  # Will be set to True when the game starts
initial_invulnerability_duration = 5  # in seconds
hit_invulnerability_duration = 2  # in seconds
invulnerability_duration = initial_invulnerability_duration  # Current duration
invulnerability_start_time = None

# Charging settings
is_charging = False
charge_start_time = None

# Right-click automatic firing settings
is_right_clicking = False
right_click_start_time = None
auto_fire_cooldown = 200  # milliseconds between shots
last_auto_fire_time = 0

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

# Boss fight variables
boss_fight_active = False
boss = None

# Load the all-time high score at startup
def load_high_score():
    try:
        with open(high_score_file_path, 'r') as file:
            high_score = int(file.read())
            print(f"Loaded high score: {high_score}")
    except (FileNotFoundError, ValueError):
        high_score = 0
        print("High score file not found or invalid, starting with high score of 0.")
    return high_score

all_time_high_score = load_high_score()

# Speech messages
speech_messages = [
    (100, "They just keep on spawning..."),
    (200, "Is there no end to them...?"),
    (300, "Something big is approaching..."),
]
displayed_speech_messages = set()
speech_message_active = None
speech_message_start_time = None
speech_display_duration = 3000  # Display each message for 3 seconds

# Main game loop
while running:
    current_time = pygame.time.get_ticks()

    if game_state == 'menu':
        play_music(menu_music_path, volume=menu_music_volume)  # Play main menu music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 'start_button_rect' in locals() and start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    reset_game()
                elif 'practice_button_rect' in locals() and practice_button_rect.collidepoint(mouse_pos):
                    game_state = 'practice'
                    reset_practice_mode()
                elif 'rules_button_rect' in locals() and rules_button_rect.collidepoint(mouse_pos):
                    previous_state = 'menu'  # Remember we came from the menu
                    game_state = 'rules'
                elif 'quit_button_rect' in locals() and quit_button_rect.collidepoint(mouse_pos):
                    running = False

        # Render the start screen
        screen.blit(background_image, (0, 0))  # Use the same background as gameplay
        title_text = font_large.render("DEBRIS", True, TEXT_COLOR)
        start_text = font_medium.render("START", True, TEXT_COLOR)
        practice_text = font_medium.render("PRACTICE ZONE", True, TEXT_COLOR)
        rules_text = font_medium.render("RULES", True, TEXT_COLOR)
        quit_text = font_medium.render("QUIT", True, TEXT_COLOR)

        # Position the text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        start_button_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        practice_button_rect = practice_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        rules_button_rect = rules_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_button_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_button_rect)
        screen.blit(practice_text, practice_button_rect)
        screen.blit(rules_text, rules_button_rect)
        screen.blit(quit_text, quit_button_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the menu state

    elif game_state == 'rules':
        play_music(menu_music_path, volume=menu_music_volume)  # Play main menu music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the previous state
                    game_state = previous_state
                    previous_state = None  # Reset previous_state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # You can add mouse interactions for the rules menu here if needed
                pass

        # Render the rules screen
        screen.blit(background_image, (0, 0))  # Use the same background

        # Define the rules text
        rules_title = font_large.render("RULES", True, TEXT_COLOR)
        movement_text = font_small.render("Movement: ---------- W A S D or Arrow Keys (Up Down Left Right)", True, TEXT_COLOR)
        aim_text = font_small.render("Aim: -------------------- MOUSE", True, TEXT_COLOR)
        charged_attack_text = font_small.render("Charged Attack: --- LEFT CLICK or HOLD LEFT CLICK", True, TEXT_COLOR)
        auto_attack_text = font_small.render("Fully-auto Attack: -- RIGHT CLICK", True, TEXT_COLOR)
        objective_text = font_small.render("Objective: ------------- SURVIVE", True, TEXT_COLOR)
        back_text = font_small.render("Press ESC to return", True, TEXT_COLOR)

        # Position the text
        spacing = 40  # Space between lines
        start_y = SCREEN_HEIGHT // 2 - 150

        rules_title_rect = rules_title.get_rect(topleft=(20, start_y))
        movement_rect = movement_text.get_rect(topleft=(20, start_y + spacing * 2))
        aim_rect = aim_text.get_rect(topleft=(20, start_y + spacing * 3))
        charged_attack_rect = charged_attack_text.get_rect(topleft=(20, start_y + spacing * 4))
        auto_attack_rect = auto_attack_text.get_rect(topleft=(20, start_y + spacing * 5))
        objective_rect = objective_text.get_rect(topleft=(20, start_y + spacing * 6))
        back_text_rect = back_text.get_rect(topleft=(20, start_y + spacing * 8))


        # Draw the text
        screen.blit(rules_title, rules_title_rect)
        screen.blit(movement_text, movement_rect)
        screen.blit(aim_text, aim_rect)
        screen.blit(charged_attack_text, charged_attack_rect)
        screen.blit(auto_attack_text, auto_attack_rect)
        screen.blit(objective_text, objective_rect)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the rules state

    elif game_state == 'paused':
        # Continue playing gameplay music or boss music
        if boss_fight_active:
            play_music(boss_music_path, volume=boss_music_volume)
        else:
            play_music(gameplay_music_path, volume=gameplay_music_volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass  # No key actions in paused state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 'continue_button_rect' in locals() and continue_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                elif 'pause_rules_button_rect' in locals() and pause_rules_button_rect.collidepoint(mouse_pos):
                    previous_state = 'paused'  # Remember we came from the paused state
                    game_state = 'rules'
                elif 'main_menu_button_rect' in locals() and main_menu_button_rect.collidepoint(mouse_pos):
                    game_state = 'menu'
                    # Stop any weapon sounds
                    left_click_channel.stop()
                    right_click_channel.stop()

        # Render the pause screen
        screen.blit(background_image, (0, 0))  # Use the same background
        pause_title = font_large.render("PAUSED", True, TEXT_COLOR)
        continue_text = font_medium.render("CONTINUE", True, TEXT_COLOR)
        pause_rules_text = font_medium.render("RULES", True, TEXT_COLOR)
        main_menu_text = font_medium.render("MAIN MENU", True, TEXT_COLOR)

        # Position the text
        pause_title_rect = pause_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        continue_button_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        pause_rules_button_rect = pause_rules_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        main_menu_button_rect = main_menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(pause_title, pause_title_rect)
        screen.blit(continue_text, continue_button_rect)
        screen.blit(pause_rules_text, pause_rules_button_rect)
        screen.blit(main_menu_text, main_menu_button_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the paused state

    elif game_state == 'practice':
        # Play appropriate music
        play_music(gameplay_music_path, volume=gameplay_music_volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                    # Stop any weapon sounds
                    left_click_channel.stop()
                    right_click_channel.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    is_charging = True
                    charge_start_time = current_time
                    # Start playing the charging sound if not already playing
                    if not left_click_channel.get_busy():
                        left_click_channel.play(left_click_charging_sound, loops=-1)
                elif event.button == 3:  # Right click
                    is_right_clicking = True
                    right_click_start_time = current_time
                    # Start playing the automatic fire sound if not already playing
                    if not right_click_channel.get_busy():
                        right_click_channel.play(right_click_fire_sound, loops=-1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Stop the charging sound immediately
                    left_click_channel.stop()
                    if is_charging:
                        # Play the shot sound
                        left_click_shot_sound.set_volume(left_click_shot_volume)
                        left_click_shot_sound.play()
                        # Calculate charging duration
                        charge_duration = (current_time - charge_start_time) / 1000  # in seconds
                        if charge_duration >= 2:
                            # Level 3: Super charged shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_3_image,
                                size=projectile_3_size,
                                speed=10,
                                max_hits=8,  # Updated from 4 to 8
                                damage=8  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_3_image
                            projectile.explosion_size = projectile_explosion_3_size
                        elif charge_duration >= 1:
                            # Level 2: Charged shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_2_image,
                                size=projectile_2_size,
                                speed=10,
                                max_hits=4,  # Updated from 2 to 4
                                damage=4  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_2_image
                            projectile.explosion_size = projectile_explosion_2_size
                        else:
                            # Level 1: Normal shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_1_image,
                                size=projectile_1_size,
                                speed=10,
                                max_hits=2,  # Updated from 1 to 2
                                damage=2  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_1_image
                            projectile.explosion_size = projectile_explosion_1_size
                        projectiles.append(projectile)
                        is_charging = False
                        charge_start_time = None
                elif event.button == 3:
                    is_right_clicking = False
                    right_click_start_time = None
                    # Stop the automatic fire sound immediately
                    right_click_channel.stop()

        # Handle invulnerability timing
        if invulnerable:
            invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
            if invulnerability_elapsed_time >= invulnerability_duration:
                invulnerable = False  # Invulnerability period is over
                player1.set_flash(False)
                # No need to set start_time

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

        # Automatic firing with right-click
        if is_right_clicking:
            if current_time - last_auto_fire_time >= auto_fire_cooldown:
                # Fire the right-click weapon projectile
                projectile = Projectile(
                    player1.pos[0], player1.pos[1], player1.angle,
                    image=right_click_weapon_image,  # Use the new image
                    size=right_click_weapon_size,
                    speed=10,
                    max_hits=1,  # Assuming it destroys 1 enemy
                    damage=1  # Set damage
                )
                projectile.explosion_image = right_click_weapon_explosion_image
                projectile.explosion_size = right_click_weapon_explosion_size
                projectiles.append(projectile)
                last_auto_fire_time = current_time

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
                continue  # Move to next projectile

            # In practice mode, no enemies, so no collision checks

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

        # Draw projectiles and explosions
        for projectile in projectiles:
            projectile.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        player1.draw(screen)

        # Draw player health
        screen.blit(life_image, (10, SCREEN_HEIGHT - 40))
        health_text = font_health.render(f"x {player_health}", True, TEXT_COLOR)
        screen.blit(health_text, (50, SCREEN_HEIGHT - 35))  # Adjust as needed

        # Display countdown during invulnerability
        if invulnerable and invulnerability_duration == initial_invulnerability_duration:
            invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
            countdown_time = max(0, invulnerability_duration - invulnerability_elapsed_time)
            countdown_text = font_large.render(f"STARTS IN: {countdown_time:.1f}", True, TEXT_COLOR)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)

        # Display 'Press ESC to Return to Main Menu' in top-left corner
        return_text = font_small.render("Press ESC to Return to Main Menu", True, TEXT_COLOR)
        screen.blit(return_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    elif game_state == 'playing':
        # Play appropriate music
        if boss_fight_active:
            play_music(boss_music_path, volume=boss_music_volume)
        else:
            play_music(gameplay_music_path, volume=gameplay_music_volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'paused'
                    # Stop any weapon sounds
                    left_click_channel.stop()
                    right_click_channel.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    is_charging = True
                    charge_start_time = current_time
                    # Start playing the charging sound if not already playing
                    if not left_click_channel.get_busy():
                        left_click_channel.play(left_click_charging_sound, loops=-1)
                elif event.button == 3:  # Right click
                    is_right_clicking = True
                    right_click_start_time = current_time
                    # Start playing the automatic fire sound if not already playing
                    if not right_click_channel.get_busy():
                        right_click_channel.play(right_click_fire_sound, loops=-1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Stop the charging sound immediately
                    left_click_channel.stop()
                    if is_charging:
                        # Play the shot sound
                        left_click_shot_sound.set_volume(left_click_shot_volume)
                        left_click_shot_sound.play()
                        # Calculate charging duration
                        charge_duration = (current_time - charge_start_time) / 1000  # in seconds
                        if charge_duration >= 2:
                            # Level 3: Super charged shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_3_image,
                                size=projectile_3_size,
                                speed=10,
                                max_hits=8,  # Updated from 4 to 8
                                damage=8  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_3_image
                            projectile.explosion_size = projectile_explosion_3_size
                        elif charge_duration >= 1:
                            # Level 2: Charged shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_2_image,
                                size=projectile_2_size,
                                speed=10,
                                max_hits=4,  # Updated from 2 to 4
                                damage=4  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_2_image
                            projectile.explosion_size = projectile_explosion_2_size
                        else:
                            # Level 1: Normal shot
                            projectile = Projectile(
                                player1.pos[0], player1.pos[1], player1.angle,
                                image=projectile_1_image,
                                size=projectile_1_size,
                                speed=10,
                                max_hits=2,  # Updated from 1 to 2
                                damage=2  # Set damage
                            )
                            projectile.explosion_image = projectile_explosion_1_image
                            projectile.explosion_size = projectile_explosion_1_size
                        projectiles.append(projectile)
                        is_charging = False
                        charge_start_time = None
                elif event.button == 3:
                    is_right_clicking = False
                    right_click_start_time = None
                    # Stop the automatic fire sound immediately
                    right_click_channel.stop()

        if not game_over:
            # Handle invulnerability timing
            if invulnerable:
                invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
                if invulnerability_elapsed_time >= invulnerability_duration:
                    invulnerable = False  # Invulnerability period is over
                    player1.set_flash(False)
                    # No need to set start_time

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

            # Automatic firing with right-click
            if is_right_clicking and not game_over:
                if current_time - last_auto_fire_time >= auto_fire_cooldown:
                    # Fire the right-click weapon projectile
                    projectile = Projectile(
                        player1.pos[0], player1.pos[1], player1.angle,
                        image=right_click_weapon_image,  # Use the new image
                        size=right_click_weapon_size,
                        speed=10,
                        max_hits=1,  # Assuming it destroys 1 enemy
                        damage=1  # Set damage
                    )
                    projectile.explosion_image = right_click_weapon_explosion_image
                    projectile.explosion_size = right_click_weapon_explosion_size
                    projectiles.append(projectile)
                    last_auto_fire_time = current_time

            # Check if boss fight should start
            if score >= 375 and not boss_fight_active:
                boss_fight_active = True
                # Do not spawn new asteroids, but keep existing ones
                # Initialize the boss
                boss = Boss(player1, SCREEN_WIDTH, SCREEN_HEIGHT)
                # Switch music to boss fight music
                play_music(boss_music_path, volume=boss_music_volume)

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
                    continue  # Move to next projectile

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
                        score += 1  # Increment score
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

                # If boss fight is active, check for collision with boss
                if boss_fight_active:
                    dist = math.hypot(boss.x - projectile.x, boss.y - projectile.y)
                    if dist <= boss.size / 2 + projectile.size / 2:
                        # Collision detected
                        boss.take_damage(projectile.damage)  # Use projectile damage
                        # Handle projectile hits
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
                        if boss.is_defeated():
                            # Boss defeated, end boss fight
                            boss_fight_active = False
                            score += 100  # Bonus points for defeating the boss
                            # Set game_state to 'victory' instead of 'game_over'
                            game_state = 'victory'
                            final_score = score
                            # Update high score if necessary
                            if final_score > all_time_high_score:
                                all_time_high_score = final_score
                                # Ensure the directory exists
                                os.makedirs(os.path.dirname(high_score_file_path), exist_ok=True)
                                # Save the new high score to the file
                                with open(high_score_file_path, 'w') as file:
                                    file.write(str(all_time_high_score))
                                print(f"New high score achieved: {all_time_high_score}")
                            # Stop any weapon sounds
                            left_click_channel.stop()
                            right_click_channel.stop()
                            break  # Exit the loop since game is over

            # Update asteroids
            for asteroid in asteroids[:]:
                asteroid.move()

                # Check for collision with player
                dist = math.hypot(asteroid.x - player1.pos[0], asteroid.y - player1.pos[1])
                if dist <= asteroid.radius + player1.size / 2:
                    if not invulnerable:
                        print("Collision with player!")
                        player_health -= 1

                        # Remove the asteroid and create explosion
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

                        if player_health <= 0:
                            game_over = True
                            game_state = 'game_over'
                            # Set final_score to current score
                            final_score = score
                            # Update high score if necessary
                            if final_score > all_time_high_score:
                                all_time_high_score = final_score
                                # Ensure the directory exists
                                os.makedirs(os.path.dirname(high_score_file_path), exist_ok=True)
                                # Save the new high score to the file
                                with open(high_score_file_path, 'w') as file:
                                    file.write(str(all_time_high_score))
                                print(f"New high score achieved: {all_time_high_score}")
                            # Stop any weapon sounds
                            left_click_channel.stop()
                            right_click_channel.stop()
                            break  # Exit the loop since game is over
                        else:
                            set_invulnerability(hit_invulnerability_duration)
                    else:
                        # During invulnerability, do not end the game
                        pass

                # Check if asteroid has moved past the left boundary
                if asteroid.is_off_screen():
                    asteroids.remove(asteroid)

            # Spawn asteroid groups periodically if not in boss fight
            if not boss_fight_active:
                if current_time - last_asteroid_group_spawn_time >= ASTEROID_GROUP_SPAWN_INTERVAL:
                    spawn_asteroid_group()
                    last_asteroid_group_spawn_time = current_time

            # Update boss if active
            if boss_fight_active:
                # Update boss movement and attacks
                boss.move()
                boss.attack(current_time)
                boss.update_projectiles()

                # Update boss projectiles and check for collision with player
                for projectile in boss.projectiles[:]:
                    # Check for collision with player
                    dist = math.hypot(projectile.x - player1.pos[0], projectile.y - player1.pos[1])
                    if dist <= projectile.rect.width / 2 + player1.size / 2:
                        if not invulnerable:
                            player_health -= 1
                            # Remove the projectile
                            boss.projectiles.remove(projectile)
                            # Handle player death
                            if player_health <= 0:
                                game_over = True
                                game_state = 'game_over'
                                final_score = score
                                # Update high score if necessary
                                if final_score > all_time_high_score:
                                    all_time_high_score = final_score
                                    # Ensure the directory exists
                                    os.makedirs(os.path.dirname(high_score_file_path), exist_ok=True)
                                    # Save the new high score to the file
                                    with open(high_score_file_path, 'w') as file:
                                        file.write(str(all_time_high_score))
                                    print(f"New high score achieved: {all_time_high_score}")
                                # Stop any weapon sounds
                                left_click_channel.stop()
                                right_click_channel.stop()
                                break  # Exit the loop since game is over
                            else:
                                set_invulnerability(hit_invulnerability_duration)
                        else:
                            # During invulnerability, do not end the game
                            pass

            # Update explosions
            for explosion in explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    # Stop the sound if it's still playing
                    if explosion.sound_channel:
                        explosion.sound_channel.stop()
                    explosions.remove(explosion)

            # Check if we need to display a speech message
            if not speech_message_active:
                for milestone, message in speech_messages:
                    if score >= milestone and milestone not in displayed_speech_messages:
                        speech_message_active = message
                        speech_message_start_time = current_time
                        displayed_speech_messages.add(milestone)
                        break

            # Check if the speech message should be cleared
            if speech_message_active:
                if current_time - speech_message_start_time >= speech_display_duration:
                    speech_message_active = None
                    speech_message_start_time = None

        # Draw everything
        screen.blit(background_image, (0, 0))

        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Draw projectiles and explosions
        for projectile in projectiles:
            projectile.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        player1.draw(screen)

        # Draw the boss and its projectiles if in boss fight
        if boss_fight_active:
            boss.draw(screen)
            boss.draw_projectiles(screen)

        # Render the score text
        score_text = font_timer.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))  # Position at top-left corner

        # Render the high score text
        high_score_text = font_timer.render(f"High Score: {all_time_high_score}", True, TEXT_COLOR)
        high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(high_score_text, high_score_rect)

        # Draw player health
        screen.blit(life_image, (10, SCREEN_HEIGHT - 40))
        health_text = font_health.render(f"x {player_health}", True, TEXT_COLOR)
        screen.blit(health_text, (50, SCREEN_HEIGHT - 35))  # Adjust as needed

        # Draw boss health if in boss fight
        if boss_fight_active:
            # Draw single heart at bottom right
            heart_x = SCREEN_WIDTH - 40
            heart_y = SCREEN_HEIGHT - 40
            screen.blit(boss_life_image, (heart_x, heart_y))
            boss_health_text = font_health.render(f"x {boss.health}", True, TEXT_COLOR)
            # Position the text to the left of the heart
            text_rect = boss_health_text.get_rect()
            text_x = heart_x - text_rect.width - 10  # 10 pixels padding
            text_y = heart_y + (boss_life_image.get_height() - text_rect.height) // 2
            screen.blit(boss_health_text, (text_x, text_y))

        # Display countdown during invulnerability
        if invulnerable and invulnerability_duration == initial_invulnerability_duration:
            invulnerability_elapsed_time = (current_time - invulnerability_start_time) / 1000  # in seconds
            countdown_time = max(0, invulnerability_duration - invulnerability_elapsed_time)
            countdown_text = font_large.render(f"GAME STARTS IN: {countdown_time:.1f}", True, TEXT_COLOR)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)

        # Draw speech box if active
        if speech_message_active:
            # Draw the speech box
            box_width = 400
            box_height = 100
            box_x = (SCREEN_WIDTH - box_width) // 2
            box_y = 50  # Top middle part of the screen
            # Draw the box background
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
            # Draw the box outline
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
            # Render the text
            speech_font = pygame.font.SysFont(None, 36)
            lines = speech_message_active.split('\n')  # In case message has multiple lines
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, box_y + 50 + i * 40))
                screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    elif game_state == 'victory':
        play_music(victory_music_path, volume=game_over_music_volume)  # Play victory music

        # Reset right-clicking status
        is_right_clicking = False
        right_click_start_time = None
        # Stop any weapon sounds
        left_click_channel.stop()
        right_click_channel.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # Draw victory screen
        screen.blit(background_image, (0, 0))  # Use the same background

        # Create text surfaces
        victory_text = font_large.render("VICTORY!", True, TEXT_COLOR)
        score_text = font_small.render(f"Final Score: {final_score} points", True, TEXT_COLOR)
        high_score_text = font_small.render(f"High Score: {all_time_high_score} points", True, TEXT_COLOR)
        restart_text = font_small.render("Press 'R' to Play Again or 'Q' to Quit", True, TEXT_COLOR)

        # Calculate positions to center the text
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

        # Blit text onto the screen
        screen.blit(victory_text, victory_rect)
        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the loop for the victory state

    elif game_state == 'game_over':
        play_music(game_over_music_path, volume=game_over_music_volume)  # Play Game Over music

        # Reset right-clicking status
        is_right_clicking = False
        right_click_start_time = None
        # Stop any weapon sounds
        left_click_channel.stop()
        right_click_channel.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # Draw game over screen
        screen.blit(background_image, (0, 0))  # Use the same background

        # Create text surfaces
        game_over_text = font_large.render("GAME OVER", True, TEXT_COLOR)
        score_text = font_small.render(f"Final Score: {final_score} points", True, TEXT_COLOR)
        high_score_text = font_small.render(f"High Score: {all_time_high_score} points", True, TEXT_COLOR)
        restart_text = font_small.render("Press 'R' to Replay or 'Q' to Quit", True, TEXT_COLOR)

        # Calculate positions to center the text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

        # Blit text onto the screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)

# Quit PyGame
pygame.quit()
