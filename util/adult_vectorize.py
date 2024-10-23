import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import argparse
from scipy.sparse import hstack

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
    numeric_features = ['age', 'fnlwgt', 'education-num', 'hours-per-week', 'capital-gain', 'capital-loss']
    categorical_features = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']

    # 处理数值特征
    numeric_transformer = StandardScaler()

    # 对类别特征进行TF-IDF向量化
    tfidf_vectorizers = {}
    tfidf_features = []

    for col in categorical_features:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_feature = vectorizer.fit_transform(df[col].astype(str))
        tfidf_vectorizers[col] = vectorizer
        tfidf_features.append(tfidf_feature)

    # 将所有类别特征的TF-IDF特征合并
    X_tfidf = hstack(tfidf_features)

    # 对数值特征进行标准化
    X_numeric = numeric_transformer.fit_transform(df[numeric_features])

    # 将数值特征和TF-IDF特征合并
    X_final = hstack([X_numeric, X_tfidf])

    # 将特征矩阵转换为 DataFrame
    numeric_columns = numeric_features
    tfidf_columns = [f"{col}_tfidf_{i}" for col in categorical_features for i in range(tfidf_vectorizers[col].idf_.shape[0])]
    all_columns = numeric_columns + tfidf_columns

    X_transformed_df = pd.DataFrame(X_final.toarray(), columns=all_columns)

    # 添加标签列
    X_transformed_df['income'] = y.reset_index(drop=True)

    # 保存向量化后的数据到 CSV 文件
    output_file_path = args.output
    X_transformed_df.to_csv(output_file_path, index=False)

    # 输出文件路径
    print(f"向量化后的数据已保存为: {output_file_path}")

if __name__ == '__main__':
    main()
