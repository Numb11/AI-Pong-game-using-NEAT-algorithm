import pygame

class Counter:

    def __init__ (self, surface, winheight, winwidth):
        pygame.font.init()

        self.winheight = winheight
        self.winwidth = winwidth
        self.surface = surface

        self.p1_score = 0
        self.p2_score = 0

        self.font = pygame.font.SysFont("arial",50, True , True)
        self.text = self.font.render("00 : 00",False,(0,0,0))

    def update(self, player):


        if player == 1:
            self.p1_score = self.p1_score + 1
        else:
            self.p2_score = self.p2_score + 1

        if len(str(self.p1_score)) > 1:
            p1_text = str(self.p1_score)

        else:
            p1_text = '0' + str(self.p1_score)

        if len(str(self.p2_score)) > 1:
            p2_text = str(self.p2_score)

        else:
            p2_text = '0' + str(self.p2_score)

        self.text = self.font.render(f"{p1_text} : {p2_text}",True,(0,0,0))

    def draw(self):
        self.surface.blit(self.text, (self.winwidth//2-50, 20))

    def get_score(self):
        return (self.p1_score, self.p2_score)