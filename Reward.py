# coding=utf-8

import pygame
import os
import random


# 奖励精灵类
class Reward(pygame.sprite.Sprite):
    def __init__(self, groups, target, src, type):
        self._layer = 10
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.type = type  # 奖励类型
        self.target = target  # 上层Surface对象
        self.target_size = self.target.image.get_size()
        self.src = src  # 资源目录
        self.filepath = os.path.join(self.src, 'jl1.png')
        if self.type == 6:
            self.filepath = os.path.join(self.src, 'speed.png')
        elif self.type == 7:
            self.filepath = os.path.join(self.src, 'power.png')
        elif self.type == 8:
            self.filepath = os.path.join(self.src, 'bomb.png')
        elif self.type == 1:
            self.filepath = os.path.join(self.src, 'jl2.png')
        elif self.type == 2:
            self.filepath = os.path.join(self.src, 'jl3.png')
        elif self.type == 3:
            self.filepath = os.path.join(self.src, 'jl4.png')
        elif self.type == 4:
            self.filepath = os.path.join(self.src, 'jl5.png')
        elif self.type == 5:
            self.filepath = os.path.join(self.src, 'jl6.png')
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.speed = [1, 1]
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.collisions = 0  # 碰撞次数
        self.rect.x = random.randint(10, self.target_size[0] - 10)
        self.rect.y = -self.img_size[0] + 10

    def update(self, updatePar):
        size = self.target.image.get_size()
        if self.rect.bottom > size[1] + self.img_size[1]:
            self.kill()
        if self.rect.right > size[0] + self.img_size[0] or self.rect.left < 0 - self.img_size[0]:
            self.speed[0] = - self.speed[0]
        self.rect = self.rect.move(self.speed)
