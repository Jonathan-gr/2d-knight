import pygame
import Constants

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.img = Constants.open_gate
        self.image = pygame.transform.scale(self.img,(Constants.tile_size*1.25,int(Constants.tile_size*1.75)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = 'exit open'



