import os
import pandas as pd

# 定义文件路径
base_dir = "Data/5_tax/tax_50k"
clean_file = os.path.join(base_dir, "tax_50k_clean_id.csv")
dirty_dir = os.path.join(base_dir, "noise_with_correct_primary_key/dirty_mix_")

# 比例列表
proportions = ["0.25", "0.5", "0.75", "1", "1.25", "1.5", "1.75", "2"]

# 添加索引列的函数
def add_index_column(file_path):
    """
    读取 CSV 文件，添加索引列，然后覆盖写回原文件。
    """
    try:
        # 读取文件
        df = pd.read_csv(file_path)
        # 添加索引列
        df.insert(0, "index", range(1, len(df) + 1))
        # 保存文件（覆盖原文件）
        df.to_csv(file_path, index=False)
        print(f"已成功处理文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")

# 为 clean 文件添加索引列
add_index_column(clean_file)

# 为 dirty 文件添加索引列
for proportion in proportions:
    dirty_file = os.path.join(dirty_dir + proportion, f"dirty_tax_mix_{proportion}.csv")
    add_index_column(dirty_file)