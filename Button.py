import pygame.mouse

import Constants


class Button():
    def __init__(self,x,y,image,width=300,height=100):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.name = None
        self.clicked = False
        self.selected = False  # New attribute to track selection



    def draw(self):
        # Optionally draw a highlight if selected
        if self.selected:
            # Create a highlight effect (like a border or change color)
            highlight_rect = self.rect.inflate(10, 10)  # Create a larger rectangle for the highlight
            pygame.draw.rect(Constants.screen, (255, 255, 255), highlight_rect, 2)  # Yellow highlight
        Constants.screen.blit(self.image, self.rect)

    def button_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if the left mouse button is pressed and it wasn't previously clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True  # Set clicked flag to True to prevent further immediate clicks
                action = True  # Trigger the action once when clicked

        # Reset the clicked flag when the mouse button is released

        self.clicked = False  # Reset clicked flag to allow future clicks

        return action

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)