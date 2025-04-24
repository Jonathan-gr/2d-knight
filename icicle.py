import pygame
import Constants



class Icicle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Constants.icicle_img, (Constants.tile_size, Constants.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.blink = False
        self.falling = False
        self.fall_time = 0
        self.fall_delay = 1100  # Delay in milliseconds (1 second)
        self.fall_speed = 2
        self.player_entered = False
        self.name = 'icicle'

    def update(self, player_pos):
        # Define a narrower range for "near"
        if self.rect.x - 90 < player_pos[0] < self.rect.x + 90 and self.rect.y < player_pos[1]:
            self.player_entered = True


        if self.player_entered:
            if not self.falling:
                if self.fall_time == 0:
                    self.fall_time = pygame.time.get_ticks()  # Start timer
                elif pygame.time.get_ticks() - self.fall_time >= self.fall_delay:
                    self.falling = True

        # Continue falling regardless of player's position once it has started
        if self.falling:
            self.rect.y += self.fall_speed
            self.fall_speed += 0.2  # Adjust fall speed as necessary



