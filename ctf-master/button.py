import pygame

class Button():
    def __init__(self, width, height, center_x, center_y, button_color, button_hover_color):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)
        self.clicked = False
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.current_color = button_color
        

    def click(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.current_color = self.button_hover_color
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.current_color = self.button_color

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action

    def draw(self, surface, text, font, text_color):

        pygame.draw.rect(surface, self.current_color, self.rect, border_radius = 10)

        textobject = font.render(text, 1, text_color)
        textrect = textobject.get_rect()
        textrect.center = self.rect.center
        
        surface.blit(textobject, textrect)
    
    def write_text(surface, text, font, text_color, c_x, c_y):
        textobject = font.render(text, 1, text_color)
        textrect = textobject.get_rect()
        textrect.center = (c_x, c_y)
        
        surface.blit(textobject, textrect)