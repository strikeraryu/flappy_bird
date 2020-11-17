import random
import pygame
import neat 
pygame.init()

#load images
yellow_bird = [pygame.image.load('assets/ybird_mid.png'), pygame.image.load('assets/ybird_down.png'), pygame.image.load('assets/ybird_up.png')]
blue_bird = [pygame.image.load('assets/bbird_mid.png'), pygame.image.load('assets/bbird_down.png'), pygame.image.load('assets/bbird_up.png')]
red_bird = [pygame.image.load('assets/rbird_mid.png'), pygame.image.load('assets/rbird_down.png'), pygame.image.load('assets/rbird_up.png')]
day = pygame.image.load('assets/bg_day.png')
night = pygame.image.load('assets/bg_night.png')
base = pygame.image.load('assets/base.png')
msg = pygame.image.load('assets/tap.png')
gameover = pygame.image.load('assets/gameover.png')
pipe_bottom = pygame.image.load('assets/pipe_green.png')
digit = [pygame.image.load('assets/0.png'), pygame.image.load('assets/1.png'), pygame.image.load('assets/2.png'), pygame.image.load('assets/3.png'), pygame.image.load('assets/4.png'), pygame.image.load('assets/5.png'), pygame.image.load('assets/6.png'), pygame.image.load('assets/7.png'), pygame.image.load('assets/8.png'), pygame.image.load('assets/9.png')]

bg = random.choice([day, night])
flappy_bird = random.choice([yellow_bird, blue_bird, red_bird])
#constant value
g = 3
speed = 5
jump = -20
win_height = 800
win_width = 600
base_height = 100
pipe_width = 60
pipe_height = 500
bg = pygame.transform.scale(bg, (win_width, win_height))
base = pygame.transform.scale(base, (win_width, base_height))
pipe_bottom = pygame.transform.scale(pipe_bottom, (pipe_width, pipe_height))
pipe_top = pygame.transform.flip(pipe_bottom, False, True)
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("FLAPPY BIRD")
clock = pygame.time.Clock()
#define class for things with gravity( i.e bird )
class obj_gravity(object):
    def __init__(self, x, y):
        self.allow = True
        self.x = x
        self.y = y
        self.vel =  0
        self.tick = 0
        self.dir = 0
        self.angle = 359
    def draw(self,win):
        self.tick += 1
        if self.vel<0:
            self.dir = -1
            self.angle += 2
        elif self.vel > 0:
            self.dir = 1
        else:
            self.dir = 0
        if self.tick >= 4 :
            self.tick=0
#Draw bird
        if not self.allow:
            win.blit(pygame.transform.rotate(flappy_bird[self.dir], self.angle), (self.x, self.y))
        else:
            win.blit(pygame.transform.rotate(flappy_bird[self.dir], self.angle), (self.x, self.y))
        if self.angle > 270 and self.dir == 1:
            self.angle -= 5

        for i in range(abs(self.vel)):
            if self.y+24<win_height-base_height and self.y>0:
                self.y += self.dir
            else:
                return True
        return False         
        
class obj_moving(object):
    def __init__(self, x, y, vel):
        self.vel = vel
        self.x = x
        self.y = y
#move the base
    def move(self):
        self.x -= self.vel
        if self.x+win_width == 0:
            self.x = 0
#draw the base
            
    def draw(self, win, img):
        win.blit(img, (self.x, self.y))
        win.blit(img, (self.x+win_width, self.y))
#pipe
class Pipe(object):
    dis = win_width - 200
    gap = 130
    
    
    def __init__(self, vel):
        self.x = [win_width+100, win_width+self.dis+100]
        self.y = [ random.randrange(200, win_height-base_height - 70), random.randrange(200, win_height-base_height - 70)]
        self.vel = vel
        self.top_crd = self.y[0] - self.gap
        self.bottom_crd = self.y[0] 

    def move(self):
        self.x[0] -= self.vel
        self.x[1] -= self.vel
        if self.x[0]+pipe_width == 0:
            self.x.pop(0)
            self.y.pop(0)
            self.x.append(self.x[0]+self.dis)
            self.y.append(random.randrange(200, win_height-base_height - 70))

    def draw(self,win): 
        tmpx = 100000
        tmp = 0
        for i in range(len(self.y)):
            n_crd = self.x[i] + pipe_width
            if self.x[i] < tmpx and n_crd >= 100:
                tmpx = self.x[i]
                tmp = self.y[i]  
        self.top_crd = tmp - self.gap
        self.bottom_crd = tmp   

        top = [self.y[0]-self.gap-pipe_height, self.y[1]-self.gap-pipe_height]
        win.blit(pipe_bottom, (self.x[0], self.y[0]))
        win.blit(pipe_top, (self.x[0], top[0]))
        win.blit(pipe_bottom, (self.x[1], self.y[1]))
        win.blit(pipe_top, (self.x[1], top[1]))

    def col(self,bird):
        top = [self.y[0]-self.gap-pipe_height, self.y[1]-self.gap-pipe_height]
        t_col = collide(flappy_bird[bird.dir], pipe_top, bird.x, bird.y, self.x[0], top[0])
        b_col = collide(flappy_bird[bird.dir], pipe_bottom, bird.x, bird.y, self.x[0], self.y[0])
        if (t_col or b_col) and bird.allow:
            return True
        return False
        
#To apply grravity on object
def gravity(vel):
    return vel+g
    
def collide(img, img1, x, y, x1, y1):
    bird_mask = pygame.mask.from_surface(img)
    obj_mask = pygame.mask.from_surface(img1)
    offset = (x1-x, y1-round(y))
    col_point = bird_mask.overlap(obj_mask, offset)
    if col_point:
        return True
    return False
def score_print(win, score):
    number = []
    x = win_width - 50
    y = 50
    if score == 0:
        number.append(0)
    else:
        while score>0:
            number.append(score%10)
            score//=10
    for i in range(len(number)):
        win.blit(digit[number[i]], (x, y))
        x -= 27

def redrawgamewindow():
    gamebg.draw(win, bg)
    pipe.draw(win)
    gamebase.draw(win, base)
    for x, bird in enumerate(birds):
        if bird.draw(win) or pipe.col(bird):
             ge[x].fitness -= 1
             birds.pop(x)
             nets.pop(x)
             ge.pop(x)
        else:
            ge[x].fitness += 1

    score_print(win, score)
    pygame.display.update()


def start_test(config_path):        
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)
    print('\nBest genome:\n{!s}'.format(winner))

  
def main(genomes, config):
#main loop
    global run, score, gamebg, gamebase, pipe, birds, nets, ge
    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(obj_gravity(100, 250))
        g.fitness = 0
        ge.append(g)

    run = True
    score = 0
    gamebg = obj_moving(0, 0, 1)
    gamebase = obj_moving(0, win_height-base_height, speed)
    pipe = Pipe(speed)


    while run and len(birds) != 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for x, bird in enumerate(birds):
            output = nets[x].activate((bird.y,abs(bird.y - pipe.top_crd),abs(bird.y - pipe.bottom_crd)))
            if output[0] > 0.5 :
                bird.vel = jump
                bird.angle = 360


        pipe.move()
        gamebase.move()
        gamebg.move()
        for x, bird in enumerate(birds):
            if bird.x == pipe.x[0]:
                score += 1
                ge[x].fitness += 5
        for bird in birds:
            bird.vel = gravity(bird.vel)
        
        redrawgamewindow()

if __name__ == "__main__":      
    config_path = 'config/config-feedforward.txt'
    start_test(config_path)