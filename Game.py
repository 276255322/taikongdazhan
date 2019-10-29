# coding=utf-8

import pygame
import sys
import os

vector2 = pygame.math.Vector2

from GameBackground import GameBackground
from Aircraft import Aircraft
from Meteorite import Meteorite
from UpdateParameter import UpdateParameter
from Bullet import Bullet

source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
circular_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
meteorite_group = pygame.sprite.Group()
aircraft_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
all_group = pygame.sprite.LayeredUpdates()


class Game:
    def __init__(self, title='太空陨石'):
        self.size = (480, 700)
        self.screen = pygame.display.set_mode(self.size)
        self.title = title
        self.color = (3, 6, 13)
        self.clock = pygame.time.Clock()
        self.bg = GameBackground((all_group, bg_group), self.screen, source_dir, vector2(0, 0))
        self.FPS = 60
        self.meteorites_count = 10
        self.bullets_count = 3
        self.s_bomb1 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB1.ogg"))
        self.s_bomb2 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB2.ogg"))
        self.s_bomb3 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB3.ogg"))
        self.s_bomb4 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB4.ogg"))
        self.s_bomb5 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB5.ogg"))
        self.s_bomb6 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB6.ogg"))
        self.szd1 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        self.szd2 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        self.szd3 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        pygame.mixer.music.load(os.path.join(source_dir, "m1.mp3"))

    def create_groups(self):
        a_count = len(aircraft_group.sprites())
        if a_count < 1:
            Aircraft((all_group, aircraft_group), (all_group, circular_group), self.screen, source_dir)
        m_count = len(meteorite_group.sprites())
        if m_count < self.meteorites_count:
            Meteorite((all_group, meteorite_group), (all_group, circular_group), self.screen, source_dir)

    def get_meteorite_destroy(self, mete):
        if mete.img_size[0] >= 200:
            return 16
        elif mete.img_size[0] >= 150:
            return 8
        elif mete.img_size[0] >= 100:
            return 4
        elif mete.img_size[0] >= 50:
            return 2
        return 0

    def play_bomb_sound(self, mete):
        if mete.img_size[0] >= 200:
            self.s_bomb6.play(0, 0, 0)
        elif mete.img_size[0] >= 150:
            self.s_bomb5.play(0, 0, 0)
        elif mete.img_size[0] >= 100:
            self.s_bomb4.play(0, 0, 0)
        elif mete.img_size[0] >= 50:
            self.s_bomb3.play(0, 0, 0)
        else:
            self.s_bomb2.play(0, 0, 0)

    def collision_groups(self):
        collisions = pygame.sprite.groupcollide(bullet_group, meteorite_group, True, False)
        for items in collisions.items():
            metes = items[1]
            for mete in metes:
                if mete.collisions > self.get_meteorite_destroy(mete):
                    self.play_bomb_sound(mete)
                    mete.destroy_start = True
                mete.collisions += 1
        air_collisions = pygame.sprite.groupcollide(meteorite_group, aircraft_group, False, False)
        for items in air_collisions.items():
            airs = items[1]
            for air in airs:
                if air.collisions > 0:
                    air.destroy_start = True
                    self.s_bomb1.play(0, 0, 0)
                if air.allowed_collision:
                    air.collisions += 1

    def draw_groups(self):
        for sprite in bg_group.sprites():
            self.screen.blit(sprite.image, sprite.rect)
        for sprite in meteorite_group.sprites():
            self.screen.blit(sprite.image, sprite.rect)
        for sprite in circular_group.sprites():
            if sprite.image is not None:
                self.screen.blit(sprite.image, sprite.rect)
        for sprite in bullet_group.sprites():
            self.screen.blit(sprite.image, sprite.rect)
        for sprite in aircraft_group.sprites():
            if sprite.allowed_collision is False and sprite.invisible is not None and sprite.invisible.image is not None:
                self.screen.blit(sprite.invisible.image, sprite.invisible.rect)
            elif sprite.allowed_collision:
                self.screen.blit(sprite.image, sprite.rect)

    def control_groups(self):
        for sprite in aircraft_group.sprites():
            if sprite.allowed_control:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_SPACE]:
                    b_count = len(bullet_group.sprites())
                    if b_count < self.bullets_count:
                        self.szd1.play(0, 0, 0)
                        bullet = Bullet((all_group, bullet_group), self.screen, source_dir)
                        bullet.rect.x = sprite.rect.x + 20
                        bullet.rect.y = sprite.rect.y
                    b_count = len(bullet_group.sprites())
                    if b_count < self.bullets_count:
                        self.szd2.play(0, 0, 0)
                        bullet1 = Bullet((all_group, bullet_group), self.screen, source_dir)
                        bullet1.rect.x = sprite.rect.x + 35
                        bullet1.rect.y = sprite.rect.y
                    b_count = len(bullet_group.sprites())
                    if b_count < self.bullets_count:
                        self.szd3.play(0, 0, 0)
                        bullet2 = Bullet((all_group, bullet_group), self.screen, source_dir)
                        bullet2.rect.x = sprite.rect.x + 5
                        bullet2.rect.y = sprite.rect.y
                if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                    upr = UpdateParameter(pygame.time.get_ticks(), self.FPS)
                    upr.direction = 1
                    sprite.update(upr)
                elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                    upr = UpdateParameter(pygame.time.get_ticks(), self.FPS)
                    upr.direction = 2
                    sprite.update(upr)
                elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                    upr = UpdateParameter(pygame.time.get_ticks(), self.FPS)
                    upr.direction = 3
                    sprite.update(upr)
                elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                    upr = UpdateParameter(pygame.time.get_ticks(), self.FPS)
                    upr.direction = 4
                    sprite.update(upr)

    def run(self):
        pygame.display.set_caption(self.title)
        pygame.mixer.music.play(-1)
        while True:
            self.clock.tick(self.FPS)
            updatePar = UpdateParameter(pygame.time.get_ticks(), self.FPS)
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
            self.collision_groups()
            self.create_groups()
            self.control_groups()
            all_group.update(updatePar)
            self.draw_groups()
            pygame.display.flip()


pygame.mixer.pre_init(22050, -16, 16, 512)
pygame.init()
game = Game()
game.run()
