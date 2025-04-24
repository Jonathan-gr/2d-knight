import Collisions
import Constants

import pygame


import Collisions
import Constants
import pygame


class Torch(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, dx, dy, initial_velocity=5):
        super().__init__()
        self.image = pygame.transform.scale(Constants.torch_img, (35, 35))
        self.rect = pygame.Rect(x, y, 5, 15)
        self.rect.x = x
        self.rect.y = y

        self.name = 'torch'
        # Player throw movement effects
        self.dx = abs(dx * 0.5)  # Scale down horizontal velocity
        self.dy = dy * 0.3  # Initial vertical velocity due to player's throw

        # Direction the torch is thrown
        self.direction = direction

        # Falling/arc parameters
        self.initial_velocity = initial_velocity  # Initial upward velocity from the throw
        self.gravity = 0.5  # Gravity effect (positive for downward)
        self.velocity_y = -self.initial_velocity  # Start by moving upward
        self.is_active = True  # To track if the torch is still in the air

    def update(self, player_pos=None):
        if self.is_active:
            # Apply gravity to vertical velocity
            self.velocity_y += self.gravity  # Increase downward speed due to gravity

            # Update position based on current velocities
            self.rect.y += self.velocity_y  # Update vertical position

            # Calculate horizontal movement based on direction and dx
            horizontal_movement = self.direction * self.dx

            # Check for tile collisions before updating horizontal position
            collide_x = Collisions.check_collision_with_tiles_x(self.rect.move(horizontal_movement, 0))

            # Update horizontal position if there’s no collision
            if not collide_x:
                print(horizontal_movement)
                self.rect.x += horizontal_movement  # Update horizontal position only if no collision

            # Now check for vertical collisions
            collide_y = Collisions.check_collision_with_tiles_y(self.rect)

            # Handle vertical collision
            if collide_y:
                self.handle_collision()

            # Check if the torch has fallen below the ground level
            if self.rect.y >= Constants.screen_height:  # Adjust this to your ground level
                self.rect.y = Constants.screen_height
                self.is_active = False  # Stop the torch

    def handle_collision(self):
        print('Collision on Y axis detected')
        # Snap torch to the tile's top and stop its downward motion
        self.rect.y -= self.velocity_y + 2  # Adjust position to prevent sinking into tile
        self.velocity_y = 0  # Stop vertical movement after landing
        self.is_active = False  # Deactivate torch after landing

    def handle_collision(self):
        print('y')
        # Snap torch to the tile's top and stop its downward motion
        self.rect.y = self.rect.y - self.velocity_y -2 # Adjust position to prevent sinking into tile
        self.velocity_y = 0  # Stop vertical movement after landing
        self.is_active = False  # Deactivate torch after landing

    def draw(self):
        # Draw the torch on the screen at its current position
        Constants.screen.blit(self.image, pygame.Rect(self.rect.x-15,self.rect.y-10,5,10))
        #pygame.draw.rect(Constants.screen,(255,255,255),self.rect,2)



