import os
import sys
import argparse
import time

import pandas as pd

# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Holoclean.Holoclean import Holoclean
from util.getScore import calculate_accuracy_and_recall, calculate_all_metrics
from util.insert_null import inject_missing_values


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Run Holoclean data cleaning script.')

    # 定义命令行参数，default 设为你之前的默认路径
    parser.add_argument('--dirty_path', type=str,
                        default='../../Data/1_hospital/dirty.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--rule_path', type=str, default='../../Data/1_hospital/dc_rules-validate-fd-Holoclean.txt',
                        help='Path to the input rule file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospital/clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, default='hospital_test',
                        help='Task name for the cleaning process.')
    parser.add_argument('--output_path', type=str, default='../../results/Holoclean/',
                        help='Path to save the output results.')
    parser.add_argument('--index_attribute', type=str, default='index',
                        help='index_attribute of data')
    parser.add_argument('--mse_attributes', type=str, nargs='*', default=[],
                        help='List of attributes to calculate MSE, separated by space. Example: --mse_attributes Attribute1 Attribute3')
    # 解析命令行参数
    args = parser.parse_args()
    mse_attributes = args.mse_attributes
    stra_path = os.path.join(args.output_path, f"{args.task_name}")
    index_attribute = args.index_attribute
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(stra_path):
        os.makedirs(stra_path)
    # 执行数据清洗操作，获取修复结果和脏单元格
    # 替换数据中的空值，统一转换为empty
    inject_missing_values(
        csv_file=args.clean_path,
        output_file=args.clean_path,
        attributes_error_ratio=None,
        missing_value_in_ori_data='NULL',
        missing_value_representation='empty'
    )
    inject_missing_values(
        csv_file=args.dirty_path,
        output_file=args.dirty_path,
        attributes_error_ratio=None,
        missing_value_in_ori_data='NULL',
        missing_value_representation='empty'
    )
    # 记录开始时间
    start_time = time.time()

    print(f"Running Holoclean with dirty file: {args.dirty_path}")

    #超，关注这里，这里运行Holoclean程序，输入必要的几个参数，同时返回清洗后的数据
    # res_df= Holoclean(
    #     args.dirty_path, args.rule_path, args.clean_path,XXX
    # )
    # 保存修复后的数据
    res_path = os.path.join(stra_path, f"{args.task_name}_repaired.csv")
    #重点：保证清洗后数据存在res_path目录下
    #res_df.to_csv(res_path, index=False)
    # print("===============================================")

    # 记录结束时间并计算总耗时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Results saved to {res_path}")
    print(f"Holoclean finished in {elapsed_time} seconds.")


    print("测评性能开始：")
    # 读取干净数据、脏数据和修复后的数据
    inject_missing_values(
        csv_file=res_path,
        output_file=res_path,
        attributes_error_ratio=None,
        missing_value_in_ori_data='NULL',
        missing_value_representation='empty'
    )
    clean_data = pd.read_csv(args.clean_path)
    dirty_data = pd.read_csv(args.dirty_path)
    cleaned_data = pd.read_csv(res_path)

    # 根据规则定义的属性集合
    attributes = clean_data.columns.tolist()
    # 调用函数并计算所有指标
    results = calculate_all_metrics(clean_data, dirty_data, cleaned_data, attributes, stra_path, args.task_name,
                                    index_attribute=index_attribute, mse_attributes=mse_attributes)
    # 定义输出文件路径
    results_path = os.path.join(stra_path, f"{args.task_name}_total_evaluation.txt")
    # 备份原始的标准输出
    original_stdout = sys.stdout
    # 重定向输出到文件
    with open(results_path, 'w', encoding='utf-8') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件
        # 打印结果
        print("测试结果:")
        print(f"Accuracy: {results.get('accuracy')}")
        print(f"Recall: {results.get('recall')}")
        print(f"F1 Score: {results.get('f1_score')}")
        print(f"EDR: {results.get('edr')}")
        print(f"Hybrid Distance: {results.get('hybrid_distance')}")
        print(f"R-EDR: {results.get('r_edr')}")
        print(f"Time: {elapsed_time}")
        print(f"speed: {100*float(elapsed_time)/clean_data.shape[0]} seconds/100num")
    # 恢复标准输出
    sys.stdout = original_stdout
    print("测评结束，详细测评日志见：" + str(stra_path))
    # results = calculate_all_metrics(clean_data, dirty_data, cleaned_data, attributes, stra_path, args.task_name,
    #                                 index_attribute=index_attribute, mse_attributes=mse_attributes)
    #
    # # 打印结果
    # print("测试结果:")
    # print(f"Accuracy: {results.get('accuracy')}")
    # print(f"Recall: {results.get('recall')}")
    # print(f"F1 Score: {results.get('f1_score')}")
    # print(f"EDR: {results.get('edr')}")
    # print(f"Hybrid Distance: {results.get('hybrid_distance')}")
    # print(f"R-EDR: {results.get('r_edr')}")
    # print(f"time(s): {elapsed_time}")
    # print("测评结束，详细测评日志见：" + str(stra_path))


if __name__ == "__main__":
    main()
