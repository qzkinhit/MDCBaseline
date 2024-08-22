import environ
import pandas as pd
from dataclean.constraint_languages.ic import *
from dataclean.constraint_languages.ic import DictValue
from dataclean.constraint_languages.pattern import Pattern
import time
import numpy as np
from dataclean.search import *
import matplotlib.pyplot as plt
from util.getNum import calculate_accuracy_and_recall


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
    list: 编辑规则模型列表。
    """
    models = []

    # 定义字典模型
    models += [DictValue('HospitalType', {'acute care hospitals'})]
    models += [DictValue('EmergencyService', {'no', 'yes'})]
    models += [DictValue('State', {'ak', 'al'})]
    models += [DictValue('Condition', {'pneumonia', 'heart attack', 'surgical infection prevention', 'heart failure',
                                       'children s asthma care'})]
    models += [
        DictValue('HospitalOwner', {'voluntary non-profit - church', 'government - local', 'government - federal',
                                    'voluntary non-profit - private', 'voluntary non-profit - other',
                                    'proprietary', 'government - state',
                                    'government - hospital district or authority'})]

    # 定义OneDeterminedOne模型
    models.append(OneDeterminedOne(["HospitalName"], ["ProviderNumber"]))
    models.append(OneDeterminedOne(["ProviderNumber"], ["HospitalName"]))
    models.append(OneDeterminedOne(["Condition", "MeasureName"], ["HospitalType"]))
    models.append(OneDeterminedOne(["HospitalName", "PhoneNumber", "HospitalOwner"], ["State"]))
    models.append(OneDeterminedOne(["HospitalName"], ["ZipCode"]))
    models.append(OneDeterminedOne(["MeasureCode"], ["MeasureName"]))
    models.append(OneDeterminedOne(["HospitalName"], ["PhoneNumber"]))
    models.append(OneDeterminedOne(["PhoneNumber"], ["HospitalName"]))
    models.append(OneDeterminedOne(["MeasureName"], ["MeasureCode"]))
    models.append(OneDeterminedOne(["MeasureCode"], ["Stateavg"]))
    models.append(OneDeterminedOne(["ProviderNumber"], ["HospitalName"]))
    models.append(OneDeterminedOne(["MeasureCode"], ["Condition"]))
    models.append(OneDeterminedOne(["HospitalName"], ["Address1"]))
    models.append(OneDeterminedOne(["HospitalName"], ["HospitalOwner"]))
    models.append(OneDeterminedOne(["City"], ["CountyName"]))
    models.append(OneDeterminedOne(["ZipCode"], ["EmergencyService"]))
    models.append(OneDeterminedOne(["HospitalName"], ["City"]))

    return models


def solve_and_clean_data(df, models, config):
    """
    使用编辑规则模型清洗数据。

    参数：
    df (DataFrame): 需要清洗的DataFrame。
    models (list): 编辑规则模型列表。
    config (dict): 配置字典。

    返回：
    DataFrame: 清洗后的DataFrame。
    """
    random.shuffle(models)  # 打乱模型顺序

    # 初始解决
    operation, output, _ = solve(df, [], [models[0]], partitionOn=list(models[0].source)[0], config=config)

    # 逐个应用其他模型
    for cleaner in models[1:]:
        try:
            operation, output, _ = solve(output, [], [cleaner], partitionOn=list(cleaner.source)[0], config=config)
        except:
            operation, output, _ = solve(output, [], [cleaner], config=config)

    return output


def main():
    # 加载数据并准备
    dirty_data_path = '../testdata/gooddata/hospitals/dirty_mix_0.5/dirty_hospitals.csv'
    clean_data_path = '../testdata/gooddata/hospitals/hospital_clean1.csv'
    columns_to_cast = ['ProviderNumber', 'ZipCode', 'PhoneNumber']

    df_dirty, df_clean = load_and_prepare_data(dirty_data_path, clean_data_path, columns_to_cast)

    # 选取的列
    selected_columns = ['Address1', 'City', 'Condition', 'CountyName', 'EmergencyService', 'HospitalName',
                        'HospitalOwner', 'HospitalType', 'MeasureCode', 'MeasureName', 'PhoneNumber', 'ProviderNumber',
                        'State', 'Stateavg', 'ZipCode']
    df_dirty_selected = df_dirty[selected_columns].copy(deep=True)
    df_clean_selected = df_clean[selected_columns].copy(deep=True)

    # 计算初始错误数据个数
    error_num = df_dirty_selected.compare(df_clean_selected).notnull().sum().sum() / 2

    # 定义patterns和模型
    models = define_patterns_and_models()

    # 配置解决器
    config = DEFAULT_SOLVER_CONFIG
    config['pattern']['operations'] = [Swap]
    config['dependency']['depth'] = 1

    # 清洗数据
    time_start = time.time()
    cleaned_df = solve_and_clean_data(df_dirty_selected, models, config)
    time_end = time.time()

    # 计算准确率和召回率
    calculate_accuracy_and_recall(df_clean_selected, df_dirty, cleaned_df, selected_columns)

    # 打印时间成本
    print('time cost', time_end - time_start, 's')


if __name__ == "__main__":
    main()