# collision.py
import all_sprites
from Constants import fire_wall
from Tiles import Tiles
import pygame
import Constants
import explosion
from explosion import Explosion
from fire_wall import Firewall


def get_tile_list():
    return Tiles().get_tile_list()
#monster collision
def check_collision_with_tiles_y(rect):

    """
    Check if the given rect collides with any tiles in the tile list.
    Returns True if a collision is detected, False otherwise.
    """
    up_rect = rect.move(0, 1)
    down_rect = rect.move(0, -1)

    for tile in get_tile_list():
        if up_rect.colliderect(tile['img_rect']) or down_rect.colliderect(tile['img_rect']):

            return True
    return False

def check_collision_with_tiles_x(rect):

    """
    Check if the given rect collides with any tiles in the tile list.
    Returns True if a collision is detected, False otherwise.
    """
    right_rect = rect.move(1, 0)  # Move 1 pixel to the right
    left_rect = rect.move(-1, 0)  # Move 1 pixel to the left

    for tile in get_tile_list():
        if right_rect.colliderect(tile['img_rect']) or left_rect.colliderect(tile['img_rect']):
            return True
    return False

#check monster horizontal
def check_horizontal_collision(rect, direction):
    """
    Check for horizontal collisions to the left or right of the rect based on the direction.
    Returns True if a collision is detected, False otherwise.
    """
    if direction > 0:  # Moving right
        check_pos = rect.right + 1
    else:  # Moving left
        check_pos = rect.left - 1

    for tile in get_tile_list():
        if tile['img_rect'].collidepoint(check_pos, rect.centery):
            return True  # Collision detected

    return False  # No collision detected

#monster dead tile check
def check_tile_below_after_monster_dead(rect):
    """
    Check if there is a tile directly below the given rect.
    Returns the tile rect if a tile exists below, otherwise None.
    """
    rect_below = rect.copy()
    rect_below.y += 1  # Move the rect down by 1 pixel to check below

    for tile in get_tile_list():
        if tile['img_rect'].colliderect(rect_below):  # Check if the tile collides with the rect below
            return True # Return the tile's rect if a tile is detected below

    return False  # No tile below


#monster collision
def check_tile_below(rect, direction,dead):
    """
    Check if there is a tile below the given rect in the direction it's moving.
    Returns True if the rect is at the edge of a tile, False otherwise.
    """
    force = 0
    if dead:
        force = 5
    if direction > 0:  # Moving right
        check_pos = rect.right + 1 + force  # Check just to the right of the bottom middle

    else:  # Moving left
        check_pos = rect.left - 1 - force # Check just to the left of the bottom middle

    rect.y += 1  # Move rect down by 1 pixel to check for tile below
    for tile in get_tile_list():
        if tile['img_rect'].collidepoint(check_pos, rect.midbottom[1]):
            rect.y -= 1  # Reset the rect position
            return False
    rect.y -= 1  # Reset the rect position
    return True


#player collision X
def handle_player_horizontal_collision(rect, dx):
    """
    Handles horizontal collisions by adjusting the player's position.
    Returns the adjusted dx (horizontal velocity).
    """

    rect.x += dx
    check_distance = 1

    # Create rects that extend slightly to the left and right of the player's rect
    left_rect = rect.move(-check_distance, 0)  # Rect shifted to the left
    right_rect = rect.move(check_distance, 0)  # Rect shifted to the right
    collision_left = False
    collision_right = False

    for tile in get_tile_list():
        if rect.colliderect(tile['img_rect']):
            if dx > 0:  # Moving right
                rect.right = tile['img_rect'].left
            elif dx < 0:  # Moving left
                rect.left = tile['img_rect'].right
            dx = 0  # Stop movement after collision

        if left_rect.colliderect(tile['img_rect']):
            collision_left = True
        # Check for adjacency on the right
        if right_rect.colliderect(tile['img_rect']):
            collision_right = True

    horizontal = collision_left or collision_right
    return dx,horizontal


def check_collision(rect, dx, dy):
    """
    Simulates moving the player by dx, dy and checks for collisions.
    Returns True if collision is detected, False otherwise.
    """
    future_rect = rect.copy()  # Copy the current rect
    future_rect.x += dx  # Apply horizontal knockback
    future_rect.y += dy  # Apply vertical knockback

    for tile in get_tile_list():  # Check collision with all tiles
        if future_rect.colliderect(tile['img_rect']):
            return True  # Collision detected

    return False  # No collision detected


#check if dead monster triggers stone collapse
def check_monster_dead_falling_on_tile(monster):


    rect_below = monster.rect.copy()
    rect_below.y += 1  # Move the rect down by 1 pixel to check below

    for tile in get_tile_list():
        if tile['img_rect'].colliderect(rect_below):  # Check if the tile collides with the rect below
            if tile['tile_type']==8 and monster.falling:
                if tile['is_tile_collapsing'] is None:  # tile['is_tile_collapsing'] is the timestamp
                    tile['is_tile_collapsing'] = pygame.time.get_ticks()  # Set the timestamp when the player steps on the tile


#player y collision
def handle_player_vertical_collision(rect, dy):
    """
    Handles vertical collisions by adjusting the player's position.
    Returns the adjusted dy (vertical velocity) and whether the player is grounded.
    """

    rect.y += dy
    grounded = False

    # Check if player is still on the ground when dy == 0 (not falling or jumping)
    if dy == 0:
        rect.y += 1  # Move the rect slightly down to see if it's still colliding
        for tile in get_tile_list():

            if rect.colliderect(tile['img_rect']) and rect.bottom == tile['img_rect'].top + 1:
                if tile['tile_type']==8:
                    if tile['is_tile_collapsing'] is None:  # tile['is_tile_collapsing'] is the timestamp
                        tile['is_tile_collapsing'] = pygame.time.get_ticks()  # Set the timestamp when the player steps on the tile
                grounded = True

            if tile['is_tile_collapsing']:

                Tiles().change_tile_image(tile)



        rect.y -= 1  # Move rect back to original position


    else:
        for tile in get_tile_list():
            if rect.colliderect(tile['img_rect']):
                if dy > 0:  # Moving down
                    rect.bottom = tile['img_rect'].top
                    dy = 0
                    grounded = True  # Player has landed on the ground
                    break
                elif dy < 0:  # Moving up
                    rect.top = tile['img_rect'].bottom
                    dy = 0
                    break



    return dy, grounded



def check_dead_player_collision_with_tiles(rect):

    for tile in get_tile_list():
        if rect.colliderect(tile['img_rect']):

            rect.bottom = tile['img_rect'].top # Stop the falling by adjusting the bottom of the rect
            break
    return rect

#player monster collision
def check_player_monster_collision(player, monster_group):

    for monster in monster_group:
        monster.player_collison = False

    inflation = (-10, +50) if not player.is_attacking else (-150, 50)

    # Inflate the player's rect
    inflated_player_rect = player.rect.inflate(*inflation)
    # Create a custom collision check function
    def is_colliding(p_rect, monster):
        return p_rect.colliderect(monster.rect)

    # Get the list of colliding monsters (including dead ones for flexibility)
    collision = [monster for monster in monster_group if is_colliding(inflated_player_rect, monster)]

    #if player is defending
    for monster in collision:
        if player.defend:
            if player.direction == 1 and player.rect.x < monster.rect.x or player.direction == -1 and player.rect.x > monster.rect.x:
                monster.direction*=-1
                return True

    #make sure the player is attacking in the right direction
    for monster in collision:
        if player.is_attacking:
            if player.direction == 1 and player.rect.x > monster.rect.x or player.direction == -1 and player.rect.x < monster.rect.x:
                return True


    #check in the player is attacking and attacking once
    if collision and player.is_attacking and player.attack_once :
        for monster in collision:
            # Handle hit logic for each monster
            if player.is_attacking:
                if (player.direction == 1 and player.rect.centerx < monster.rect.centerx) or \
                        (player.direction == -1 and player.rect.centerx > monster.rect.centerx):
                    if player.rect.top <= monster.rect.bottom and player.rect.bottom >= monster.rect.top:
                        attack_hitbox = player.get_attack_hitbox()
                        if attack_hitbox.colliderect(monster.rect):
                            monster.on_hit(player.regular_attack,player.direction)
        player.attack_once = False
        return False

    #while the attacking animation is showing he is invulnerable
    if collision and player.is_attacking:
        return False

    #if he was hit
    elif collision:
        for monster in collision:
            if not monster.dead_flag:
                player.damage_taken()
                monster.player_collison = True


    return False

#player hitting a statue

def check_player_hit_statue_collision(player):


    #make sure the player is attacking in the right direction
    for statue in all_sprites.get_sprite_group('stone_statue_group'):

        if player.is_attacking and player.attack_once:
            if (player.direction == 1 and player.rect.centerx < statue.rect.centerx) or \
                    (player.direction == -1 and player.rect.centerx > statue.rect.centerx):
                mid =((player.rect.top + player.rect.bottom) // 2)

                if statue.rect.top+15 <= mid <= statue.rect.bottom-15:

                    attack_hitbox = player.get_attack_hitbox()
                    if attack_hitbox.colliderect(statue.rect) and not statue.invulnerable:
                        if statue.on_hit(player.regular_attack):
                            return statue
                        player.attack_once = False


def check_fireball_player_collision(player, fireball_group,explosion_group):
    for fireball in fireball_group:
        shrink_amount_x = player.rect.width // 2  # Shrink the width by 1/4 on each side
        shrink_amount_y = player.rect.height // 4  # Shrink the height by 1/4 on each side

        reduced_player_rect = player.rect.inflate(-shrink_amount_x, -shrink_amount_y)

        if reduced_player_rect.colliderect(fireball.rect):


            # Determine the side of impact
            fireball_center = fireball.rect.center
            player_center = player.rect.center

            dx = fireball_center[0] - player_center[0]
            dy = fireball_center[1] - player_center[1]

            if abs(dx) > abs(dy):  # More horizontal impact
                if dx > 0:  # Impact from the right
                    if dy-20 > 0:
                        impact_side = 'bottom-right'
                    elif dy+25 < 0:
                        impact_side = 'top-right'
                    else:
                        impact_side = 'right'
                else:  # Impact from the left
                    if dy -20> 0:
                        impact_side = 'bottom-left'
                    elif dy+25 < 0:
                        impact_side = 'top-left'
                    else:
                        impact_side = 'left'
            else:  # More vertical impact
                if dy > 0:  # Impact from below
                    if dx -10> 0:
                        impact_side = 'bottom-right'
                    elif dx+10 < 0:
                        impact_side = 'bottom-left'
                    else:
                        impact_side = 'bottom'
                else:  # Impact from above
                    if dx -10> 0:
                        impact_side = 'top-right'
                    elif dx +10< 0:
                        impact_side = 'top-left'
                    else:
                        impact_side = 'top'


            player.knockback(impact_side,4)

            if not (player.defend and ((player.direction == 1 and player_center[0]+10 < fireball_center[0]) or
                                  (player.direction == -1 and player_center[0]-10 > fireball_center[0]))):
                player.damage_taken()

            # # Assuming you have a method to handle player damage
            # # Create explosion object at the calculated position
            boom = explosion.Explosion(fireball.rect.centerx, fireball.rect.centery)  # Pass direction for custom effects
            explosion_group.add(boom)
            # # Optionally, remove the fireball and apply damage
            fireball.kill()





import math


def check_tile_fireball_collision(fireball_group):
    for tile in get_tile_list():
        tile_center_x = tile['img_rect'].centerx
        tile_center_y = tile['img_rect'].centery

        for fireball in fireball_group:
            if tile['img_rect'].colliderect(fireball.rect):
                # Fireball center
                fireball_center_x = fireball.rect.centerx
                fireball_center_y = fireball.rect.centery

                # Calculate difference between the fireball and the tile center
                dx = fireball_center_x - tile_center_x
                dy = fireball_center_y - tile_center_y

                # Determine the movement direction based on dx and dy
                angle_radians = math.atan2(dy, dx)

                # Convert radians to degrees for easier interpretation
                angle_degrees = math.degrees(angle_radians)


                # Threshold to determine if movement is more horizontal or vertical
                threshold = 0.1  # You can adjust this value

                if abs(dx) > abs(dy) * (1 + threshold):  # Horizontal movement
                    if dx > 0:
                        direction = "right"
                    else:
                        direction = "left"
                elif abs(dy) > abs(dx) * (1 + threshold):  # Vertical movement
                    if dy > 0:
                        direction = "down"
                    else:
                        direction = "up"
                else:
                    # Fireball is moving diagonally or close to equal, decide based on the angle
                    if -45 <= angle_degrees < 45:
                        direction = "right"
                    elif 45 <= angle_degrees < 135:
                        direction = "down"
                    elif 135 <= angle_degrees or angle_degrees < -135:
                        direction = "left"
                    else:
                        direction = "up"


                if direction == 'right':  # Fireball moving right

                    fire_wall_init = Firewall(tile['img_rect'].right, tile_center_y, 5000, 30,-90)  # Right side
                elif direction == 'down':  # Fireball moving down

                    fire_wall_init = Firewall(tile_center_x, tile['img_rect'].bottom, 5000,30, 180)  # Bottom side
                elif direction == 'left':  # Fireball moving left

                    fire_wall_init = Firewall(tile['img_rect'].left - 25, tile_center_y, 5000, 30,90)  # Left side
                elif direction == 'up':  # Fireball moving up

                    fire_wall_init = Firewall(tile_center_x, tile['img_rect'].top - 25, 5000,30, 0)  # Top side

                # Add the explosion and firewall
                explosion = Explosion(fireball_center_x, fireball_center_y)
                all_sprites.get_sprite_group('explosion_group').add(explosion)
                fireball.kill()
                all_sprites.get_sprite_group('firewall_group').add(fire_wall_init)

                # Add the explosion and firewall
                explosion = Explosion(fireball_center_x, fireball_center_y)
                all_sprites.get_sprite_group('explosion_group').add(explosion)
                fireball.kill()
                all_sprites.get_sprite_group('firewall_group').add(fire_wall_init)


def check_player_firewall_collision(player,firewall_group):
    for wall in firewall_group:

        shrink_amount_x = wall.rect.width - 20  # Shrink the width by 1/2 on each side
        shrink_amount_y = wall.rect.height -40

        reduced_wall_rect = wall.rect.inflate(-shrink_amount_x,shrink_amount_y)

        reduced_wall_rect.y += 8

        #pygame.draw.rect(Constants.screen, (255, 255, 255), reduced_wall_rect, 2)
        if reduced_wall_rect.colliderect(player.rect):
            player.damage_taken()
            return

def check_player_hit_flying_demon(player):

    #check in the player is attacking and attacking once
    for demon in all_sprites.get_sprite_group('flying_demon_group'):
        if player.rect.colliderect(demon.rect):
            if player.is_attacking and player.attack_once and demon.behavior_state == 'idle' and not demon.invulnerable:
                    # Handle hit logic for each monster
                        if (player.direction == 1 and player.rect.centerx < demon.rect.centerx) or \
                                (player.direction == -1 and player.rect.centerx > demon.rect.centerx):
                            if player.rect.top <= demon.rect.bottom and player.rect.bottom >= demon.rect.top:
                                attack_hitbox = player.get_attack_hitbox(50)
                                if attack_hitbox.colliderect(demon.rect):
                                    demon.on_hit(4,player.direction)
                                    player.attack_once= False
            elif not player.is_attacking and (demon.is_swooping or demon.is_circling):
                player.damage_taken()



def check_player_hit_fireboss(player):

    for fire_boss in all_sprites.get_sprite_group('demon_boss_group'):
            if player.is_attacking and player.attack_once and fire_boss.current_mode == 'idle' and not fire_boss.invulnerable:
                    # Handle hit logic for each monster
                    if player.rect.colliderect(fire_boss.rect):
                        if (player.direction == 1 and player.rect.centerx < fire_boss.rect.centerx) or \
                                (player.direction == -1 and player.rect.centerx > fire_boss.rect.centerx):
                            if player.rect.top <= fire_boss.rect.bottom and player.rect.bottom >= fire_boss.rect.top:
                                    fire_boss.on_hit(1)
                                    player.attack_once= False

def check_player_fireboss_collision(rect):
    for fire_boss in all_sprites.get_sprite_group('demon_boss_group'):
        if fire_boss.current_mode != 'flaming_demon':
            continue

        # Calculate the dimensions of the reduced boss rect
        shrink_amount_x = -5  # Shrinking by 5
        shrink_amount_y = -50  # Shrinking by 50

        # Create a new rect for the boss
        reduced_boss_rect = fire_boss.rect.inflate(shrink_amount_x, shrink_amount_y)

        # Check collision
        if reduced_boss_rect.colliderect(rect):
            return True

    return False


def check_player_strike_crumbling_wall(rect,direction):

    shrink_amount_x = rect.width -5
    shrink_amount_y = rect.height // 1.5

    increased_player_rect = rect.inflate(shrink_amount_x, -shrink_amount_y)

    for tile in get_tile_list():

        if tile['tile_type']==8 and tile['img_rect'].colliderect(increased_player_rect):
            if (direction==1 and rect.x < tile['img_rect'].x or  direction==-1 and rect.x > tile['img_rect'].x):
                if tile['is_tile_collapsing'] is None:  # tile['is_tile_collapsing'] is the timestamp
                    tile['is_tile_collapsing'] = pygame.time.get_ticks()


#player spike collision
def check_player_spike_collision(player, spike_group):


    return pygame.sprite.spritecollide(player, spike_group, False)

#player icicle collision
def check_player_icicle_collision(player, icicle_group):


    for ice in icicle_group:
        if player.rect.colliderect(ice.rect):
            if ice.falling:
                ice.kill()
            return True
    return False

#player exit collision
def check_player_exit_collision(player, exit_group):

    return pygame.sprite.spritecollide(player, exit_group, False)

#player exit collision
def check_player_closed_gate_collision(player, closed_gate):

    return pygame.sprite.spritecollide(player, closed_gate, False)

#player heart collision
def check_player_heart_collision(player, heart_group):


    collided_hearts =  pygame.sprite.spritecollide(player, heart_group, True)

    for heart in collided_hearts:
        return (heart.tile_x,heart.tile_y)



def check_player_rare_blue_gem_collision(player, rare_blue_gem):

    collided_gems = pygame.sprite.spritecollide(player, rare_blue_gem, True)

    for gem in collided_gems:
        return (gem.tile_x, gem.tile_y)


def check_tile_torch_collision(torch_group):
    for torch in torch_group:


        for tile in get_tile_list():
            if tile['img_rect'].colliderect(torch.rect):
                print(f"Collision detected: Torch at {torch.rect} and Tile at {tile['img_rect']}")

                # Handle horizontal collisions (if no vertical collision)
                if torch.rect.right > tile['img_rect'].left and torch.rect.left < tile['img_rect'].left:
                    # Collision on the left side of the tile
                    torch.rect.right = tile['img_rect'].left  # Snap to the left side of the tile
                    torch.dx = -abs(torch.dx)  # Reverse horizontal direction (bounce left)
                    print("Horizontal collision on left side.")
                    break  # Exit after handling one collision

                elif torch.rect.left < tile['img_rect'].right and torch.rect.right > tile['img_rect'].right:
                    # Collision on the right side of the tile
                    torch.rect.left = tile['img_rect'].right  # Snap to the right side of the tile
                    torch.dx = abs(torch.dx)  # Reverse horizontal direction (bounce right)
                    print("Horizontal collision on right side.")
                    break  # Exit after handling one collision


