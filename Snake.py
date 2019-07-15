from pygame.locals import *
from random import randint
import pygame
import time
import random

class Coord:
    x = 1
    y = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, other):
        return self.x == other.x and self.y == other.y;

    def equalsAny(self, others):
        for other in others:
            if (self.x == other.x and self.y == other.y):
                return True

        return False
 
class Apple:
    position = None
 
    def __init__(self, position):
        self.position = position
 
    def draw(self, surface, image, bsize):
        surface.blit(image, ((self.position.x-1)*bsize, (self.position.y-1)*bsize))
 
class Snake:
    direction = 'right'
    length = 0
    head = None
    tail = []
 
    def __init__(self, length):
       self.length = length
       self.head = Coord(length, 1)
       for i in range(1,length):
           self.tail.append(Coord(i, 1))

    def update(self):
        self.tail.insert(0, Coord(self.head.x, self.head.y));

        if self.direction == 'right':
            self.head.x += 1
        if self.direction == 'left':
            self.head.x -= 1
        if self.direction == 'up':
            self.head.y -= 1
        if self.direction == 'down':
            self.head.y += 1

        if self.head.x < 1:
            self.head.x = 20

        if self.head.y < 1:
            self.head.y = 20

        if self.head.x > 20:
            self.head.x = 1

        if self.head.y > 20:
            self.head.y = 1

        while ((len(self.tail)+1) > self.length):
            del self.tail[-1]

    def eat(self, apple):
        self.length += 1
 
    def moveRight(self):
        if self.direction != 'left':
            self.direction = 'right'
 
    def moveLeft(self):
        if self.direction != 'right':
            self.direction = 'left'
 
    def moveUp(self):
        if self.direction != 'down':
            self.direction = 'up'
 
    def moveDown(self):
        if self.direction != 'up':
            self.direction = 'down'
 
    def draw(self, surface, image, headimage, bsize):
        surface.blit(headimage, ((self.head.x-1) * bsize, (self.head.y-1) * bsize))
        for i in self.tail:
            surface.blit(image, ((i.x-1) * bsize, (i.y-1) * bsize))

class Game:
    windowWidth = 400
    windowHeight = 400
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = False
        self._display_surf = None
        self._sneak_head_surf = None
        self._snake_tail_surf = None
        self._apple_surf = None
        self.snake = Snake(3) 
        self.apple = Apple(Coord(5,5))
 
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Pygame - Snake')

        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        self._snake_tail_surf = pygame.Surface((20, 20))
        self._snake_tail_surf.fill((255, 255, 255))

        self._sneak_head_surf = pygame.Surface((20, 20))
        self._sneak_head_surf.fill((0, 255, 0))

        self._apple_surf = pygame.Surface((20, 20))
        self._apple_surf.fill((255, 0, 0))

        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if (event.key == K_RIGHT):
                self.snake.moveRight()

            if (event.key == K_LEFT):
                self.snake.moveLeft()

            if (event.key == K_UP):
                self.snake.moveUp()

            if (event.key == K_DOWN):
                self.snake.moveDown()

            if (event.key == K_ESCAPE):
                self._running = False

    def on_loop(self):
        dead = False
        ateApple = False

        self.snake.update()

        if self.apple.position.equals(self.snake.head):
            self.snake.eat(self.apple)
            self.apple.position = self.generateApplePosition()
            ateApple = True

        if (self.snake.head.equalsAny(self.snake.tail)):
            dead = True

        return ateApple, dead
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.snake.draw(self._display_surf, self._snake_tail_surf, self._sneak_head_surf, 20)
        self.apple.draw(self._display_surf, self._apple_surf, 20)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        clock = pygame.time.Clock()
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
 
            ateApple, dead = self.on_loop()
            self.on_render()

            if (dead == True):
                print('Game over')
                exit(0)
 
            clock.tick(10)
        self.on_cleanup()

    def generateApplePosition(self):
        newApplePosition = None

        while newApplePosition == None:
            newApplePosition = Coord(randint(1,20), randint(1,20))
            if (newApplePosition.equals(self.snake.head) or newApplePosition.equalsAny(self.snake.tail)):
                newApplePosition = None

        return newApplePosition
 
if __name__ == "__main__" :
    game = Game()
    game.on_execute()
