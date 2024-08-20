import pygame
import time
import sys
from Paddle import Paddle
from Game import *
import neat
import os
import pickle

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)


def eval_genomes(genomes, config):
    #Training genomes against genomes

    width, height = 900, 600


    for i, (genome_id1, genome1) in enumerate(genomes): # genomes is a  lsit of tuples
        if i == len(genomes) -1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:    
            if genome2.fitness == None:
                genome2.fitness = 0
            print("------------------------------------------------------")
            game = Game(width, height, BLACK, BLACK, 20000)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-9")
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True)) # outputting where the algorithm is at
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1)) #Saves a acheckpoint after every 1 generation allwoing the restarting of the network from differing points

    winner = p.run(eval_genomes, 1) # calcualting fitness
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f) # Save python object

def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = Game(900, 600, BLACK, BLACK, 120)
    game.ai_vs_player(winner, config)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    print("Welcome!,what would you like to run: \n 1. Human  vs Computer \n 2. Train AI")
    if input("Choice:") == "1":
        test_ai(config)
    else:
        run_neat(config)

