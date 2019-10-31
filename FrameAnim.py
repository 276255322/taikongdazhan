# coding=utf-8

import pygame
import os
import gl


# 帧循环动画精灵
class FrameAnim(pygame.sprite.Sprite):
    def __init__(self, groups, target, circular_max):
        self._layer = 20
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层对象
        self.image = None  # Surface对象
        self.rect = None  # Surface矩形
        self.frames = None  # 帧动画集合
        self.frame = 0  # 当前动画帧索引
        self.frame_count = 0  # 总帧数
        self.last_time = 0
        self.circular = 0  # 动画循环次数
        self.circular_max = circular_max  # 动画循环最大次数
        self.anim_size = None  # 动画大小
        self.anim_position = None  # 动画位置
        self.anim_deviation = [0, 0]  # 动画偏移位置
        self.anim_move = None  # 动画移动方式
        self.anim_size_multiple = 0  # 动画放大倍数
        self.show = False

    def load(self, dirname, frame_count):
        li = []
        for i in range(1, frame_count + 1):
            path = os.path.join(gl.source_dir + "/" + dirname, str(i) + ".png")
            img = pygame.image.load(path).convert_alpha()
            if i == 1:
                self.image = img
                self.rect = self.image.get_rect()
            li.append(img)
        self.frame_count = len(li)
        self.frames = li

    def update(self, updatePar):
        if 0 < self.circular_max < self.circular:
            self.kill()
            return
        if self.frame == self.frame_count - 1:
            self.circular += 1
        if updatePar.current_time > self.last_time + updatePar.fps:
            self.image = self.frames[self.frame]
            if self.anim_size is None and self.anim_size_multiple < 2:
                self.image = pygame.transform.scale(self.image, self.target.img_size)
            elif self.anim_size_multiple < 2:
                self.image = pygame.transform.scale(self.image, self.anim_size)
            img_rect = self.image.get_rect()
            if self.anim_size_multiple > 1:
                self.image = pygame.transform.scale(self.image, [img_rect.width * self.anim_size_multiple,
                                                                 img_rect.height * self.anim_size_multiple])
                img_rect = self.image.get_rect()
            self.show = True
            is_move = False
            if self.anim_move is not None:
                if self.circular == 0 and self.frame == 1:
                    self.rect = img_rect
                    self.rect.x += self.anim_deviation[0]
                    self.rect.y += self.anim_deviation[1]
                    is_move = False
                else:
                    self.rect = self.rect.move(self.anim_move)
                    img_rect.x = self.rect.x
                    img_rect.y = self.rect.y
                    self.rect = img_rect
                    is_move = True
            else:
                self.rect = img_rect
            if is_move is False:
                if self.anim_position is None:
                    self.rect.x = self.target.rect.x
                    self.rect.y = self.target.rect.y
                else:
                    self.rect.x = self.anim_position[0]
                    self.rect.y = self.anim_position[1]
            if self.anim_move is None:
                self.rect.x += self.anim_deviation[0]
                self.rect.y += self.anim_deviation[1]
            self.frame += 1
            if self.frame >= self.frame_count:
                self.frame = 0
            self.last_time = updatePar.current_time
