import environ
import pandas as pd
from dataclean.constraint_languages.ic import *
from dataclean.constraint_languages.ic import DictValue
from dataclean.constraint_languages.pattern import Pattern
import time
import numpy as np
from dataclean.search import *
import matplotlib.pyplot as plt
from util.getNum import getErrorNum, getCorrectRepairs, calculate_accuracy_and_recall


def load_and_prepare_data(dirty_data_path, clean_data_path, columns_to_cast):
    """
    加载并准备数据。

    参数：
    dirty_data_path (str): 脏数据的路径。
    clean_data_path (str): 干净数据的路径。
    columns_to_cast (list): 需要转换为字符串的列名列表。

    返回：
    tuple: 脏数据和干净数据的DataFrame。
    """
    df_dirty = pd.read_csv(dirty_data_path)
    df_clean = pd.read_csv(clean_data_path)

    # 将指定列转换为字符串类型
    for column in columns_to_cast:
        df_dirty[column] = df_dirty[column].astype(str)
        df_clean[column] = df_clean[column].astype(str)

    return df_dirty, df_clean


def define_patterns_and_models():
    """
    定义patterns和编辑规则模型。

    返回：
    tuple: 包含patterns和编辑规则模型的列表。
    """
    patterns = []
    patterns += [Pattern('gender', "[M|F]")]
    patterns += [Pattern('areacode', "[0-9][0-9][0-9]")]
    patterns += [Pattern('phone', "\d{3}-\d{4}")]
    patterns += [Pattern('state', "[A-Z]{2}")]
    patterns += [Pattern('zip', "[1-9][0-9]{4}")]
    patterns += [Pattern('maritalstatus', "[M|S]")]
    patterns += [Pattern('haschild', "[Y|N]")]

    models = []
    models.append(OneDeterminedOne(["zip"], ["state"]))
    models.append(OneDeterminedOne(["zip"], ["city"]))
    models.append(OneToOne(["areacode"], ["state"]))
    models1 = []
    models1.append(OneDeterminedOne(["fname"], ["gender"]))

    models2 = []
    models2.append(OneToOne(["areacode"], ["state"]))

    return patterns, models, models1, models2


def solve_data(df, models, config, partition_col):
    """
    使用编辑规则模型清洗数据。

    参数：
    df (DataFrame): 需要清洗的DataFrame。
    models (list): 编辑规则模型列表。
    config (dict): 配置字典。
    partition_col (str): 用于分区的列名。

    返回：
    tuple: (清洗操作, 清洗后的DataFrame)
    """
    operation, output, _ = solve(df, [], models, partitionOn=partition_col, config=config)
    return operation, output


def evaluate_results(output, df_dirty, df_clean, set_columns):
    """
    计算并输出修复的精度和召回率。

    参数：
    output (DataFrame): 修复后的DataFrame。
    df_dirty (DataFrame): 原始脏数据。
    df_clean (DataFrame): 清洁数据。
    set_columns (list): 需要比较的列。

    返回：
    None
    """
    total_repair = getErrorNum(output, df_dirty, set_columns)
    now_error = getErrorNum(output, df_clean, set_columns)
    total_error = getErrorNum(df_dirty, df_clean, set_columns)

    correct_repairs = getCorrectRepairs(df_clean, output, df_dirty, set_columns)

    precision = correct_repairs / total_repair if total_repair > 0 else 0
    recall = correct_repairs / total_error if total_error > 0 else 0

    print(f"Total Repairs: {total_repair}")
    print(f"Correct Repairs: {correct_repairs}")
    print(f"Current Errors: {now_error}")
    print(f"Total Errors: {total_error}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")


def main():
    print("Logs saved in " + environ.logfilename)

    # 数据路径
    dirty_data_path = '../testdata/gooddata/tax_200k/dirty_mix_0.5/dirty_tax.csv'
    clean_data_path = '../testdata/gooddata/tax_200k/tax_200k_clean.csv'
    set_columns = ["zip", "state", "city", "fname", "gender", "areacode"]

    # 加载数据
    df_dirty, df_clean = load_and_prepare_data(dirty_data_path, clean_data_path, ['zip', 'areacode', 'salary', 'rate'])
    df=df_dirty.copy(deep=True)
    # # 初始错误计算
    # error_num00 = getErrorNum(df_dirty[100:200], df_clean[100:200], set_columns)
    # print(f"Initial Errors (Subset): {error_num00}")
    #
    # error_num01 = getErrorNum(df_dirty, df_clean, set_columns)
    # print(f"Initial Errors (Full Set): {error_num01}")

    # 定义模型和patterns
    patterns, models, models1, models2 = define_patterns_and_models()

    # 配置解决器
    config = DEFAULT_SOLVER_CONFIG
    config['dependency']['depth'] = 3

    # 清洗数据
    time_start = time.time()

    operation, output = solve_data(df, models, config, "zip")
    operation, output = solve_data(output, models1, config, "fname")
    operation, output = solve_data(output, models2, config, "areacode")

    time_end = time.time()
    print(f'Cleaning operation: {operation}')
    print(f'Time cost: {time_end - time_start} s')

    # 保存修复后的数据
    output.to_csv('../testdata/Tax/tax200k_repair_dep.csv')

    # 评估修复结果
    # evaluate_results(output, df_dirty, df_clean, set_columns)
    # 计算准确率和召回率
    calculate_accuracy_and_recall(df_clean, df_dirty, output, set_columns)


if __name__ == "__main__":
    main()