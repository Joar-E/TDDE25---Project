import pygame

class Button():
    def __init__(self, width, height, center_x, center_y, button_colour,
                 button_hover_colour, text, font, text_colour):
        """ Creates a rectangle with the given parameters and position """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)
        self.clicked = False
        self.button_colour = button_colour
        self.button_hover_colour = button_hover_colour
        self.current_colour = button_colour
        self.text = text
        self.font = font
        self.text_colour = text_colour
        

    def click(self):
        """ Checks if the button was clicked or not """
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.current_colour = self.button_hover_colour
            #if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicked = True
                        action = True
        else:
            self.current_colour = self.button_colour

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action

    def draw(self, surface):
        """
        Draws a button rectangle and writes the given texten 
        in the center of the rectangle
        """
        pygame.draw.rect(surface, self.current_colour, self.rect, border_radius = 10)

        textobject = self.font.render(self.text, 1, self.text_colour)
        textrect = textobject.get_rect()
        textrect.center = self.rect.center
        
        surface.blit(textobject, textrect)
    
    def write_text(surface, text, font, text_colour, c_x, c_y):
        """ Writes text at the given position"""
        textobject = font.render(text, 1, text_colour)
        textrect = textobject.get_rect()
        textrect.center = (c_x, c_y)
        
        surface.blit(textobject, textrect)