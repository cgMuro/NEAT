import pygame
import os
import random
import neat

# Pygame screen and font config
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
pygame.font.init()
STAT_FONT = pygame.font.SysFont("Arial", 50)
END_FONT = pygame.font.SysFont("Arial", 70)

# Create screen and write caption
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('No Connection Dino')


# IMAGES
# dino
DINO_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dino0000.png")))
DINO_RUNNING_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinorun0000.png")), (70, 70)),
           pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinorun0001.png")), (70, 70))]
DINO_DUCKING_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinoduck0000.png")), (70, 70)),
           pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinoduck0001.png")), (70, 70))]
# cactus
CACTUS_IMGS = [
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusSmall0000.png")),
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusSmallMany0000.png")),
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusBig0000.png"))
]
# bird
BIRD = [pygame.image.load(os.path.join(os.getcwd(), "images/Bird", "berd.png")),
        pygame.image.load(os.path.join(os.getcwd(), "images/Bird", "berd2.png"))]
# ground
BASE_IMG = pygame.image.load(os.path.join(os.getcwd(), "images/Others", "track.png"))

# Neat config for generations and red lines
GENERATIONS = 0
DRAW_LINES = True


# ------- DINO -------
class Dino:
    ''' Class that represents the dino behavior '''

    def __init__(self):
        self.x = 15     # x position
        self.y = 320    # y position
        self.height = DINO_IMG.get_height()   # Dino height
        self.width = DINO_IMG.get_width()     # Dino width
        self.tick_count = 0   # Passing of time 

    # Function that makes the dino jump
    def jump(self):
        # Allow jump only when on the ground
        if self.y == 320:
            self.y -= 150

        # Add gravity
        gravity = 3
        if self.y < 320:
            self.y += gravity
            gravity += 5

    # Function that draws the dino
    def draw(self):
        self.tick_count += 1

        if self.tick_count == 0:
            # Draw the normal dino when time is 0
            SCREEN.blit(DINO_IMG, (self.x, self.y))
        # Draw the walking dino as time passes
        elif self.tick_count % 15 == 0:
            SCREEN.blit(DINO_RUNNING_IMG[0], (self.x, self.y))
        else:
            SCREEN.blit(DINO_RUNNING_IMG[1], (self.x, self.y))


# ------- CACTUS -------
class Cactus:
    ''' Class that represents the cactus (obstacle) behavior '''

    def __init__(self):
        self.IMG = random.choice(CACTUS_IMGS)   # Choose randomly for one of the three types of cactus
        self.x = SCREEN_WIDTH   # x position
        self.y = 275 if CACTUS_IMGS.index(self.IMG) == 2 else 300   # y position based on the cactus chosen
        self.width = self.IMG.get_width()    # Cactus width
        self.height = self.IMG.get_height()  # Cactus height
        self.VEL = 5    # Cactus velocity
        self.passed = False   # Check if the dino has got through the obstacle (cactus)

    # Define the movement of the cactus over time
    def move(self):
        self.x -= self.VEL  # Move the cactus from right to left at the set velocity

    # Draw the cactus
    def draw(self):
        SCREEN.blit(self.IMG, (self.x, self.y))

    # Check if there is a collision between the dino and the obstacle (cactus)
    def collision(self, dino):
        # Check if they dino touch the cactus on the top 
        if self.y == (dino.y + dino.height):
            return True
        # Check if the dino is at the same height as the cactus and collides with it on the front
        if self.x == dino.x and (dino.y + dino.height) - self.y >= 0:
            return True

        # If no collision
        return False


# ------- BASE -------
class Base:
    ''' Class that represents the ground behavior '''

    VEL = 5  # Velocity of the ground
    WIDTH = BASE_IMG.get_width()   # Width of the ground

    def __init__(self):
        self.y = 350   # y position
        self.x1 = 0    # x1 position
        self.x2 = self.WIDTH   # x2 position

    # Make the ground move  
    def move(self):
        self.x1 -= self.VEL  # Change x1 position based on the velocity
        self.x2 -= self.VEL  # Change x2 position based on the velocity

        # Adjust for when the ground goes out of the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    # Draw the ground
    def draw(self):
        SCREEN.blit(BASE_IMG, (self.x1, self.y))
        SCREEN.blit(BASE_IMG, (self.x2, self.y))


# ------- DRAW WINDOW -------
def draw_window(dinos, cacti, base, score, gen, cactus_idx):
    if gen == 0:
        gen = 1

    # Draw the base
    base.draw()

    # Draw every cactus
    for cactus in cacti:
        cactus.draw()

    for dino in dinos:
        # Draw line from dino to cacatus, if draw lines is selected
        if DRAW_LINES:
            try:
                pygame.draw.line(SCREEN, (255,0,0), (dino.x + dino.width/2, dino.y + dino.height/2), (cacti[cactus_idx].x + cacti[cactus_idx].width/2, cacti[cactus_idx].y), 5)
            except:
                pass
        # Draw every dino
        dino.draw()

    # Draw the score on the screen
    score_label = STAT_FONT.render("Score: " + str(score),1,(0,0,0))
    SCREEN.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 15, 10))

    # Draw the number of generations on the screen
    score_label = STAT_FONT.render("Generation: " + str(gen-1),1,(0,0,0))
    SCREEN.blit(score_label, (10, 10))

    # Draw the number of dinos alive on the screen
    score_label = STAT_FONT.render("Alive: " + str(len(dinos)),1,(0,0,0))
    SCREEN.blit(score_label, (10, 50))

    pygame.display.update()


# ------- Running Game -------
def eval_genomes(genomes, config):
    global GENERATIONS
    # Increase the generation by one
    GENERATIONS += 1

    # Init networks, dinos and genomes list
    nets = []
    dinos = []
    ge = []

    # Iterate through the genomes
    for _, genome in genomes:
        genome.fitness = 0    # Init a fitness of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)   # Init a neat feed forward network 
        nets.append(net)    # Add the network to the list of networks
        dinos.append(Dino())   # Add Dino to the list of dinos
        ge.append(genome)   # Add the genome to the list of genomes
    
    # Init theground
    base = Base()
    # Init the list of obstacles
    cacti = [Cactus()]
    # Init the score
    score = 0
    # Init the clock
    clock  = pygame.time.Clock()

    # Set run to true
    run = True

    # Keep running the game as long as run is true and there are dinos
    while run and len(dinos) > 0:
        # Set FFPs
        clock.tick(60)
        # Fill the screen with white
        SCREEN.fill((255, 255, 255))

        # Check if game has ended
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                break


        # Determine which of the cactus on the screen to use for neural network input
        cactus_idx = 0
        if len(dinos) > 0:
            if len(cacti) > 1 and dinos[0].x > cacti[0].x:
                # Set the index of the cactus to use  
                cactus_idx = 1 

        # Iterate through every dino
        for idx, dino in enumerate(dinos):
            # Increase the fitness of that dino genome by 0.1
            ge[idx].fitness += 0.1
            # Get the out from the network by passing: the height of the dino, the distance between the dino and the cactus(obstacle), the height of the cactus, and the width of the cactus
            output = nets[idx].activate((
                (dino.y - dino.height), abs(dino.x + dino.width - cacti[cactus_idx].x), (cacti[cactus_idx].y - cacti[cactus_idx].height), cacti[cactus_idx].width
            ))
            # If the output is greater than 0.5 make the dino jump
            if output[0] > 0.5:
                dino.jump()
        
        # Move the ground
        base.move()

        # Init the remove cacti array
        remove_cacti = []
        # Init add cactus
        add_cactus = False

        # Iterate through every cactus
        for cactus in cacti:
            # Make the cactus move
            cactus.move()
            
            # Iterate through the dinos
            for idx, dino in enumerate(dinos):
                # If there is a collision
                if cactus.collision(dino):
                    ge[idx].fitness -= 1    # Reduce by 1 the fitness of that dino
                    nets.pop(idx)           # Remove its network from the list of networks
                    ge.pop(idx)             # Remove its genome from the list of genomes
                    dinos.pop(idx)          # Remove the dino from the list of dinos
            
            # If the cactus is out of the screen
            if cactus.x + cactus.width < 0:
                # Add it to the remove cacti list
                remove_cacti.append(cactus)

            # If the dino got through the obstacle (cactus)
            if not cactus.passed and cactus.x < dino.x:
                cactus.passed = True
                add_cactus = True

        # Generate a new cactus
        if add_cactus:
            score += 1  # Increase the score
            # Increase the fitness of every genome that has survived by 3
            for g in ge:
                g.fitness += 3
            # Add new cactus to the list of cacti
            cacti.append(Cactus())
        
        # Remove every cactus out of the screen from the list of cacti
        for r in remove_cacti:
            cacti.remove(r)

        # Call the draw window function
        draw_window(dinos, cacti, base, score, GENERATIONS, cactus_idx)
        
        
def run(config_file):
    # Set the neat configuration
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    # Create the population
    population = neat.Population(config)

    # Add a report and statistics in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Get the best genome from the population
    winner = population.run(eval_genomes, 50)

    print(f'\nBest genome:\n{winner}')


if __name__ == '__main__':
    # Get the path of the neat config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # Run the game along with neat
    run(config_path)