import pygame
import Constants

class Heart(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(Constants.heart_image,(Constants.tile_size//2,Constants.tile_size//2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.blink = False
            self.name = 'Heart'
            self.tile_x = x // Constants.tile_size  # Calculate tile column
            self.tile_y = y // Constants.tile_size   # Calculate tile row
