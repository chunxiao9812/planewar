import random
import sys
import pygame
from config import *
from pygame import mixer

width = WIDTH
height = HEIGHT
# 初始化pygame
pygame.init()
pygame.mixer.init()
# 设置Pygame的声道数量，这里设置为12声道
mixer.set_num_channels(12)
CREAT_ENEMY = pygame.USEREVENT
pygame.mixer.music.load('score/sound/game_music.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.HWSURFACE)
pygame.display.set_caption('飞机大战 编者:海天飞歌')
clock = pygame.time.Clock()
pygame.time.set_timer(CREAT_ENEMY, MILLIS)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # index = random.randint(1, 16)
        self.image = pygame.image.load('score/background/background-1.jpg').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.y += 1
        if self.rect.top >= height:
            bg1.rect.y = 0
        if self.rect.top == 0:
            bg2.rect.y = -height
        if self.rect.y > height:
            self.kill()


class Hero(pygame.sprite.Sprite):
    def __init__(self, speed):
        global height, width
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('score/plane/me1-3.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width *= 0.7
        self.rect.height *= 0.7
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.rect.x = width / 2 - self.rect.width / 2
        self.rect.y = height - self.rect.height - 30
        self.speed = speed
        self.fps = 0
        # self.frame_index = 0

    def shoot(self):
        # self.frame_index += 1
        # if self.frame_index < self.fps:
        #     # return
        #     self.frame_index = 0
        bullet1 = Bullet(0, 6)
        bullet1.rect.centerx = self.rect.centerx
        bullet1.rect.bottom = self.rect.top + bullet1.rect.height / 2

        bullet2 = Bullet(1, 6)
        bullet2.rect.centerx = self.rect.centerx - 25
        bullet2.rect.bottom = self.rect.top + bullet2.rect.height / 2

        bullet3 = Bullet(-1, 6)
        bullet3.rect.centerx = self.rect.centerx + 26
        bullet3.rect.bottom = self.rect.top + bullet3.rect.height / 2
        bullet_group.add(bullet1, bullet2, bullet3)

        bullet_sound = pygame.mixer.Sound('score/sound/get_bomb.wav')
        bullet_sound.set_volume(0.2)
        bullet_sound.play()

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            if self.fps == 0:
                self.shoot()
            self.fps += 1
            if self.fps > 10:
                self.fps = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

        if self.fps == 0:
            self.shoot()
        self.fps += 1
        if self.fps > 10:
            self.fps = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('score/bullet/bullet-13.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy

    def update(self, *args):
        self.rect.y -= self.speedy
        self.rect.x -= self.speedx
        if self.rect.y < -30:
            self.kill()
        # print(self.rect.y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        # index = random.randint(1, 16)
        # self.image = pygame.image.load('score/enemy/enemy%s-1.png' % index).convert_alpha()
        self.image = pygame.image.load('score/enemy/enemy3-1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = -self.rect.height
        # print(self.rect.x, self.rect.y)
        self.speed = random.randint(3, 10)

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.kill()
        # print(self.rect.y)


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        index = random.randint(1, 16)
        self.images = [pygame.image.load('score/bomb/bomb-' + str(i) + '.png') for i in range(1, 7)]
        # self.speed = random.randint(3, 10)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.bomb_fps = 0

        bomb_sound = pygame.mixer.Sound('score/sound/use-bomb.wav')
        bomb_sound.set_volume(0.2)
        bomb_sound.play()

    def update(self, *args):
        if self.image_index < 5:
            self.bomb_fps += 1
            if self.bomb_fps % 4 == 0:
                self.image_index += 1
                self.image = self.images[self.image_index]
        else:
            self.kill()


hero = Hero(5)
bg1 = Background()
bg2 = Background()
bg2.rect.y = -bg2.rect.height

hero_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
hero_group.add(hero)
bg_group.add(bg1, bg2)

running = True
while True:
    if running:
        clock.tick(60)
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type == CREAT_ENEMY:
            enemy_group.add(Enemy(random.randint(3, 10)))
        peng = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
        for enemy in peng.keys():
            bomb = Bomb()
            bomb.rect = enemy.rect
            bomb_group.add(bomb)
        # hero_peng = pygame.sprite.groupcollide(enemy_group, hero_group, True, True)
        # for hero in hero_peng.keys():
        #     bomb = Bomb()
        #     bomb.rect = hero.rect
        #     bomb_group.add(bomb)
        for group in [bg_group, bullet_group, hero_group, enemy_group, bomb_group]:
            group.update()
            group.draw(screen)
        pygame.display.flip()
