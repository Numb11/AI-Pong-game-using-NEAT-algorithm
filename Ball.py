import random, pygame

class Ball:
    def __init__ (self, surface, winheight, winwidth, color):
        self.surface = surface
        self.start_x = winwidth//2
        self.start_y = 0
        self.posx = 0
        self.posy = 0
        self.winheight = winheight
        self.winwidth = winwidth
        self.color = color

    def spawn_ball(self, player):
        self.start_y = random.randint(100, self.winheight-100)
        self.start_x = self.winwidth//2

        self.posy,self.posx = self.start_y, self.start_x

        self.generate_trajectory(player)

    def draw_ball(self):
        pygame.draw.circle(self.surface, (self.color), (self.posx,self.posy),10, 10)


    def move_ball(self):
        if self.direction == 1:
                self.posx = self.posx-2
                self.posy = (self.gradient*self.posx) + self.c
        else:
                self.posx = self.posx+2
                self.posy = (self.gradient*self.posx) + self.c

        print(self.posx,self.posy)


    def generate_trajectory(self, direction):
        self.direction = direction

        if self.direction == 1:
            self.endy = random.randint(0,self.winheight)
            self.endx = 0

        elif self.direction == 2:
            self.endy = random.randint(0,self.winheight)
            self.endx = self.winwidth




        self.gradient = ((self.endy - self.start_y)/(self.endx - self.start_x))
        self.c = (self.endy - self.gradient*self.endx)





        
    def get_ballcoords(self):
        return (self.posx,self.posy)

    def phit(self, player):
        self.start_x = self.posx
        self.start_y = self.posy
        
        if player == 1:
            self.generate_trajectory(2)
        else: 
            self.generate_trajectory(1)

    def border_collision(self, border):
        self.gradient = -1/self.gradient 
        if border == 1:
            self.posy = self.posy + 10
        elif border == 0:
            self.posy = self.posy - 10


        self.start_x = self.posx
        self.generate_trajectory(self.direction)
    def get_direction(self):
        return self.direction