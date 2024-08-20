import pygame

class Paddle:

    def __init__(self, posx, posy, color, win_h):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.win_h = win_h
        self.paddle = pygame.rect.Rect((self.posx,self.posy,20,100))
        
    def increment_posy(self, y):
        if 0 < (self.posy + y) < self.win_h - 50:
            self.posy = self.posy + y
        else:
            print("window overflow")

    def draw(self, surface):
        self.paddle = pygame.rect.Rect((self.posx,self.posy,20,100))
        pygame.draw.rect(surface, (self.color), self.paddle)

    def get_coords(self):
        return (self.posx,self.posy)
    
    
