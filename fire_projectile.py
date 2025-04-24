import pygame
import Constants
import math


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.name = None
        # Load two images and store them in a list for animation
        self.images = [
            pygame.transform.scale(Constants.fire_ball, (30, 30)),
            pygame.transform.scale(Constants.fire_ball2, (30, 30)),
            pygame.transform.scale(Constants.fire_ball3, (30, 30))
        ]

        self.image_index = 0  # To keep track of the current image
        self.animation_speed = 100  # Switch image every 100ms
        self.last_animation_time = pygame.time.get_ticks()

        # Rotate both images based on the angle
        self.images = [pygame.transform.rotate(image, -math.degrees(angle)) for image in self.images]

        self.image = self.images[self.image_index]  # Set the initial image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.angle = angle  # Store the angle for movement

        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def update(self,player_pos=None):
        #pygame.draw.rect(Constants.screen, (255, 255, 255), self.rect, 2)
        current_time = pygame.time.get_ticks()

        # Calculate the new position based on the angle and speed
        self.pos_x += self.speed * math.cos(self.angle)
        self.pos_y += self.speed * math.sin(self.angle)

        # Update the rectangle position using the rounded values
        self.rect.centerx = round(self.pos_x)
        self.rect.centery = round(self.pos_y)

        # Animate the fireball (switch between the two images)
        if current_time - self.last_animation_time > self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)  # Alternate between 0 and 1
            self.image = self.images[self.image_index]
            self.last_animation_time = current_time

        # Check if the fireball goes off screen and remove it
        if self.rect.right < 0 or self.rect.left > Constants.screen_width or self.rect.bottom < 0 or self.rect.top > Constants.screen_height:
            self.kill()

    def get_fireball_direction(self):
        # Convert radians to degrees
        angle_degrees = math.degrees(self.angle) % 360  # Ensure angle is between 0-360


        if 45 <= angle_degrees < 135:  # Moving down
            return 'down'
        elif 135 <= angle_degrees < 225:  # Moving left
            return 'left'
        elif 225 <= angle_degrees < 315:  # Moving up
            return 'up'
        else:  # Moving right
            return 'right'