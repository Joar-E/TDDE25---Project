import pygame

class Button():
    def __init__(self, width, height, center_x, center_y):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)
        self.clicked = False
    
    def draw(self, surface, button_color, text, font, text_color):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, button_color, self.rect)

        textobject = font.render(text, 1, text_color)
        textrect = textobject.get_rect()
        textrect.center = self.rect.center
        
        surface.blit(textobject, textrect)
        return action