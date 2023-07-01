import pygame, neat, os, random, sys

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


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, dinos, obstacles
    clock = pygame.time.Clock()
    points = 0

    dinos = [Dino()]
    obstacles = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f"Score: {str(points)}", True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

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
                    remove(i)

        
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE] and not dinos[0].dino_jump:
            dinos[0].dino_jump = True
            dinos[0].dino_run = False

        score()
        background()
        pygame.display.update()

main()