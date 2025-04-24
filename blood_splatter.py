import pygame
import Constants
import random
import math


class BloodSplatter(pygame.sprite.Sprite):
    def __init__(self, x, y, player_direction, angle, speed, sizea=20,sizeb=35):
        super().__init__()
        self.name = None
        # Load the blood splatter images
        self.images = [
            pygame.transform.scale(Constants.blood_splatter1, (random.uniform(sizea, sizeb) , random.uniform(sizea, sizeb))),
            pygame.transform.scale(Constants.blood_splatter2, (random.uniform(sizea, sizeb), random.uniform(sizea, sizeb))),
            pygame.transform.scale(Constants.blood_splatter3, (random.uniform(sizea, sizeb), random.uniform(sizea, sizeb))),
            pygame.transform.scale(Constants.blood_splatter4, (random.uniform(sizea, sizeb), random.uniform(sizea, sizeb))),
            pygame.transform.scale(Constants.blood_splatter5, (random.uniform(sizea, sizeb), random.uniform(sizea, sizeb))),
        ]

        # Flip images for left direction
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images]

        # Set the image list based on player direction
        if player_direction == -1:
            self.image_list = self.images_left  # Use flipped images for left direction
        else:
            self.image_list = self.images  # Use regular images for right direction

        # Calculate velocity based on angle and speed
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = -math.sin(angle) * speed  # Negative because pygame's Y-axis increases downwards

        # Set initial image and position
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Animation settings
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150
        self.total_frames = len(self.images)
        self.current_image = 0
        self.finished = False

    def update(self,player_pos=None):
        """ Update the position and animation of the blood splatter """
        if not self.finished:
            # Move the splatter based on its velocity
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

            # Apply gravity to make the blood fall over time
            self.velocity_y += 0.1  # Simulate gravity

            # Animate the blood splatter
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_image += 1
                if self.current_image >= self.total_frames:
                    self.finished = True
                else:
                    # Update the current image in the sequence
                    self.image = self.image_list[self.current_image]
        else:
            # Remove the blood splatter after the animation ends
            self.kill()# When the demon dies, you spawn two blood splatters

def create_blood_splatters(x, y, player_direction,number_of_splatters,sizea=20,sizeb=35):
    blood_splatters = []

    for i in range(number_of_splatters):
        # Set up the base angle and speed for both splatters
        speed = random.uniform(2, 4)  # Random speed for both splatters
        angle = math.radians(random.uniform(0,180 ))  # Random angle between 15 and 45 degrees

        # Create first blood splatter flying in one direction
        blood_splatter = BloodSplatter(x, y, player_direction, angle, speed,sizea,sizeb)

        # Add the blood splatters to the list
        blood_splatters.append(blood_splatter)

    return blood_splatters