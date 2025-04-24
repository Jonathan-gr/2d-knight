import pygame
import Constants

class ClosedExit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = Constants.closed_gate3

        # Scale the initial image
        self.image = pygame.transform.scale(self.img, (Constants.tile_size * 1.25, int(Constants.tile_size * 1.75)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = None

        # List of images for opening the gate
        self.opening_images = [
            pygame.transform.scale(Constants.closed_gate3, (Constants.tile_size * 1.25, int(Constants.tile_size * 1.75))),
            pygame.transform.scale(Constants.closed_gate2, (Constants.tile_size * 1.25, int(Constants.tile_size * 1.75))),
            pygame.transform.scale(Constants.closed_gate1, (Constants.tile_size * 1.25, int(Constants.tile_size * 1.75)))
        ]

        self.current_image = 0  # Index of the current image
        self.is_opening = False  # To control when to start the opening animation
        self.last_update = pygame.time.get_ticks()  # Keep track of time for the animation
        self.frame_delay = 1000  # Time between frames in milliseconds (adjust this for desired speed)

    def update(self,player_pos=None):
        if self.is_opening:
            now = pygame.time.get_ticks()
            # Check if enough time has passed to switch to the next image
            if now - self.last_update > self.frame_delay:
                self.last_update = now  # Reset the last update time
                self.current_image += 1  # Move to the next frame

                # If the animation is not done, update the image
                if self.current_image < len(self.opening_images):
                    self.image = self.opening_images[self.current_image]
                else:
                    self.is_opening = False  # Stop animating when all images have been shown
                    self.kill()

    def open_gate(self):
        # Trigger the gate opening animation
        self.is_opening = True
        self.current_image = 0  # Start from the first image in the animation
        self.last_update = pygame.time.get_ticks()  # Reset timing for a smooth animation start
