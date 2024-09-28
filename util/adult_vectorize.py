import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import argparse

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='Adult dataset vectorization and label conversion.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file (cleaned Adult dataset).')
    parser.add_argument('--output', type=str, required=True, help='Path to save the output CSV file (vectorized dataset).')
    args = parser.parse_args()
    return args

# 主函数
def main():
    # 解析命令行参数
    args = parse_arguments()

    # 加载 Adult 数据集
    file_path = args.input
    df = pd.read_csv(file_path)

    # 将 'income' 列的 '<50K' 映射为 0， '>50K' 映射为 1
    df['income'] = df['income'].apply(lambda x: 0.0 if x == '<=50K' else 1.0)

    # 分离特征和标签
    X = df.drop(columns=['income'])  # 特征
    y = df['income']  # 标签

    # 定义数值型特征和类别型特征
    numeric_features = ['age', 'fnlwgt', 'education-num', 'hours-per-week']
    categorical_features = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']

    # 构建特征转换器
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),  # 标准化数值型特征
            ('cat', OneHotEncoder(), categorical_features)  # 独热编码类别型特征
        ])

    # 将预处理步骤整合为流水线
    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

    # 进行特征向量化转换
    X_transformed = pipeline.fit_transform(X)

    # 将转换后的数据转换为 DataFrame
    # 获取独热编码后的类别特征名称，兼容旧版本的 get_feature_names 方法
    encoded_feature_names = pipeline.named_steps['preprocessor'].transformers_[1][1].get_feature_names(categorical_features)
    feature_names = numeric_features + list(encoded_feature_names)

    # 转换为 DataFrame 格式
    X_transformed_df = pd.DataFrame(X_transformed.toarray(), columns=feature_names)

    # 添加标签列
    X_transformed_df['income'] = y.reset_index(drop=True)

    # 保存向量化后的数据到 CSV 文件
    output_file_path = args.output
    X_transformed_df.to_csv(output_file_path, index=False)

    # 输出文件路径
    print(f"向量化后的数据已保存为: {output_file_path}")

if __name__ == '__main__':
    main()
