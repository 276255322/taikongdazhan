# coding=utf-8

import pygame
import os
import random
import gl

vector2 = pygame.math.Vector2


# 背景类
class GameBackground(pygame.sprite.Sprite):
    def __init__(self, groups, target, pos):
        self._layer = -1
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层Surface对象
        self.target_size = self.target.image.get_size()
        self.image = pygame.image.load(os.path.join(gl.source_dir, "xkbj2.jpg"))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y + (self.target_size[1] - self.rect.height)
        self.parent = False
        self.last_time = 0
        cent = self.rect.width - self.target_size[0]
        if cent > 0:
            self.rect.x = -(random.randint(0, cent))
        self.show = False

    def update(self, updatePar):
        self.show = True
        if updatePar.current_time > self.last_time + updatePar.fps + 50:
            self.rect.y += 1
            self.last_time = updatePar.current_time
        if self.rect.y > self.target_size[1]:
            self.kill()
        if not self.parent:
            if self.rect.y >= 0:
                self.parent = True
                GameBackground(self.groups, self.target, vector2(0, -self.target_size[1]))
