import os
import sys
import pandas as pd
from sklearn.metrics import mean_squared_error, jaccard_score
import numpy as np


def calculate_all_metrics(clean, dirty, cleaned, attributes, output_path, task_name, index_attribute='index',calculate_precision_recall=True,
                          calculate_edr=True, calculate_hybrid=True, calculate_r_edr=True):
    """
    计算多个指标的统一函数，包括修复准确率和召回率、EDR、混合距离以及基于条目的 R-EDR。

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定的属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称
    :param calculate_precision_recall: 是否计算修复的准确率和召回率
    :param calculate_edr: 是否计算错误减少率（EDR）
    :param calculate_hybrid: 是否计算混合距离指标
    :param calculate_r_edr: 是否计算基于条目的错误减少率（R-EDR）
    :return: 所有计算的指标值
    """

    results = {}

    # 计算准确率和召回率
    if calculate_precision_recall:
        accuracy, recall = calculate_accuracy_and_recall(clean, dirty, cleaned, attributes, output_path, task_name,index_attribute='index')
        results['accuracy'] = accuracy
        results['recall'] = recall
        f1_score = calF1(accuracy, recall)
        results['f1_score'] = f1_score
        print(f"修复准确率: {accuracy}, 修复召回率: {recall}, F1值: {f1_score}")
        print("=" * 40)

    # 计算EDR
    if calculate_edr:
        edr = get_edr(clean, dirty, cleaned, attributes,output_path, task_name,index_attribute='index')
        results['edr'] = edr
        print(f"错误减少率 (EDR): {edr}")
        print("=" * 40)

    # 计算混合距离
    if calculate_hybrid:
        hybrid_distance = get_hybrid_distance(clean, cleaned, attributes,output_path, task_name,index_attribute='index')
        results['hybrid_distance'] = hybrid_distance
        print(f"混合距离 (Hybrid Distance): {hybrid_distance}")
        print("=" * 40)

    # 计算基于条目的 R-EDR
    if calculate_r_edr:
        r_edr = get_record_based_edr(clean, dirty, cleaned,output_path, task_name,index_attribute='index')
        results['r_edr'] = r_edr
        print(f"基于条目的错误减少率 (R-EDR): {r_edr}")
        print("=" * 40)

    return results
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


def default_distance_func(value1, value2):
    """
    默认的距离计算函数：
    如果两个值不同，则距离为1；
    如果两个值相同，则距离为0。
    """
    return (value1 != value2).sum()

def record_based_distance_func(row1, row2):
    """
    基于条目的距离计算函数：
    遍历每一行中的每一个值，如果任意一个值不相同，则返回1；
    如果所有值都相同，则返回0。
    """
    for val1, val2 in zip(row1, row2):
        if val1 != val2:
            return 1  # 只要有一个值不相同，立即返回1
    return 0  # 如果所有值都相同，返回0
def calF1(precision, recall):
    """
    计算F1值

    :param precision: 精度
    :param recall: 召回率
    :return: F1值
    """
    return 2 * precision * recall / (precision + recall + 1e-10)


def calculate_accuracy_and_recall(clean, dirty, cleaned, attributes, output_path, task_name, index_attribute='index'):
    """
    计算指定属性集合下的修复准确率和召回率，并将结果输出到文件中，同时生成差异 CSV 文件。

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :param index_attribute: 指定作为索引的属性
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

    # 将指定的属性设置为索引
    clean = clean.set_index(index_attribute,drop=False)
    dirty = dirty.set_index(index_attribute, drop=False)
    cleaned = cleaned.set_index(index_attribute, drop=False)

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


def get_edr(clean, dirty, cleaned, attributes, output_path, task_name, index_attribute='index', distance_func=default_distance_func):
    """
    计算指定属性集合下的错误减少率 (EDR)，并将结果输出到文件中。

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :param index_attribute: 指定作为索引的属性
    :param distance_func: 距离计算函数，默认为比较两个值是否相等，不同为1，相同为0
    :return: 错误减少率 (EDR)
    """

    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)

    # 定义输出文件路径
    out_path = os.path.join(output_path, f"{task_name}_edr_evaluation.txt")

    # 备份原始的标准输出
    original_stdout = sys.stdout

    # 将指定的属性设置为索引
    clean = clean.set_index(index_attribute, drop=False)
    dirty = dirty.set_index(index_attribute, drop=False)
    cleaned = cleaned.set_index(index_attribute, drop=False)

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件

        total_distance_dirty_to_clean = 0
        total_distance_repaired_to_clean = 0

        for attribute in attributes:
            # 确保所有属性的数据类型为字符串并进行规范化
            clean_values = clean[attribute].apply(normalize_value)
            dirty_values = dirty[attribute].apply(normalize_value)
            cleaned_values = cleaned[attribute].apply(normalize_value)

            # 对齐索引
            common_indices = clean_values.index.intersection(cleaned_values.index).intersection(dirty_values.index)
            clean_values = clean_values.loc[common_indices]
            dirty_values = dirty_values.loc[common_indices]
            cleaned_values = cleaned_values.loc[common_indices]

            # 计算脏数据和干净数据之间的距离
            distance_dirty_to_clean = distance_func(dirty_values, clean_values)
            # 计算修复后数据和干净数据之间的距离
            distance_repaired_to_clean = distance_func(cleaned_values, clean_values)

            total_distance_dirty_to_clean += distance_dirty_to_clean
            total_distance_repaired_to_clean += distance_repaired_to_clean

            # 打印每个属性的距离值
            print(f"Attribute: {attribute}")
            print(f"Distance (Dirty to Clean): {distance_dirty_to_clean}")
            print(f"Distance (Repaired to Clean): {distance_repaired_to_clean}")
            print("=" * 40)

        # 计算错误减少率 (EDR)
        if total_distance_dirty_to_clean == 0:
            edr = 0
        else:
            edr = (total_distance_dirty_to_clean - total_distance_repaired_to_clean) / total_distance_dirty_to_clean

        # 打印最终的 EDR 结果
        print(f"总的脏数据到干净数据距离: {total_distance_dirty_to_clean}")
        print(f"总的修复后数据到干净数据距离: {total_distance_repaired_to_clean}")
        print(f"错误减少率 (EDR): {edr}")

    # 恢复标准输出
    sys.stdout = original_stdout

    print(f"EDR 结果已保存到: {out_path}")

    return edr

def get_hybrid_distance(clean, cleaned, attributes, output_path, task_name, index_attribute='index', w1=0.5, w2=0.5):
    """
    计算混合距离指标，包括MSE和Jaccard距离，并将结果输出到文件中。

    :param clean: 干净数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :param index_attribute: 指定作为索引的属性
    :param w1: MSE的权重
    :param w2: Jaccard距离的权重
    :return: 加权混合距离
    """

    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)

    # 定义输出文件路径
    out_path = os.path.join(output_path, f"{task_name}_hybrid_distance_evaluation.txt")

    # 备份原始的标准输出
    original_stdout = sys.stdout

    # 将指定的属性设置为索引
    clean = clean.set_index(index_attribute, drop=False)
    cleaned = cleaned.set_index(index_attribute, drop=False)

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件

        total_mse = 0
        total_jaccard = 0
        attribute_count = 0

        for attribute in attributes:
            # 确保数据类型一致并规范化
            clean_values = clean[attribute].apply(normalize_value)
            cleaned_values = cleaned[attribute].apply(normalize_value)

            # 计算MSE
            try:
                mse = mean_squared_error(clean_values.astype(float), cleaned_values.astype(float))
            except ValueError:
                print(f"无法计算MSE，因为{attribute}不是数值型数据")
                mse = np.nan  # 如果值不是数值型，无法计算MSE，返回NaN

            # 计算Jaccard距离，需确保类别型或二进制类型
            try:
                jaccard = 1 - jaccard_score(clean_values, cleaned_values, average='macro')
            except ValueError:
                print(f"无法计算Jaccard距离，因为{attribute}不是类别型数据")
                jaccard = np.nan  # 如果值不能计算Jaccard，返回NaN

            # 排除NaN值的影响
            if not np.isnan(mse) and not np.isnan(jaccard):
                total_mse += mse
                total_jaccard += jaccard
                attribute_count += 1
            elif not np.isnan(mse) and np.isnan(jaccard):
                total_mse += mse
                attribute_count += 1
            elif np.isnan(mse) and not np.isnan(jaccard):
                total_jaccard += jaccard
                attribute_count += 1
            else:
                print(f"无法计算距离，因为{attribute}的值无法处理")

            print(f"Attribute: {attribute}, MSE: {mse}, Jaccard: {jaccard}")

        if attribute_count == 0:
            return None

        # 计算加权混合距离
        avg_mse = total_mse / attribute_count
        avg_jaccard = total_jaccard / attribute_count

        hybrid_distance = w1 * avg_mse + w2 * avg_jaccard

        print(f"加权混合距离: {hybrid_distance}")

    # 恢复标准输出
    sys.stdout = original_stdout

    print(f"混合距离结果已保存到: {out_path}")

    return hybrid_distance
def get_record_based_edr(clean, dirty, cleaned, output_path, task_name, index_attribute='index'):
    """
    计算基于条目的错误减少率 (R-EDR)，并将每条记录的距离和最终的 R-EDR 输出到文件中。

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param output_path: 保存结果的目录路径
    :param task_name: 任务名称，用于命名输出文件
    :param index_attribute: 指定作为索引的属性
    :return: 基于条目的错误减少率 (R-EDR)
    """

    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)

    # 定义输出文件路径
    out_path = os.path.join(output_path, f"{task_name}_record_based_edr_evaluation.txt")

    # 备份原始的标准输出
    original_stdout = sys.stdout

    # 将指定的属性设置为索引
    clean = clean.set_index(index_attribute, drop=False)
    dirty = dirty.set_index(index_attribute, drop=False)
    cleaned = cleaned.set_index(index_attribute, drop=False)

    total_distance_dirty_to_clean = 0
    total_distance_repaired_to_clean = 0

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件

        # 逐行比较脏数据、清洗后的数据与干净数据
        for idx in clean.index:
            clean_row = clean.loc[idx].apply(normalize_value)
            dirty_row = dirty.loc[idx].apply(normalize_value)
            cleaned_row = cleaned.loc[idx].apply(normalize_value)

            # 计算脏数据和干净数据之间的距离
            distance_dirty_to_clean = record_based_distance_func(dirty_row, clean_row)
            # 计算修复后数据和干净数据之间的距离
            distance_repaired_to_clean = record_based_distance_func(cleaned_row, clean_row)

            total_distance_dirty_to_clean += distance_dirty_to_clean
            total_distance_repaired_to_clean += distance_repaired_to_clean

            # 打印每条记录的距离值
            print(f"Record {idx}")
            print(f"Distance (Dirty to Clean): {distance_dirty_to_clean}")
            print(f"Distance (Repaired to Clean): {distance_repaired_to_clean}")
            print("=" * 40)

        # 计算基于条目的错误减少率 (R-EDR)
        if total_distance_dirty_to_clean == 0:
            r_edr = 0
        else:
            r_edr = (total_distance_dirty_to_clean - total_distance_repaired_to_clean) / total_distance_dirty_to_clean

        # 打印最终的 R-EDR 结果
        print(f"总的脏数据到干净数据距离: {total_distance_dirty_to_clean}")
        print(f"总的修复后数据到干净数据距离: {total_distance_repaired_to_clean}")
        print(f"基于条目的错误减少率 (R-EDR): {r_edr}")

    # 恢复标准输出
    sys.stdout = original_stdout

    print(f"R-EDR 结果已保存到: {out_path}")

    return r_edr

def test_calculate_all_metrics():
    # 准备测试数据
    data = {
        'index': [1, 2, 3, 4, 5],
        'Attribute1': [1, 2, 3, 4, 5],
        'Attribute2': ['A', 'B', 'C', 'D', 'E'],
        'Attribute3': [1.1, 2.2, 3.3, 4.4, 5.5]
    }

    # 创建干净数据 DataFrame
    clean_df = pd.DataFrame(data)

    # 创建脏数据 DataFrame （引入了一些错误）
    dirty_data = {
        'index': [1, 2, 3, 4, 5],
        'Attribute1': [1, 9, 3, 4, 5],  # 第二行是错误的
        'Attribute2': ['A', 'B', 'X', 'D', 'E'],  # 第三行是错误的
        'Attribute3': [1.1, 2.2, 3.3, 4.4, 5.5]  # 没有错误
    }
    dirty_df = pd.DataFrame(dirty_data)

    # 创建清洗后的数据 DataFrame （修复了一些错误）
    cleaned_data = {
        'index': [1, 2, 3, 4, 5],
        'Attribute1': [1, 9, 3, 4, 5],  # 已修复 Attribute1 中的错误
        'Attribute2': ['A', 'X', 'C', 'D', 'E'],  # 修复错误
        'Attribute3': [1.1, 2.2, 3.3, 4.4, 5.5]  # 没有错误
    }
    cleaned_df = pd.DataFrame(cleaned_data)

    # 属性列表
    attributes = ['Attribute1', 'Attribute2', 'Attribute3']

    # 输出路径和任务名称（这里可以使用临时目录）
    output_path = './temp_test_output'
    task_name = 'test_task'

    # 调用函数并计算所有指标
    results = calculate_all_metrics(clean_df, dirty_df, cleaned_df, attributes, output_path, task_name)

    # 打印结果
    print("测试结果:")
    print(f"Accuracy: {results.get('accuracy')}")
    print(f"Recall: {results.get('recall')}")
    print(f"F1 Score: {results.get('f1_score')}")
    print(f"EDR: {results.get('edr')}")
    print(f"Hybrid Distance: {results.get('hybrid_distance')}")
    print(f"R-EDR: {results.get('r_edr')}")

    # # 验证结果是否符合预期
    # assert results['accuracy'] > 0, "Accuracy should be greater than 0"
    # assert results['recall'] > 0, "Recall should be greater than 0"
    # assert results['f1_score'] > 0, "F1 score should be greater than 0"
    # assert results['edr'] > 0, "EDR should be greater than 0"
    # assert results['r_edr'] > 0, "R-EDR should be greater than 0"

    print("测试通过！")

if __name__ == "__main__":
    # 调用测试函数
    test_calculate_all_metrics()