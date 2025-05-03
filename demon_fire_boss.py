import pygame
import math
import random
import Constants
import all_sprites
import blood_splatter
from monster import Monster
from fire_projectile import Fireball
from fire_wall import Firewall
from gust import Gust

class DemonBoss(Monster):
    def init_monster(self, x, y):

        self.name = 'fire_boss'
        # Default demon images
        self.images_left = Constants.boss_arr
        self.images_right = [pygame.transform.flip(img, True, False) for img in self.images_left]
        self.current_images = self.images_left  # Default state images

        # Fire and flaming demon modes
        self.fire_mode_left = Constants.fire_mode1_arr
        self.fire_mode_right = [pygame.transform.flip(img, True, False) for img in self.fire_mode_left]
        self.flaming_demon = Constants.fire_mode2_arr
        self.is_flaming = False

        self.scream_arr = Constants.demon_boss_scream_arr
        self.scream_arr_left = [pygame.transform.flip(img, True, False) for img in self.scream_arr]
        self.is_screaming=False

        self.wind_arr = Constants.wind_arr
        self.wind_arr_left = [pygame.transform.flip(img, True, False) for img in self.wind_arr]
        self.is_wind_attack=False

        self.image_index = 0
        self.animation_speed = 200
        self.last_animation = pygame.time.get_ticks()

        self.image = self.images_left[0]  # Default initial image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Fire/Flaming Demon mode control
          # Time to stay in fire/flaming mode (5 seconds)
        self.last_mode_switch = 0  # Last time the mode switched
        self.current_mode = 'idle'  # Start in default mode
        self.number_of_modes =3

        # Mode durations
        self.default_duration = 1000  # 2 seconds in default mode
        self.flaming_demon_duration = random.uniform(3000,4000)  # 3 seconds in fire mode
        self.scream_duration = 2000  # 2 seconds in scream mode
        self.wind_duration = 3000  #

        self.probabilities = {
            'scream_mode': 0.5,  # 30% chance
            'fire_mode': 0.3,  # 50% chance
            'wind_attack': 0.2  # 20% chance
        }
        self.original_probabilities = self.probabilities.copy()

        # Fireball shooting parameters
        self.blast_count = 0  # Count of fireballs shot
        self.number_of_blasts = 4
        self.shot_delay = 400  # 100 ms delay between shots
        self.last_shot_time = 0  # Last time a fireball was shot
        self.number_of_fireballs = 8
        # Fireball shooting parameters
        self.shoot_interval = self.scream_duration  # Fireball shooting happens in scream mode

        # Fireball sprite group
        self.fireball_group = all_sprites.get_sprite_group('fireball_group')
        #firewall grouop
        self.fire_wall_group = all_sprites.get_sprite_group('firewall_group')
        self.gust_group = all_sprites.get_sprite_group('gust_group')

        #time for fire_wall duration
        self.fire_wall_duration = 6000

        self.gust_interval = 400  # Time in milliseconds between gusts
        self.last_gust_time = 0  # Track when the last gust was created

        self.speed = 2
        self.health = 5

    def on_hit(self, hit):
        print('HIT HIT HIT')
        self.start_blinking()
        self.health-=hit
        splatter_list = blood_splatter.create_blood_splatters(self.rect.centerx, self.rect.centery,
                                                              self.direction, int(random.uniform(3,8)), 30, 40)
        for splatter in splatter_list:
            self.blood_splattergroup.add(splatter)

        if self.health<=0:
            if self.health <= 0:


                self.current_mode = 'dead'


    def switch_to_fire_mode(self):

        self.is_flaming = True
        self.is_screaming = False
        self.is_wind_attack = False
        self.current_mode = 'fire_mode'
        self.current_images = self.fire_mode_left
        self.image_index = 0
        self.last_mode_switch = pygame.time.get_ticks()


    def switch_to_flaming_demon(self):

        self.current_mode = 'flaming_demon'
        self.image_index = 0
        self.last_mode_switch = pygame.time.get_ticks()

    def switch_to_wind_attack(self):

        self.is_flaming = False
        self.is_screaming = False
        self.is_wind_attack = True
        self.current_mode = 'wind_attack'
        self.image_index = 0
        self.last_mode_switch = pygame.time.get_ticks()

    def switch_to_default_mode(self):

        self.current_mode = 'idle'
        self.image_index = 0
        self.last_mode_switch = pygame.time.get_ticks()



    def switch_to_scream_mode(self):

        self.is_flaming = False
        self.is_screaming = True
        self.is_wind_attack = False
        self.current_mode = 'scream_mode'
        self.image_index = 0
        self.last_mode_switch = pygame.time.get_ticks()
        self.blast_count = 0

    def switch_to_default_after_scream(self):
        self.switch_to_default_mode()

    def update(self, player_pos,player):


        current_time = pygame.time.get_ticks()
        self.update_blinking()
        if self.current_mode == 'dead':
            self.rect.x+=5

            if self.rect.left > Constants.screen_width:
                self.kill()
        else:

            # Handle mode transitions based on time intervals
            if self.current_mode == 'idle' and current_time - self.last_mode_switch > self.default_duration:
                self.perform_weighted_action()


            elif self.current_mode == 'fire_mode':
                # Check if the animation cycle for fire mode is complete
                if self.image_index == len(self.fire_mode_left) - 1:
                    # When the last frame of fire mode is reached, switch to flaming demon mode
                    self.switch_to_flaming_demon()

            elif self.current_mode == 'flaming_demon':
                # Check if the flaming demon mode duration is complete
                if current_time - self.last_mode_switch > self.flaming_demon_duration:
                    # Switch back to idle after the flaming demon duration
                    self.switch_to_default_mode()
                else:
                    self.chase_player(player_pos)


            # Fireball logic should only trigger during scream mode
            elif self.current_mode == 'scream_mode':
                if self.blast_count < self.number_of_blasts and current_time - self.last_shot_time > self.shot_delay:
                    fireballs = self.shoot_fireballs(player_pos)
                    self.fireball_group.add(fireballs)
                    self.last_shot_time = current_time
                    self.blast_count += 1  # Increment the shot count
                elif self.blast_count >= self.number_of_blasts:
                    self.switch_to_default_mode()


            elif self.current_mode == 'wind_attack':
                if current_time - self.last_mode_switch > self.wind_duration:
                    # Switch back to idle after the wind duration
                    print('sccx')
                    self.animation_speed = 200
                    player.slowed = False
                    self.number_of_gusts = 0
                    self.switch_to_default_mode()
                else:
                    self.animation_speed = 100
                    direction = 'left'  if player_pos[0] > self.rect.x else 'right'
                    player.knockback(direction,6)
                    if direction=='right':
                        if player.direction == 1:
                            player.slowed = True
                        else:
                            player.slowed = False

                    elif direction=='left':
                        if player.direction == -1:
                            player.slowed = True
                        else:
                            player.slowed = False
                    # Check if 200 milliseconds have passed since the last gust
                    if current_time - self.last_gust_time >= self.gust_interval:
                        # Spawn a new gust
                        x = self.rect.right + 35 if direction == 'left' else self.rect.left - 35
                        gust_init = Gust(x, self.rect.top + 30, 900, direction)
                        self.gust_group.add(gust_init)

                        # Update the time of the last gust creation
                        self.last_gust_time = current_time
                    #player.handle_player_winded()

        # Handle animation timing for all modes
        if current_time - self.last_animation > self.animation_speed:
            self.last_animation = current_time
            # Update image index for animation cycling
            self.image_index = (self.image_index + 1) % len(self.current_images)
            self.image = self.current_images[self.image_index]

        # Handle sprite flipping based on player position
        if self.current_mode in ('fire_mode', 'idle'):
            if player_pos[0] < self.rect.x:
                self.current_images = self.fire_mode_left if self.current_mode == 'fire_mode' else self.images_left
            else:
                self.current_images = self.fire_mode_right if self.current_mode == 'fire_mode' else self.images_right

        elif self.current_mode == 'flaming_demon':
            self.current_images = self.flaming_demon

        elif self.current_mode == 'scream_mode':
            self.current_images = self.scream_arr if  player_pos[0] < self.rect.x else self.scream_arr_left

        elif self.current_mode == 'wind_attack':
            self.current_images = self.wind_arr if player_pos[0] < self.rect.x else self.wind_arr_left

        elif self.current_mode == 'dead':
            self.current_images = self.fire_mode_left if player_pos[0] < self.rect.x else self.fire_mode_right


        super().update()

    import random

    def shoot_fireballs(self, player_pos):
        """Generate and shoot fireballs in the direction the demon is facing."""
        # Determine the direction vector from the demon to the player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery

        # Calculate the base angle to the player
        base_angle = math.atan2(dy, dx)  # Angle in radians

        # Generate angles with some random variation
        angles = self.generate_fireball_angles(base_angle)

        # Set the starting x position for fireballs
        if self.rect.x < player_pos[0]:
            x = self.rect.right
        else:
            x = self.rect.left

        # Create fireballs with the calculated angles
        fireballs = [Fireball(x, self.rect.top + 30, angle) for angle in angles]
        return fireballs

    def generate_fireball_angles(self, base_angle):
        """Generate fireball angles based on the direction the demon is facing, with randomness."""
         # Adjust this for spread (e.g., 22.5 degrees)
        angles = []

        for i in range(-self.number_of_fireballs // 2, self.number_of_fireballs // 2 + 1):
            # Add some random variation to each angle
            delta_angle = math.pi / random.uniform(6, 10)
            random_offset = random.uniform(-0.2, 0.2)  # Adjust the range for more/less randomness
            angle = base_angle + i * delta_angle + random_offset
            angles.append(angle)

        return angles

    def draw(self, surface):
        if not self.blink:
            surface.blit(self.image, self.rect.topleft)

    def chase_player(self, player_pos):
        # Get the direction vector to the player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery

        # Calculate distance
        distance = (dx**2 + dy**2) ** 0.5  # Euclidean distance

        if distance > 0:  # Prevent division by zero
            # Normalize the direction vector
            dx /= distance
            dy /= distance

            # Move the demon towards the player
            self.rect.x += dx * random.uniform(1,3)
            self.rect.y += dy * random.uniform(1,3)

    def perform_weighted_action(self):
        # Create a list of actions and corresponding weights
        actions = [
            self.switch_to_scream_mode,
            self.switch_to_fire_mode,
            self.switch_to_wind_attack
        ]

        weights = [
            self.probabilities['scream_mode'],
            self.probabilities['fire_mode'],
            self.probabilities['wind_attack']
        ]

        # Choose an action based on the weights
        selected_action = random.choices(actions, weights)[0]

        # Perform the selected action
        selected_action()

        # If scream mode was selected, increase the chance for wind attack next time
        if selected_action == self.switch_to_scream_mode:

            self.probabilities['wind_attack'] += 0.2  # Increase wind attack probability
            # Normalize the weights (make sure total probability stays 1 or less)
            total_probability = sum(self.probabilities.values())
            self.probabilities = {k: v / total_probability for k, v in self.probabilities.items()}

        # If wind attack was performed, reset probabilities to their original state
        elif selected_action == self.switch_to_wind_attack:

            self.probabilities = self.original_probabilities.copy()
