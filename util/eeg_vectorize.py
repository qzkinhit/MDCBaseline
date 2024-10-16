import pandas as pd
from scipy.io import arff
from sklearn.preprocessing import StandardScaler
import argparse

# 1. 读取 ARFF 文件
def load_arff_data(file_path):
    data, meta = arff.loadarff(file_path)
    df = pd.DataFrame(data)
    return df

# 2. 提取 EEG 特征和处理标签列
def extract_features_and_labels(df):
    # 直接将前14列EEG数据通道作为特征
    eeg_features = df.iloc[:, :14]  # 前14列为EEG信号数据
    
    # 标签列 eyeDetection，转换为整数
    eeg_labels = df['eyeDetection'].apply(lambda x: int(x.decode('utf-8')))
    
    return eeg_features, eeg_labels

# 3. 对特征进行标准化
def standardize_features(eeg_features):
    scaler = StandardScaler()
    standardized_features = scaler.fit_transform(eeg_features)
    return pd.DataFrame(standardized_features, columns=eeg_features.columns)

# 4. 保存为CSV文件
def save_to_csv(features, labels, output_path):
    standardized_data = features.copy()
    standardized_data['eyeDetection'] = labels  # 将标签加入标准化后的数据
    standardized_data.to_csv(output_path, index=False)
    print(f"标准化后的数据已保存到: {output_path}")

# 主函数：加载ARFF数据、标准化并保存
def main(input_file, output_file):
    # 加载ARFF数据
    df = load_arff_data(input_file)
    
    # 提取特征和标签
    eeg_features, eeg_labels = extract_features_and_labels(df)
    
    # 对特征进行标准化
    standardized_features = standardize_features(eeg_features)
    
    # 保存为CSV文件
    save_to_csv(standardized_features, eeg_labels, output_file)

# 命令行接口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process EEG ARFF file, standardize features, and save as CSV.')
    
    # 输入文件和输出文件的命令行参数
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input ARFF file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output CSV file.')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行主函数
    main(args.input_file, args.output_file)

