import pygame, neat, os, random, sys, pickle
import math

pygame.init()

#Global constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font("freesansbold.ttf", 20)

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())
        self.vel = self.JUMP_VEL
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
    
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
    
    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.vel * 4
            self.vel -= 0.8
        if self.vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.vel = self.JUMP_VEL
    
    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height),2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x+54, self.rect.y+12), obstacle.rect.center, 2)

class Obstacle:
    def __init__(self,image, num_of_cacti):
        self.image = image
        self.type = num_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, num_of_cacti):
        super().__init__(image, num_of_cacti)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, num_of_cacti):
        super().__init__(image, num_of_cacti)
        self.rect.y = 300

def remove(index):
    dinos.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, dinos, obstacles, ge, nets
    clock = pygame.time.Clock()
    points = 0

    dinos = []
    obstacles = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    for genome_id, genome in genomes:
        dinos.append(Dino())
        ge.append(genome)
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

    def score():
        global points, game_speed
        points += 1
        for i, dino in enumerate(ge):
            ge[i].fitness += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f"Score: {str(points)}", True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def stats():
        global dinos, game_speed, ge
        text_1 = FONT.render(f"Dinosaurs Alive: {str(len(dinos))}", True, (0, 0, 0))
        text_3 = FONT.render(f"Generations: {str(p.generation+1)}", True,(0,0,0))
        text_2 = FONT.render(f"Game Speed: {str(game_speed)}", True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_3, (50, 480))
        SCREEN.blit(text_2, (50, 510))

    #this function is used to move the background
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        if x_pos_bg + image_width >= SCREEN_WIDTH:
            x_pos_bg = 0
        x_pos_bg -= game_speed


    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        SCREEN.fill("white")
        for dinosaur in dinos:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        if len(dinos) == 0:
            break

        if len(obstacles) == 0:
            rand = random.randint(0, 1)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinos):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -=1
                    remove(i)
                    
        # sends AI the coords of dino and obstacle
        for i, dino in  enumerate(dinos):
            output = nets[i].activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacle.rect.midtop)))
            if output[0] > 0.5 and dino.rect.y == dino.Y_POS:
                dino.dino_jump = True
                dino.dino_run = False

        
        # user_input = pygame.key.get_pressed()
        # if user_input[pygame.K_SPACE]:
        #     dinos[0].dino_jump = True
        #     dinos[0].dino_run = False

        stats()
        score()
        background()
        pygame.display.update()

def run(config_path):
    global p
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)