# coding=utf-8


# 玩家对象
class Play:
    def __init__(self):
        self.score = 0  # 得分
        self.play = 0  # 游戏可玩次数
        self.bomb = 0  # bomb数量
        self.power = 0  # 子弹等级
        self.reward_play = 0  # 已奖励游戏次数
