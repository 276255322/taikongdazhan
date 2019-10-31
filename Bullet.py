# coding=utf-8

import pygame
import os
import gl


# 子弹精灵类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, target, carrier):
        self._layer = 10
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层对象
        self.carrier = carrier  # 载体对象
        self.target_size = self.target.image.get_size()
        self.filepath = os.path.join(gl.source_dir, 'fgzd.png')
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.speed = [0, -5]
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.collisions = 0  # 碰撞次数
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.target_size[0] / 2 - self.img_size[0] / 2
        self.rect.y = self.target_size[1]
        self.show = False

    def update(self, updatePar):
        size = self.target.image.get_size()
        if self.rect.bottom > size[1] + self.img_size[1] or self.rect.top < 0 - self.img_size[1]:
            self.kill()
        if self.rect.right > size[0] + self.img_size[0] or self.rect.left < 0 - self.img_size[0]:
            self.kill()
        self.show = True
        self.rect = self.rect.move(self.speed)
