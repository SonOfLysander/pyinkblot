#!/usr/bin/env python2.4

#pygene
from pygene.gene import OrBitGene
from pygene.gamete import Gamete
from pygene.organism import Organism, MendelOrganism
from pygene.population import Population

import random
import os
import glob

# pprint is very good to print out list,dicts for debug purposses
import pprint

#pygame imports
import pygame, math, sys 
from pygame.locals import * 

#import pgu.gui as pgui

# global variable to control the gridsize
gridsize = 12

__author__ = "Bulkan Evcimen"

class PatternGrid(object):
    ''' PatternGrid '''
    
    def __init__(self,screen,gridsize,color=None):
        ''' __init__ create some attributes '''
        
        self.__screen = screen
        
        self.__gridsize = gridsize
        self.__cell_width = screen.get_width() / gridsize
        self.__cell_height = screen.get_height() / gridsize
        
        # create a block size dependant on screen and gridsize
        self.__block = pygame.Surface((self.__cell_width,self.__cell_height))
        if color == None:
            self.__color = ( random.random()*255,random.random()*255,random.random()*255)
        else:
            self.__color = color
        self.__block.fill(color)

    def getScreen(self):
        return self.__screen

    def clear(self):
        self.__screen.fill((0,0,0))
        
    def render(self,grid = None):
        ''' render the grid onto the screen '''
        
        # check that grid is not None
        if not grid:
            return
        
        
        # fill screen with black
        self.__screen.fill((0,0,0))

        #print "render | gridsize-->%d" %self.__gridsize

        # iterate through the grid
        for col in xrange(gridsize):
            for row in xrange(gridsize):

                if grid[col][row] == '0':
                    # draw red block onto white background
                    self.__screen.blit(self.__block, (row*self.__cell_width,col*self.__cell_height) )
                    self.__screen.blit(self.__block, (self.__screen.get_width() - (row * self.__cell_width)-self.__cell_width, col*self.__cell_height) )


#---------------------------------------------------------------------------
#pygene 

def newPattern(prob=0.5):
    ''' creates a new pattern grid '''
    grid = [[None for num in xrange(gridsize)] for x in xrange(gridsize)]

    half = gridsize/2 

    for col in xrange(half):
        for row in xrange(gridsize):
            if random.random() >= prob:
                grid[col][row] = '0'
                grid[half+col][row] = '0'
            else:
                grid[col][row] = '1'
                grid[half+col][row] = '1'
    return grid


def genomeString(grid=None):
    ''' creates a new genome string and returns it '''
    if grid == None:
        grid = newPattern()
        
    #pprint.pprint(grid)
    genome = []
        
    for col in xrange(len(grid)):
        for row in xrange(len(grid)):
            genome.append(grid[col][row])
    return "".join(genome)

class PatternGene(OrBitGene):
    mutProb = 0.1
    
    def __repr__(self):
        return str(self.value)


# create a genome string
gs = genomeString()

#print "gs|length --> %d" %len(gs)

# dict to hold the genome
genome = {}

# for each of the 1/0 values in the string create a PatternGene
for i in xrange(len(gs)):
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
        ''' returns the grid representation of the organism '''
        grid = []
        temp = []
        count = 0
        #print "getGrid|num of genes-->%d" %self.numgenes
        for i in xrange(self.numgenes):
            temp.append(str(self[i]))
            count += 1
            
            if count >= gridsize:
                grid.append(temp)
                #print '\ttemp-->%d' %len(temp)
                temp = []

                count = 0

        #print len(grid)
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
    

def selectOrg(newSelected,sPatterns=None, pop=None):
    #if selected == newSelected:
    #    print "%d \t %d " %(selected,newSelected)
    #    return

    org = pop[newSelected]

    if len(sPatterns) == 0:
        sPatterns.append(org)
        print "Organism %d selected" %(newSelected+1)
    else:
        for o in sPatterns:
            #print type(o),id(o),id(org)
            if str(o) == str(org):
                print "Organism %d already selected!" %(newSelected+1)
                return
        sPatterns.append(org)
    #    pprint.pprint(sPatterns)
    #pprint.pprint(sPatterns)

def save(Surface):
    ''' Save the Surface as a PNG to the images folder '''
    try:
        os.chdir('images')
    except OSError:
        os.mkdir('images')
        os.chdir('images')
    globret = glob.glob('*.png')
    count = 1
    while 1:
        if str(count)+".png" not in globret:
            break
        else:
            count += 1
    print "saving %s" %(str(count)+".png")
    pygame.image.save(Surface, str(count) + '.png')
    os.chdir('..')

def main():
    #main screen
    screen = pygame.display.set_mode((800, 650)) 
    
    subscreens = {}
    
    # control FPS
    clock = pygame.time.Clock() 

    
    #update the y position of the subsurface
    y = 1


    # list of colours
    colors = ( (155,127,223),(60,150,50),(20,60,20),(30,40,50),(100,100,100),(125,50,5),(169,69,69) )

    #create 6-sub surface
    for i in range(6):
        # TODO add key;reference to a dict
        s = screen.subsurface((1,y,110,100))
        
        subscreens[i] = PatternGrid(s,gridsize,colors[i])
        
        # increment the y co-ordinate
        y += 105

    # generation counter
    gen = 0
    
    # this subsurface will be used 
    mainscreen= PatternGrid(screen.subsurface((150,1,600,550)),gridsize,colors[-1])
    
   
    pop = PatternPopulation()

    # fixed the flicker, but probably not pygame way!
    render = True

    #selected index
    selected = -1

    selectedPatterns = []

    while True:
        clock.tick(30)
        
        # do we need draw stuff? Also this uses up less CPU
        if render:
        
            #iterate through the population
            for i in xrange(len(pop)):
                org = pop[i]
                #print org
                s = subscreens[i]
                s.render(org.getGrid())

            pygame.display.flip() 
                
            render = False
            
        # handle pygame events   
        for event in pygame.event.get(): 
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                # quit the game
                if event.key == K_ESCAPE: sys.exit(0)
                
                # go to next Generation
                if event.key == K_SPACE:

                    # check if we have things that are selected
                    if selectedPatterns:
                        
                        # create an empty population
                        pop = PatternPopulation(init=0)

                        for org in selectedPatterns:
                            pop.add(org)

                        #print 'moreOrg --> %d\nselectedPatterns --> %d' %(moreOrg,len(selectedPatterns))

                        # TODO: fix the harcoded organism count
                        moreOrg =  6-len(selectedPatterns)
                        #print 'moreOrg --> %d' %moreOrg

                        # do we need to add more organism's?
                        if moreOrg > 0:
                            for i in xrange(moreOrg):
                                pop.add(PatternOrganism())

                        # reset some variables
                        selectedPatterns = []
                        selected = -1
                        gen = 0
                        pop.gen()
                    else:
                        gen += 1
                        print "generation %s: " % gen
                        pop.gen()
                    
                    mainscreen.clear()
                    # render the screen
                    render = True
                
                # handle the display of the selected patterns
                if event.key == K_1:
                    mainscreen.render(pop[0].getGrid())
                    render = True
                    selectOrg(0,selectedPatterns,pop)
                    selected = 0

                if event.key == K_2:
                    mainscreen.render(pop[1].getGrid())
                    render = True
                    selectOrg(1,selectedPatterns,pop)
                    selected = 1

                if event.key == K_3:
                    mainscreen.render(pop[2].getGrid())
                    render = True
                    selectOrg(2,selectedPatterns,pop)
                    selected = 2

                if event.key == K_4:
                    mainscreen.render(pop[3].getGrid())
                    render = True
                    selectOrg(3,selectedPatterns,pop)
                    selected = 3

                if event.key == K_5:
                    mainscreen.render(pop[4].getGrid())
                    render = True
                    selectOrg(4,selectedPatterns,pop)
                    selected = 4

                if event.key == K_6:
                    mainscreen.render(pop[5].getGrid())
                    render = True
                    selectOrg(5,selectedPatterns,pop)
                    selected = 5


                # select
                if event.key == K_s:
                    save(mainscreen.getScreen())
        #pygame.display.flip()


if __name__ == '__main__':
    main()

