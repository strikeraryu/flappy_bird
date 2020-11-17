import pygame
import random
pygame.init()

game_run = True

# __GAME__  !!Flappy Bird!!
while game_run:
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
    g = 2
    speed = 4
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
        def __init__(self, x, y, vel):
            self.x = x
            self.y = y
            self.vel = vel
            self.tick = 0
            self.dir = 0
            self.angle = 359

        def draw(self,win):
            if self.vel<0:
                self.tick += 1
                self.dir = -1
                self.angle += 2
            elif self.vel > 0:
                self.dir = 1
            else:
                self.dir = 0
            if self.vel >= 4 :
                self.tick=0

            for i in range(abs(self.vel)):
                if self.y+24<win_height-base_height:
                    self.y += self.dir
                else:
                    global game
                    game = False
                    break            
#Draw bird
            if not allow:
                win.blit(pygame.transform.rotate(flappy_bird[self.dir], self.angle), (self.x, self.y))
            else:
                win.blit(pygame.transform.rotate(flappy_bird[self.dir], self.angle), (self.x, self.y))

            if self.angle > 270 and self.dir == 1:
                self.angle -= 5
            

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
    class pipe(object):
        dis = win_width - 200
        gap = 130
        
        
        def __init__(self, vel):
            self.x = [win_width+100, win_width+self.dis+100]
            self.y = [ random.randrange(200, win_height-base_height - 70), random.randrange(200, win_height-base_height - 70)]
            self.vel = vel

        def move(self):
            self.x[0] -= self.vel
            self.x[1] -= self.vel
            if self.x[0]+pipe_width == 0:
                self.x.pop(0)
                self.y.pop(0)
                self.x.append(self.x[0]+self.dis)
                self.y.append(random.randrange(200, win_height-base_height - 70))

        def draw(self,win):
            top = [self.y[0]-self.gap-pipe_height, self.y[1]-self.gap-pipe_height]

            t_col = collide(flappy_bird[bird.dir], pipe_top, bird.x, bird.y, self.x[0], top[0])
            b_col = collide(flappy_bird[bird.dir], pipe_bottom, bird.x, bird.y, self.x[0], self.y[0])

            global allow
            if (t_col or b_col) and allow:
                bird.vel = -10
                pygame.time.delay(150)
                allow = False
                
            win.blit(pipe_bottom, (self.x[0], self.y[0]))
            win.blit(pipe_top, (self.x[0], top[0]))
            win.blit(pipe_bottom, (self.x[1], self.y[1]))
            win.blit(pipe_top, (self.x[1], top[1]))

            
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
        bird.draw(win)
        score_print(win, score)
        if not start:
            win.blit(msg, (win_width/2-100 , win_height/2-200))
        if not game:
                global run
                run = False
                win.blit(gameover, (win_width/2-96 , win_height/2-200))
                pygame.display.update()
                pygame.time.delay(1500)
        pygame.display.update()
        

#main loop
    run = True
    start = False
    game = True
    allow = True
    click = False
    score = 0
    bird = obj_gravity(100, 250, 0)
    gamebg = obj_moving(0, 0, 1)
    gamebase = obj_moving(0, win_height-base_height, speed)
    pipe = pipe(speed)


    while run:
        clock.tick(30)

#To check event done in window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or click)  and bird.tick==0 and allow == True:
            bird.vel = jump
            bird.angle = 360
            start = True

        if start:
            if allow:
                pipe.move()
                gamebase.move()
                gamebg.move()
                if bird.x == pipe.x[0]:
                    score += 1
            bird.vel = gravity(bird.vel)

        redrawgamewindow()

    
