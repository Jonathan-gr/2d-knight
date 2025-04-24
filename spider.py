import pygame
import Constants

from monster import Monster
import Collisions

class Spider(Monster):
    def init_monster(self,x,y,width=45,height=25):
        # Specific initialization for Spider
        self.name = 'spider'
        self.image1 = Constants.spider_img1
        self.attack_image = pygame.transform.scale(Constants.spider_attack, (45, 25))  # Scale the image
        self.attack_image_left = pygame.transform.flip(self.attack_image, True, False)

        self.eating_images = [
            pygame.transform.scale(Constants.spider_eating_1, (50, 25)),
            pygame.transform.scale(Constants.spider_eating_2, (50, 25)),
            pygame.transform.scale(Constants.spider_eating_3, (50, 25)),

        ]
        # Create the flipped versions of the eating images
        self.eating_images_left = [
            pygame.transform.flip(img, True, False) for img in self.eating_images
            # Flip horizontally (True for horizontal, False for vertical)
        ]

        self.image_index_eating = 0  # To keep track of the current image
        self.animation_speed_eating = 200  # Switch image every 100ms
        self.last_animation_time_eating = 0

        self.image_left1 = pygame.transform.flip(self.image1, True, False)
        img = pygame.transform.scale(self.image1, (width, height))  # Scale the image to common size
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_collison = False
        self.blink = False


    def dead(self):
        # Override to use specific death image
        self.image = pygame.transform.scale(Constants.spider_dead, (50, 25))  # Scale the image
        super().dead()

    def on_hit(self,hit,player_direction):
        if not Collisions.check_horizontal_collision(self.rect, player_direction):
            force = 0
            if self.dead_flag:
                force += 2
            self.rect.x += hit + force if player_direction == 1 else -(hit + force)
            super().on_hit(hit)

    def update(self,player_pos=None):

        if self.dead_flag and pygame.event.get(pygame.USEREVENT + 1):
            self.kill()  # Remove from all groups if using pygame.sprite.Group

        collision_detected = Collisions.check_horizontal_collision(self.rect, self.direction)
        Collisions.check_monster_dead_falling_on_tile(self)

        if not self.dead_flag:
            if Constants.GAME_OVER == -1:

                current_time = pygame.time.get_ticks()



                if not self.player_collison:
                    self.rect.x += self.direction
                    if self.direction > 0:  # Moving right
                        self.image = self.image1
                    else:  # Moving left
                        self.image = self.image_left1
                else:
                    # Check if it's time to switch images based on the elapsed time
                    if current_time - self.last_animation_time_eating > self.animation_speed_eating:

                        self.image_index_eating = (self.image_index_eating + 1) % len(
                            self.eating_images)  # Alternate between images
                        if self.direction == 1:
                            self.image = self.eating_images[self.image_index_eating]
                        else:
                            self.image = self.eating_images_left[self.image_index_eating]
                        self.last_animation_time_eating = current_time  # Update the correct timer

                    self.rect.y -= 5


            else:
                self.image = self.image1 if self.direction > 0 else self.image_left1

                self.rect.x += self.direction
            if collision_detected:
                self.direction *= -1
                self.rect.x += self.direction * 2

            self.move_counter += 1

        # Apply gravity
        self.apply_gravity()

        super().update()
