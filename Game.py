# coding=utf-8

import pygame
import sys
import os
import random

vector2 = pygame.math.Vector2

from GameBackground import GameBackground
from Aircraft import Aircraft
from Meteorite import Meteorite
from UpdateParameter import UpdateParameter
from Play import Play
from Reward import Reward
from TextAnim import TextAnim

source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
circular_group = pygame.sprite.Group()
s_reward_group = pygame.sprite.Group()
p_reward_group = pygame.sprite.Group()
reward_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
meteorite_group = pygame.sprite.Group()
aircraft_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
all_group = pygame.sprite.LayeredUpdates()


class Game:
    def __init__(self, title='太空陨石'):
        self.play_number = 5
        self.size = (480, 700)
        self.image = pygame.display.set_mode(self.size)
        self.rect = self.image.get_rect()
        self.title = title
        self.color = (3, 6, 13)
        self.clock = pygame.time.Clock()
        self.clock_ticks = None
        self.bg = GameBackground((all_group, bg_group), self, source_dir, vector2(0, 0))
        self.FPS = 60
        self.meteorites_count = 10
        self.reward_play_nums = [1000, 5000, 10000, 50000, 100000, 200000, 300000, 400000, 500000, 600000, 700000,
                                 800000, 900000, 1000000]  # 游戏次数奖励集合
        self.reward_count = 2
        self.font = pygame.font.SysFont("simsunnsimsun", 16)
        self.anim_font = pygame.font.SysFont("simsunnsimsun", 16)
        self.s_bomb1 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB1.ogg"))
        self.s_bomb2 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB2.ogg"))
        self.s_bomb3 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB3.ogg"))
        self.s_bomb4 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB4.ogg"))
        self.s_bomb5 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB5.ogg"))
        self.s_bomb6 = pygame.mixer.Sound(os.path.join(source_dir, "BOMB6.ogg"))
        self.szd1 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        self.szd2 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        self.szd3 = pygame.mixer.Sound(os.path.join(source_dir, "zd1.ogg"))
        self.reward_money = pygame.mixer.Sound(os.path.join(source_dir, "reward_money.ogg"))
        self.reward_play = pygame.mixer.Sound(os.path.join(source_dir, "reward_play.ogg"))
        self.reward_power = pygame.mixer.Sound(os.path.join(source_dir, "reward_power.ogg"))
        self.aircraft_time = 0
        self.reward_time = 0
        self.meteorite_time = 0
        self.play1 = Play(0, 0)
        self.play1_icon = pygame.image.load(os.path.join(source_dir, "fj_x.png")).convert_alpha()
        self.play2 = Play(0, 1)
        self.play2_icon = pygame.image.load(os.path.join(source_dir, "fj1_x.png")).convert_alpha()
        self.Continue = False
        pygame.mixer.music.load(os.path.join(source_dir, "m1.mp3"))

    def create_groups(self):
        is_play1 = False
        is_play2 = False
        for air in aircraft_group.sprites():
            if air.play.index == 0:
                is_play1 = True
            elif air.play.index == 1:
                is_play2 = True
        if self.aircraft_time == 0 or self.clock_ticks - self.aircraft_time > 4000:
            if is_play1 is False and self.play1.play > 0:
                self.aircraft_time = self.clock_ticks
                Aircraft((all_group, aircraft_group), (all_group, circular_group), self, self.play1, source_dir)
        if self.meteorite_time == 0 or self.clock_ticks - self.meteorite_time > 100:
            m_count = len(meteorite_group.sprites())
            if m_count < self.meteorites_count:
                self.meteorite_time = self.clock_ticks
                Meteorite((all_group, meteorite_group), (all_group, circular_group), self, source_dir)
        if self.reward_time == 0 or self.clock_ticks - self.reward_time > 100:
            r_count = len(reward_group.sprites())
            if r_count < self.reward_count:
                self.reward_time = self.clock_ticks
                rtype = random.randint(0, 1)
                if rtype == 1:
                    Reward((all_group, reward_group, s_reward_group), self, source_dir, random.randint(0, 5))
                else:
                    Reward((all_group, reward_group, p_reward_group), self, source_dir, random.randint(6, 8))

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
            self.s_bomb6.stop()
            self.s_bomb6.play(0, 0, 0)
        elif mete.img_size[0] >= 150:
            self.s_bomb5.stop()
            self.s_bomb5.play(0, 0, 0)
        elif mete.img_size[0] >= 100:
            self.s_bomb4.stop()
            self.s_bomb4.play(0, 0, 0)
        elif mete.img_size[0] >= 50:
            self.s_bomb3.stop()
            self.s_bomb3.play(0, 0, 0)
        else:
            self.s_bomb2.stop()
            self.s_bomb2.play(0, 0, 0)

    def play_bomb_score(self, air, mete):
        score = 1
        if mete.img_size[0] >= 200:
            score = 16
        elif mete.img_size[0] >= 150:
            score = 8
        elif mete.img_size[0] >= 100:
            score = 4
        elif mete.img_size[0] >= 50:
            score = 2
        position = [mete.rect.x + mete.img_size[0] / 2, mete.rect.y + mete.img_size[1] / 2]
        TextAnim((all_group, text_group), mete, 10, self.anim_font, str(score), position)
        air.add_score(score)

    def collision_groups(self):
        collisions = pygame.sprite.groupcollide(bullet_group, meteorite_group, True, False, pygame.sprite.collide_mask)
        for items in collisions.items():
            bullet = items[0]
            metes = items[1]
            for mete in metes:
                if mete.collisions > self.get_meteorite_destroy(mete):
                    self.play_bomb_sound(mete)
                    self.play_bomb_score(bullet.carrier, mete)
                    mete.destroy_start = True
                mete.collisions += 1
        air_collisions = pygame.sprite.groupcollide(meteorite_group, aircraft_group, False, False,
                                                    pygame.sprite.collide_mask)
        for items in air_collisions.items():
            airs = items[1]
            for air in airs:
                if air.collisions > 0:
                    if air.power > 0:
                        for i in range(0, air.power):
                            re = Reward((all_group, reward_group, p_reward_group), self, source_dir, 7)
                            x = random.randint(air.rect.x - 50, air.rect.x + 50)
                            if x < 0 or x > self.size[0]:
                                x = air.rect.x
                            re.rect.x = x
                            re.rect.y = random.randint(air.rect.y - 80, air.rect.y - 50)
                    air.destroy_start = True
                    self.s_bomb1.stop()
                    self.s_bomb1.play(0, 0, 0)
                if air.allowed_collision:
                    air.collisions += 1
        reward_collisions = pygame.sprite.groupcollide(aircraft_group, reward_group, False, False)
        for items in reward_collisions.items():
            items[0].reward((all_group, text_group), items[1])
        bomb_collisions = pygame.sprite.groupcollide(bomb_group, meteorite_group, False, True)
        for items in bomb_collisions.items():
            bomb = items[0]
            metes = items[1]
            for mete in metes:
                self.play_bomb_sound(mete)
                self.play_bomb_score(bomb.target, mete)

    def draw_groups(self):
        for sprite in bg_group.sprites():
            self.image.blit(sprite.image, sprite.rect)
        for sprite in meteorite_group.sprites():
            self.image.blit(sprite.image, sprite.rect)
        for sprite in circular_group.sprites():
            if sprite.image is not None:
                self.image.blit(sprite.image, sprite.rect)
        for sprite in bullet_group.sprites():
            self.image.blit(sprite.image, sprite.rect)
        for sprite in bomb_group.sprites():
            self.image.blit(sprite.image, sprite.rect)
        for sprite in aircraft_group.sprites():
            if sprite.allowed_collision is False and sprite.invisible is not None and sprite.invisible.image is not None:
                self.image.blit(sprite.invisible.image, sprite.invisible.rect)
            elif sprite.allowed_collision:
                self.image.blit(sprite.image, sprite.rect)
        for sprite in reward_group.sprites():
            self.image.blit(sprite.image, sprite.rect)
        for sprite in text_group.sprites():
            self.image.blit(sprite.image, sprite.rect)

    def control_groups(self):
        if self.Continue:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_y] or key_pressed[pygame.K_RETURN]:
                self.Continue = False
                self.play1 = Play(0, self.play_number)
                self.play2 = Play(1, self.play_number)
            elif key_pressed[pygame.K_n] or key_pressed[pygame.K_ESCAPE]:
                sys.exit()
        for sprite in aircraft_group.sprites():
            if sprite.allowed_control:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_SPACE]:
                    sprite.launch_bullet(self, all_group, bullet_group)
                if key_pressed[pygame.K_b]:
                    sprite.launch_bomb(all_group, bomb_group)
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

    def show_info(self):
        score_count = self.play1.score + self.play2.score
        n = 0
        for sprite in aircraft_group.sprites():
            if n == 0:
                self.play1.bomb = sprite.bomb
                self.play1.power = sprite.power
                self.play1.move_speed = sprite.move_speed
            elif n == 1:
                self.play2.bomb = sprite.bomb
                self.play2.power = sprite.power
                self.play2.move_speed = sprite.move_speed
            n += 1
        score = self.font.render(f'得分:{score_count}', True, (255, 255, 0))
        s_position_x = (self.size[0] - score.get_size()[0]) / 2
        s_position_y = 10
        self.image.blit(score, (s_position_x, s_position_y))
        score = self.font.render(f'P1:{self.play1.score}', True, (255, 255, 0))
        self.image.blit(score, (12, s_position_y))
        score = self.font.render(f' B:{self.play1.bomb}', True, (255, 255, 0))
        self.image.blit(score, (12, 30))
        score = self.font.render(f' P:{self.play1.power}', True, (255, 255, 0))
        self.image.blit(score, (12, 50))
        self.image.blit(self.play1_icon, (5, 70))
        score = self.font.render(f' :{self.play1.play}', True, (255, 255, 0))
        self.image.blit(score, (20, 72))
        if self.play1.play <= 0:
            score = self.font.render(f'开始或继续请按【Y】或【Enter】,退出请按【N】或【Esc】', True, (255, 255, 0))
            s_position_x = (self.size[0] - score.get_size()[0]) / 2
            s_position_y = (self.size[1] - score.get_size()[1]) / 2
            self.image.blit(score, (s_position_x, s_position_y))
            score = self.font.render(f'【w,s,a,d】或【↑↓→←】移动,【空格】开火,【b】扔炸弹', True, (0, 255, 0))
            s_position_x = (self.size[0] - score.get_size()[0]) / 2
            self.image.blit(score, (s_position_x, s_position_y + 30))
            self.Continue = True

    def run(self):
        pygame.display.set_caption(self.title)
        pygame.mixer.music.play(-1)
        while True:
            self.clock.tick(self.FPS)
            self.clock_ticks = pygame.time.get_ticks()
            updatePar = UpdateParameter(self.clock_ticks, self.FPS)
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
            self.collision_groups()
            self.create_groups()
            self.control_groups()
            all_group.update(updatePar)
            self.draw_groups()
            self.show_info()
            pygame.display.flip()


pygame.mixer.pre_init(22050, -16, 16, 512)
pygame.init()
game = Game()
game.run()
