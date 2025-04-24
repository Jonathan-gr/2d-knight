

import random
import pygame
import Constants

class Gust(pygame.sprite.Sprite):
        def __init__(self, x, y,duration,direction,sizex=50,sizey=60):
            pygame.sprite.Sprite.__init__(self)
            self.images = [
                (pygame.transform.scale(Constants.gust1, (sizex, sizey))),
                (pygame.transform.scale(Constants.gust2, (sizex, sizey))),
                (pygame.transform.scale(Constants.gust3, (sizex, sizey))),
                (pygame.transform.scale(Constants.gust4, (sizex, sizey)))

            ]
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.blink = False
            self.name =  None
            self.image_index = 0  # To keep track of the current image
            self.animation_speed = 100  # Switch image every 100ms
            self.last_animation_time = pygame.time.get_ticks()
            self.duration = duration
            self.init_time = pygame.time.get_ticks()
            self.direction = direction

        def update(self,player_pos=None):

            current_time = pygame.time.get_ticks()

            if current_time - self.last_animation_time > self.animation_speed:
                self.image_index = (self.image_index + 1) % len(self.images)  # Alternate between 0 and 1
                self.image = self.images[self.image_index]
                self.last_animation_time = current_time
                if self.direction == 'left':
                    self.rect.x +=8
                else:
                    self.rect.x-=8

                self.rect.y+=random.uniform(-20,20)



            elif current_time - self.init_time > self.duration:
                self.kill()
