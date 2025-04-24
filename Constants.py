import pygame
import os
import Button
import pickle



#init
main_menu = True
worlds_menu = False
level = 1
secret_levels = set([5])
world = 1
max_level = 9
levels_visited = set()
worlds_known = 1

player_health = 3
start_lvl_health = 3
collected_items = {}

screen_width = 1550
screen_height = 800
pygame.init()

player_start_pos_x = 50
player_start_pos_y = screen_height-250

player_start_positions = {1:[player_start_pos_x,player_start_pos_y],
                          2:[player_start_pos_x,player_start_pos_y],
                          3:[player_start_pos_x,player_start_pos_y],
                          4:[player_start_pos_x,player_start_pos_y],
                          5:[player_start_pos_x,player_start_pos_y],
                          5.5:[400,0],
                          6:[player_start_pos_x,player_start_pos_y],
                          7:[player_start_pos_x+150,300],
                          50:[440,690]}

gems_available = {1: {2:1,4:1,5:1,7:1,50:1},2: {1:1,2:1,6:2}}
gems_collected = {1: {2:0,4:0,5:0,7:0,50:0},2: {1:0,2:0,6:0}}




boss_levels = set([8,9])
screen = pygame.display.set_mode((screen_width, screen_height))
tile_size = 50

ROWS = 30
COLS = 16
img_on_ground = 0.25

CLOCK = pygame.time.Clock()
FPS = 60

GAME_OVER = 0
game_over_timer = 0
button_alpha = 0  # Start fully transparent
# Constants
FADE_IN_DURATION = 1000  # Duration of the fade-in effect in milliseconds
MAX_ALPHA = 255  # Maximum opacity (fully opaque)

PICKLE_IN = open(f"C:/Users/Tal/PycharmProjects/Hello_world/worlds/world{world}/level{level}_data", 'rb')
WORLD_DATA = pickle.load(PICKLE_IN)


#fonts
health_score_font = pygame.font.SysFont('Bauhaus 93',30)
white = (255,255,255)


bg_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/backgrounds/dark_forest.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

world_2_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/backgrounds/world2.png')
world_2_img = pygame.transform.scale(world_2_img, (screen_width, screen_height))

stone_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/tiles/stone_tile.png')
cracked_stone_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/tiles/stone.png')
cracked_stone_img_3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/tiles/stone_cracked3.png')

stone_left_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/stone_left.png')
stone_right_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/stone_right.png')
spike_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/tiles/spikes.png')
falling_stone_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/tiles/falling_stone.jpg')

stone_statue_img = pygame.image.load('images/statues/stone_statue.png')

icicle_img = pygame.image.load('images/tiles/icicle.png')

torch_img = pygame.image.load('images/torch/torch.png')
torch_throw_img = pygame.image.load('images/torch/torch_throw.png')


restart_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/restart_button.png')
play_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/play_button.png')
quit_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/quit_button.png')
game_ove_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/game_over_button.png')
back_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/back-removebg-preview.png')
worlds_button =  pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/worlds.png')
confirm_button = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/confirm.png')
restart_world_button = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/Buttons/restartworld-removebg-preview.png')

spider_img1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/spider.png')
spider_hurt= pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/spider_hurt.jpg')
spider_dead = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/spider_dead.png')
spider_attack = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/spider_attack.png')
spider_eating_1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/spider/spider_eating_corpse3__1_-removebg-preview.png')
spider_eating_2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/spider/spider_eating_corpse4__1_-removebg-preview.png')
spider_eating_3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/spider/spider_eating_corpse5__1_-removebg-preview.png')


boss_fly1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fly/fly1.png')
boss_fly2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fly/fly2.png')
boss_fly3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fly/fly3.png')
boss_arr = [boss_fly1,boss_fly2,boss_fly3]

boss_mode1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/fire_mode1-removebg-preview.png')
boss_mode2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/fire_mode2__1_-removebg-preview.png')
boss_mode3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/fire_mode3__1_-removebg-preview.png')

flaming_boss1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/real_fire1.png')
flaming_boss2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/real_fire2.png')
flaming_boss3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/fire_mode/real_fire3.png')

scream1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/scream/scream-removebg-preview.png')
scream2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/scream/scream2-removebg-preview.png')

fire_mode1_arr = [boss_mode1,boss_mode2,boss_mode3]
fire_mode2_arr = [flaming_boss1,flaming_boss2,flaming_boss3]
demon_boss_scream_arr = [scream1,scream2]

wind = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/wind/wind.png')
wind2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/demon_boss_1/wind/wind2.png')
wind_arr = [wind,boss_fly1]

gust1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/wind/gust1.png')
gust2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/wind/gust2.png')
gust3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/wind/gust3.png')
gust4 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/wind/gust4.png')
gust_arr = [gust1,gust2]

platform_x_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/platform_x.png')
platform_y_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/platform_y.png')
lava_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/lava.png')
coin_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/coin.png')

open_gate = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gates/gate2-removebg-preview.png')
closed_gate1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gates/closed_gate1-removebg-preview.png')
closed_gate2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gates/closed_gate2-removebg-preview.png')
closed_gate3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gates/closed_gate3-removebg-preview.png')


save_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/save_btn.png')
load_img = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/load_btn.png')

#projectiles
fire_ball = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/fireball.png')
fire_ball2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/fireball2.png')
fire_ball3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/fireball3.png')

fire_wall = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/fire_wall_2.png')
fire_wall2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/fire_wall_3.png')


explosion1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/explotion1-removebg-preview.png')
explosion2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/explotion2-removebg-preview.png')
explosion3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/projectiles/explotion3-removebg-preview.png')

blood_splatter1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/blood/blood1-removebg-preview.png')
blood_splatter2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/blood/blood2-removebg-preview.png')
blood_splatter3 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/blood/blood3-removebg-preview.png')
blood_splatter4 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/blood/blood4-removebg-preview.png')
blood_splatter5 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/blood/blood5-removebg-preview.png')

heart_image = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/player/rpg_elements/heart_icon.png') # Replace with the correct path to your heart image
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust the size of the heart

common_gem = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gems/common_blue_gem.png') # Replace with the correct path to your heart image
common_gem = pygame.transform.scale(common_gem, (30, 35))

rare_gem = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/gems/rare_blue_gem-removebg-preview.png') # Replace with the correct path to your heart image
rare_gem = pygame.transform.scale(rare_gem, (30, 30))

# Directory where the images are stored
image_dir = 'C:/Users/Tal/PycharmProjects/Hello_world/images/player/walk'
# List to hold the player images
player_walking_right = []
# Loop through the filenames with a common pattern
for i in range(1, 1+len([f for f in os.listdir(image_dir) if f.endswith('.png')])):
    image_path = os.path.join(image_dir, f'walk{i}.png')
    image = pygame.image.load(image_path)
    player_walking_right.append(image)


# Directory where the images are stored
image_dir = 'C:/Users/Tal/PycharmProjects/Hello_world/images/player/dead'
# List to hold the player images
player_dead = []
# Loop through the filenames with a common pattern
for i in range(1, len([f for f in os.listdir(image_dir) if f.endswith('.png')])):

    image_path = os.path.join(image_dir, f'dead{i}.png')
    image = pygame.image.load(image_path)
    player_dead.append(image)



# Directory where the images are stored
image_dir = 'C:/Users/Tal/PycharmProjects/Hello_world/images/player/hurt'
# List to hold the player images
player_hurt = []
# Loop through the filenames with a common pattern
for i in range(1, 1+len([f for f in os.listdir(image_dir) if f.endswith('.png')])):

    image_path = os.path.join(image_dir, f'hurt{i}.png')
    image = pygame.image.load(image_path)
    player_hurt.append(image)

# Directory where the images are stored
image_dir = 'C:/Users/Tal/PycharmProjects/Hello_world/images/player/jump'
# List to hold the player images
player_jump = []
# Loop through the filenames with a common pattern
for i in range(1, 1+len([f for f in os.listdir(image_dir) if f.endswith('.png')])):

    image_path = os.path.join(image_dir, f'jump{i}.png')
    image = pygame.image.load(image_path)
    player_jump.append(image)



# Directory where the images are stored
image_dir = 'C:/Users/Tal/PycharmProjects/Hello_world/images/enemies/small_demon'
# List to hold the player images
flying_demon_arr = []
# Loop through the filenames with a common pattern
for i in range(1, 1+len([f for f in os.listdir(image_dir) if f.endswith('.png')])):

    image_path = os.path.join(image_dir, f'demon{i}.png')
    image = pygame.image.load(image_path)
    flying_demon_arr.append(image)


attack_right = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/player/attack/attack1.png')
attack_right_2 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/player/attack/attack2.png')
attack_right_1 = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/player/attack/attack2-removebg-preview.png')
player_attack = [attack_right,attack_right_2,attack_right_1]



defend = pygame.image.load('C:/Users/Tal/PycharmProjects/Hello_world/images/player/defend.png')


#Buttons

restart_button_on_screen = Button.Button(screen_width//2 -325,screen_height//2,restart_button)
game_over_button_on_screen = Button.Button(screen_width//2 -300,screen_height//2-300,game_ove_button,600,200)
play_button_on_screen = Button.Button(screen_width//2 -325,screen_height//2,play_button)
quit_button_on_screen = Button.Button(screen_width//2 +50,screen_height//2,quit_button)
back_button_on_screen = Button.Button(screen_width//2 +50,screen_height//2+250,back_button)
worlds_button_on_screen = Button.Button(screen_width//2-150,screen_height//2+150,worlds_button)
confirm_button_on_screen = Button.Button(screen_width//2-250,screen_height//2+250,confirm_button)
restart_world_button_on_screen = Button.Button(screen_width//2-550,screen_height//2+250,restart_world_button)
mouse_clicked = False