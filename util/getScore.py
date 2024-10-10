import os
import sys
import pandas as pd
def normalize_value(value):
    """
    将数值规范化为字符串格式，去掉小数点及其后的零
    :param value: 要规范化的值
    :return: 规范化后的字符串
    """
    try:
        # 尝试将值转换为浮点数，再转换为整数，然后转换为字符串
        float_value = float(value)
        if float_value.is_integer():
            return str(int(float_value))  # 去掉小数点及其后的零
        else:
            return str(float_value)
    except ValueError:
        # 如果值无法转换为浮点数，则返回原始值的字符串形式
        return str(value)

def calculate_accuracy_and_recall(clean, dirty, cleaned, attributes, output_path, task_name):
    """
    计算指定属性集合下的修复准确率和召回率，并将结果输出到文件中，同时生成差异 CSV 文件。

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :return: 修复准确率和召回率
    """

    os.makedirs(output_path, exist_ok=True)

    # 定义输出文件路径
    out_path = os.path.join(output_path, f"{task_name}_evaluation.txt")

    # 差异 CSV 文件路径
    clean_dirty_diff_path = os.path.join(output_path, f"{task_name}_clean_vs_dirty.csv")
    dirty_cleaned_diff_path = os.path.join(output_path, f"{task_name}_dirty_vs_cleaned.csv")
    clean_cleaned_diff_path = os.path.join(output_path, f"{task_name}_clean_vs_cleaned.csv")

    # 备份原始的标准输出
    original_stdout = sys.stdout

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件

        total_true_positives = 0
        total_false_positives = 0
        total_true_negatives = 0

        # 创建差异 DataFrame 来保存不同的数据项
        clean_dirty_diff = pd.DataFrame(columns=['Attribute', 'Index', 'Clean Value', 'Dirty Value'])
        dirty_cleaned_diff = pd.DataFrame(columns=['Attribute', 'Index', 'Dirty Value', 'Cleaned Value'])
        clean_cleaned_diff = pd.DataFrame(columns=['Attribute', 'Index', 'Clean Value', 'Cleaned Value'])

        for attribute in attributes:
            # 确保所有属性的数据类型为字符串
            # 确保所有属性的数据类型为字符串并进行规范化
            clean_values = clean[attribute].apply(normalize_value)
            dirty_values = dirty[attribute].apply(normalize_value)
            cleaned_values = cleaned[attribute].apply(normalize_value)

            # 对齐索引
            common_indices = clean_values.index.intersection(cleaned_values.index).intersection(dirty_values.index)
            clean_values = clean_values.loc[common_indices]
            dirty_values = dirty_values.loc[common_indices]
            cleaned_values = cleaned_values.loc[common_indices]

            # 正确修复的数据
            true_positives = ((cleaned_values == clean_values) & (dirty_values != cleaned_values)).sum()
            # 修错的数据
            false_positives = ((cleaned_values != clean_values) & (dirty_values != cleaned_values)).sum()
            # 所有应该需要修复的数据
            true_negatives = (dirty_values != clean_values).sum()

            # 记录干净数据和脏数据之间的差异
            mismatched_indices = dirty_values[dirty_values != clean_values].index
            clean_dirty_diff = pd.concat([clean_dirty_diff, pd.DataFrame({
                'Attribute': attribute,
                'Index': mismatched_indices,
                'Clean Value': clean_values.loc[mismatched_indices],
                'Dirty Value': dirty_values.loc[mismatched_indices]
            })])

            # 记录脏数据和清洗后数据之间的差异
            cleaned_indices = cleaned_values[cleaned_values != dirty_values].index
            dirty_cleaned_diff = pd.concat([dirty_cleaned_diff, pd.DataFrame({
                'Attribute': attribute,
                'Index': cleaned_indices,
                'Dirty Value': dirty_values.loc[cleaned_indices],
                'Cleaned Value': cleaned_values.loc[cleaned_indices]
            })])

            # 记录干净数据和清洗后数据之间的差异
            clean_cleaned_indices = cleaned_values[cleaned_values != clean_values].index
            clean_cleaned_diff = pd.concat([clean_cleaned_diff, pd.DataFrame({
                'Attribute': attribute,
                'Index': clean_cleaned_indices,
                'Clean Value': clean_values.loc[clean_cleaned_indices],
                'Cleaned Value': cleaned_values.loc[clean_cleaned_indices]
            })])

            total_true_positives += true_positives
            total_false_positives += false_positives
            total_true_negatives += true_negatives
            print("Attribute:", attribute, "修复正确的数据:", true_positives, "修复错误的数据:", false_positives,
                  "应该修复的数据:", true_negatives)
            print("=" * 40)

        # 总体修复的准确率
        accuracy = total_true_positives / (total_true_positives + total_false_positives)
        # 总体修复的召回率
        recall = total_true_positives / total_true_negatives

        # 输出最终的准确率和召回率
        print(f"修复准确率: {accuracy}")
        print(f"修复召回率: {recall}")

    # 恢复标准输出
    sys.stdout = original_stdout

    # 保存差异数据到 CSV 文件
    clean_dirty_diff.to_csv(clean_dirty_diff_path, index=False)
    dirty_cleaned_diff.to_csv(dirty_cleaned_diff_path, index=False)
    clean_cleaned_diff.to_csv(clean_cleaned_diff_path, index=False)

    print(f"差异文件已保存到:\n{clean_dirty_diff_path}\n{dirty_cleaned_diff_path}\n{clean_cleaned_diff_path}")

    return accuracy, recall