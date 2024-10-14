########################################
# Baran: The Error Correction System
# Mohammad Mahdavi
# moh.mahdavi.l@gmail.com
# April 2019
# Big Data Management Group
# TU Berlin
# All Rights Reserved
########################################

# 依赖库和模块导入
import os
import re
import io
import sys
import math
import argparse
import pandas as pd
import json
import time
import shutil
import pickle
import difflib
import unicodedata
import multiprocessing
import bs4
import bz2
import numpy
import py7zr
import mwparserfromhell
import sklearn.svm
import sklearn.ensemble
import sklearn.naive_bayes
import sklearn.linear_model
import raha
import warnings
import signal
from datetime import datetime

from Cleaner.Baran_Raha.correction_with_raha import Correction
from Cleaner.Baran_Raha.detection import Detection
from util.getScore import calculate_accuracy_and_recall

warnings.filterwarnings("ignore")

def check_string(string: str):
    if re.search(r"-inner_error-", string):
        return "-inner_error-" + string[-6:-4]
    elif re.search(r"-outer_error-", string):
        return "-outer_error-" + string[-6:-4]
    elif re.search(r"-inner_outer_error-", string):
        return "-inner_outer_error-" + string[-6:-4]
    elif re.search(r"-dirty-original_error-", string):
        return "-original_error-" + string[-9:-4]
    else:
        return ''


def handler(signum, frame):
    raise TimeoutError("Time exceeded")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirty_path', type=str, default='../../Data/1_hospital/dirty.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospital/clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, help="Task name (dataset name)", default='test')
    parser.add_argument('--output_path', type=str, default='../../results/raha_baran',
                        help='Path to save the output results.')
    args = parser.parse_args()

    # 生成输出目录路径
    dirty_path = args.dirty_path
    clean_path = args.clean_path
    task_name = args.task_name
    output_path = args.output_path

    stra_path = f"{output_path}/results_{task_name}"

    # 如果输出目录不存在，创建该目录
    if not os.path.exists(stra_path):
        os.makedirs(stra_path)

    dataset_name = task_name
    dataset_dictionary = {
        "name": task_name + check_string(dirty_path),
        "path": dirty_path,
        "clean_path": clean_path
    }
    time_limit = 24 * 3600  # 24 小时时间限制
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(time_limit)

    clean_in_cands = []

    try:
        # 获取Raha的错误检测结果
        time_start = time.time()
        app1 = Detection()
        detected_cells = app1.run(dataset_dictionary)
        p, r, f = app1.d.get_data_cleaning_evaluation(detected_cells)[:3]
        time_end = time.time()

        # 输出文件路径保存在 stra_path 中
        out_path = f"{stra_path}/onlyED_{task_name}{check_string(dirty_path)}.txt"
        with open(out_path, 'w') as f:
            sys.stdout = f
            print(f"{p}\n{r}\n{f}")
            print(time_end - time_start)

        # 开始错误修正过程
        time_start = time.time()
        data = raha.dataset.Dataset(dataset_dictionary)
        app = Correction()
        correction_dictionary = app.run(app1.d,clean_in_cands)
        p, r, f = data.get_data_cleaning_evaluation(correction_dictionary)[-3:]

        out_path = f"{stra_path}/oriED+EC_{task_name}{check_string(dirty_path)}.txt"
        res_path = f"{stra_path}/repaired_{task_name}{check_string(dirty_path)}.csv"

        repaired_df = pd.read_csv(dirty_path)
        for cell, value in correction_dictionary.items():
            repaired_df.iloc[cell[0], cell[1]] = value
        repaired_df.to_csv(res_path, index=False)

        with open(out_path, 'w') as f:
            sys.stdout = f
            print(f"{p}\n{r}\n{str(f)}")
            time_end = time.time()
            print(time_end - time_start)

        # 分析修复结果
        sys.stdout = sys.__stdout__
        out_path = f"{stra_path}/all_compute_{task_name}{check_string(dirty_path)}.txt"
        with open(out_path, 'w') as f:
            sys.stdout = f
            actual_errors = data.get_actual_errors_dictionary()
            actual_errors_list = list(actual_errors.keys())
            repaired_cells = list(correction_dictionary.keys())

            repair_right_cells = [cell for cell in repaired_cells if
                                  cell in actual_errors and correction_dictionary[cell] == actual_errors[cell]]
            rec_right = sum(1 for cell in actual_errors_list if cell in repair_right_cells)

            # 输出各种统计结果
            print(f"rep_right:{len(repair_right_cells)}")
            print(f"rec_right:{rec_right}")
            print(f"wrong_cells:{len(actual_errors_list)}")
            print(f"prec:{p}")
            print(f"rec:{r}")

            # 分析修复的正确和错误情况
            wrong2right = len([cell for cell in repair_right_cells if cell in actual_errors_list])
            right2right = len([cell for cell in repair_right_cells if cell not in actual_errors_list])
            wrong2wrong = len(
                [cell for cell in repaired_cells if cell in actual_errors_list and cell not in repair_right_cells])
            right2wrong = len(
                [cell for cell in repaired_cells if cell not in actual_errors_list and cell not in repair_right_cells])

            print(f"wrong2right:{wrong2right}")
            print(f"right2right:{right2right}")
            print(f"wrong2wrong:{wrong2wrong}")
            print(f"right2wrong:{right2wrong}")

            # 分析干净候选集
            clean_in_cands = list(set(clean_in_cands))
            clean_in_cands = [cell for cell in clean_in_cands if cell in repaired_cells]
            clean_in_cands_repair_right = [cell for cell in clean_in_cands if cell in repair_right_cells]
            print(f"clean_in_cands AFTER filter:{len(clean_in_cands)}")
            print(
                f"proportion of clean value in candidates and selected correctly:{len(clean_in_cands_repair_right) / (len(clean_in_cands) + 1e-8)}")

        sys.stdout = sys.__stdout__
        print(f"Repaired data saved to {res_path}")
        print("===============================================")
        print("测评性能开始：")
        # 读取干净数据、脏数据和修复后的数据
        clean_data = pd.read_csv(args.clean_path)
        dirty_data = pd.read_csv(args.dirty_path)
        cleaned_data = pd.read_csv(res_path)

        # 根据规则定义的属性集合
        attributes = clean_data.columns.tolist()

        # 调用函数计算修复准确率和召回率
        accuracy, recall = calculate_accuracy_and_recall(clean_data, dirty_data, cleaned_data, attributes,
                                                         stra_path, args.task_name)

        # 输出修复的准确率和召回率
        print(f"修复准确率: {accuracy}")
        print(f"修复召回率: {recall}")
        # 定义输出文件路径
        out_path = os.path.join(stra_path, f"{args.task_name}_evaluation.txt")

        print("测评结束，详细测评日志见：" + str(out_path))

    except TimeoutError as e:
        print(f"Time exceeded: {e}, {task_name}, {dirty_path}")
        with open(f"{stra_path}/timeout_log.txt", "a") as out_file:
            now = datetime.now()
            out_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            out_file.write("Baran with Raha.py: ")
            out_file.write(f" {task_name} {dirty_path}\n")

if __name__ == "__main__":
    main()