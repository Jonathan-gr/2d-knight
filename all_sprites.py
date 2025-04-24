import pygame



sprite_group_names = [
    "enemy_group", "spike_group", "icicle_group", "exit_group", "closed_gate_group",
    "heart_group", "stone_statue_group", "fireball_group", "explosion_group",
    "firewall_group", "flying_demon_group", "demon_boss_group",
    "BloodSplatter_group", "rare_gem_group","gust_group","torch_group"
]

# Create a dictionary to hold all groups
all_sprites_groups_dict = {}

# Initialize all sprite groups in a loop
def init_all_sprites(sprite_group_names):
    for group in sprite_group_names:
        all_sprites_groups_dict[group] = pygame.sprite.Group()
    return all_sprites_groups_dict


def get_sprite_group(group_name):
    return all_sprites_groups_dict[group_name]

def empty_all_sprites(all_sprites_groups):
    for sprite_group in all_sprites_groups:
        for sprite in sprite_group:
            sprite.kill()
        sprite_group.empty()

def update_all_sprites(all_sprites_groups,player_pos,player_):

    for sprite_group in all_sprites_groups:
        for sprite in sprite_group:

            if sprite.name == 'fire_boss':
                sprite.update(player_pos,player_)
            else:
                sprite.update(player_pos)


def draw_all_sprites_and_player(all_sprites_groups, surface, player):
    # Draw sprites in the specified order
    all_sprites_groups['icicle_group'].draw(surface)
    all_sprites_groups['exit_group'].draw(surface)
    all_sprites_groups['closed_gate_group'].draw(surface)

    # Draw stone statues one by one
    for statue in all_sprites_groups['stone_statue_group']:
        statue.draw(surface)

    all_sprites_groups['fireball_group'].draw(surface)


    # Draw the player
    player.draw()


    all_sprites_groups['firewall_group'].draw(surface)
    all_sprites_groups['BloodSplatter_group'].draw(surface)
    for demon_boss in all_sprites_groups['demon_boss_group']:
        if not demon_boss.blink:
            demon_boss.draw(surface)

    all_sprites_groups['gust_group'].draw(surface)
    for torch in all_sprites_groups['torch_group']:
        torch.draw()
    all_sprites_groups['explosion_group'].draw(surface)


