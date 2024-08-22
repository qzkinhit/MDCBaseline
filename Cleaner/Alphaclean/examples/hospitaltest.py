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


def define_models():
    """
    定义字典和模型规则。

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

    # 定义OneToOne和OneDeterminedOne模型
    models.append(OneToOne(["HospitalName"], ["ProviderNumber"]))
    models.append(OneDeterminedOne(["Condition", "MeasureName"], ["HospitalType"]))
    models.append(OneDeterminedOne(["HospitalName", "PhoneNumber", "HospitalOwner"], ["State"]))
    models.append(OneDeterminedOne(["HospitalName"], ["ZipCode"]))
    models.append(OneToOne(["HospitalName"], ["PhoneNumber"]))
    models.append(OneToOne(["MeasureCode"], ["MeasureName"]))
    models.append(OneDeterminedOne(["MeasureCode"], ["Stateavg"]))
    models.append(OneToOne(["ProviderNumber"], ["HospitalName"]))
    models.append(OneDeterminedOne(["MeasureCode"], ["Condition"]))
    models.append(OneDeterminedOne(["HospitalName"], ["Address1"]))
    models.append(OneDeterminedOne(["HospitalName"], ["HospitalOwner"]))
    models.append(OneDeterminedOne(["City"], ["CountyName"]))
    models.append(OneDeterminedOne(["ZipCode"], ["EmergencyService"]))
    models.append(OneDeterminedOne(["HospitalName"], ["City"]))

    return models


def solve_data(df, models, config):
    """
    使用编辑规则模型清洗数据。

    参数：
    df (DataFrame): 需要清洗的DataFrame。
    models (list): 编辑规则模型列表。
    config (dict): 配置字典。

    返回：
    tuple: (清洗操作, 清洗后的DataFrame)
    """
    try:
        operation, output, _ = solve(df, [], [models[0]], partitionOn=list(models[0].source)[0], config=config)
    except:
        try:
            operation, output, _ = solve(df, [], [models[0]], partitionOn=models[0].attr, config=config)
        except:
            operation, output, _ = solve(df, [], [models[0]], partitionOn=list(models[0].hint)[0], config=config)

    for cleaner in models[1:]:
        try:
            operation, output, _ = solve(output, [], [cleaner], partitionOn=list(cleaner.source)[0], config=config)
        except:
            try:
                operation, output, _ = solve(output, [], [cleaner], partitionOn=cleaner.attr, config=config)
            except:
                operation, output, _ = solve(output, [], [cleaner], partitionOn=list(cleaner.hint)[0], config=config)

    return operation, output


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

    # 定义模型
    models = define_models()

    # 配置解决器
    config = DEFAULT_SOLVER_CONFIG
    config['pattern']['operations'] = [Swap]
    config['dependency']['depth'] = 5

    # 清洗数据
    time_start = time.time()
    operation, output = solve_data(df_dirty_selected, models, config)
    time_end = time.time()

    # 计算错误数
    error_num2 = output.compare(df_clean_selected).notnull().sum().sum() / 2
    print('time cost', time_end - time_start, 's')
    print(f"Initial Errors: {error_num}, Remaining Errors: {error_num2}")

    # 计算准确率和召回率
    calculate_accuracy_and_recall(df_clean_selected, df_dirty, output, selected_columns)

    # 输出结果
    time_cost = time_end - time_start
    print(f'Time Cost: {time_cost}s')


if __name__ == "__main__":
    main()