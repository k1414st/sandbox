# -*- coding: utf-8 -*-
"""
optunaチュートリアル的なコード
"""
import time
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import optuna


################################################################################
# case 1. simple function base
"""
簡単な関数をハイパーパラメータ空間とみなし、最適化 (最小化)
"""


def objective(trial):
    # 探索範囲と分布を指定
    x = trial.suggest_uniform('x', -10, 10)
    y = trial.suggest_uniform('y', -10, 10)
    # 最小化対象
    objective_to_minimize = (x-1.234)**2 + (y+5.678)**2
    return objective_to_minimize


# 学習
study = optuna.create_study()
study.optimize(objective, n_trials=100)
print('objective: %.4f' % study.best_value)
print(study.best_params)
print(study.best_trial)


################################################################################
time.sleep(5)
################################################################################
# case 2. simulation base
"""
ダミーデータ作成
3変数はDFと相関があり、残り17変数は相関なし
(L1回帰が有効と思われるデータを作為的に作成)
"""
N_POS = N_NEG = 100
N_F1 = 3
N_F2 = 17

prm_dist = np.random.uniform(0.1, 1, size=(4, N_F1))
X1_pos = np.random.normal(loc=prm_dist[0], scale=prm_dist[1], size=(N_POS, N_F1))
X1_neg = np.random.normal(loc=prm_dist[2], scale=prm_dist[3], size=(N_NEG, N_F1))
X2 = np.random.normal(loc=0, scale=1, size=(N_POS+N_NEG, N_F2))
X = np.concatenate([np.concatenate([X1_pos, X1_neg], axis=0), X2], axis=1)
y = np.concatenate([np.ones(shape=(N_POS,)), np.zeros(shape=(N_NEG,))])

X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.3)


def get_model_auc(**kwargs):
    """ モデルを作り、AUCを測定 """
    lr = LogisticRegression(**kwargs)
    lr.fit(X_train, y_train)
    y_test_pred = lr.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, y_test_pred)


"""
ベンチマーク（無調整）
"""
auc_base = get_model_auc()


"""
optunaによる最適化モデル
"""


def objective(trial):
    # 探索範囲と分布を指定
    penalty = trial.suggest_categorical('penalty', ['l1', 'l2'])
    C = trial.suggest_loguniform('C', 1e-3, 1e3)
    return -get_model_auc(penalty=penalty, C=C)


# 学習
study = optuna.create_study()
study.optimize(objective, n_trials=100)

"""
比較
"""
print()
print('base : %.4f' % auc_base)
print('tuned: %.4f' % -study.best_value)
print(study.best_params)
print(study.best_trial)
