import copy
import pygame
import Constants

class Tiles:
    _instance = None

    def __new__(cls, tile_list=None):
        if cls._instance is None:
            cls._instance = super(Tiles, cls).__new__(cls)
            # Initialize tile lists
            cls._instance.tile_list = tile_list if tile_list else []
            cls._instance.original_tile_list = cls.custom_deepcopy(cls._instance.tile_list)
        return cls._instance

    def __init__(self, tile_list=None):
        if tile_list is not None:
            self.tile_list = tile_list
            self.original_tile_list = self.custom_deepcopy(tile_list)

    @staticmethod
    def custom_deepcopy(tile_list):
        """Custom deep copy that includes storing original images."""
        copied_list = []
        for tile in tile_list:

            copied_tile = tile.copy()  # Shallow copy the dictionary

            # Store original image for reset
            copied_tile['original_img'] = copied_tile['img']  # Store the original image

            if 'img' in copied_tile:
                copied_tile['img'] = tile['img']  # Preserve the image reference
            copied_list.append(copied_tile)
        return copied_list

    def get_tile_list(self):
        return self.tile_list

    def get_original_tile_list(self):
        return self.original_tile_list

    def remove_tile(self, tile):
        """Safely remove the tile from the tile_list."""
        if tile in self.tile_list:
            self.tile_list.remove(tile)

    def reset_tiles(self):
        """Method to reset the tile list using the original."""


        # Perform deep copy to restore tile list
        self.tile_list = self.custom_deepcopy(self.original_tile_list)

        # Restore the original images
        # for tile in self.tile_list:
        #     tile['img'] = tile['original_img']  # Reset the image to its original state
        #     tile['is_tile_collapsing'] = None

    def set_original_list(self,tile_list):
        self.original_tile_list = self.custom_deepcopy(tile_list)

    def change_tile_image(self,tile):
        # Calculate the elapsed time
        elapsed_time = pygame.time.get_ticks() - tile['is_tile_collapsing']

        # Update the tile image based on elapsed time
        if elapsed_time < 100:
            # 0-5 seconds: No change, initial tile
            pass
        elif elapsed_time < 1000:
            # 5-10 seconds: Change to cracked stone
            tile['img'] = pygame.transform.scale(Constants.cracked_stone_img,
                                                 (tile['img_rect'].width, tile['img_rect'].height))

        elif elapsed_time < 2000:
            # 10-15 seconds: Change to very cracked stone
            tile['img'] = pygame.transform.scale(Constants.cracked_stone_img_3,
                                                 (tile['img_rect'].width, tile['img_rect'].height))

        else:
            # 15 seconds and above: Remove the tile
            Tiles().remove_tile(tile)