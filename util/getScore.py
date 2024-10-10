import os
import sys


def calculate_accuracy_and_recall(clean, dirty, cleaned, attributes, output_path, task_name):
    """
    计算指定属性集合下的修复准确率和召回率，并将结果输出到文件中

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :return: 修复准确率和召回率
    """
    # 创建结果存储目录
    os.makedirs(output_path, exist_ok=True)

    # 定义输出文件路径
    out_path = os.path.join(output_path, f"{task_name}_evaluation.txt")

    # 备份原始的标准输出
    original_stdout = sys.stdout

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件

        total_true_positives = 0
        total_false_positives = 0
        total_true_negatives = 0

        for attribute in attributes:
            # 确保所有属性的数据类型为字符串
            clean_values = clean[attribute].astype(str)
            dirty_values = dirty[attribute].astype(str)
            cleaned_values = cleaned[attribute].astype(str)

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

            # 打印 dirty_values 和 clean_values 不同的那些行及其索引
            mismatched_indices = dirty_values[dirty_values != clean_values].index
            print("打印 dirty_values 和 clean_values 不同的那些行")
            print(f"Dirty Values at mismatched indices:\n{dirty_values.loc[mismatched_indices]}")
            print(f"Clean Values at mismatched indices:\n{clean_values.loc[mismatched_indices]}")
            print("=" * 40)

            # 打印修复错误的数据
            print("打印没修复的数据")
            false_positives_indices = cleaned_values[
                (cleaned_values != clean_values) & (dirty_values == cleaned_values)].index
            print(f"Dirty Values at false positive indices:\n{dirty_values.loc[false_positives_indices]}")
            print(f"Clean Values at false positive indices:\n{clean_values.loc[false_positives_indices]}")
            print(f"Cleaned Values at false positive indices:\n{cleaned_values.loc[false_positives_indices]}")

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

    return accuracy, recall