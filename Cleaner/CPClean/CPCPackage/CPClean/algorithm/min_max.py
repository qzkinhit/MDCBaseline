import numpy as np
import pandas as pd
import time
from collections import Counter
from .utils import product, majority_vote
# from ....utils import Pool
from functools import partial

def min_max(mm, y, K):
    """MinMax algorithm. Given a similarity matrix, return whether it is CP or not and the 
       best scenario for each label.
        mm (np.array): shape Nx2. the min and max similarity of each row. 
        y (list): labels
        K (int): KNN hyperparameter
        Return:
            cc (list of boolean):whether CPed or not

    """
    assert len(set(y)) == 2 # 开始判定了类别数只能为2，需要改动才能支持更多类别
    pred_set = set()
    best_scenarios = {}

    for c in [0, 1]: # 只支持两个类别
        best_scenario = np.zeros(len(y))
        mask = (y == c)

        # set min max
        best_scenario[mask] = mm[:, 1][mask]
        best_scenario[(mask == False)] = mm[:, 0][(mask == False)]

        # run KNN
        order = np.argsort(-best_scenario, kind="stable")
        top_K = y[order][:K]

        pred = majority_vote(top_K)

        if pred == c:
            pred_set.add(c)

        best_scenarios[c] = (best_scenario, pred)

    is_cc = len(pred_set) == 1

    return is_cc, best_scenarios, list(pred_set)

def min_max_val(MM, y, K):
    q1_results = []
    scenarios = []
    cc_preds = []
    for mm in MM:
        cc, sc, pred = min_max(mm, y, K)
        q1_results.append(cc)
        scenarios.append(sc)
        cc_preds.append(pred)

    q1_results = np.array(q1_results)
    return q1_results, scenarios, cc_preds