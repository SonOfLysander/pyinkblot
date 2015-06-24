# PyInkblot #

Simply mirroring a random plotting of half of a grid onto the second half, you can create pictures that look 'organic' like Rorschach Inkblots.

PyInkblot uses pygene for the Genetic Algorithm backend and pygame to draw the 'organisms' onto the screen. The user selects 0 or more (up to 6) of the organisms to go into a new population, more organism's will be added until there is 6 in the new population. Then a new generation is created using this population.

**The user is the fitness function**

[Here](http://au.youtube.com/watch?v=ODhoVnY5Ygo) is a screen-capture video of the latest version in svn running. The framerate is slow but it's like that.

[Here](http://au.youtube.com/watch?v=J6g3lj-YJJA) is a screen-capture video of the initial pyinkblot, it was the initial proof-of-concept, to see if it (or i could) do what i had in mind with pygame.

## Requirements ##
  * [pygame1.8.0](http://www.pygame.org)
  * [pygene0.2.1](http://www.freenet.org.nz/python/pygene/)
  * python2.4

## Usage ##

  * You select using the keys **1-6** the pattern/organism you want to go to the next gen
  * Press the **spacebar** to go to next generation
  * After you have selected an pattern/organism you save it out as a PNG buy pressing **S**



## Screen Shots/Images ##
**This is a screenshot of the current version in svn**

![http://bulkan.googlepages.com/Picture1.png](http://bulkan.googlepages.com/Picture1.png)

**This is a image from the current version**

![http://bulkan.googlepages.com/5.png](http://bulkan.googlepages.com/5.png)

**This image is from the initial proof of concept**

![http://bulkan.googlepages.com/11.png](http://bulkan.googlepages.com/11.png)