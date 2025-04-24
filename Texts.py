import pygame
import Constants
def draw_health(heart_image, player_health, x, y, spacing=10):
    """
    Draws a heart image multiple times, equal to the player's health.

    heart_image: The image of the heart to be drawn.
    player_health: The current health of the player (how many hearts to draw).
    x, y: Coordinates where the first heart should be drawn.
    spacing: The space between each heart image (optional).
    """
    for i in range(player_health):
        # Draw each heart image with some spacing between them
        Constants.screen.blit(heart_image, (x + i * (heart_image.get_width() + spacing), y))

# Function to draw the rare blue gems with the "X" and the gem count
def draw_rare_blue_gems(rare_blue_gem_image, x, y, gem_count):
    # Blit the gem image
    Constants.screen.blit(rare_blue_gem_image, (x, y))

    # Set the font and size for the text
    font = pygame.font.SysFont('Arial', 24)  # You can change the font and size if desired

    # Create the text to display ("X" followed by the gem count)
    text = f"X {gem_count}"

    # Render the text with a color (white in this example)
    text_surface = font.render(text, True, (255, 255, 255))  # (255, 255, 255) is white

    # Blit the text next to the gem image
    Constants.screen.blit(text_surface, (x + rare_blue_gem_image.get_width() + 10, y))  # Adjust the x-offset as needed


