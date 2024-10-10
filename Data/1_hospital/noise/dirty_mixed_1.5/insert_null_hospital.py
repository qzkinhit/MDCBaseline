import os
import sys

# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from util.insert_null import inject_missing_values

# 属性列表
attributes = [
    "ProviderNumber",
    "HospitalName",
    "Address1",
    "Address2",
    "Address3",
    "City",
    "State",
    "ZipCode",
    "CountyName",
    "PhoneNumber",
    "HospitalType",
    "HospitalOwner",
    "EmergencyService",
    "Condition",
    "MeasureCode",
    "MeasureName",
    "Score",
    "Sample",
    "Stateavg"
]

# 每个属性注入1.5%的错误比例
attributes_error_ratio = {attribute: 1.5 for attribute in attributes}

inject_missing_values(
    csv_file='dirty_hospitals.csv',
    output_file='dirty_hospitals_null.csv',
    attributes_error_ratio=attributes_error_ratio,
    missing_value_in_ori_data='NULL',
    missing_value_representation='empty'
)

inject_missing_values(
    csv_file='../../clean_index.csv',
    output_file='../../clean_index.csv',
    attributes_error_ratio=None,
    missing_value_in_ori_data='NULL',
    missing_value_representation='empty'
)
