import pygame

class Cell:
    def __init__(self, x, y, color, size) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.start_node = False
        self.end_node = False
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
    
    def set_color(self, new_color):
        self.rect.color = new_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        
    
