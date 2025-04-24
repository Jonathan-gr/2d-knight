import pygame
import Constants

class RareBlueGem(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(Constants.rare_gem, (25, 25))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.blink = False
            self.name = 'blue gem'
            self.tile_x = x // Constants.tile_size  # Calculate tile column
            self.tile_y = y // Constants.tile_size   # Calculate tile row