import os
import sys
import argparse
import time
import re

import pandas as pd
# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from util.insert_null import inject_missing_values

from Cleaner.Holistic_BigDansing.bigdansing import BigDansing
import multiprocessing
from datetime import datetime
from util.getScore import calculate_accuracy_and_recall, calculate_all_metrics

def check_string(string: str):
    if re.search(r"-inner_error-", string):
        return "-inner_error-" + string[-6:-4]
    elif re.search(r"-outer_error-", string):
        return "-outer_error-" + string[-6:-4]
    elif re.search(r"-inner_outer_error-", string):
        return "-inner_outer_error-" + string[-6:-4]
    elif re.search(r"-dirty-original_error-", string):
        return "-original_error-" + string[-9:-4]
    else:
        return ""

def run_big_dansing(task_name, output_path,PERFECTED, ONLYED, rule_path, dirty_path, clean_path):
    bd = BigDansing(task_name,output_path,PERFECTED, ONLYED)
    bd.run(rule_path, dirty_path, clean_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean_path', type=str, default="../../Data/2_flights/clean.csv")
    parser.add_argument('--dirty_path', type=str, default="../../Data/2_flights/dirty.csv")
    parser.add_argument('--rule_path', type=str, default="../../Data/2_flights/dc_rules_holoclean.txt")
    parser.add_argument('--task_name', type=str, default="bigdansing_flights_test0")
    parser.add_argument('--output_path', type=str,default="../../results/bigdansing/")
    parser.add_argument('--onlyed', type=int, default=0)
    parser.add_argument('--perfected', type=int, default=0)
    parser.add_argument('--index_attribute', type=str, default='index')
    args = parser.parse_args()

    dirty_path = args.dirty_path
    clean_path = args.clean_path
    rule_path = args.rule_path
    task_name = args.task_name
    output_path=args.output_path
    ONLYED = args.onlyed
    PERFECTED = args.perfected
    index_attribute = args.index_attribute
    stra_path =os.path.join(output_path, "Repaired_res", task_name[:-1])
    res_path = os.path.join(output_path, "Repaired_res", task_name[:-1],
                                    "repaired_" + task_name + check_string(
                                        dirty_path.split("/")[-1]) + ".csv")

    # 设置超时时间（秒）
    time_limit = 24 * 3600  # 24小时
    
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
    print(f"Running bigdansing with dirty file: {args.dirty_path}")
    process = multiprocessing.Process(target=run_big_dansing, args=(task_name, output_path,PERFECTED, ONLYED, rule_path, dirty_path, clean_path))
    process.start()
    process.join(time_limit)
    if process.is_alive():
        process.terminate()
        process.join()
        print("Time exceeded:", task_name, dirty_path)
        with open("./aggre_results/timeout_log.txt", "a") as out_file:
            now = datetime.now()
            out_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            out_file.write(f" BigDansing.py: {task_name} {dirty_path}\n")

    print("===============================================")
    # 记录结束时间并计算总耗时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Results saved to {res_path}")
    print(f"BigDansing finished in {elapsed_time} seconds.")
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
                                    index_attribute)

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
