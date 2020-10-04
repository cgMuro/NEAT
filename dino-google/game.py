import pygame
import os
import random
import neat


pygame.font.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
STAT_FONT = pygame.font.SysFont("Arial", 50)
END_FONT = pygame.font.SysFont("Arial", 70)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('No Connection Dino')


# Images
DINO_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dino0000.png")))
DINO_RUNNING_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinorun0000.png")), (70, 70)),
           pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinorun0001.png")), (70, 70))]
DINO_JUMPING_IMG = pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinoJump0000.png"))
DINO_DUCKING_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinoduck0000.png")), (70, 70)),
           pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "images/Dino", "dinoduck0001.png")), (70, 70))]

CACTUS_IMGS = [
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusSmall0000.png")),
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusSmallMany0000.png")),
    pygame.image.load(os.path.join(os.getcwd(), "images/Cactus", "cactusBig0000.png"))
]

BIRD = [pygame.image.load(os.path.join(os.getcwd(), "images/Bird", "berd.png")),
        pygame.image.load(os.path.join(os.getcwd(), "images/Bird", "berd2.png"))]

BASE_IMG = pygame.image.load(os.path.join(os.getcwd(), "images/Others", "track.png"))

GENERATIONS = 0
DRAW_LINES = True


# ------- DINO -------
class Dino:
    def __init__(self):
        self.x = 15
        self.y = 320
        self.height = DINO_IMG.get_height()
        self.width = DINO_IMG.get_width()
        self.tick_count = 0   # Passing of time 

    def jump(self):

        if self.y == 320:
            self.y -= 150

        gravity = 3
        if self.y < 320:
            self.y += gravity
            gravity += 5


    def draw(self):
        self.tick_count += 1

        if self.tick_count == 0:
            SCREEN.blit(DINO_IMG, (self.x, self.y))
        elif self.tick_count % 15 == 0:
            SCREEN.blit(DINO_RUNNING_IMG[0], (self.x, self.y))
        else:
            SCREEN.blit(DINO_RUNNING_IMG[1], (self.x, self.y))


# ------- CACTUS -------
class Cactus:

    def __init__(self):
        self.IMG = random.choice(CACTUS_IMGS)
        self.x = SCREEN_WIDTH
        self.y = 275 if CACTUS_IMGS.index(self.IMG) == 2 else 300
        self.width = self.IMG.get_width()
        self.height = self.IMG.get_height()
        self.VEL = 5
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self):
        SCREEN.blit(self.IMG, (self.x, self.y))

    def collision(self, dino):

        if self.y == (dino.y + dino.height):
            return True

        if self.x == dino.x and (dino.y + dino.height) - self.y >= 0:
            return True

        # If no collision
        return False


# ------- BASE -------
class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()

    def __init__(self):
        self.y = 350
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL 
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        SCREEN.blit(BASE_IMG, (self.x1, self.y))
        SCREEN.blit(BASE_IMG, (self.x2, self.y))


# ------- DRAW WINDOW -------
def draw_window(dinos, cacti, base, score, gen, cactus_idx):
    if gen == 0:
        gen = 1

    base.draw()

    for cactus in cacti:
        cactus.draw()

    for dino in dinos:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(SCREEN, (255,0,0), (dino.x + dino.width/2, dino.y + dino.height/2), (cacti[cactus_idx].x + cacti[cactus_idx].width/2, cacti[cactus_idx].y), 5)
                # pygame.draw.line(SCREEN, (255,0,0), (dino.x + dino.width/2, dino.y + dino.height/2), (cacti[cactus_idx].x + cacti[cactus_idx].width/2, cacti[cactus_idx].height), 5)
            except:
                pass
        # draw bird
        dino.draw()

    # score
    score_label = STAT_FONT.render("Score: " + str(score),1,(0,0,0))
    SCREEN.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Generation: " + str(gen-1),1,(0,0,0))
    SCREEN.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(dinos)),1,(0,0,0))
    SCREEN.blit(score_label, (10, 50))

    pygame.display.update()





# ------- Running Game -------


def eval_genomes(genomes, config):
    global GENERATIONS
    GENERATIONS += 1

    nets = []
    dinos = []
    ge = []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dino())
        ge.append(genome)
    
    base = Base()
    cacti = [Cactus()]
    score = 0

    clock  = pygame.time.Clock()

    run = True


    while run and len(dinos) > 0:
        # Set FFPs
        clock.tick(60)

        SCREEN.fill((255, 255, 255))

        # Check if game has ended
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                break


        # determine whether to use the first or second pipe on the screen for neural network input
        cactus_idx = 0
        if len(dinos) > 0:
            if len(cacti) > 1 and dinos[0].x > cacti[0].x:  
                cactus_idx = 1 



        for idx, dino in enumerate(dinos):
            ge[idx].fitness += 0.1

            output = nets[idx].activate(((dino.y - dino.height), abs(dino.x + dino.width - cacti[cactus_idx].x), (cacti[cactus_idx].y - cacti[cactus_idx].height), cacti[cactus_idx].width))
        
            if output[0] > 0.5:
                dino.jump()
        
        base.move()

        remove_cacti = []
        add_cactus = False

        for cactus in cacti:
            cactus.move()
            
            for idx, dino in enumerate(dinos):
                if cactus.collision(dino):
                    ge[idx].fitness -= 1
                    nets.pop(idx)
                    ge.pop(idx)
                    dinos.pop(idx)
                    
            if cactus.x + cactus.width < 0:
                remove_cacti.append(cactus)

            if not cactus.passed and cactus.x < dino.x:
                cactus.passed = True
                add_cactus = True

        if add_cactus:
            score += 1
            for g in ge:
                g.fitness += 3
            cacti.append(Cactus())
        
        for r in remove_cacti:
            cacti.remove(r)

        draw_window(dinos, cacti, base, score, GENERATIONS, cactus_idx)
        
        
def run(config_file):
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    print(f'\nBest genome:\n{winner}')


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)