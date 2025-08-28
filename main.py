import pygame
import random
pygame.init()

W, H = 800, 600

fps = 60

white = (255, 255, 255)

screen = pygame.display.set_mode((W, H))

pygame.display.set_caption("flappy bird") 

font = pygame.font.SysFont("Bauhaus 93", 59)
Bg = pygame.image.load("image\Bg.png")
ground_img = pygame.image.load("image\ground.png")
restart = pygame.image.load("image\Restart.png")

#game variables

ground_scroll = 0
scroll_speed = 5
flying = False
Game_over = False
pipe_gap = 120
pipe_freq = 1500
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
passed_pipe = False

#game functions

def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color,),(x, y))

def reset_game():
    pipe_group.empty()#remove the pipes
    flappy.rect.center = (110, H // 2)#bird pos
    global score, passed_pipe
    score = 0
    passed_pipe = False
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"image\Bird{i}.png")for i in range(1,4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center = (x, y))
        self.vel = 0
        self.clicked = False

        
    def update(self):
        if flying:
            self.vel = min(self.vel + 0.5, 8)
            self.rect.y += int(self.vel)
            
        if not Game_over:
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.vel =- 10
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            self.counter += 1
            if self.counter> 5:
                self.counter = 0
                self.index = (self.index +1) % len(self.images)  
            self.image = pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)



class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image\pipe.png")
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y - pipe_gap //2))
        else:
            self.rect = self.image.get_rect(topleft=(x, y + pipe_gap //2))
    def update(self):
        self.rect.x-= scroll_speed
        if self.rect.right< 0 :
            self.kill()
        





class Button():
    def __init__(self, x, y, img):
        self.image = img
        self.rect = self.image.get_rect(topleft=(x,y))
        
    def draw(self):
        pos = pygame.mouse.get_pos()#to get the CURRENT pos of the mouse
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        screen.blit(self.image,self.rect)
        return False# this means if the button hasn't been clicked
            
        

#grouping the sprites
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#objects of class Bird

flappy = Bird(100,H//2)
bird_group.add(flappy)
Restart_button = Button(W//2 - 50, H//2 - 80, restart)

Clock = pygame.time.Clock()
running = True

while running:
    Clock.tick(fps)
    screen.blit(Bg, (0, 0))
    if not Game_over and flying:
        time_now = pygame.time.get_ticks()

        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            pipe(W, H // 2 + pipe_height, -1).add(pipe_group)#this is for the bottom/lower pipe
            pipe(W, H // 2 + pipe_height, 1).add(pipe_group)#this is for the top/upper pipe
            last_pipe = time_now

        ground_scroll = (ground_scroll - scroll_speed) % 35
        pipe_group.update()
    screen.blit(ground_img, (ground_scroll, 420))      
    bird_group.update()
    bird_group.draw(screen)
    pipe_group.draw(screen)
    draw_text(str(score), font, white, W // 2, 20)
    if (pipe_group)\
        and (flappy.rect.left > pipe_group.sprites()[0].rect.left)\
        and (flappy.rect.right < pipe_group.sprites()[0].rect.right)\
        and (not passed_pipe): 
        passed_pipe = True

    if (passed_pipe and pipe_group)\
        and (flappy.rect.left > pipe_group.sprites()[0].rect.right):
        score +=1
        passed_pipe = False

    if Game_over:
        if Restart_button.draw():
            reset_game()
            Game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not Game_over:
            flying = True


    pygame.display.update()

pygame.quit()
