import pygame
pygame.init()

class Button:
    def __init__(self, pos, button_font, base_colour, hovering_colour, input_text, image, x_start, y_start, x_end, y_end):
        if image is not None:
            self.image = pygame.image.load(image)
        else:
            self.image = pygame.image.load("assets/Play_Rect.png")
        
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.button_font = button_font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.input_text = input_text
        self.text = self.button_font.render(self.input_text, True, self.base_colour)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

    def text_update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)        
        screen.blit(self.text, self.text_rect)
        
    def checkforinput(self, position):
        if position[0] in range(self.x_start, self.x_end) and position[1] in range(self.y_start, self.y_end):
            return True
        else:
            return False
        
    def changecolour(self, position):
        if position[0] in range(self.x_start, self.x_end) and position[1] in range(self.y_start, self.y_end):
            self.text = self.button_font.render(self.input_text, True, self.hovering_colour)
        else:
            self.text = self.button_font.render(self.input_text, True, self.base_colour)