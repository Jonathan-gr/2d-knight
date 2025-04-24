import pygame
from abc import ABC, abstractmethod
import Collisions
import Constants
import math
import all_sprites

class Monster(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, health=15,fireball_group = None):
        super().__init__()
        self.name = 'monster'
        self.image = None
        self.rect = None
        self.gravity = 1
        self.velocity = 0
        self.direction = 1
        self.move_counter = 0
        self.animation_counter = 0
        self.health = health
        self.dead_flag = False
        self.death_timer_event = pygame.USEREVENT + 1
        self.hit_player = False
        self.death_duration = 4000
        self.falling = False
        self.blood_splattergroup = all_sprites.get_sprite_group('BloodSplatter_group')
        self.fireball_group = fireball_group



        # Blinking attributes
        self.blink = False
        self.blink_interval = 100
        self.blink_duration = 2000
        self.last_blink_time = pygame.time.get_ticks()
        self.blink_end_time = 0
        self.invulnerable = False
        self.health=4
        self.init_monster(x, y)

    @abstractmethod
    def init_monster(self, x, y):
        """Initialize the specific monster. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def update(self,player_pos=None):
        """Update the monster's state. Must be implemented by subclasses."""
        #pygame.draw.rect(Constants.screen, (255, 255, 255), self.rect, 2)
        pass

    @abstractmethod
    def on_hit(self, hit):
        """Handles what happens when the monster is hit."""

        self.health -= hit
        if self.health <= 0 and not self.dead_flag:
            self.dead()

    def dead(self):
        """Handles the death of the monster."""
        self.dead_flag = True
        pygame.time.set_timer(self.death_timer_event, self.death_duration)

    def apply_gravity(self):
        """Apply gravity to the monster."""
        if not Collisions.check_tile_below_after_monster_dead(self.rect):
            self.velocity += self.gravity
            if self.velocity > 10:
                self.velocity = 10
            self.rect.y += self.velocity
            self.falling = True
        else:
            self.falling = False
            self.velocity = 0

    def start_blinking(self):
        """Start the blinking process."""
        self.blink = True
        self.invulnerable = True
        self.last_blink_time = pygame.time.get_ticks()
        self.blink_end_time = self.last_blink_time + self.blink_duration

    def update_blinking(self):
        """Update the blinking state."""
        current_time = pygame.time.get_ticks()
        if self.invulnerable:
            if current_time > self.blink_end_time:
                self.invulnerable = False
                self.blink = False

            if (current_time - self.last_blink_time) % self.blink_interval < self.blink_interval / 2:
                self.blink = True
            else:
                self.blink = False
        else:
            self.blink = False

    def start_circling(self, player_pos):
        # Record the center of the circle as the player's position
        self.behavior_state = 'circling'
        self.circle_center_x = player_pos[0]
        self.circle_center_y = player_pos[1]

        # Calculate the radius based on the current distance to player
        dx = self.rect.x - self.circle_center_x
        dy = self.rect.y - self.circle_center_y
        self.circle_radius = math.hypot(dx, dy)

        # Initialize the angle for circling
        self.current_angle = math.atan2(dy, dx)

        # Set the speed of circling
        self.circle_speed = 0.05

        # Set circling state and time
        self.is_circling = True
        self.circle_start_time = pygame.time.get_ticks()  # Track the start time of circling
        self.last_behavior_change_time = self.circle_start_time

    def circle_around_player(self):
        # Update the angle to move in a circular path
        self.current_angle += self.circle_speed
        self.rect.x = self.circle_center_x + self.circle_radius * math.cos(self.current_angle)
        self.rect.y = self.circle_center_y + self.circle_radius * math.sin(self.current_angle)

        # Check if the demon should stop circling based on the circle duration
        current_time = pygame.time.get_ticks()
        if current_time - self.circle_start_time > self.circle_duration:
            self.is_circling = False
            self.behavior_state = 'idle'
            self.last_behavior_change_time = current_time


    def start_swoop(self, player_pos):
        # Record the player's position at the start of the swoop
        self.behavior_state = 'swooping'
        self.swoop_target_x = player_pos[0]
        self.swoop_target_y = player_pos[1]

        # Store the initial position
        self.swoop_initial_x = self.rect.x
        self.swoop_initial_y = self.rect.y

        # Reset elapsed time for the swoop
        self.swoop_elapsed_time = 0
        self.swoop_start_time = pygame.time.get_ticks()
        self.last_update_time = self.swoop_start_time

    def swoop_toward_player(self):
        # Calculate elapsed time ratio as a fraction of the swoop duration
        elapsed_ratio = min(self.swoop_elapsed_time / self.swoop_duration, 1)  # Clamp ratio between 0 and 1

        # Smoothly interpolate the demon's horizontal position from its starting position to the target X
        self.rect.x = self.swoop_initial_x + (self.swoop_target_x - self.swoop_initial_x) * elapsed_ratio

        # Calculate vertical displacement using a sine wave for smooth motion
        amplitude = 150  # Height of the vertical curve
        frequency = 1.5  # Number of oscillations during the swoop
        self.rect.y = self.swoop_initial_y + amplitude * math.sin(elapsed_ratio * frequency * 2 * math.pi)

        # Increment swoop elapsed time
        self.swoop_elapsed_time += pygame.time.get_ticks() - self.last_update_time
        self.last_update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if not self.blink:
            surface.blit(self.image, self.rect.topleft)
        else:
            # Optional: Draw something else or change the appearance when blinking
            pass