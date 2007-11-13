#pygene
from pygene.gene import OrBitGene
from pygene.gamete import Gamete
from pygene.organism import Organism, MendelOrganism
from pygene.population import Population

import random

import pprint

#pygame
import pygame, math, sys 
from pygame.locals import * 

import pgu.gui as pgui

gridsize = 16


class PatternGrid(object):
    ''' PatternGrid '''
    
    def __init__(self,screen, gridsize=16):
        ''' __init__ create some attributes '''
        
        self.__screen = screen
        
        self.__gridsize = gridsize
        self.__cell_width = screen.get_width() / gridsize
        self.__cell_height = screen.get_height() / gridsize
        
        # create a block size dependant on screen and gridsize
        self.__block = pygame.Surface((self.__cell_width,self.__cell_height))
        self.__block.fill(( random.random()*255,random.random()*255,random.random()*255))
        
    def render(self,grid = None):
        ''' render the grid onto the screen '''
        
        # check that grid is not None
        if not grid:
            return
        
        
       
        #TODO instead of rendering own grid render one that is passed in!
        
        # fill screen with black
        self.__screen.fill((0,0,0))
        
        # iterate through the grid
        for col in xrange(self.__gridsize):
            #pprint.pprint(len(grid[col]))
            for row in xrange(self.__gridsize):
                
                if grid[col][row] == '1':
                    # draw red block onto white background
                    self.__screen.blit(self.__block, (row*self.__cell_width,col*self.__cell_height) )
                    self.__screen.blit(self.__block, (self.__screen.get_width() - row * self.__cell_width, col*self.__cell_height) )
        pygame.display.flip() 



def newPattern(prob=0.5):
    ''' creates a new pattern grid '''
    grid = [[None for num in xrange(gridsize)] for x in xrange(gridsize)]
    for col in xrange(gridsize):
        for row in xrange(gridsize):
            if random.random() > prob:
                grid[col][row] = '1'
            else:
                grid[col][row] = '0'
    return grid


def genomeString(grid=None):
    ''' creates a new genome string and returns it '''
    if grid == None:
        grid = newPattern()
        
    genome = []
        
    for col in xrange(len(grid)):
        for row in xrange(len(grid)):
            genome.append(grid[col][row])
    return "".join(genome)

#---------------------------------------------------------------------------
#pygene 

class PatternGene(OrBitGene):
    mutProb = 0.1
    
    def __repr__(self):
        print self.value
        return str(self.value)


# create a genome string
gs = genomeString()

# dict to hold the genome
genome = {}

# for each of the 1/0 values in the string create a PatternGene
for i in range(len(gs)):
    genome[str(i)] = PatternGene
    
class PatternOrganism(MendelOrganism):
    genome = genome
    
    def __repr__(self):
        ''' represent an PatternOrganism as a string '''
        chars = []
        for i in xrange(self.numgenes):
            chars.append(str(self[i]))
        return ''.join(chars)
        
    
    def getGrid(self):
        grid = []
        temp = []
        count = 0
        for i in xrange(self.numgenes):
            temp.append(str(self[i]))
            count += 1
            
            if count >= gridsize:
                grid.append(temp)
                temp = []
                count = 0

                temp.append(str(self[i]))
                count += 1
        
        return grid
    
    def fitness(self):
        '''the user will be the "fitness function" but still need to override'''
        return 0.0


class PatternPopulation(Population):
    
    initPopulation = 6
    species = PatternOrganism
    
    childCull = 6
    
    childCount = 6
    
    mutants = 0.25
    


def main():
    

    #main screen
    screen = pygame.display.set_mode((750, 640)) 
    
    subscreens = {}
    
    clock = pygame.time.Clock() 

    
    #update the y position of the subscreens
    y = 1

    #create 7-sub screens
    for i in range(6):
        # TODO add key;reference to a dict
        s = screen.subsurface((10,y,200,100))
        
        subscreens[i] = PatternGrid(s)
        y += 105

    gen = 0
    
   
    pop = PatternPopulation()


    while True:
        clock.tick(1)
        #b = pop.getRandom()
        
        
        #iterate through the population
        for i in xrange(len(pop)):
            #TODO: instead of printing it out using pygame to draw on screen
            org = pop[i]
            #print org
            s = subscreens[i]
            s.render(org.getGrid())
            
        # TODO: handle pygame events   
        for event in pygame.event.get(): 
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit(0)     # quit the game
                if event.key == K_SPACE:
                    print "generation %s: " % gen
                    gen += 1
                    pop.gen()


if __name__ == '__main__':
    main()

