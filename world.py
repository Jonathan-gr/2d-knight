import math
from collections import defaultdict

import raycasting
import Constants
import all_sprites
import pygame
from flying_demon import Flyingdemon
from demon_fire_boss import DemonBoss
from closed_exit import ClosedExit
from rare_blue_gem import RareBlueGem
from stone_statue import StoneStatue
import Spikes
from icicle import Icicle
from spider import Spider
from Heart import Heart
import Exit
from fire_wall import Firewall
import pickle
from Tiles import Tiles
from torch import Torch


all_sprites_groups_dict = all_sprites.init_all_sprites(all_sprites.sprite_group_names)
monsters = []
world_consumables_dict = defaultdict(set)
world_consumables_dict_alpha = defaultdict(set)

class World():
	def __init__(self, data,level=None):
		# Initialize the tile list as an instance variable
		self.tile_list = []
		self.last_visible_tiles = {}


		# Define tile size
		tile_size = Constants.tile_size

		for row_count, row in enumerate(data):
			for col_count, tile in enumerate(row):
				if tile == 1:
					self.create_and_append_tile(Constants.stone_img, col_count, row_count, tile_size,1)
				elif tile == 2:
					self.create_and_append_tile(Constants.stone_left_img, col_count, row_count, tile_size,2)
				elif tile == 3:
					self.create_and_append_tile(Constants.stone_right_img, col_count, row_count, tile_size,3)
				elif tile == 8:
					self.create_and_append_tile(Constants.stone_img, col_count, row_count, tile_size, 8)

				elif tile == 4:
					enemy = Spider(col_count * tile_size, row_count * tile_size + 25, None)
					all_sprites_groups_dict['enemy_group'].add(enemy)
					monsters.append([enemy, col_count * tile_size, row_count * tile_size + 25])

				elif tile == 5:
					spike = Spikes.Spikes(col_count * tile_size, row_count * tile_size + 27)
					all_sprites_groups_dict['spike_group'].add(spike)

				elif tile == 6:
					exit = Exit.Exit(col_count * tile_size - 10, row_count * tile_size - tile_size // 2 - 12)
					all_sprites_groups_dict['exit_group'].add(exit)

				elif tile == 7:

					if (col_count,row_count) in world_consumables_dict_alpha[level]:
						continue
					heart = Heart(col_count * tile_size + 12, row_count * tile_size + 12)
					all_sprites_groups_dict['heart_group'].add(heart)


				elif tile == 9:
					statue = StoneStatue(col_count * tile_size, row_count * tile_size - tile_size // 2 - 12)
					all_sprites_groups_dict['stone_statue_group'].add(statue)

				elif tile == 10:
					firewall_init = Firewall(col_count * tile_size, row_count * tile_size + 25)
					all_sprites_groups_dict['firewall_group'].add(firewall_init)

				elif tile == 11:
					flying_demon_init = Flyingdemon(col_count * tile_size, row_count * tile_size,
					all_sprites_groups_dict['BloodSplatter_group'])
					all_sprites_groups_dict['flying_demon_group'].add(flying_demon_init)

				elif tile == 12:
					closed_gate_init = ClosedExit(col_count * tile_size - 13,
					row_count * tile_size - tile_size // 2 - 11)
					all_sprites_groups_dict['closed_gate_group'].add(closed_gate_init)

				elif tile == 13:
					if (col_count,row_count) in world_consumables_dict_alpha[level]:
						continue
					rare_gem_init = RareBlueGem(col_count * tile_size + 12, row_count * tile_size + 12)
					all_sprites_groups_dict['rare_gem_group'].add(rare_gem_init)

				elif tile == 14:
					icicle_init = Icicle(col_count * tile_size, row_count * tile_size)
					all_sprites_groups_dict['icicle_group'].add(icicle_init)

				elif tile == 15:
					demon_boss_init = DemonBoss(col_count * tile_size, row_count * tile_size,
					all_sprites_groups_dict['fireball_group'])
					all_sprites_groups_dict['demon_boss_group'].add(demon_boss_init)

	def create_and_append_tile(self, image, col_count, row_count, tile_size, tile_type):
			img = pygame.transform.scale(image, (tile_size, tile_size))
			img_rect = img.get_rect()
			img_rect.x = col_count * tile_size
			img_rect.y = row_count * tile_size

			tile = {
				'img': img,
				'img_rect': img_rect,
				'tile_type': tile_type,
				'stepped_on_count': 0,
				'is_tile_collapsing': None
			}
			self.tile_list.append(tile)

	def calculate_visible_tiles(self, player_tile_x, player_tile_y, light_radius, player):
		visible_tiles = {}
		torch_visible_tiles = {}

		def calculate_from_position(pos_x, pos_y, target_dict):
			for dy in range(-light_radius, light_radius + 1):
				for dx in range(-light_radius, light_radius + 1):
					tile_x = (pos_x // Constants.tile_size) + dx
					tile_y = (pos_y // Constants.tile_size) + dy

					for tile in self.tile_list:
						if tile['img_rect'].topleft == (tile_x * Constants.tile_size, tile_y * Constants.tile_size):
							distance = math.sqrt(dx ** 2 + dy ** 2)

							if distance <= light_radius:
								intensity = max(0, 1 - (distance / light_radius))
								if (tile_x, tile_y) in target_dict:
									target_dict[(tile_x, tile_y)] += intensity
								else:
									target_dict[(tile_x, tile_y)] = intensity
							break  # Exit loop once the tile is found

		# Calculate visible tiles based on player's position
		if player.jumping:
			visible_tiles = self.last_visible_tiles  # Reuse last calculated tiles
		else:
			calculate_from_position(player_tile_x, player_tile_y, visible_tiles)

		# Check the effect of torches
		for torch in all_sprites.get_sprite_group('torch_group'):
			calculate_from_position(torch.rect.x, torch.rect.y, torch_visible_tiles)

		# Combine player and torch visible tiles
		for tile in torch_visible_tiles:
			if tile in visible_tiles:
				visible_tiles[tile] += torch_visible_tiles[tile]
			else:
				visible_tiles[tile] = torch_visible_tiles[tile]

		# Clamp intensity values to a maximum of 1
		for tile in visible_tiles:
			visible_tiles[tile] = min(1, visible_tiles[tile])

		# Store the visible tiles for future use
		self.last_visible_tiles = visible_tiles

		return visible_tiles

	def calculate_visible_sprites(self, player_tile_x, player_tile_y):
		# Reset visible arrays
		visible_spikes = []
		visible_hearts = []
		visible_gems = []
		visible_spiders = []
		visible_demons = []

		# List of sprite groups and their corresponding visible lists
		sprite_groups = [
			all_sprites_groups_dict['spike_group'],
			all_sprites_groups_dict['heart_group'],
			all_sprites_groups_dict['rare_gem_group'],
			all_sprites_groups_dict['enemy_group'],
			all_sprites_groups_dict['flying_demon_group']
		]
		visible_arrays = [visible_spikes, visible_hearts, visible_gems, visible_spiders, visible_demons]

		# Max distances for each type of sprite (adjust these individually if needed)
		max_distances = raycasting.max_distances

		# Convert player tile position to pixel coordinates
		player_x_pixel = player_tile_x
		player_y_pixel = player_tile_y

		# Iterate over each sprite group, their visible array, and their max distance
		for group_name, group, visible_array, max_distance in zip(
				["Spikes", "Hearts", "Gems", "Spiders", "Demons"],
				sprite_groups,
				visible_arrays,
				max_distances
		):
			# Process each sprite in the group
			for sprite in group:
				sprite_x = sprite.rect.x
				sprite_y = sprite.rect.y

				# Calculate distance between player and sprite in pixels
				distance = math.sqrt((sprite_x - player_x_pixel) ** 2 + (sprite_y - player_y_pixel) ** 2)

				# If the sprite is within the maximum distance, add it to the visible array
				if distance <= max_distance:
					intensity = max(0, 1 - (distance / max_distance))
					visible_array.append((sprite, intensity))

		# Return all visible sprite lists
		return visible_spikes, visible_hearts, visible_gems, visible_spiders, visible_demons

	def draw_tiles_with_lighting(self, visible_tiles, tile_size):


		for tile in self.tile_list:
			x, y = tile['img_rect'].x, tile['img_rect'].y
			screen_x, screen_y = x // tile_size, y // tile_size
			raycasting.draw_tiles_with_lighting(tile,x,y,screen_x,screen_y, visible_tiles, tile_size)

			#pygame.draw.rect(Constants.screen, (255, 255, 255), tile['img_rect'], 2)

	def draw_sprites_with_lighting(self, visible_sprites):
		for visible_sprite in visible_sprites:
			for sprite, intensity in visible_sprite:
				if sprite.blink:
					continue
				raycasting.draw_sprite_with_lighting(Constants.screen, sprite, intensity)

	def draw_world(self, visible_tiles, visible_sprites, tile_size):
		self.draw_tiles_with_lighting(visible_tiles, tile_size)
		self.draw_sprites_with_lighting(visible_sprites)



	def reset_world(self,world, level, player, same_level,secret=False):

		# Clear groups
		all_sprites.empty_all_sprites(all_sprites_groups_dict.values())
		# Load world data from file
		pickle_in = open(f"C:/Users/Tal/PycharmProjects/Hello_world/worlds/world{world}/level{level}_data", 'rb')
		world_data = pickle.load(pickle_in)  # Load original world data

		self.enter_level_set_consumables(level, same_level)

		self.__init__(world_data,level)  # Call the constructor of the current instance to initialize it with new data


		if same_level:
			Tiles().reset_tiles()
			self.tile_list = Tiles().get_tile_list()

		else:

			Tiles().set_original_list(self.tile_list)
			Tiles(self.tile_list)

		# Get player start position
		if secret:
			level+=0.5

		if level not in Constants.player_start_positions:
			x, y = Constants.player_start_pos_x, Constants.player_start_pos_y
		else:
			x, y = Constants.player_start_positions[level][0], Constants.player_start_positions[level][1]

		player.init_and_restart_player(x, y, Constants.start_lvl_health, player.get_rare_blue_gems())

	def enter_level_set_consumables(self, level, same_level):
		if not same_level:
			# Initialize the alpha dict entry if it doesn't exist
			if level not in world_consumables_dict_alpha:
				world_consumables_dict_alpha[level] = set()

			# For a new level, add current consumables to the alpha dict
			world_consumables_dict_alpha[level].update(world_consumables_dict[level])
			world_consumables_dict[level] = set()  # Start with an empty set for the new level
		else:
			# If the level has been visited and is being reset, restore from alpha
			if level in world_consumables_dict_alpha:
				world_consumables_dict[level] = world_consumables_dict_alpha[level].copy()
			else:
				world_consumables_dict[level] = set()  # No previous data

	def collect_item(self, item, level):
		# Add the collected item to the list of collected items for this level
		if level not in Constants.collected_items:
			Constants.collected_items[level] = []

		Constants.collected_items[level].append(item)  # Store item ID or name
