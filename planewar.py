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
hero_hp = 3
score = 0
# 统计战斗数据
defeat_count = 0  # 击败敌机数
# damage_count = 0  # 被击中次数
impact_count = 0  # 被撞击次数


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

    def shoot(self):
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

    def reset(self):
        self.__init__(self.speed)


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

            # 鼠标控制飞机移动
            if event.type == pygame.MOUSEMOTION:
                # print('鼠标移动')
                pos = pygame.mouse.get_pos()
                # prin t(pos)
                # 隐藏鼠标指针
                # 这个隐藏鼠标指针效果更好
                pygame.mouse.set_visible(False)
                # 这个鼠标指针隐藏效果差一点
                # hide_mouse_sorsor()
                # win32api.SetCursor(None)
                # 鼠标位置绑定飞机位置(鼠标跟踪效果)
                hero.rect.y = pos[1]
                hero.rect.x = pos[0]
                # 当英雄飞机血量小于等于零，显示鼠标指针
                if hero_hp <= 0:
                    pygame.mouse.set_visible(True)
        peng = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
        for enemy in peng.keys():
            bomb = Bomb()
            bomb.rect = enemy.rect
            bomb_group.add(bomb)
            score += 1000
            defeat_count += 1


        hero_peng = pygame.sprite.groupcollide(hero_group, enemy_group, False, True)
        for hero in hero_peng.keys():
            bomb = Bomb()
            bomb.rect = hero.rect
            bomb_group.add(bomb)

        # 获取按键列表
            key_pressed = pygame.key.get_pressed()
            if running:
                # 游戏结束按空格键
                if key_pressed[pygame.K_SPACE]:
                    # 游戏重新开始
                    player_hp = 3
                    for enemy in enemy_group:
                        enemy.reset()
                    score = 0
                    hero.reset()
                    running = False
                    bg_music.play(-1)
        # 敌机和英雄飞机
        # for enemy in enemy_group:
        #     pass
        if hero_peng:
            # enemy.bomb.set_used(enemy.rect.x, enemy.rect.y)
            impact_count += 1
            score += 1000
            ###########################################################################
            # 减少玩家的血量
            hero_hp -= 1
        # 如果玩家血量减少到零
        elif hero_hp == 0:
            hero.reset()
            hero_hp = 3
            # 游戏状态设置为False
            running = True
            # pygame.mixer.music.stop()
            pygame.mixer.stop()
            defeat_count = 0
            # damage_count = 0
            impact_count = 0
            score = 0
        for group in [bg_group, bullet_group, hero_group, enemy_group, bomb_group]:
            group.update()
            group.draw(screen)

            # 使用 SimHei 字体，并设置 16 号大小
            font = pygame.font.Font('D://pythonfiles/pythonProject/planewar/score/fonts/SimHei.ttf', 16)
            # text = f"击毁数:{defeat_count} 被击中:{damage_count} 被撞击:{impact_count}"
            text = f"击中敌机数:{defeat_count}  被撞击:{impact_count}"
            # 文字内容、抗锯齿、颜色
            text = font.render(text, True, (255, 255, 255))
            # 绘制文本内容
            screen.blit(text, (180, 20))
            # 创建字体
            font = pygame.font.Font('score/fonts/SimHei.ttf', 20)
            # 设置位置
            score_text = font.render('分数: %s ' % score, True, (255, 255, 255))
            # 绘制文字
            screen.blit(score_text, (15, 15))
            for i in range(hero_hp):
                image = pygame.transform.scale(hero.image, (hero.rect.width/2, hero.rect.height/2))
                screen.blit(image, (10 + i * (image.get_width() + 5), height - image.get_width() - 10))
        pygame.display.flip()
