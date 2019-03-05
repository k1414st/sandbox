# -*- coding: utf-8 -*-
"""
Bellman方程式の漸化式を用いて
簡単な例で
価値テーブルを計算してみる
"""

import numpy as np

# 割引率
GAMMA = 0.9
# 報酬テーブル
# rewards = np.array([0, 2, 1, 3, 1.1, 2, 2, 2.2, 2])
rewards = np.array([2, 1, 1, 3])
# 報酬テーブル長
L = len(rewards)

# 更新式（左右端は別処理）
def update(v, i):
    if i == 0:
        return rewards[i] + GAMMA * v[1]
    elif i == L-1:
        return rewards[i] + GAMMA * v[L-1]
    else:
        return rewards[i] + GAMMA * max(v[i-1], v[i+1])

# 価値テーブル
v = np.random.uniform(0, 1, size=(L,))

# 漸化式を適用するループ
print(0, v)
for loop in range(1, 1000):
    for i in range(len(v)):
        v[i] = update(v, i)
    print(loop, v)


