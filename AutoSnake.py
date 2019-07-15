from pygame.locals import *
from Snake import Game
import pygame
import random

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import numpy as np

LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 5000
 
if __name__ == "__main__" :
    game = Game()
    game.on_init()

    actions = [
        pygame.event.Event(pygame.KEYDOWN, {'key': K_UP}),
        pygame.event.Event(pygame.KEYDOWN, {'key': K_DOWN}),
        pygame.event.Event(pygame.KEYDOWN, {'key': K_RIGHT}),
        pygame.event.Event(pygame.KEYDOWN, {'key': K_LEFT})
    ]

    maxSteps = 300;
    clock = pygame.time.Clock()
    steps = maxSteps
    reward = 0

    while( steps > 0 ):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                exit(0)
        action = random.randrange(0, 3)
        game.on_event(actions[action])
        ateApple, dead = game.on_loop()
        #game.on_render()

        if (dead == True):
            print('Died')
            break;

        reward += 1
        if ateApple:
            reward += 100

        clock.tick(1000)
        steps -= 1

    print('Steps done:', (maxSteps-steps))
    print('Reward:', reward)

    game.on_cleanup()