import os
import sys
import argparse
import pandas as pd

# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Horizon.horizon import Horizon
from util.getScore import calculate_accuracy_and_recall


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Run Horizon data cleaning script.')

    # 定义命令行参数，default 设为你之前的默认路径
    parser.add_argument('--dirty_path', type=str, default='../../Data/1_hospital/noise_with_correct_primary_key/dirty_mix_0.5/dirty_hospitals.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--rule_path', type=str, default='../../Data/1_hospital/dc_rules-validate-fd-horizon.txt',
                        help='Path to the input rule file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospital/hosptial_clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, default='hospital_test',
                        help='Task name for the cleaning process.')
    parser.add_argument('--output_path', type=str, default='../../results/horizon/hospital_test',
                        help='Path to save the output results.')

    # 解析命令行参数
    args = parser.parse_args()

    # 执行数据清洗操作，获取修复结果和脏单元格
    print(f"Running Horizon with dirty file: {args.dirty_path}")
    pattern_expressions, dirty_c, elapsed_time = Horizon(
        args.dirty_path, args.rule_path, args.clean_path
    )
    # 保存修复后的数据
    res_path = os.path.join(args.output_path, f"{args.task_name}_repaired.csv")
    res_df = pd.read_csv(args.dirty_path)
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
    print(f"Results saved to {res_path}")
    print(f"Horizon finished in {elapsed_time} seconds.")
    print("测评性能开始：")
    # 读取干净数据、脏数据和修复后的数据
    clean_data = pd.read_csv(args.clean_path)
    dirty_data = pd.read_csv(args.dirty_path)
    cleaned_data = pd.read_csv(args.output_path+'/'+args.task_name+'_repaired.csv')

    # 根据规则定义的属性集合
    attributes = clean_data.columns.tolist()

    # 调用函数计算修复准确率和召回率
    accuracy, recall = calculate_accuracy_and_recall(clean_data, dirty_data, cleaned_data, attributes, args.output_path, args.task_name)

    # 输出修复的准确率和召回率
    print(f"修复准确率: {accuracy}")
    print(f"修复召回率: {recall}")
    # 定义输出文件路径
    out_path = os.path.join(args.output_path, f"{args.task_name}_evaluation.txt")

    print("测评结束，详细测评日志见："+str(out_path))


if __name__ == "__main__":
    main()

# python run_horizon_base.py --dirty_path ../../Data/1_hospital/test/dirty_hospitals.csv --rule_path ../../Data/1_hospital/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/1_hospital/hospital_clean_index.csv --task_name hospital_horizon_test --output_path ../../results/horizon/hospital_horizon_test
