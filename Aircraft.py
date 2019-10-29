# coding=utf-8

import pygame
import os

from CircularAnim import CircularAnim


# 飞机精灵类
class Aircraft(pygame.sprite.Sprite):
    def __init__(self, groups, destroy_groups, target, src):
        self._layer = 10
        self.groups = groups
        self.destroy_groups = destroy_groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层Surface对象
        self.target_size = self.target.get_size()
        self.src = src  # 资源目录
        self.filepath = os.path.join(self.src, 'fj.png')
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.speed = [0, -4]
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.collisions = 0  # 碰撞次数
        self.allowed_collision = False  # 允许碰撞
        self.allowed_control = False  # 允许控制
        self.invisible = None  # 隐身动画
        self.destroy_start = False  # 是否开启自毁
        self.destroy = None  # 自毁动画
        size = self.target.get_size()
        self.rect.x = size[0] / 2 - self.img_size[0] / 2
        self.rect.y = size[1]

    def update(self, updatePar):
        size = self.target.get_size()
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
        if self.invisible is None and self.allowed_collision is False:
            self.invisible = CircularAnim(self.destroy_groups, self, 4)
            self.invisible.load("wdysfj.png", 64, 64, 4)
        if self.allowed_collision is False and self.allowed_control is False:
            self.rect = self.rect.move(self.speed)
        if self.allowed_control and updatePar.direction > 0:
            if updatePar.direction == 1:
                if self.rect.y <= 0:
                    return
                self.rect = self.rect.move([0, -4])
            elif updatePar.direction == 2:
                if self.rect.y + self.img_size[1] >= size[1]:
                    return
                self.rect = self.rect.move([0, 4])
            elif updatePar.direction == 3:
                if self.rect.x <= 0:
                    return
                self.rect = self.rect.move([-4, 0])
            elif updatePar.direction == 4:
                if self.rect.x + self.img_size[0] >= size[0]:
                    return
                self.rect = self.rect.move([4, 0])
