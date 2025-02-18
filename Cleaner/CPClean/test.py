import numpy as np
import pandas as pd
import os
import utils
import argparse
from CPCPackage.training.preprocess import preprocess
import warnings
import time
import pickle
from experiment import *
from CPCPackage.repair.imputers import *
from CPCPackage.training.knn import KNN
from CPCPackage.repair.repair import repair, num_imputers
from build_dataset import build_dataset, build_real_dataset

model = {
    "fn": KNN,
    "params": {"n_neighbors":3}
}

# 需要配置的参数 info val_size dataset_name version
info = {
    "label": "labels", # name of label column
}
val_size = 100

dataset_name = "smartfactory"
version = "_systematic_10"
data_clean = "D:\PyCharm\PycharmProjects\MDCBaseline\Data\\" + dataset_name + "\\" + dataset_name + "_data_vectorized.csv"
data_dirty = "D:\PyCharm\PycharmProjects\MDCBaseline\Data\\" + dataset_name + "\\explicit_for_CPClean\\" + dataset_name + version + ".csv"

data = build_real_dataset(data_clean, data_dirty, info, val_size=val_size, test_size=None,
                       max_size=None, save_dir=None, random_state=1)

data["X_train_repairs"] = repair(data["X_train_dirty"])
        
data = preprocess(data)
        
data["X_val"] = data["X_val"][:val_size]
data["y_val"] = data["y_val"][:val_size]

print("Preprocess Finished")

boost_results = run_boost_clean(data, model)

original_result, cp_result = run_cp_clean(data, model, n_jobs=1)

print("clean before: ", original_result)
print("boostclean after: ", boost_results)
print("cpclean after: ", cp_result)


result_path = "D:\PyCharm\PycharmProjects\MDCBaseline\\results\\"
file_boost = result_path + "boostclean\\" + dataset_name + "\\" + dataset_name + version + "_output.txt"
file_cp = result_path + "cpclean\\" + dataset_name + "\\" + dataset_name + version + "_output.txt"

with open(file_boost, 'w') as file:
    file.write("clean before: " + str(original_result))
    file.write("\nboostclean after: " + str(boost_results))

with open(file_cp, 'w') as file:
    file.write("clean before: " + str(original_result))
    file.write("\ncpclean after: " + str(cp_result))