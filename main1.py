from pygame import *
from typing import Any
from random import randint
from time import time as timer

win = display.set_mode((700,500))
display.set_caption('v2')


mixer.init()
mixer.music.load('gg.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.mp3')

damage = mixer.Sound('lego-breaking.mp3')
sound = mixer.Sound("lego-breaking.mp3")
finish = mixer.Sound('podbrosili-nebolshuyu-svyazku-klyuchey.mp3')
font.init()
font1 = font.Font(None, 70)
wik = font1.render('YOU WIN',True, (255,255,255))
lose = font1.render('YOU LOSE',True, (255,255,255))
font2 = font.Font(None, 40)

game = True
class GameSprite(sprite.Sprite):
    def __init__(self , p_img , play_x , play_y ,p_spe, p_s_x , p_s_y ):
        super().__init__()
        self.image = transform.scale(image.load(p_img) , (p_s_x , p_s_y ))
        self.speed = p_spe
        self.rect = self.image.get_rect()
        self.rect.x = play_x
        self.rect.y = play_y
    def reset(self):
        win.blit(self.image,(self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        global last_time
        global real_time
        global num_fire
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 440:
            self.rect.y += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if key_pressed[K_SPACE]:
            if num_fire < 5 and real_time == False:
                num_fire += 1
                fire_sound.play()
                self.fire()
            if num_fire >= 5 and real_time == False:
                last_time = timer()
                real_time = True
    def fire(self):
        bullet = Bullet('pyla.png', self.rect.x, self.rect.y, 20, 120, 100)
        bullets.add(bullet)

class Enemy1(GameSprite):
    direct = 'left'
    def update(self):
        if self.rect.x >= 600:
            self.direct = 'left'
        if self.rect.x <= 400:
            self.direct = 'right'

        if self.direct == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50,700-50)
            



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y ,wall_w, wall_h):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.wall_w = wall_w
        self.wall_h = wall_h
        self.image = Surface((self.wall_w, self.wall_h))
        self.image.fill((color1,color2,color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

        
clock = time.Clock()

bg = GameSprite('xruchowka.jpg', 0, 0, 0, 700, 500)
hero = Player('boms.png', 0, 300, 3, 80 , 80)
enemy1 = Enemy1('oxrana.png', 600, 80, 3, 100 , 100)
enemys = sprite.Group()
bullets = sprite.Group()
for i in range(1, 8):
    enemy = Enemy('oxrana.png', randint(50,700-50),10,1,80,80)
    enemys.add(enemy)
victory = GameSprite('key.png', 550, 0, 0, 50, 50)
startg = timer()

last_time = 0
num_fire = 0
real_time = False


wall1 = wall(255,255,255,400,0,10,200)
while game:
    bg.reset()

    for e in event.get():
        if e.type == QUIT:
            game = False

    keys_pressed = key.get_pressed()
    if keys_pressed[K_q]:
        sound.play()
    
    collide = sprite.groupcollide(enemys, bullets, True, True)
    if collide:
        damage.play()
    for c in collide:
        enemy = Enemy('oxrana.png', randint(50,700-50),10,1,80,80)
        enemys.add(enemy)

    victory.update()
    enemy1.update()
    enemys.draw(win)
    bullets.draw(win)
    hero.update()
    hero.reset()
    if real_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                ammo_net = font2.render('Reload',1,(255,0,0))
                win.blit(ammo_net,(260, 460))
            else:
                num_fire = 0
                real_time = False
                
    enemys.update()
    bullets.update()
    enemy1.reset()
    victory.reset()
    wall1.draw_wall()


    if sprite.collide_rect(hero, victory):
        win.blit(wik, (200, 200))
        finish.play()
    if sprite.collide_rect(hero, enemy1) or sprite.collide_rect(hero, wall1):
        win.blit(lose, (200, 200))
        damage.play()
        hero.rect.x = 80
        hero.rect.y = 80
    if sprite.spritecollide(hero, enemys, True): 
            damage.play()
            enemy = Enemy('oxrana.png', randint(50,700-50),10,1,80,80)
            enemys.add(enemy)


    display.update()
    clock.tick(60)
