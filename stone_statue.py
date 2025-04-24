import pygame
import math
from fire_projectile import Fireball
import Constants
import random
import all_sprites

from monster import Monster

class StoneStatue(Monster):
    def __init__(self, x, y,firing_distance=2100):
        super().__init__(x, y,1)
        self.image = pygame.transform.scale(Constants.stone_statue_img, (Constants.tile_size * 1.25, Constants.tile_size * 1.75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fireball_group = all_sprites.get_sprite_group('fireball_group')
        self.fireball_cooldown = random.uniform(2000,4000)
        self.last_fireball_time = pygame.time.get_ticks()
        self.firing_distance = firing_distance
        self.name = 'stone_statue'

    def init_monster(self, x, y):
        """Initialize the specific monster (StoneStatue)."""
        # You can use this to initialize additional attributes if needed
        pass

    def on_hit(self, hit):
        super().start_blinking()
        self.health-=1
        if self.health<=0:
            return True

    def update(self, player_position):

        self.update_blinking()
        current_time = pygame.time.get_ticks()
        # Check if it's time to fire a new fireball
        distance = math.sqrt((self.rect.x-player_position[0])**2 + (self.rect.y-player_position[1])**2)
        if distance <=self.firing_distance:
            if current_time - self.last_fireball_time >= self.fireball_cooldown:

                self.fire_fireball(player_position)
                self.last_fireball_time = current_time

                self.fireball_cooldown = random.uniform(100, 2500)

            #pygame.draw.rect(Constants.screen, (255, 255, 255), self.rect, 2)

    def draw(self, surface):

        if not self.blink:
            surface.blit(self.image, self.rect.topleft)
        else:
            # Optional: Draw something else or change the appearance when blinking
            pass

    def fire_fireball(self, player_position):

        dx = player_position[2][0] - self.rect.centerx
        dy = player_position[2][1] - self.rect.centery
        angle = math.atan2(dy, dx)
        fireball = Fireball(self.rect.centerx, self.rect.centery, angle)
        self.fireball_group.add(fireball)
        #print("Fireball launched by statue!")
