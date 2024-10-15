import os
import sys
import argparse
import time

import pandas as pd

# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Horizon.horizon import Horizon
from util.getScore import calculate_accuracy_and_recall, calculate_all_metrics


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Run Horizon data cleaning script.')

    # 定义命令行参数，default 设为你之前的默认路径
    parser.add_argument('--dirty_path', type=str,
                        default='../../Data/1_hospital/dirty.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--rule_path', type=str, default='../../Data/1_hospital/dc_rules-validate-fd-horizon.txt',
                        help='Path to the input rule file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospital/clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, default='hospital_test',
                        help='Task name for the cleaning process.')
    parser.add_argument('--output_path', type=str, default='../../results/horizon/',
                        help='Path to save the output results.')

    # 解析命令行参数
    args = parser.parse_args()
    stra_path = os.path.join(args.output_path, f"{args.task_name}")
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(stra_path):
        os.makedirs(stra_path)
    # 执行数据清洗操作，获取修复结果和脏单元格
    # 记录开始时间
    start_time = time.time()
    print(f"Running Horizon with dirty file: {args.dirty_path}")
    pattern_expressions, dirty_c, _ = Horizon(
        args.dirty_path, args.rule_path, args.clean_path
    )
    # 保存修复后的数据
    res_path = os.path.join(stra_path, f"{args.task_name}_repaired.csv")
    res_df = pd.read_csv(args.dirty_path, dtype={'ZipCode': str, 'PhoneNumber': str})
    for i in range(len(res_df)):
        for v in pattern_expressions[i]:
            value_to_assign = pattern_expressions[i][v]
            try:
                value_to_assign = int(value_to_assign)
            except ValueError:
                pass
            res_df.loc[i, v] = value_to_assign

    res_df.to_csv(res_path, index=False)
    print("===============================================")
    # 记录结束时间并计算总耗时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Results saved to {res_path}")
    print(f"Horizon finished in {elapsed_time} seconds.")
    print("测评性能开始：")
    # 读取干净数据、脏数据和修复后的数据
    clean_data = pd.read_csv(args.clean_path)
    dirty_data = pd.read_csv(args.dirty_path)
    cleaned_data = pd.read_csv(res_path)

    # 根据规则定义的属性集合
    attributes = clean_data.columns.tolist()

    # 调用函数并计算所有指标
    results = calculate_all_metrics(clean_data, dirty_data, cleaned_data, attributes, stra_path, args.task_name)

    # 打印结果
    print("测试结果:")
    print(f"Accuracy: {results.get('accuracy')}")
    print(f"Recall: {results.get('recall')}")
    print(f"F1 Score: {results.get('f1_score')}")
    print(f"EDR: {results.get('edr')}")
    print(f"Hybrid Distance: {results.get('hybrid_distance')}")
    print(f"R-EDR: {results.get('r_edr')}")
    print(f"time(s): {elapsed_time}")
    print("测评结束，详细测评日志见：" + str(stra_path))


if __name__ == "__main__":
    main()
