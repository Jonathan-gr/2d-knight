
import pygame

import Constants
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # This function applies the camera offset to a given entity (like a player or sprite)
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # This function centers the camera on the player (target)
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to the size of the level (world bounds)
        x = min(0, x)  # Left
        x = max(-(self.width - Constants.screen_width), x)  # Right
        y = min(0, y)  # Top
        y = max(-(self.height - Constants.screen_height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
