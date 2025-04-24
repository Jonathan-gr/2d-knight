import pygame
import Constants

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size=50):
        super().__init__()

        self.images = [
           (pygame.transform.scale(Constants.explosion1, (size, size))),
            (pygame.transform.scale(Constants.explosion2, (size, size))),
          (pygame.transform.scale(Constants.explosion3, (size, size)))

        ]

        self.name = None
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100 if size == 50 else 300 # milliseconds per frame
        self.total_frames = len(self.images)
        self.finished = False

    def update(self,player_pos=None):
        if not self.finished:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_image += 1
                if self.current_image >= self.total_frames:
                    self.finished = True
                else:
                    self.image = self.images[self.current_image]
        else:
            self.kill()

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.image, self.rect.topleft)
