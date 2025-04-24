import math


import pygame

import Constants
import Collisions
import all_sprites


from torch import Torch



class Player():
    def __init__(self,x,y,health=Constants.start_lvl_health):
        self.init_and_restart_player(x,y)

    def init_and_restart_player(self,x,y,health=Constants.player_health,rare_blue_gems=0):
        self.images_right = []
        self.images_left = []
        self.images_dead = []
        self.images_hurt = []
        self.images_jump = []
        self.jump_left = []
        self.images_attack_right = []
        self.images_attack_left = []
        self.images_dict = {}
        self.walk_index = 0
        self.walk_counter = 0
        self.walk_speed = 4
        self.slowed_speed = 1  # Speed when hurt
        self.rare_blue_gems = rare_blue_gems
        self.rare_blue_gems_for_this_level = 0
        self.rare_blue_gems_for_worlds = Constants.gems_collected

        self.torch_group = all_sprites.get_sprite_group('torch_group')
        self.torch_thrown = False
        self.torch_cooldown = 2000
        self.torch_cooldown_animation = 100
        self.torch_animation = False
        self.torch_start_time = 0

        for image in Constants.player_dead:
            self.images_dead.append(image)  # Append the scaled image to the list
        self.images_dict['dead'] = self.images_dead

        for jmp_img in Constants.player_jump:
            jmp_img = pygame.transform.scale(jmp_img, (100, 72))  # Scale the image
            self.images_jump.append(jmp_img)
        self.images_dict['jump'] = self.images_jump

        self.jump_left = [pygame.transform.flip(img, True, False) for img in self.images_jump]
        self.images_dict['jump_left'] = self.jump_left

        for atk_img in Constants.player_attack:
            atk_img = pygame.transform.scale(atk_img, (100, 72))  # Scale the image
            self.images_attack_right.append(atk_img)
        self.images_dict['attack_right'] = self.images_attack_right

        self.attack_left = [pygame.transform.flip(img, True, False) for img in self.images_attack_right]
        self.images_dict['attack_left'] = self.attack_left

        for image in Constants.player_hurt:
            img_hurt = pygame.transform.scale(image, (76, 72))  # Scale the image
            self.images_hurt.append(img_hurt)
        self.images_dict['hurt'] = self.images_hurt

        self.images_hurt_left = [pygame.transform.flip(img, True, False) for img in self.images_hurt]
        self.images_dict['hurt_left'] =  self.images_hurt_left

        for image in Constants.player_walking_right:
            image = pygame.transform.scale(image, (100, 72))  # Scale the image
            img_left = pygame.transform.flip(image,True,False)
            self.images_right.append(image)  # Append the scaled image to the list
            self.images_left.append(img_left)
        self.images_dict['walking_right'] = self.images_right
        self.images_dict['walking_left'] = self.images_left

        img_defend_right = pygame.transform.scale(Constants.defend, (100, 72))  # Scale the image
        img_defend_left = pygame.transform.flip(img_defend_right,True,False)
        self.images_dict['defend_right'] = img_defend_right
        self.images_dict['defend_left'] = img_defend_left

        self.img_torch_throw = pygame.transform.scale(Constants.torch_throw_img, (100, 72))
        self.img_torch_throw_left = pygame.transform.flip(self.img_torch_throw, True, False)


        self.img = self.images_right[self.walk_index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(x,y,38,72)
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.jumping = False
        self.jump_index = 0
        self.gravity = 1
        self.direction = 1
        self.dx = 0
        self.dy = 0
        self.grounded = False
        self.falling = False
        self.horizontal_collision= False

        self.death_animation_index = 0
        self.death_animation_timer = 0  # To control the speed of the animation
        self.death_animation_speed = 7  # Lower value = faster animation
        self.is_dead = False  # Flag to check if player is dead

        self.health = health
        self.invulnerable = False  # Invulnerability state
        self.invulnerable_time = 0  # Time until invulnerability ends
        self.invulnerability_duration = 1000  # Duration of invulnerability in milliseconds (1 second)
        self.hurt_animation_index = 0
        self.blink = False  # Tracks whether to render the player or not
        self.blink_interval = 100  # Blink interval (in milliseconds)

        self.attack_index = 0
        self.attack_timer = 0
        self.attack_duration = 200  # Duration in milliseconds for each frame
        self.is_attacking = False
        self.attack_key_down = False
        self.attack_once = False
        self.regular_attack = 5

        self.defend = False
        self.is_hurt = False
        self.hurt_time = 0

        self.slowed_time = 0
        self.slowed_duration = 500
        self.slowed = False



    def get_rare_blue_gems(self):
        return self.rare_blue_gems

    def get_rare_blue_gems_level(self):
        return self.rare_blue_gems_for_this_level

    def get_rare_blue_gems_world(self,world,level):

        return self.rare_blue_gems_for_worlds.get(world,{}).get(level,0)

    def set_rare_blue_gems(self,val):
        self.rare_blue_gems = val

    def set_rare_blue_gems_level(self,val):
        self.rare_blue_gems_for_this_level = val

    def set_rare_blue_gems_world(self,world,level,val):
        self.rare_blue_gems_for_this_world[world][level] = val

    def set_vel(self,vel):
        self.velocity = vel
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def get_dy(self):
        return self.dy
    def set_dy(self,dy):
        self.dy = dy
    def get_rect(self):
        return self.rect
    def get_vel(self):
        return self.velocity

    def update_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def handle_jumping_state(self, grounded):
        if grounded:
            self.jumping = False
        else:
            self.jumping = True

    def damage_taken(self):

        if not self.invulnerable:
            self.is_hurt = True
            self.hurt_time = pygame.time.get_ticks()
            self.health -= 1
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
            return True
        return False

    def get_attack_hitbox(self,more_damage=0):
        width = 20+more_damage # Width of the attack hitbox
        height = self.rect.height  # Height of the attack hitbox
        if self.direction == 1:  # Attacking to the right
            return pygame.Rect(self.rect.right, self.rect.top, width, height)

        return pygame.Rect(self.rect.left - width, self.rect.top, width, height)



    def handle_keys(self):

        # Initialize movement deltas
        self.dx, self.dy = 0, self.velocity  # Set dy to current vertical velocity

        # Get key presses
        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_RIGHT]:
            self.direction = 1
            if not self.defend:
                self.dx = self.walk_speed
                self.walk_counter += 1
                self.img = self.images_dict['walking_right'][self.walk_index]

        elif keys[pygame.K_LEFT]:
            self.direction = -1
            if not self.defend:
                self.dx = -self.walk_speed
                self.walk_counter += 1
                self.img = self.images_dict['walking_left'][self.walk_index]

        else:
            self.walk_index = 1
            self.walking_direction()

        # Attack key press detection
        if not self.is_attacking and not self.attack_key_down and keys[pygame.K_LCTRL]:
            self.is_attacking = True
            self.attack_index = 0  # Start from the first frame
            self.attack_timer = pygame.time.get_ticks()  # Reset timer
            self.attack_key_down = True  # Set flag to indicate the key has been pressed
            self.attack_once = True

        # Reset the attack key-down flag once the key is released
        if not keys[pygame.K_LCTRL]:
            self.attack_key_down = False

        if keys[pygame.K_DOWN]:
            self.defend = True

        else:
            self.defend = False

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_x] and not self.defend and not self.is_attacking:
              # Get the current time in milliseconds


            if not self.torch_thrown:
                # Throw the torch
                self.torch_thrown = True
                self.torch_start_time = current_time  # Reset cooldown timer
                self.torch_animation = True

                x = self.rect.right - 10 if self.direction == 1 else self.rect.left+2
                initial_dx = 5 * self.direction

                torch_init = Torch(x, self.rect.y, self.direction, initial_dx, self.dy)

                self.torch_group.add(torch_init)

                # Reset torch_thrown after cooldown has expired
        if self.torch_thrown and (current_time - self.torch_start_time >= self.torch_cooldown_animation):
            self.torch_animation = False

        if self.torch_thrown and (current_time - self.torch_start_time >= self.torch_cooldown):
            self.torch_thrown = False
            self.torch_group.empty()

    def walking_direction(self):
        self.img = self.images_dict['walking_right'][self.walk_index] if self.direction == 1 else \
        self.images_dict['walking_left'][self.walk_index]

    def handle_attack(self):
        current_time = pygame.time.get_ticks()

        if self.is_attacking:

            if current_time - self.attack_timer >= self.attack_duration:

                # Check if the attack animation has completed
                self.is_attacking = False  # End the attack
                self.attack_timer = current_time  # Reset the timer for the next frame
                self.attack_once = False

            # Update the image based on the attack_index
            if self.defend:
                self.attack_index = 0

            self.img = self.images_dict['attack_right'][self.attack_index] if self.direction == 1 else \
            self.images_dict['attack_left'][self.attack_index]

            self.defend = False
            self.attack_index=1

            Collisions.check_player_strike_crumbling_wall(self.rect,self.direction)

    def handle_collisions(self):
        # Horizontal collisions with tiles
        self.dx,self.horizontal_collision = Collisions.handle_player_horizontal_collision(self.rect, self.dx)

        # Vertical collisions with tiles
        self.dy, self.grounded = Collisions.handle_player_vertical_collision(self.rect, self.dy)



        # Reset jump if the player has landed
        if self.grounded:
            self.jumping = False
            self.velocity = 0  # Reset velocity to 0 when grounded
            self.dy = 0  # Ensure dy is 0 when grounded

        if self.rect.top > Constants.screen_height:
            Constants.GAME_OVER=-1
            Constants.game_over_timer = pygame.time.get_ticks()  # Record the current time in milliseconds
            Constants.button_alpha = 0  # Reset alpha when game over is triggered

    def handle_jump_and_gravity(self):
        keys = pygame.key.get_pressed()

        # Jumping
        if not self.jumping and keys[pygame.K_SPACE] and self.dy == 0:
            self.velocity = -15  # Adjust jump velocity if necessary
            self.jumping = True
            self.grounded = False
            self.jump_index = (self.jump_index + 1) % len(self.images_jump)

        # Apply gravity
        if not self.grounded:
            self.velocity += self.gravity
            if self.velocity > 10:
                self.velocity = 10  # Cap the fall speed
        else:
            self.velocity = 0  # No vertical movement when grounded

        if self.dy>0:
            self.falling = True

        else:
            self.falling = False

    def handle_animations(self):
        if self.jumping and not self.is_attacking:
            self.img = self.images_dict['jump'][self.jump_index] if self.direction == 1 else \
            self.images_dict['jump_left'][self.jump_index]


        # Handle walking animations
        elif self.walk_counter > 10:  # Adjust cooldown if necessary
            self.walk_counter = 0
            self.walk_index += 1
            if self.walk_index >= len(self.images_right):
                self.walk_index = 0
            self.walking_direction()

        if self.defend and not self.is_attacking:
            self.img = self.images_dict['defend_right'] if self.direction == 1 else self.images_dict['defend_left']

        elif self.is_hurt and pygame.time.get_ticks() - self.hurt_time < 300:  # 500ms (0.5 seconds) delay
            self.img = self.images_dict['hurt'][0] if self.direction == 1 else self.images_dict['hurt_left'][0]


        elif self.torch_animation and not self.is_attacking and not self.defend:
            self.img = self.img_torch_throw if self.direction == 1 else self.img_torch_throw_left
        #pygame.draw.rect(Constants.screen,(255,255,255),self.rect,2)

    def handle_invulnerability(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time > self.invulnerability_duration:
                self.invulnerable = False  # End invulnerability after duration
                self.blink = False  # Stop blinking
                self.walk_speed = 4  # Reset walk speed to normal
            else:
                self.walk_speed = self.slowed_speed  # Slow player down while invulnerable
                # Toggle the blink state based on time
                if (current_time - self.invulnerable_time) % self.blink_interval < self.blink_interval / 2:
                    self.blink = True  # Hide player (blink)
                else:
                    self.blink = False  # Show player

    def update(self):

        if Constants.GAME_OVER == 0:

            self.handle_keys()  # Handles movement and attack inputs
            self.handle_attack()  # Handles the attack animation and logic
            self.handle_collisions()  # Handles horizontal and vertical collisions
            self.handle_jump_and_gravity()  # Manages jumping and gravity
            self.handle_animations()  # Handles player animation frames
            self.handle_invulnerability()  # Manages invulnerability state

            self.handle_slow_effect()

        elif Constants.GAME_OVER==-1:
            self.handle_death_animation()


    def draw(self):
        # Blit the player image to the screen, unless blinking (invulnerable)

        if Constants.GAME_OVER==0 and not self.blink:
            Constants.screen.blit(self.img, pygame.Rect(self.rect.x-30,self.rect.y,50,72))


    def handle_death_animation(self):
        # Increment the timer
        self.death_animation_timer += 1

        # Change the image based on the timer
        if self.death_animation_timer >= self.death_animation_speed:
            self.death_animation_timer = 0  # Reset the timer
            self.death_animation_index += 1  # Move to the next frame

            # Check if the animation has reached the last frame
            if self.death_animation_index >= len(self.images_dead):

                self.death_animation_index = len(self.images_dead) - 1  # Stay on the last frame


        #falling
        self.rect.y += self.gravity

        # Use the collision module to handle collision with tiles
        self.rect = Collisions.check_dead_player_collision_with_tiles(self.rect)


        if self.death_animation_index == 0:
            pass
        elif self.death_animation_index != len(self.images_dead)-1:
            self.rect.bottom+=22
        else:
            self.rect.bottom += 28
        # Update the player's image
        self.img = pygame.transform.flip(self.images_dict['dead'][self.death_animation_index], True,
                                         False) if self.direction != 1 else self.images_dict['dead'][
            self.death_animation_index]

        # Draw the player
        Constants.screen.blit(self.img, pygame.Rect(self.rect.x,self.rect.y,40,72))

    def knockback(self, impact_side, knockback_force):
        """Applies knockback to the player based on the impact side."""
        #print(f"Player knocked back from {impact_side}")
        self.slowed_time = pygame.time.get_ticks()

        if not self.grounded:
            knockback_force+=4
        # Calculate diagonal knockback forces
        diagonal_force = knockback_force / math.sqrt(2)
        diagonal_force_x, diagonal_force_y = diagonal_force, diagonal_force

        # Prevent movement if grounded or horizontal collision
        if self.grounded:
            diagonal_force_y = 0  # No knockback on Y-axis if grounded

        temp, self.horizontal_collision = Collisions.handle_player_horizontal_collision(self.rect, self.dx)

        if self.horizontal_collision:
            diagonal_force_x = 0  # No knockback on X-axis if horizontal collision detected

        # Initialize knockback directions
        dx, dy = 0, 0

        # Set knockback based on impact side
        if impact_side == 'top-left':
            dx, dy = diagonal_force_x, diagonal_force_y
        elif impact_side == 'top-right':
            dx, dy = -diagonal_force_x, diagonal_force_y
        elif impact_side == 'bottom-left':
            dx, dy = diagonal_force_x, -diagonal_force_y
        elif impact_side == 'bottom-right':
            dx, dy = -diagonal_force_x, -diagonal_force_y
        elif impact_side == 'left':
            dx = diagonal_force_x
        elif impact_side == 'right':
            dx = -diagonal_force_x
        elif impact_side == 'top':
            dy = diagonal_force_y
        elif impact_side == 'bottom':
            dy = -diagonal_force_y

        # Check for collision in new position before moving
        if not Collisions.check_collision(self.get_rect(),dx, dy):
            self.update_position(dx, dy)


        # Apply slow effect and set a timer to restore speed
        #self.slowed = True


    def handle_slow_effect(self,speed=3):
        """Restores the player's speed after the slow effect wears off."""

        if self.slowed:
            current_time = pygame.time.get_ticks()
            if current_time - self.slowed_time > self.slowed_duration:
                self.walk_speed = 4  # Restore player speed to normal
                self.slowed = False
                print("Player speed restored to normal")

            else:
                print('---------------------')
                self.walk_speed = speed
        else:
            self.walk_speed =4


    def handle_player_winded(self):
        if self.slowed:
            self.walk_speed = 2.5
        else:
            self.walk_speed = 4