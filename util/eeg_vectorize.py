import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
from scipy.io import arff
import argparse

# 定义解析命令行参数的函数
def parse_args():
    parser = argparse.ArgumentParser(description="EEG 数据统计特征提取工具（按时间步处理，保留标签）")
    parser.add_argument('--input', type=str, required=True, help="输入的 .arff 文件路径")
    parser.add_argument('--output', type=str, required=True, help="保存提取特征的 CSV 文件路径")
    return parser.parse_args()

# 提取按时间步的统计特征，并保留标签
def extract_statistical_features_by_time_step(df, label_column):
    features = pd.DataFrame()

    # 对每一行（每个时间步）进行统计特征提取
    for index, row in df.iterrows():
        features.loc[index, 'mean'] = np.mean(row.drop(label_column))  # 排除标签列
        features.loc[index, 'variance'] = np.var(row.drop(label_column))
        features.loc[index, 'max'] = np.max(row.drop(label_column))
        features.loc[index, 'min'] = np.min(row.drop(label_column))
        features.loc[index, 'median'] = np.median(row.drop(label_column))
        features.loc[index, 'kurtosis'] = kurtosis(row.drop(label_column))
        features.loc[index, 'skewness'] = skew(row.drop(label_column))

        # 保留标签信息
        features.loc[index, 'label'] = row[label_column]

    return features

# 主程序
if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()

    # 读取 EEG Eye State 数据集
    data, meta = arff.loadarff(args.input)
    df = pd.DataFrame(data)

    # 如果需要将字符串数据转换为数值型
    df = df.apply(pd.to_numeric, errors='ignore')

    # 假设标签列为最后一列，可以根据具体的标签列名或位置修改
    label_column = df.columns[-1]

    # 提取统计特征，保留标签
    features = extract_statistical_features_by_time_step(df, label_column)

    # 保存提取的特征到CSV文件
    features.to_csv(args.output, index=False)

    print(f"统计特征提取完成，已保存至 {args.output}")
