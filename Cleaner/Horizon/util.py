import csv
import re

import pandas as pd


def check_string(string: str):
    if re.search(r"-inner_error-", string):
        return "-inner_error-" + string[-6:-4]
    elif re.search(r"-outer_error-", string):
        return "-outer_error-" + string[-6:-4]
    elif re.search(r"-inner_outer_error-", string):
        return "-inner_outer_error-" + string[-6:-4]
    elif re.search(r"-dirty-original_error-", string):
        return "-original_error-" + string[-9:-4]


def calF1(precision, recall):
    """
    计算F1值

    :param precision: 精度
    :param recall: 召回率
    :return: F1值
    """
    return 2 * precision * recall / (precision + recall + 1e-10)
# def calDetPrecRec(pattern_expressions, dirty_path, clean_path,dirty_c):
#     """
#     计算检测的准确率和召回率
#
#     :param pattern_expressions: 模式表达式
#     :param dirty_path: 脏数据文件路径
#     :param clean_path: 干净数据文件路径
#     :return: 检测的准确率和召回率
#     """
#     attrList = []
#     dirty_dict = []
#
#     # 读取脏数据文件
#     with open(dirty_path, 'r', encoding='utf-8') as f:
#         reader = csv.DictReader(f, restval='nan')
#         for line in reader:
#             dirty_dict.append(line)
#             attrList = list(line.keys())
#
#     # 读取干净数据文件
#     clean_df = pd.read_csv(clean_path, header=0)
#     clean_df.columns = attrList
#
#     tot = 0
#     correct_rec = 0
#
#     # 计算正确检测的数量和总检测数量
#     with open(dirty_path, 'r', encoding='utf-8') as f:
#         reader = csv.DictReader(f, restval='nan')
#         cnt = 0
#         for line in reader:
#             for v in pattern_expressions[cnt]:
#                 if pattern_expressions[cnt][v] != dirty_dict[cnt][v]:
#                     if (cnt, list(clean_df.columns).index(v)) in dirty_c:
#                         correct_rec += 1
#                 tot += 1
#             cnt += 1
#
#     precision = correct_rec / tot
#     recall = correct_rec / len(dirty_c)
#     return precision, recall




def calRepPrec(pattern_expressions, dirty_path, clean_path):
    """
    计算修复的精度

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    :param clean_path: 干净数据文件路径
    :return: 修复的精度
    """
    attrList = []
    dirty_dict = []

    # 读取脏数据文件，存储为字典列表
    with open(dirty_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            dirty_dict.append(line)
            attrList = list(line.keys())

    # 读取干净数据文件
    df = pd.read_csv(clean_path, header=0)
    df.columns = attrList

    tot = 0
    correct = 0

    # 计算修复的正确数量和总数量
    with open(clean_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        cnt = 0
        for line in reader:
            for v in pattern_expressions[cnt]:
                if pattern_expressions[cnt][v] != dirty_dict[cnt][v]:
                    if pattern_expressions[cnt][v] == line[v]:
                        correct += 1
                    tot += 1
            cnt += 1
    return correct / tot


def calRepRec(pattern_expressions, dirty_path, clean_path):
    """
    计算修复的召回率

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    :param clean_path: 干净数据文件路径
    :return: 修复的召回率
    """
    attrList = []

    # 读取脏数据文件，获取属性列表
    with open(dirty_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            attrList = list(line.keys())
            break

    # 读取干净数据文件
    df = pd.read_csv(clean_path, header=0)
    df.columns = attrList

    dirty_dict = []
    tot = 0
    correct = 0

    # 读取脏数据文件，存储为字典列表
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            dirty_dict.append(line)

    # 计算修复的正确数量和总数量
    with open(clean_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        cnt = 0
        for line in reader:
            for v in dirty_dict[cnt]:
                if dirty_dict[cnt][v] != line[v]:
                    try:
                        if pattern_expressions[cnt][v] == line[v]:
                            correct += 1
                    except:
                        pass
                    tot += 1
            cnt += 1
    return correct / tot

