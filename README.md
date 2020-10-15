# NEAT plays Flappy Bird, Chrome Dinosaur and Car Racing

In this repository there are 3 different programs that run the genetic algorithm called NEAT (NeuroEvolution of Augmenting Topologies) using the neat-python package.

### Requirements
```
    pip install neat
    pip install graphviz
    pip install matplotlib
    pip install numpy
    pip install pygame
```

&nbsp;

## Flappy Bird
I started by watching this [video](https://www.youtube.com/watch?v=OGHA-elMrxI), I took his code from this [repository](https://github.com/techwithtim/NEAT-Flappy-Bird) and I spent most of the time making small changes and reading the [neat-python docs](https://neat-python.readthedocs.io/en/latest/) to understand the algorithm better.

&nbsp;

## Chrome Dinosaur
I was inspired by this [video](https://www.youtube.com/watch?v=sB_IGstiWlc&t=220s), so I build the chrome dinosaur game from scratch using pygame, and then implemented NEAT to play it.
The images were taken from this [repository](https://github.com/Code-Bullet/Google-Chrome-Dino-Game-AI).      
The game is far from perfect (it misses some components and the jump doesn't work that well), however the really important part was to implement NEAT in the game.

I used 4 inputs: 
- the distance between the player and the obstacle
- the height of the player
- the height of the obstacle
- the width of the obstacle

And 1 output: jump or don't jump

&nbsp;

## Racing Cars
I saw another example of NEAT in this [video](https://www.youtube.com/watch?v=2o-jMhXmmxA&t=11s), and I wanted to try it. So I got the code for the game from this github [repository](https://github.com/monokim/framework_tutorial/tree/master/neat), and I made some changes to see how it performed:
-   I draw 2 new (awful) maps, and adapted the game and the algorithm to deal with them
-   Added to the inputs of the neural network the speed of the car
-   Increased the number of hidden layers by one (however most of the times it made the algorithm perform worse)
-   Changed the activation function from tanh to a list of three functions (gauss, tanh, clamped) choosen randomly with a 50% probability after every generation
