
import Constants
import pygame
LIGHT_RADIUS = 6  # The maximum distance the player can see in tiles

MAX_LIGHT_SPIKE_DISTANCE = 200
MAX_LIGHT_HEART_DISTANCE = 400
MAX_LIGHT_GEM_DISTANCE = 400

max_distances = [
	MAX_LIGHT_SPIKE_DISTANCE,
	MAX_LIGHT_HEART_DISTANCE,
	MAX_LIGHT_GEM_DISTANCE,
	MAX_LIGHT_GEM_DISTANCE,
	MAX_LIGHT_GEM_DISTANCE
]
LIGHT_BLOCKERS = [1,2,3,8]



def draw_sprite_with_lighting(screen, sprite, intensity):
    x, y = sprite.rect.x, sprite.rect.y

    # Blit the original sprite image first
    screen.blit(sprite.image, (x, y))

    # Create a surface for the sprite with transparency, same size as the sprite's rect
    sprite_surface = pygame.Surface(sprite.rect.size, pygame.SRCALPHA)

    # Blit the sprite's image onto this new surface
    sprite_surface.blit(sprite.image, (0, 0))

    # Create a shadow surface with transparency
    shadow_surface = pygame.Surface(sprite.rect.size, pygame.SRCALPHA)

    # Shadow color with alpha based on intensity
    shadow_color = (0, 0, 0, int((1 - intensity) * 255))  # Shadow gets darker as intensity decreases
    shadow_surface.fill(shadow_color)

    # Blend the shadow onto the sprite surface using BLEND_RGBA_MULT
    sprite_surface.blit(shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Draw the sprite surface with the shadow onto the screen at the correct position
    screen.blit(sprite_surface, (x, y))


def draw_tiles_with_lighting(tile,x,y,screen_x,screen_y, visible_tiles, tile_size):


    # Draw the tile first

    Constants.screen.blit(tile['img'], (x, y))
    #pygame.draw.rect(Constants.screen, (255, 255, 255), tile['img_rect'], 2)
    # Apply lighting based on visibility and intensity
    if (screen_x, screen_y) in visible_tiles:
        intensity = visible_tiles[(screen_x, screen_y)]
        shadow_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, int((1 - intensity) * 255))  # Darker for lower intensity
        shadow_surface.fill(shadow_color)
        Constants.screen.blit(shadow_surface, (x, y))
    else:
        # Draw fully dark shadow if not visible
        shadow_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 255))  # Fully dark
        Constants.screen.blit(shadow_surface, (x, y))
