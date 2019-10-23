import pygame
import sys
import os
import random

source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
pygame.init()

# 陨石类
class Meteorite():
    def __init__(self, size):
        m_index = random.randint(1, 4)
        m_path = os.path.join(source_dir, 'ys' + str(m_index) + '.png')
        self.image = pygame.image.load(m_path).convert_alpha()
        m_wh = random.randint(10, 200);
        self.image = pygame.transform.scale(self.image, (m_wh, m_wh))
        mx_true = random.randint(0, 1)
        my_true = random.randint(0, 1)
        if mx_true == 1 or my_true == 1:
            self.image = pygame.transform.flip(self.image, mx_true == 1, my_true == 1)
        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.speed = [0, random.randint(1, 5)]
        self.rect = self.image.get_rect()
        self.img_size = self.image.get_size()
        self.rect.left = random.randint(-self.img_size[0], size[0] + 10)
        self.rect.top = -self.img_size[0] + 10

    def update(self):
        self.rect = self.rect.move(self.speed)


class Game():
    def __init__(self, title='太空陨石'):
        self.size = (480, 700)
        self.screen = pygame.display.set_mode(self.size)
        self.title = title
        self.color = (3, 6, 13)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load( os.path.join(source_dir, "xkbj2.jpg"))
        self.background_size = self.background.get_size()
        self.background_height = 0
        self.meteorites = []
        self.time_passed = 0
        self.meteorites_count = 50;

    def draw_background(self):
        move_distance = (self.size[1] / 10000) * self.time_passed
        self.background_height += move_distance
        # 如果超出窗口的高度，将height重置为零
        if self.background_height >= self.background_size[1]:
            self.background_height = 0
        self.screen.fill(self.color)
        # 两张背景图一起显示，营造背景图不间断的一直滚动的效果
        self.screen.blit(self.background, (0, -self.background_size[1] + self.background_height))
        self.screen.blit(self.background, (0, self.background_height))

    def create_meteorites(self):
        if len(self.meteorites) >= self.meteorites_count:
            return
        meteorite = Meteorite(size = self.size)
        self.meteorites.append(meteorite)

    def draw_meteorites(self, screen, size):
        # 清理跑出范围的陨石
        for meteorite in self.meteorites:
            if meteorite.rect.bottom > size[1] + meteorite.img_size[1]:
                self.meteorites.remove(meteorite)

        # 更新陨石位置
        for meteorite in self.meteorites:
            meteorite.update()

        # 绘制陨石
        for meteorite in self.meteorites:
            screen.blit(meteorite.image, meteorite.rect)

    def run(self):
        pygame.display.set_caption(self.title)
        while True:
            self.time_passed = self.clock.tick(60)
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()

            self.draw_background()
            self.create_meteorites()
            self.draw_meteorites(screen = self.screen, size = self.size)
            pygame.display.flip()


game = Game()
game.run()



