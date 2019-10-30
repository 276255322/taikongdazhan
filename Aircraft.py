# coding=utf-8

import pygame
import os
import random

from CircularAnim import CircularAnim
from Bullet import Bullet
from TextAnim import TextAnim


# 飞机精灵类
class Aircraft(pygame.sprite.Sprite):
    def __init__(self, groups, destroy_groups, target, play, src):
        self._layer = 10  # 层数
        self.play = play  # 玩家对象
        self.groups = groups  # 所属组
        self.destroy_groups = destroy_groups  # 毁灭动画组
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层对象
        self.target_size = self.target.image.get_size()  # 上层对象大小
        self.src = src  # 资源目录
        self.filepath = os.path.join(self.src, 'fj.png')
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.speed = [0, -4]  # 飞机速度
        self.power = 0  # 武器威力
        self.move_speed = 0  # 移动速度
        self.bomb = 3  # 炸弹数量
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.collisions = 0  # 碰撞次数
        self.allowed_collision = False  # 允许碰撞
        self.allowed_control = False  # 允许控制
        self.invisible = None  # 隐身动画
        self.destroy_start = False  # 是否开启自毁
        self.destroy = None  # 自毁动画
        self.mask = pygame.mask.from_surface(self.image)  # 飞机遮罩用于碰撞检测
        self.rect.x = self.target_size[0] / 2 - self.img_size[0] / 2
        self.rect.y = self.target_size[1]

    def add_score(self, num):
        self.play.score += num
        if self.play.reward_play > len(self.target.reward_play_nums):
            return
        n = 0
        for r_score in self.target.reward_play_nums:
            if self.play.reward_play == n:
                if self.play.score >= r_score:
                    self.play.play += 1
                    self.play.reward_play += 1
                    self.target.reward_play.play(0, 0, 0)
                    return
            n += 1

    def add_bomb(self, num):
        self.bomb += num
        if self.bomb > 5:
            self.bomb = 5
            return False
        self.target.reward_power.play(0, 0, 0)
        return True

    def add_move_speed(self, num):
        self.move_speed += num
        if self.move_speed > 3:
            self.move_speed = 3
            return False
        self.target.reward_power.play(0, 0, 0)
        return True

    def add_power(self, num):
        self.power += num
        if self.power > 6:
            self.power = 6
            return False
        self.target.reward_power.play(0, 0, 0)
        return True

    def get_move_speed(self):
        if self.move_speed == 1:
            return 4
        elif self.move_speed == 2:
            return 5
        elif self.move_speed == 3:
            return 6
        return 3

    def reward(self, text_group, rews):
        for rew in rews:
            score = 0
            if rew.type == 1:
                score = 30
            elif rew.type == 2:
                score = 50
            elif rew.type == 3:
                score = 100
            elif rew.type == 4:
                score = 150
            elif rew.type == 5:
                score = 200
            elif rew.type == 6:
                if self.add_move_speed(1) is False:
                    score = 500
            elif rew.type == 7:
                if self.add_power(1) is False:
                    score = 500
            elif rew.type == 8:
                if self.add_bomb(1) is False:
                    score = 500
            if score > 0:
                self.add_score(score)
                self.target.reward_money.play(0, 0, 0)
                TextAnim(text_group, rew, 10, self.target.anim_font, str(score), None)
        for rew in rews:
            rew.kill()

    def update(self, updatePar):
        size = self.target.image.get_size()
        if self.invisible is not None:
            if self.invisible.circular > 2 and self.allowed_control is False:
                self.allowed_control = True
            elif self.invisible.circular > 4 and self.allowed_collision is False:
                self.allowed_collision = True
                self.invisible.kill()
        if self.destroy_start and self.destroy is None:
            self.destroy = CircularAnim(self.destroy_groups, self, 4)
            self.destroy.load("fjbz.png", 64, 64, 4)
            self.kill()
            self.play.play -= 1
        if self.invisible is None and self.allowed_collision is False:
            self.invisible = CircularAnim(self.destroy_groups, self, 4)
            self.invisible.load("wdysfj.png", 64, 64, 4)
        if self.allowed_collision is False and self.allowed_control is False:
            self.rect = self.rect.move(self.speed)
        if self.allowed_control and updatePar.direction > 0:
            spd = self.get_move_speed()
            if updatePar.direction == 1:
                if self.rect.y <= 0:
                    return
                self.rect = self.rect.move([0, -spd])
            elif updatePar.direction == 2:
                if self.rect.y + self.img_size[1] >= size[1]:
                    return
                self.rect = self.rect.move([0, spd])
            elif updatePar.direction == 3:
                if self.rect.x <= 0:
                    return
                self.rect = self.rect.move([-spd, 0])
            elif updatePar.direction == 4:
                if self.rect.x + self.img_size[0] >= size[0]:
                    return
                self.rect = self.rect.move([spd, 0])

    def launch_bomb(self, all_group, bomb_group):
        if self.bomb <= 0:
            return
        b_count = len(bomb_group.sprites())
        if b_count > 0:
            return
        self.bomb -= 1
        for i in range(1, 50):
            bomb = CircularAnim((all_group, bomb_group), self, 1)
            bomb.load("fjbz.png", 64, 64, 4)
            sz = random.randint(50, 200)
            bomb.anim_size = [sz, sz]
            x_cent = self.target_size[0] / 2
            y_cent = self.target_size[1] / 2
            py = sz / 2
            x = random.randint(0, 1)
            if x == 0:
                x = random.randint(0, x_cent)
            else:
                x = -random.randint(0, x_cent)
            y = random.randint(0, 1)
            if y == 0:
                y = random.randint(0, y_cent)
            else:
                y = -random.randint(0, y_cent)
            bomb.anim_position = [x_cent + x - py, y_cent + y - py]

    def launch_bullet(self, target, all_group, bullet_group):
        bullets_count = 3
        bullets_speed = 5
        if self.power == 1:
            bullets_speed = 6
            bullets_count = 6
        elif self.power == 2:
            bullets_speed = 7
            bullets_count = 9
        elif self.power > 2:
            bullets_speed = 8
            bullets_count = 12
        if self.power == 4:
            bullets_count = 18
        elif self.power == 5:
            bullets_speed = 7
            bullets_count = 24
        elif self.power > 5:
            bullets_speed = 8
            bullets_count = 34

        b_count = len(bullet_group.sprites())
        if b_count < bullets_count:
            target.szd1.stop()
            target.szd1.play(0, 0, 0)
            bullet = Bullet((all_group, bullet_group), target, self, self.src)
            bullet.rect.x = self.rect.x + 20
            bullet.rect.y = self.rect.y
            bullet.speed[1] = - bullets_speed
        if b_count < bullets_count:
            target.szd2.stop()
            target.szd2.play(0, 0, 0)
            bullet1 = Bullet((all_group, bullet_group), target, self, self.src)
            bullet1.rect.x = self.rect.x + 35
            bullet1.rect.y = self.rect.y
            bullet1.speed[1] = - bullets_speed
        if b_count < bullets_count:
            target.szd3.stop()
            target.szd3.play(0, 0, 0)
            bullet2 = Bullet((all_group, bullet_group), target, self, self.src)
            bullet2.rect.x = self.rect.x + 5
            bullet2.rect.y = self.rect.y
            bullet2.speed[1] = - bullets_speed
        if self.power > 2:
            if b_count < bullets_count:
                target.szd1.stop()
                target.szd1.play(0, 0, 0)
                bullet3 = Bullet((all_group, bullet_group), target, self, self.src)
                bullet3.rect.x = self.rect.x + 50
                bullet3.rect.y = self.rect.y
                bullet3.speed[1] = - bullets_speed
            if b_count < bullets_count:
                target.szd1.stop()
                target.szd1.play(0, 0, 0)
                bullet4 = Bullet((all_group, bullet_group), target, self, self.src)
                bullet4.rect.x = self.rect.x - 10
                bullet4.rect.y = self.rect.y
                bullet4.speed[1] = - bullets_speed
        if self.power > 5:
            if b_count < bullets_count:
                target.szd1.stop()
                target.szd1.play(0, 0, 0)
                bullet5 = Bullet((all_group, bullet_group), target, self, self.src)
                bullet5.rect.x = self.rect.x + 65
                bullet5.rect.y = self.rect.y
                bullet5.speed[1] = - bullets_speed
            if b_count < bullets_count:
                target.szd1.stop()
                target.szd1.play(0, 0, 0)
                bullet6 = Bullet((all_group, bullet_group), target, self, self.src)
                bullet6.rect.x = self.rect.x - 25
                bullet6.rect.y = self.rect.y
                bullet6.speed[1] = - bullets_speed
