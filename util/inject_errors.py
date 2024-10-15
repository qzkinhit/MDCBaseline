import pandas as pd
import numpy as np
import argparse
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='在数据集中注入错误。')
    parser.add_argument('--input', type=str, required=True, help='输入CSV文件的路径（向量化后的数据集）。')
    parser.add_argument('--output', type=str, required=True, help='保存带有注入错误的输出CSV文件的路径。')
    parser.add_argument('--error_type', type=str, required=True, choices=['random', 'system'], help='要注入的错误类型：随机错误或系统错误。')
    parser.add_argument('--percent', type=float, required=True, help='要注入错误的数据百分比。')
    args = parser.parse_args()
    return args

# 注入随机错误（对整行注入错误）
def inject_random_error(df, percent, target_column):
    """
    在指定比例的行中注入随机错误，将这些行的数值特征替换为最大值的3倍，标签列除外。
    """
    # 根据百分比计算要注入错误的行数
    num_samples = int(len(df) * percent / 100)
    
    # 随机选择行
    random_indices = np.random.choice(df.index, size=num_samples, replace=False)
    
    # 对这些行中的每一个数值型特征列，排除标签列，替换值为最大值的3倍
    for col in df.select_dtypes(include=[np.number]).columns:
        if col == target_column:
            continue  # 跳过标签列
        max_value = df[col].max()  # 获取列的最大值
        df.loc[random_indices, col] = max_value * 3  # 将随机选择的行替换为最大值的3倍
    
    return df

# 注入系统错误（对整行注入错误）
def inject_system_error(df, percent, target_column):
    """
    在指定比例的行中注入系统错误，基于模型权重调整特征值，标签列除外。
    """
    # 分离特征和标签
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # 使用 SGD 模型训练
    sgd = SGDClassifier()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    sgd.fit(X_train, y_train)
    
    # 获取特征权重，并选出权重最大的三个特征
    feature_weights = np.abs(sgd.coef_)[0]
    top_3_indices = feature_weights.argsort()[-3:][::-1]
    top_3_features = X.columns[top_3_indices]
    
    # 按照三个最高权重特征对数据进行排序
    df_sorted = df.sort_values(by=top_3_features.tolist(), ascending=False)
    
    # 选取前百分之 x% 的行
    num_samples = int(len(df) * percent / 100)
    top_samples = df_sorted.head(num_samples)
    
    # 对于选定的行，替换这三个最高权重特征的值为均值
    for feature in top_3_features:
        mean_value = df[feature].mean()  # 计算全数据集中该特征的均值
        df.loc[top_samples.index, feature] = mean_value  # 将这些行中该特征的值替换为均值
    
    return df

# 主函数
def main():
    # 解析命令行参数
    args = parse_arguments()
    
    # 加载数据集
    df = pd.read_csv(args.input)
    
    # 设定最后一列为标签列
    target_column = df.columns[-1]
    
    # 进行错误注入
    if args.error_type == 'random':
        print(f'Injecting random errors into {args.percent}% of the dataset...')
        df_with_errors = inject_random_error(df, args.percent, target_column)
    elif args.error_type == 'system':
        print(f'Injecting system errors into {args.percent}% of the dataset...')
        df_with_errors = inject_system_error(df, args.percent, target_column)
    
    # 保存结果到输出文件
    df_with_errors.to_csv(args.output, index=False)
    print(f'Injected errors saved to {args.output}')

if __name__ == '__main__':
    main()
