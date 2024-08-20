import pygame
from Paddle import *
from Ball import *
from Counter import *
import neat
import os

class Game:
    def __init__ (self, winwidth, winheight, lcolor, rcolor, fps):
        self.winwidth = winwidth
        self.winheight = winheight

        self.p1_score = 0
        self.p2_score = 0

        self.leftp = Paddle(40,250,lcolor, winheight)
        self.rightp = Paddle(860, 250, rcolor, winheight)

        self.lefthit = 0
        self.righthit = 0

        BLACK = (0,0,0)
        WHITE = (255,255,255)
        GREEN = (0,255,0)

        self.WIDTH, self.HEIGHT = winwidth,winheight
        self.gameWin = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.FPS = fps
        self.ball = Ball(self.gameWin, self.winheight, self.winwidth, GREEN)

        self.counter = Counter(self.gameWin, self.HEIGHT, self.WIDTH)


    def train_ai(self, genome1, genome2, config):
        run = True
        clock = pygame.time.Clock()
        executing = True
        last_player_lost = 2
        point_scored = True
        new_game = True

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        while executing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                
            leftpcoord = self.leftp.get_coords()
            ballcoord = self.ball.get_ballcoords()
            rightpcoord = self.rightp.get_coords()

            output1 = net1.activate((leftpcoord[1],ballcoord[1], abs(leftpcoord[0] - ballcoord[0])))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.playery_change(10)
            else:
                self.playery_change(-10)

            output2 = net2.activate((rightpcoord[1],ballcoord[1], abs(rightpcoord[0] - ballcoord[0])))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.aiy_change(10)
            else:
                self.aiy_change(-10)

        

            self.score = self.counter.get_score()

            if self.score[0] >= 1 or self.score[1] >= 1 or self.lefthit > 50:
                self.calculate_fitness(genome1, genome2)
                break



            if new_game:
                self.ball.spawn_ball(random.randint(1,2))
                new_game = False

            self.ball.move_ball()

            self.check_paddle_collision()

            point_score_stat = self.check_for_point()


            if point_score_stat:
                self.counter.update(point_score_stat)
                if point_score_stat == 1:
                    self.ball.spawn_ball(2)
                else:
                    self.ball.spawn_ball(1)

            self.check_for_border_collision()

            self.draw_game_enviro()

            pygame.display.flip()
            clock.tick(self.FPS)

    def calculate_fitness(self, genome1, genome2):
        genome1.fitness = genome1.fitness + self.lefthit
        genome2.fitness = genome2.fitness + self.righthit

    def ai_vs_player(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)



        clock = pygame.time.Clock()
        executing = True
        last_player_lost = 2
        point_scored = True
        new_game = True

        while executing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    executing = False
                    break
            
            #Moving right paddle using genome

            leftpcoord = self.leftp.get_coords()
            ballcoord = self.ball.get_ballcoords()
            rightpcoord = self.rightp.get_coords()

            
            output = net.activate((rightpcoord[1],ballcoord[1], abs(rightpcoord[0] - ballcoord[0])))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.aiy_change(10)
            else:
                self.aiy_change(-10)


            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.playery_change(-10)
    
            if keys[pygame.K_DOWN]:
                self.playery_change(10)
              

            if new_game:
                self.ball.spawn_ball(1)
                new_game = False

            self.ball.move_ball()

            self.check_paddle_collision()

            point_score_stat = self.check_for_point()

            if point_score_stat:
                self.counter.update(point_score_stat)
                if point_score_stat == 1:
                    self.ball.spawn_ball(2)
                else:
                    self.ball.spawn_ball(1)

            self.check_for_border_collision()

            self.draw_game_enviro()

            pygame.display.flip()
            clock.tick(self.FPS)



    def draw_game_enviro(self):
        self.gameWin.fill((108,147,92))
        pygame.draw.rect(self.gameWin, (255,255,255), (self.winwidth//2,0, 20, self.winheight))
        self.leftp.draw(self.gameWin)
        self.rightp.draw(self.gameWin)
        self.ball.draw_ball()
        self.counter.draw()

    def check_paddle_collision(self):
        ball_coords = self.ball.get_ballcoords()
        leftpcoords = self.leftp.get_coords()
        rightpcoords = self.rightp.get_coords()

        if (abs(ball_coords[0] - leftpcoords[0]) < 20):
            if ball_coords[1] < leftpcoords[1] and abs(ball_coords[1] - leftpcoords[1]) < 50:
                pass
            elif ball_coords[1] > leftpcoords[1] and abs(ball_coords[1] - leftpcoords[1]) < 100:
                pass

                if self.ball.get_direction() != 2:
                    self.lefthit = self.lefthit + 1
                    self.ball.phit(1)
                    return True
        

        if (abs(rightpcoords[0] - ball_coords[0]) < 20):
            if ball_coords[1] < rightpcoords[1] and abs(ball_coords[1] - rightpcoords[1]) < 50:
                pass
            elif ball_coords[1] > rightpcoords[1] and abs(ball_coords[1] - rightpcoords[1]) < 100:
                pass

                if self.ball.get_direction() != 1:
                    self.righthit = self.righthit + 1
                    self.ball.phit(2)
                    return True 


    def playery_change(self, y_change):
        self.leftp.increment_posy(y_change)

    def aiy_change(self, y_change):
        self.rightp.increment_posy(y_change)   

    def check_for_point(self):
        ball_coords = self.ball.get_ballcoords()

        if ball_coords[0] < 50:
            self.p2_score = self.p2_score +1
            return 2

        elif ball_coords[0] > self.winwidth - 50:
            self.p1_score = self.p1_score + 1

            return 1
        
    def check_for_border_collision(self):
        ball_coords = self.ball.get_ballcoords()

        if ball_coords[1] > self.winheight - 25:
            self.ball.border_collision(1)
        elif ball_coords[1] < 25:
            self.ball.border_collision(0)
        



