from random import randint
from pygame import *
font.init()
mixer.init()

clock = time.Clock()
run = True
win_width = 800
win_height = 500
mode = 'menu'
lost = 0
fire_time = 30
res_time = 180
res_text = None
points = 0

class Button(sprite.Sprite):
    def __init__(self,y,x,width,height,color,text):
        super().__init__()
        self.image = Rect(y,x,width,height)
        self.img = Surface((width, height))
        self.rect = self.img.get_rect()
        self.text = font.SysFont('arial', 24).render(text, True, (0,0,0))
        self.rect.y = y
        self.rect.x = x
        self.color = color
    def fill(self):
        draw.rect(main_win, self.color,self.image)
    def update(self):
        main_win.blit(self.image, (self.x, self.y))
    def txt_render(self):
        main_win.blit(self.text,(self.rect.y +50, self.rect.x + 15))
    def outline(self, size):
        draw.rect(main_win, (0,0,0), self.image, size)
    def collidepoint(self, y, x):
        return self.image.collidepoint(y,x)

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (int(win_width/10), int(win_width/10)))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def update(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))
class Hero(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 710:
            self.rect.x += self.speed
    def fire(self):
        global fire_time
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and fire_time <= 0:
            bullet = Bullet('bullet.png', self.rect.centerx - 11, self.rect.top, 10)
            #bullet.reduct()
            bullets.add(bullet)
            fire_time = 10

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = randint(-100,0)
            self.rect.x = randint(int(win_width/10), int(win_width*0.9))
            self.speed = randint(1,2)
            lost += 1

class Bullet(sprite.Sprite):
    def __init__(self, img, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (int(win_width/30), int(win_width/30)))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

main_win = display.set_mode((win_width, win_height))
display.set_caption('Space Shooter')
bg = transform.scale(image.load('galaxy.jpg'), (win_width,win_height))

#sprites
spaceShip = Hero('rocket.png',int(win_width/2), int(win_height - win_width/9), 7)
win = font.SysFont('arial', 100).render('You Win', True, (0,255,0))
lose = font.SysFont('arial', 100).render('You Lose', True, (255,0,0))
pointsText = font.SysFont('arial', 25).render('Points:', True, (255,255,255))
lostText = font.SysFont('arial', 25).render('Lost:' + str(lost), True, (255,255,255))
enemies = sprite.Group()
for i in range(4):
    enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,2))
    enemies.add(enemy)
buttonStart = Button(300,100,200,90 ,(255,255,0), 'START')
buttonExit = Button(300,250,200,90,(255,255,0), ' EXIT')
bullets = sprite.Group()

mixer.music.load('space.ogg')
mixer.music.play()

while run:
    fire_time -= 1
    main_win.blit(bg,(0,0))
    pointsText = font.SysFont('arial', 25).render('Points:' + str(points), True, (255,255,255))
    main_win.blit(pointsText,(int(win_width/70),int(win_width/70)))
    lostText = font.SysFont('arial', 25).render('Lost:' + str(lost), True, (255,255,255))
    main_win.blit(lostText,(int(win_width/70),int(win_width/15)))

    if mode == 'menu':
        main_win.blit(bg, (0,0))
        buttonStart.fill()
        buttonStart.outline(3)
        buttonStart.txt_render()
        buttonExit.fill()
        buttonExit.outline(3)
        buttonExit.txt_render()
    
    elif mode == 'game':
        spaceShip.move()
        spaceShip.update()
        spaceShip.fire()
        enemies.update()
        enemies.draw(main_win)
        bullets.update()
        bullets.draw(main_win)
        if lost > 2:
            mode = 'EndGame'
            res_text = lose
        sprites_list = sprite.spritecollide(spaceShip,enemies, False)
        if len(sprites_list) > 0:
            mode = 'EndGame'
            res_text = lose
        sprites_list = sprite.groupcollide(enemies,bullets, True, True)
        if len(sprites_list) > 0:
            for i in range(len(sprites_list)):
                enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,2))
                enemies.add(enemy)
                points += 1
        if points > 111:
            mode = 'EndGame'
            res_text = win

    elif mode == 'EndGame':
        res_time -= 1
        main_win.blit(res_text,(100,100))
        if res_time <= 0:
            mode = 'menu'

           


    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            y, x = e.pos
            if buttonStart.collidepoint(y, x):
                mode = 'game'
                res_time = 180
                lost = 0
                points = 0
                enemies = sprite.Group()
                for i in range(4):
                    enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,2))
                    enemies.add(enemy)
                    spaceShip.rect.x = int(win_width/2)
                for b in bullets:
                    b.kill()
            if buttonExit.collidepoint(y, x):
                run = False

    display.update()
    clock.tick(60)
            

