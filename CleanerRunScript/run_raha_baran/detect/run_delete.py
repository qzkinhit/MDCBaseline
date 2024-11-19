########################################
# Script for repairing by deleting rows with too many errors
########################################
import argparse
import os
import shutil
import sys
import time
import pandas as pd
# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Baran_Raha.repairing_with_delete import Detection
from util.getScore import calculate_accuracy_and_recall

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirty_path', type=str, default='../../Data/1_hospitals/dirty.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospitals/clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, help="Task name (dataset name)", default='test_DELETE')
    parser.add_argument('--output_path', type=str, default='../../results/raha_baran',
                        help='Path to save the output results.')

    args = parser.parse_args()

    # Retrieve paths and task name from the arguments
    clean_path = args.clean_path
    dirty_path = args.dirty_path
    task_name = args.task_name
    output_path = args.output_path

    # Load data
    rep_df = pd.read_csv(dirty_path)
    clean_df = pd.read_csv(clean_path)

    # Prepare the result path
    stra_path = f"{output_path}/results-{task_name}"
    if os.path.exists(stra_path):
        shutil.rmtree(stra_path)
    dataset_name = task_name

    # Only add .csv extension if it's not already part of the filename
    res_file_name = os.path.basename(dirty_path)
    if not res_file_name.endswith('.csv'):
        res_file_name += ".csv"

    res_path = f"{stra_path}/repaired_{task_name}_{res_file_name}"

    # Create dictionary for the dataset to pass to the detection
    dataset_dictionary = {
        "name": dataset_name,
        "path": dirty_path,
        "clean_path": clean_path
    }
    # Run the detection algorithm
    start_time = time.time()
    app = Detection()
    detection_dictionary = app.run(dataset_dictionary)

    # Track the number of errors per row
    error_dict = {}
    for cell, val in detection_dictionary.items():
        if cell[0] in error_dict:
            error_dict[cell[0]] += 1
        else:
            error_dict[cell[0]] = 1

    # Identify rows to drop based on error count (more than 50% errors)
    drop_list = []
    for row, error_count in error_dict.items():
        if error_count > len(clean_df.columns) * 0.5:
            drop_list.append(row)

    # Drop rows with too many errors
    rep_df = rep_df.drop(drop_list, axis=0)

    # Save the repaired data to CSV
    os.makedirs(os.path.dirname(res_path), exist_ok=True)
    rep_df.to_csv(res_path, index=False)
    print(f"Repaired data saved to {res_path}")

    print("===============================================")
    print("测评性能开始：")

    # 读取干净数据、脏数据和修复后的数据
    clean_data = pd.read_csv(args.clean_path)
    dirty_data = pd.read_csv(args.dirty_path)
    cleaned_data = pd.read_csv(res_path)

    # 根据规则定义的属性集合
    attributes = clean_data.columns.tolist()

    # 调用函数计算修复准确率和召回率
    accuracy, recall = calculate_accuracy_and_recall(clean_data, dirty_data, cleaned_data, attributes, args.output_path, args.task_name)

    # 输出修复的准确率和召回率
    print(f"修复准确率: {accuracy}")
    print(f"修复召回率: {recall}")

    # 定义输出文件路径
    out_path = os.path.join(stra_path, f"{args.task_name}_evaluation.txt")

    print(f"测评结束，详细测评日志见：{out_path}")