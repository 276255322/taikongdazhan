# coding=utf-8

import pygame
import os
import random

from CircularAnim import CircularAnim


# 陨石精灵类
class Meteorite(pygame.sprite.Sprite):
    def __init__(self, groups, destroy_groups, target, src):
        self._layer = 10
        self.groups = groups
        self.destroy_groups = destroy_groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层对象
        self.target_size = self.target.image.get_size()
        self.destroy_start = False  # 是否开启自毁
        self.destroy = None  # 自毁动画
        self.src = src  # 资源目录
        self.filepath = os.path.join(self.src, 'ys' + str(random.randint(1, 4)) + '.png')
        self.image = pygame.image.load(self.filepath).convert_alpha()
        m_wh = random.randint(10, 200)
        self.image = pygame.transform.scale(self.image, (m_wh, m_wh))
        mx_true = random.randint(0, 1)
        my_true = random.randint(0, 1)
        if mx_true == 1 or my_true == 1:
            self.image = pygame.transform.flip(self.image, mx_true == 1, my_true == 1)
        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.speed = [0, random.randint(1, 5)]
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.rect.left = random.randint(-self.img_size[0], self.target_size[0] + 10)
        self.rect.top = -self.img_size[0] + 10
        self.bottom_max = random.randint(0, self.target_size[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.collisions = 0  # 碰撞次数

    def update(self, updatePar):
        size = self.target.image.get_size()
        if self.destroy_start and self.destroy is None:
            self.destroy = CircularAnim(self.destroy_groups, self, 4)
            self.destroy.load("ysbz.png", 64, 64, 4)
            self.kill()
        elif self.rect.bottom > size[1] + self.img_size[1]:
            self.kill()
        self.rect = self.rect.move(self.speed)
