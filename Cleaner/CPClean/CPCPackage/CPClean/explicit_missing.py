import pandas as pd
import os

# 读取两个 CSV 文件
file1 = 'D:\PyCharm\PycharmProjects\MDCBaseline\Data\har\har_data_vectorized.csv'
file2 = 'D:\PyCharm\PycharmProjects\MDCBaseline\Data\har\har_systematic_5.csv'
def contrast(file1, file2, file3):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # 确保两个 DataFrame 的形状相同
    if df1.shape != df2.shape:
        print("Warning: The two files have different shapes. Please check the data.")
    else:
        # 比较两个 DataFrame 中不同的值，将不同的值置为 NaN
        result = df1.copy()  # 创建一个副本
        result[df1 != df2] = None  # 如果值不同，就置为空（None 或 NaN）

        # 计算不同的值的数量
        total_values = df1.size  # 总的值的数量（包括所有行和列）
        different_values = (df1 != df2).sum().sum()  # 计算不同值的数量

        # 计算不同值占总值的百分比
        percentage_diff = (different_values / total_values) * 100

        # 输出结果到一个新的 CSV 文件
        result.to_csv(file3, index=False)

# 指定要遍历的文件夹路径
folder_path = 'D:\PyCharm\PycharmProjects\MDCBaseline\Data\\soilmoisture'


vector_file = ""
# 使用 os.walk 遍历文件夹中的文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if "vectorized" in file:
            file_path = os.path.join(root, file)  # 获取完整的文件路径
            vector_file = file_path

# 要创建的文件夹路径
folder_name = folder_path + '\explicit_for_CPClean'

# 创建文件夹（如果不存在）
os.makedirs(folder_name, exist_ok=True)

# 获取并返回文件夹的绝对路径
absolute_path = os.path.abspath(folder_name)

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if "systematic" in file:
            file_path = os.path.join(root, file)  # 获取完整的文件路径
            cp_path = os.path.join(absolute_path, file)
            contrast(vector_file, file_path, cp_path)