import pygame
import math
import Constants
from monster import Monster
import random
import blood_splatter

class Flyingdemon(Monster):
    def init_monster(self, x, y):
        # Specific initialization for Flyingdemon

        self.images = Constants.flying_demon_arr
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images]

        self.image_index = 0
        self.animation_speed = 200
        self.last_animation = pygame.time.get_ticks()

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.player_collision = False

        # Swoop-specific variables
        self.swoop_interval = 5000  # Time between swoops (in milliseconds)
        self.swoop_duration = random.uniform(2000, 3000)  # How long the swoop lasts
        self.swoop_start_time = 0  # Time when the swoop starts
        self.is_swooping = False  # Track whether the demon is in a swoop

        self.swoop_target_x = 0  # Target x-position for the swoop
        self.swoop_target_y = 0  # Target y-position for the swoop
        self.swoop_elapsed_time = 0  # Time spent swooping

        self.swoop_speed_x = 0  # Horizontal speed for the swoop
        self.swoop_initial_y = self.rect.y  # Save the initial y-position for the curve
        self.last_update_time = 0

        # Add circling-specific attributes
        self.circle_center_x = 0  # X position of the center of the circle
        self.circle_center_y = 0  # Y position of the center of the circle
        self.circle_radius = 100  # Radius of the circle
        self.circle_speed = random.uniform(0.01, 0.04)  # Speed of circling movement (angle increment per frame)
        self.current_angle = 0  # Current angle in radians for circular movement
        self.is_circling = False  # Track whether the demon is circling
        # Detection range to start circling
        self.detection_range = 200  # Adjust this value as needed

        self.transition_delay = 2000  # Delay in milliseconds between behaviors
        self.last_behavior_change_time = 0
        self.behavior_state = 'idle'  # Can be 'idle', 'swooping', or 'circling'
        self.health = 4

        self.circle_duration = random.uniform(3000, 5000)  # Circling time in milliseconds (3-5 seconds)
        self.circle_start_time = 0  # Track when circling starts

    def dead(self):
        super().dead()

    def on_hit(self, hit, player_direction):
        self.start_blinking()
        self.rect.x += hit if player_direction == 1 else -(hit)
        self.health -= 1

        if self.health <= 0:
            splatter_list = blood_splatter.create_blood_splatters(self.rect.centerx, self.rect.centery, self.direction, 5)
            for splatter in splatter_list:
                self.blood_splattergroup.add(splatter)
            self.kill()


    def update(self, player_pos):

        self.update_blinking()
        current_time = pygame.time.get_ticks()
        distance_to_player = math.hypot(self.rect.x - player_pos[0], self.rect.y - player_pos[1])

        if self.is_circling:
            # Handle circling behavior
            self.circle_around_player()

        elif self.is_swooping:
            # Handle swooping behavior
            self.swoop_toward_player()
            if current_time - self.swoop_start_time > self.swoop_duration:
                self.is_swooping = False
                self.rect.y = self.swoop_initial_y  # Reset the y-position after swoop
                self.behavior_state = 'idle'
                self.last_behavior_change_time = current_time

        else:
            # Handle transition to circling or swooping
            if distance_to_player <= self.detection_range and current_time - self.last_behavior_change_time > self.transition_delay:
                self.start_circling(player_pos)
            elif not self.is_swooping and current_time - self.swoop_start_time > self.swoop_interval:
                self.is_swooping = True
                self.start_swoop(player_pos)


            if player_pos[1]<self.rect.y:
                self.rect.y-=1
            else:
                self.rect.y+=1

        # Handle animation timing
        if current_time - self.last_animation > self.animation_speed:
            self.last_animation = current_time
            self.image_index = (self.image_index + 1) % len(self.images)

            if player_pos[0] < self.rect.x:
                self.image = self.images_left[self.image_index]
            else:
                self.image = self.images[self.image_index]

        super().update()


