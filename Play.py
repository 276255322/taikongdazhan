# coding=utf-8


# 玩家对象
class Play:
    def __init__(self, index, play):
        self.index = index  # 0：表示玩家1， 1：表示玩家2
        self.score = 0  # 得分
        self.play = play  # 游戏可玩次数
        self.bomb = 0  # bomb数量
        self.power = 0  # 子弹等级
        self.move_speed = 0  # 移动速度
        self.reward_play = 0  # 已奖励游戏次数
