
import pygame
import Constants

class Spikes(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(Constants.spike_img,(Constants.tile_size,Constants.tile_size//2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.blink=False
            self.name = 'spikes'

        def update(self,player_pos = None):
            pass
            #pygame.draw.rect(Constants.screen, (255, 255, 255), self.rect, 2)
