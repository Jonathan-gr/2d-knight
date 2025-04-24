import pygame
import pickle
from os import path

import Constants

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = Constants.tile_size

options = 15
screen_width = Constants.screen_width
screen_height = Constants.screen_height

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

world = 1

#load images




#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = [[0] * Constants.ROWS for _ in range(Constants.COLS)]



#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for line in range(0, len(world_data[0])):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def draw_world():
	for row in range(len(world_data)):
		for col in range(len(world_data[0])):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#stone
					img = pygame.transform.scale(Constants.stone_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				elif world_data[row][col] == 2:
					#stone left
					img = pygame.transform.scale(Constants.stone_left_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				elif world_data[row][col] == 3:
					#estoneleft
					img = pygame.transform.scale(Constants.stone_right_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				elif world_data[row][col] == 4:
					#spider
					img = pygame.transform.scale(Constants.spider_img1, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				elif world_data[row][col] == 5:
					#spike
					img = pygame.transform.scale(Constants.spike_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))

				elif world_data[row][col] == 6:
					#exit
					img = pygame.transform.scale(Constants.open_gate, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))

				elif world_data[row][col] == 7:
					#heart
					img = pygame.transform.scale(Constants.heart_image, (tile_size//2, tile_size//2))
					screen.blit(img, (col * tile_size+12 , row * tile_size+12))

				elif world_data[row][col] == 8:
					#crumbling stone
					img = pygame.transform.scale(Constants.cracked_stone_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

				elif world_data[row][col] == 9:
					#statue
					img = pygame.transform.scale(Constants.stone_statue_img, (tile_size*1.25, tile_size*1.75))
					screen.blit(img, (col * tile_size, row * tile_size-tile_size//2 -14))

				elif  world_data[row][col] == 10:
					img = pygame.transform.scale(Constants.fire_wall, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

				elif  world_data[row][col] == 11:
					img = pygame.transform.scale(Constants.flying_demon_arr[0], (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

				elif world_data[row][col] == 12:
					#exit
					img = pygame.transform.scale(Constants.closed_gate3, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))

				elif world_data[row][col] == 13:
					#exit
					img = pygame.transform.scale(Constants.rare_gem, (tile_size//2, tile_size//2))
					screen.blit(img, (col * tile_size+12 , row * tile_size+12))

				elif world_data[row][col] == 14:
					#exit
					img = pygame.transform.scale(Constants.icicle_img, (tile_size, tile_size//2))
					screen.blit(img, (col * tile_size , row * tile_size))

				elif  world_data[row][col] == 15:
					img = pygame.transform.scale(Constants.boss_arr[0], (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()
		print(pos)
			#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width - 100, 0, Constants.save_img)
load_button = Button(screen_width - 100, 100, Constants.load_img)

#main game loop
run = True
while run:

	clock.tick(fps)
	screen.blit(Constants.bg_img, (0, 0))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f"C:/Users/Tal/PycharmProjects/Hello_world/worlds/world{world}/level{level}_data", 'wb')

		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data

		if path.exists(f"C:/Users/Tal/PycharmProjects/Hello_world/worlds/world{world}/level{level}_data"):
			pickle_in = open(f"C:/Users/Tal/PycharmProjects/Hello_world/worlds/world{world}/level{level}_data", 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	#event handler
	for event in pygame.event.get():
		# Quit game
		if event.type == pygame.QUIT:
			run = False

		# Mouse down event to start dragging
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size

			# Check that the coordinates are within the tile area
			if x < Constants.ROWS and y < Constants.COLS:
				clicked = True  # Start dragging
				drag_value = world_data[y][x]  # Store the current value when first clicked

				if pygame.mouse.get_pressed()[0] == 1:
					drag_value = world_data[y][x] + 1  # Prepare to increment the value
					if drag_value > options:
						drag_value = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					drag_value -= 1
					if drag_value<0:
						drag_value = options

		# Mouse up event to stop dragging
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False  # Stop dragging

		# Keydown event to detect up and down key presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1

			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	# While the mouse button is held down, update the tiles
	if clicked:
		pos = pygame.mouse.get_pos()
		x = pos[0] // tile_size
		y = pos[1] // tile_size

		# Check that the coordinates are within the tile area
		if x < len(world_data[0]) and y < len(world_data):
			# Set the dragged value for the tile
			world_data[y][x] = drag_value

	#update game display window
	pygame.display.update()

pygame.quit()

