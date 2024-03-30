from pygame import *
from typing import Any
from random import randint
from time import time as timer

win = display.set_mode((700,500))
display.set_caption('v3')

mixer.init()
mixer.music.load('20BlasterCluster.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.mp3')
dmg_sound = mixer.Sound('death.mp3')


font.init()
font1 = font.Font(None, 70)
lose = font1.render('YOU LOSE',True, (255,0,0))
Win = font1.render('YOU WIN',True, (0,255,0))
font2 = font.Font(None, 40)

lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self , p_img , play_x , play_y ,p_spe, p_s_x , p_s_y ):
        super().__init__()
        self.image = transform.scale(image.load(p_img), (p_s_x , p_s_y ))
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
        bullet = Bullet('pyla.png', self.rect.centerx, self.rect.top, 20, 120, 100)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50,700-50)
            lost = lost + 1
#class boss(GameSprite):
 #   def update(self):
  #      self.rect.y += self.speed


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

clock = time.Clock()

bg = GameSprite('fonv3.jpg', 0, 0, 0, 700, 500)
hero = Player('pytin.png', 0, 350, 6, 150 , 150)
enemys = sprite.Group()
bullets = sprite.Group()
for i in range(1, 8):
    enemy = Enemy('zelenski.png', randint(50,700-50),10,1,80,80)
    enemys.add(enemy)
#Boss = boss('zelenski.png', 0, 350, 1, 350 , 350)

score = 0
goal = 100000000
life = 10000000
bosshp = 10
startg = timer()

run = True
finish = False
last_time = 0
num_fire = 0
real_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    tscore = font2.render('СЧЁТ:'+str(score),True, (255,255,255))
    tlose = font2.render('ПОТЕРИ:'+str(lost),True, (255,255,255))
    tlife = font2.render('ЖИЗНИ:'+str(life),True, (255,0,0))

    collide = sprite.groupcollide(enemys, bullets, True, True)
    if collide:
        dmg_sound.play()
    for c in collide:
        score += 1
        enemy = Enemy('zelenski.png', randint(50,700-50),10,1,80,80)
        enemys.add(enemy)

    if not finish:
        bg.reset()
        win.blit(tscore,(10,10))
        win.blit(tlose,(10,40))
        win.blit(tlife,(10,70))
        enemys.draw(win)
        bullets.draw(win)
        hero.reset()
        #if score >= 10:
            #Boss.reset()
            #Boss.update()
        
        if real_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                ammo_net = font2.render('Reload',1,(255,0,0))
                win.blit(ammo_net,(260, 460))
            else:
                num_fire = 0
                real_time = False
        enemys.update()
        hero.update()
        bullets.update()
        
        #if sprite.spritecollide(Boss, bullets, True):
            #bosshp -= 1
        if sprite.spritecollide(hero, enemys, True): 
            life -= 1
            dmg_sound.play()
            enemy = Enemy('zelenski.png', randint(50,700-50),10,1,80,80)
            enemys.add(enemy)
        if score >= goal:
            finish = True
            win.blit(Win, (200, 200))
        if life <= 0:
            finish = True
            win.blit(lose, (200, 200))
        #if bosshp <= 0:
            #boss.kill()
        display.update()

    clock.tick(60)
