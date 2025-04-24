import pygame
import Constants
import Collisions


class Firewall(pygame.sprite.Sprite):
    def __init__(self, x, y, duration=None,width=50,angle=0):
        super().__init__()

        self.images = [
            pygame.transform.scale(Constants.fire_wall, (width, 25)),
            pygame.transform.scale(Constants.fire_wall2, (width, 25)),
        ]
        self.falling = False
        self.angle = angle
        self.images = [pygame.transform.rotate(img, self.angle) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image_index = 0  # To keep track of the current image
        self.animation_speed = 100  # Switch image every 100ms
        self.last_animation_time = 0
        self.duration = duration
        self.init_time = pygame.time.get_ticks()
        self.name = 'fire wall'

        # Rotate the firewall
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self, player_pos=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)  # Alternate between images
            self.image = self.images[self.image_index]
            self.last_animation_time = current_time  # Update the correct timer

        collide_y = Collisions.check_collision_with_tiles_y(self.rect)
        collide_x = Collisions.check_collision_with_tiles_x(self.rect)

        if (collide_x or collide_y) and self.falling:
            self.kill()

        if not collide_y:
            if 45 <= self.angle < 135 or -135 <= self.angle < -45:
                self.rect.y += 1

        if not collide_y and not collide_x:
            self.angle += 5  # Rotate by 5 degrees each frame
            self.angle = self.angle % 360  # Keep the angle in [0, 360]

            # Rotate the image based on the current angle
            self.image = pygame.transform.rotate(self.images[self.image_index], self.angle)
            # Update the rect to maintain the center of the object
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y += 2.5
            self.falling = True

        elif self.duration and current_time - self.init_time > self.duration:
            self.kill()
