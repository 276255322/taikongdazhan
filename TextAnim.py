# coding=utf-8

import pygame


# 文本动画精灵
class TextAnim(pygame.sprite.Sprite):
    def __init__(self, groups, target, circular_max, font, text, position):
        self._layer = 999
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层对象
        self.font = font
        self.text = text
        self.image = None
        self.rect = None
        self.position = position  # 动画位置
        self.frame = 0  # 当前动画帧索引
        self.circular = 0  # 动画循环次数
        self.circular_max = circular_max  # 动画循环最大次数
        self.last_time = 0

    def update(self, updatePar):
        if 0 < self.circular_max < self.circular:
            self.kill()
            return
        if self.frame == 5:
            self.circular += 1
        if updatePar.current_time > self.last_time + updatePar.fps:
            if self.frame == 1:
                self.image = self.font.render(self.text, True, (255, 255, 255))
            elif self.frame == 2:
                self.image = self.font.render(self.text, True, (255, 255, 0))
            elif self.frame == 3:
                self.image = self.font.render(self.text, True, (255, 0, 0))
            elif self.frame == 4:
                self.image = self.font.render(self.text, True, (0, 0, 0))
            elif self.frame == 5:
                self.image = self.font.render(self.text, True, (0, 255, 255))
            else:
                self.image = self.font.render(self.text, True, (0, 0, 255))
            self.rect = self.image.get_rect()
            if self.position is None:
                self.rect.x = self.target.rect.x
                self.rect.y = self.target.rect.y
            else:
                self.rect.x = self.position[0]
                self.rect.y = self.position[1]
            self.frame += 1
            if self.frame > 5:
                self.frame = 0
            self.last_time = updatePar.current_time
