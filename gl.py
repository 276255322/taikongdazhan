# coding=utf-8

import pygame
import os

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
