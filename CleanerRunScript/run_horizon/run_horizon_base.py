import os
import sys
import argparse
import pandas as pd
# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Horizon.horizon import Horizon
from Cleaner.Horizon.util import calRepPrec, calRepRec, calF1


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Run Horizon data cleaning script.')

    # 定义命令行参数，default 设为你之前的默认路径
    parser.add_argument('--dirty_path', type=str, default='../../Data/hospital/noise_with_correct_primary_key/dirty_mix_0.5/dirty_hospitals.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--rule_path', type=str, default='../../Data/hospital/dc_rules-validate-fd-horizon.txt',
                        help='Path to the input rule file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/hospital/hosptial_clean_index.csv',
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

    # 计算检测的精度和召回率
    # det_prec, det_rec = calDetPrecRec(pattern_expressions, args.dirty_path, args.clean_path, dirty_c)
    # 计算修复的精度、召回率和 F1 值
    rep_precision = calRepPrec(pattern_expressions, args.dirty_path, args.clean_path)
    rep_recall = calRepRec(pattern_expressions, args.dirty_path, args.clean_path)
    rep_f1 = calF1(rep_precision, rep_recall)

    # 打印评估结果
    # print(f"Detection precision: {det_prec}")
    # print(f"Detection recall: {det_rec}")
    print(f"Repair precision: {rep_precision}")
    print(f"Repair recall: {rep_recall}")
    print(f"Repair F1 score: {rep_f1}")
    print(f"Elapsed time: {elapsed_time} seconds")

    # 创建结果存储目录
    os.makedirs(args.output_path, exist_ok=True)

    # 保存评估结果到文件
    out_path = os.path.join(args.output_path, f"{args.task_name}_evaluation.txt")
    original_stdout = sys.stdout  # 备份原始的标准输出

    # 重定向输出到文件
    with open(out_path, 'w') as f:
        sys.stdout = f  # 将 sys.stdout 重定向到文件
        # print(f"Detection precision: {det_prec}")
        # print(f"Detection recall: {det_rec}")
        print(f"Repair precision: {rep_precision}")
        print(f"Repair recall: {rep_recall}")
        print(f"Repair F1 score: {rep_f1}")
        print(f"Elapsed time: {elapsed_time} seconds")

    # 恢复标准输出
    sys.stdout = original_stdout

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
    print(f"Results saved to {res_path}")


if __name__ == "__main__":
    main()