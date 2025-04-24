import pygame
import Constants
from Button import Button
from Constants import gems_collected



class WorldMenu():
    def __init__(self,player):
        self.font = pygame.font.Font(None, 36)  # Initialize the font
        # Create buttons for six worlds
        self.world_buttons = [
            Button(100, 100, Constants.bg_img),  # World 1
            Button(100, 220, Constants.world_2_img),  # World 2
            Button(100, 340, Constants.bg_img),  # World 3
            Button(100, 460, Constants.bg_img),  # World 4
            Button(100, 580, Constants.bg_img),  # World 5
            Button(100, 700, Constants.bg_img),  # World 6
        ]
        self.available_worlds = Constants.worlds_known  # Number of worlds available to play
        self.player = player
        self.current_world = 1


    def draw(self):
        for i, button in enumerate(self.world_buttons):
            if i < self.available_worlds:  # Draw only available world buttons
                button.draw()
                # Render the world number text
                # world_number_text = self.font.render(f"World {i + 1}", True, (255, 255, 255))  # White color
                # # Draw the world number text next to the button
                # Constants.screen.blit(world_number_text, (button.rect.x - 50, button.rect.y + 30))

                # Get the gem status for the current world

                gems_collected = sum(Constants.gems_collected[i+1].values())# +1 because world indices start from 1

                total_gems_world = Constants.gems_available[i+1]
                total_gems = sum(total_gems_world.values())
                # Draw the gem image
                gem_x = button.rect.x + 315  # Adjust position based on your layout
                gem_y = button.rect.y + 30  # Align with button
                Constants.screen.blit(Constants.rare_gem, (gem_x, gem_y))

                # Render the gem status text next to the gem image
                gem_status_text = self.font.render(f"{gems_collected}/{total_gems}", True, (255, 255,255))  # Yellow color for gems
                Constants.screen.blit(gem_status_text, (gem_x + 40, gem_y+5))  # Adjust position as needed

    def handle_clicks(self):
        for i, button in enumerate(self.world_buttons):
            if i < self.available_worlds and button.button_clicked():
                # Reset selection on all buttons before selecting the clicked one
                for b in self.world_buttons:
                    b.selected = False
                button.selected = True  # Highlight the selected button
                self.current_world = i+1

    def get_selected_world(self):
        return self.current_world

    def unlock_world(self):
        if self.available_worlds < len(self.world_buttons):
            self.available_worlds += 1  # Unlock next world
