

import pygame
import Constants
from explosion import Explosion
import player
import Exit

from Collisions import check_player_hit_fireboss, check_player_fireboss_collision, check_tile_fireball_collision, \
	check_player_icicle_collision, check_player_monster_collision, check_player_spike_collision, \
	check_player_exit_collision, check_player_heart_collision, check_player_hit_statue_collision, \
	check_fireball_player_collision, check_player_firewall_collision, check_player_hit_flying_demon, \
	check_player_closed_gate_collision, check_player_rare_blue_gem_collision, check_monster_dead_falling_on_tile
from Tiles import Tiles
import Texts
from Heart import Heart
from fire_wall import Firewall
import all_sprites
from world import World, world_consumables_dict
import raycasting
from world_menu import WorldMenu

pygame.init()

clock = Constants.CLOCK
fps = Constants.FPS

screen_width = Constants.screen_width
screen_height = Constants.screen_height

screen = Constants.screen
pygame.display.set_caption('Platformer')

#define game variables
tile_size = Constants.tile_size

all_sprites_groups_dict = all_sprites.init_all_sprites(all_sprites.sprite_group_names)
monsters = []


# def draw_grid():
# 	for line in range(0, len(world_data[0])):
# 		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
# 		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


# def draw(self):
	# 	for tile in Tiles().tile_list:
	# 		screen.blit(tile['img'], tile['img_rect'])
	# 		print('sd')
	# 		#pygame.draw.rect(screen,(255,255,255),tile['img_rect'],2)

if Constants.level not in Constants.player_start_positions:  # Check if the dictionary is empty or the key doesn't exist
	x, y = Constants.player_start_pos_x, Constants.player_start_pos_y
else:
	x, y = Constants.player_start_positions[Constants.level][0], Constants.player_start_positions[Constants.level][1]
player = player.Player(x,y)
world = World(Constants.WORLD_DATA)
Tiles(world.tile_list)
world_menu = WorldMenu(player)

run = True


def updates():

	all_sprites.update_all_sprites(all_sprites_groups_dict.values(),(player.rect.x,player.rect.y,player.rect.center),player)
	player.update()

def drawings():

	# Assuming player.x and player.y represent the player’s position
	player_pos = (player.rect.x , player.rect.y)

	# Calculate which tiles are visible based on the player’s position and light radius
	visible_tiles = world.calculate_visible_tiles(player_pos[0],player_pos[1], raycasting.LIGHT_RADIUS,player)
	visible_spike, visible_hearts, visible_gems, visibile_spider, visible_demons = world.calculate_visible_sprites(player_pos[0],player_pos[1])
	visible_sprites = [visible_spike,visible_hearts,visible_gems,visibile_spider,visible_demons]

	# Draw the world, applying light and shadow
	world.draw_world(visible_tiles,visible_sprites,Constants.tile_size)

	all_sprites.draw_all_sprites_and_player(all_sprites_groups_dict, screen, player)


def open_gate():
	for gate in all_sprites_groups_dict['closed_gate_group']:
		gate.is_opening = True
		exit_init = Exit.Exit(gate.rect.x, gate.rect.y)
		all_sprites_groups_dict['exit_group'].add(exit_init)


def reset_health_and_gems():

	player.set_rare_blue_gems(player.get_rare_blue_gems() + player.get_rare_blue_gems_level())
	player.set_rare_blue_gems_level(0)
	Constants.start_lvl_health = player.health
	Constants.levels_visited.add(Constants.level)


def handle_game_over():
	time_elapsed = pygame.time.get_ticks() - Constants.game_over_timer
	# Apply fade-in effect
	if time_elapsed > Constants.FADE_IN_DURATION:
		if Constants.button_alpha < Constants.MAX_ALPHA:
			# Calculate the alpha increment based on elapsed time
			alpha_increment = Constants.MAX_ALPHA * (
						time_elapsed - Constants.FADE_IN_DURATION) / Constants.FADE_IN_DURATION
			button_alpha = min(int(alpha_increment), Constants.MAX_ALPHA)  # Ensure alpha doesn't exceed MAX_ALPHA

		# Set the alpha for the button surface
		Constants.restart_button_on_screen.set_alpha(button_alpha)
		Constants.game_over_button_on_screen.set_alpha(button_alpha)
		Constants.quit_button_on_screen.set_alpha(button_alpha)

		Constants.restart_button_on_screen.draw()
		Constants.game_over_button_on_screen.draw()
		Constants.quit_button_on_screen.draw()

		if Constants.restart_button_on_screen.button_clicked() or pygame.key.get_pressed()[pygame.K_RETURN]:
			Constants.gems_collected[Constants.world][Constants.level] = player.get_rare_blue_gems_world(
				Constants.world, Constants.level) - player.get_rare_blue_gems_level()
			player.set_rare_blue_gems_level(0)
			world.reset_world(Constants.world, Constants.level, player, True)
			Constants.GAME_OVER = 0

		elif Constants.quit_button_on_screen.button_clicked():
			Constants.gems_collected[Constants.world][Constants.level] = player.get_rare_blue_gems_world(
				Constants.world, Constants.level) - player.get_rare_blue_gems_level()
			player.set_rare_blue_gems_level(0)
			Constants.main_menu = True


def handle_dead_stone():
	global explosion
	dead_stone.kill()
	explosion = Explosion(dead_stone.rect.centerx, dead_stone.rect.centery, 100)
	all_sprites_groups_dict['explosion_group'].add(explosion)
	firewall = Firewall(dead_stone.rect.x, dead_stone.rect.bottom - 25)
	all_sprites_groups_dict['firewall_group'].add(firewall)
	heart = Heart(dead_stone.rect.x + 15, dead_stone.rect.y + 15)
	all_sprites_groups_dict['heart_group'].add(heart)


def hanlde_main_menu():
	global run
	Constants.play_button_on_screen.draw()
	Constants.quit_button_on_screen.draw()
	Constants.worlds_button_on_screen.draw()
	# Handle button clicks only after a full click-release cycle
	if not Constants.mouse_clicked and pygame.mouse.get_pressed()[0] == 1:
		# Check if the quit button is clicked
		if Constants.quit_button_on_screen.button_clicked():
			run = False
		# Check if the play button is clicked
		elif Constants.play_button_on_screen.button_clicked():
			Constants.main_menu = False
		# Check if the worlds button is clicked
		elif Constants.worlds_button_on_screen.button_clicked():
			Constants.main_menu = False
			Constants.worlds_menu = True

		# Set the clicked flag to prevent repeated clicks
		Constants.mouse_clicked = True

	# Reset the clicked flag when the mouse button is released
	elif pygame.mouse.get_pressed()[0] == 0:
		Constants.mouse_clicked = False


def handle_worlds_menu():
	Constants.back_button_on_screen.draw()
	Constants.confirm_button_on_screen.draw()
	Constants.restart_world_button_on_screen.draw()
	world_menu.draw()
	world_menu.handle_clicks()
	world_chosen = world_menu.get_selected_world()
	if Constants.confirm_button_on_screen.button_clicked() and world_chosen:
		if Constants.world != world_chosen:
			Constants.level = 1
		Constants.world = world_chosen
		reset_health_and_gems()
		world.reset_world(Constants.world, Constants.level, player, False)
	if Constants.restart_world_button_on_screen.button_clicked():
		Constants.level = 1
		world.reset_world(Constants.world, Constants.level, player, False)
	# Handle button clicks only after a full click-release cycle
	if not Constants.mouse_clicked and pygame.mouse.get_pressed()[0] == 1:
		# Check if the back button is clicked
		if Constants.back_button_on_screen.button_clicked():
			Constants.main_menu = True
			Constants.worlds_menu = False

		# Set the clicked flag to prevent repeated clicks
		Constants.mouse_clicked = True

	# Reset the clicked flag when the mouse button is released
	elif pygame.mouse.get_pressed()[0] == 0:
		Constants.mouse_clicked = False


def check_game_collisions():
	global dead_stone
	# spike collision
	if player.falling and check_player_spike_collision(player, all_sprites_groups_dict['spike_group']):
		player.damage_taken()
	# icicle collision
	if check_player_icicle_collision(player, all_sprites_groups_dict['icicle_group']):
		player.damage_taken()

	# check if player exited
	elif check_player_exit_collision(player, all_sprites_groups_dict['exit_group']) and (
			pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
		Constants.GAME_OVER = 1

	# closed gate
	elif Constants.level not in Constants.boss_levels and len(all_sprites_groups_dict['closed_gate_group']) > 0 and len(
			all_sprites_groups_dict['flying_demon_group']) == 0:
		open_gate()
	# check heart collision
	heart_collision = check_player_heart_collision(player, all_sprites_groups_dict['heart_group'])
	if heart_collision:
		world_consumables_dict[Constants.level].add(heart_collision)
		player.health += 1
	# check gem collision
	gem_collision = check_player_rare_blue_gem_collision(player, all_sprites_groups_dict['rare_gem_group'])
	if gem_collision:
		world_consumables_dict[Constants.level].add(gem_collision)
		player.set_rare_blue_gems_level(player.get_rare_blue_gems_level() + 1)
		Constants.gems_collected[Constants.world][Constants.level] += 1

	# check firewall collision
	elif check_player_firewall_collision(player, all_sprites_groups_dict['firewall_group']):
		pass
	# check if statue hit
	dead_stone = check_player_hit_statue_collision(player)


def check_secret_levels():
	if Constants.level == 5 and 400 <= player.rect.centerx <= 450 and player.rect.bottom < -25:
		reset_health_and_gems()
		Constants.level = 50
		world.reset_world(Constants.world, Constants.level, player, False)

	elif Constants.level == 50 and player.rect.bottom >= Constants.screen_height - 1:
		reset_health_and_gems()
		Constants.level = 5
		world.reset_world(Constants.world, Constants.level, player, False, True)


while run:


	clock.tick(fps)
	screen.blit(Constants.bg_img, (0, 0))

	# Main Menu Logic
	if Constants.main_menu:

		# Draw buttons
		hanlde_main_menu()

	# Worlds Menu Logic
	elif Constants.worlds_menu:

		# Draw back button
		handle_worlds_menu()

	else:

		updates()
		drawings()

		# fireball hit
		check_fireball_player_collision(player, all_sprites_groups_dict['fireball_group'],
										all_sprites_groups_dict['explosion_group'])
		# monster collision
		check_player_monster_collision(player, all_sprites_groups_dict['enemy_group'])

		if len(all_sprites_groups_dict['demon_boss_group']) > 0:
			check_tile_fireball_collision(all_sprites_groups_dict['fireball_group'])
			if check_player_fireboss_collision(player.rect):
				player.damage_taken()

		elif Constants.level in Constants.boss_levels:
			open_gate()

		check_secret_levels()


		# if game is not over
		if Constants.GAME_OVER == 0:
			Texts.draw_health(Constants.heart_image, player.health, 25, 25)
			Texts.draw_rare_blue_gems(Constants.rare_gem, 25, 75,
									  player.get_rare_blue_gems() + player.get_rare_blue_gems_level())

			#hanlde collisions
			check_game_collisions()
			if dead_stone:
				handle_dead_stone()

			# check player flying demon collision
			check_player_hit_flying_demon(player)

			#check player boss hit
			check_player_hit_fireboss(player)

			if player.health<=0:
				Constants.GAME_OVER = -1
				Constants.game_over_timer = pygame.time.get_ticks()  # Record the current time in milliseconds
				Constants.button_alpha = 0  # Reset alpha when game over is triggered

		elif Constants.GAME_OVER==-1:
				handle_game_over()

		elif Constants.GAME_OVER==1:

			reset_health_and_gems()
			Constants.level += 1

			if Constants.level>Constants.max_level:
				Constants.level=1
			Constants.GAME_OVER = 0
			if Constants.level <= Constants.max_level:
				world_data = []
				world.reset_world(Constants.world,Constants.level,player,False)

			else:
				pass


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()

