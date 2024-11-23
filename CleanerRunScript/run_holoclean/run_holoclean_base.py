import os
import sys
import argparse
import time
import pandas as pd



# 获取当前脚本所在目录的上级目录路径
sys.path.append('Cleaner/Holoclean/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
sys.path.append('../../Cleaner/Holoclean/')
from util.get_T_table import transform_csv_file
import Cleaner.Holoclean as holoclean
from Cleaner.Holoclean.detect import NullDetector, ViolationDetector
from Cleaner.Holoclean.repair.featurize import *
from util.getScore import calculate_accuracy_and_recall, calculate_all_metrics
from util.insert_null import inject_missing_values


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Run Holoclean data cleaning script.')

    # 定义命令行参数
    parser.add_argument('--dirty_path', type=str,
                        default='../../Data/1_hospitals/dirty_index.csv',
                        help='Path to the input dirty CSV file.')
    parser.add_argument('--rule_path', type=str, default='../../Data/1_hospitals/dc_rules_dc_holoclean.txt',
                        help='Path to the input rule file.')
    parser.add_argument('--clean_path', type=str, default='../../Data/1_hospitals/clean_index.csv',
                        help='Path to the input clean CSV file.')
    parser.add_argument('--task_name', type=str, default='hospital_test',
                        help='Task name for the cleaning process.')
    parser.add_argument('--output_path', type=str, default='../../results/Holoclean/',
                        help='Path to save the output results.')
    parser.add_argument('--index_attribute', type=str, default='index',
                        help='Index attribute of the data.')
    parser.add_argument('--mse_attributes', type=str, nargs='*', default=[],
                        help='List of attributes to calculate MSE, separated by space.')

    # 解析命令行参数
    args = parser.parse_args()

    # 设置路径
    mse_attributes = args.mse_attributes
    stra_path = os.path.join(args.output_path, f"{args.task_name}")
    index_attribute = args.index_attribute

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(stra_path):
        os.makedirs(stra_path)
    ori_empty_clean_path = os.path.splitext(args.clean_path)[0] + '_ori_empty.csv'
    ori_empty_dirty_path = os.path.splitext(args.dirty_path)[0] + '_ori_empty.csv'
    # 替换数据中的空值，统一转换为 'empty'
    inject_missing_values(
        csv_file=args.clean_path,
        output_file=ori_empty_clean_path,
        missing_value_in_ori_data='empty',
        missing_value_representation='',
        attributes_error_ratio=None
    )
    inject_missing_values(
        csv_file=args.dirty_path,
        output_file=ori_empty_dirty_path,
        missing_value_in_ori_data='empty',
        missing_value_representation='',
        attributes_error_ratio=None
    )
    # 读取脏数据，重命名索引列为 index_col 并保存
    dirty_data = pd.read_csv(ori_empty_dirty_path)
    if index_attribute in dirty_data.columns:  # 确保 'index' 列存在
        # dirty_data.rename(columns={index_attribute: 'index_col'}, inplace=True)
        dirty_data.drop(columns=[index_attribute], inplace=True)
    else:
        print(index_attribute + " attribute not found in the data. Skipping replacement.")
    # 生成新的文件路径
    dirty_holoclean_path = os.path.splitext(args.dirty_path)[0] + "_holoclean.csv"
    dirty_data.to_csv(dirty_holoclean_path, index=False, encoding='utf-8')

    # 加载去掉索引后的数据到 Holoclean
    print(f"Running Holoclean with modified dirty file: {dirty_holoclean_path}")
    # 记录开始时间
    start_time = time.time()

    # 运行 Holoclean
    # print(f"Running Holoclean with dirty file: {args.dirty_path}")
    hc = holoclean.HoloClean(
        db_user='datacleanuser',
        db_name='holo',
        domain_thresh_1=0,
        domain_thresh_2=0,
        weak_label_thresh=0.99,
        max_domain=10000,
        cor_strength=0.6,
        nb_cor_strength=0.8,
        epochs=10,
        weight_decay=0.01,
        learning_rate=0.001,
        threads=1,
        batch_size=1,
        verbose=True,
        timeout=3 * 60000,
        feature_norm=False,
        weight_norm=False,
        print_fw=True
    ).session

    hc.load_data(args.task_name[2:], dirty_holoclean_path)
    hc.load_dcs(args.rule_path)
    hc.ds.set_constraints(hc.get_dcs())

    detectors = [NullDetector(), ViolationDetector()]
    hc.detect_errors(detectors)

    hc.setup_domain()
    featurizers = [
        InitAttrFeaturizer(),
        OccurAttrFeaturizer(),
        FreqFeaturizer(),
        ConstraintFeaturizer(),
    ]
    hc.repair_errors(featurizers)


    # 使用 evaluate 保存修复后的数据
    res_path = os.path.join(stra_path, f"{args.task_name}_repaired.csv")
    clean_data = pd.read_csv(ori_empty_clean_path)
    clean_data_attributes = clean_data.columns.tolist()
    # 生成新的 clean 数据路径，替换为 *_holoclean.csv 格式
    clean_holoclean_path = os.path.splitext(args.clean_path)[0] + "_holoclean.csv"
    # 运行函数以处理CSV文件并生成新的路径
    transform_csv_file(ori_empty_clean_path, clean_holoclean_path)


    hc.evaluate(
        fpath=clean_holoclean_path,  # 使用修改后的 clean_holoclean.csv
        tid_col='tid',
        attr_col='attribute',
        val_col='correct_val',
        output_csv_path=res_path,  # 保存修复后的数据
        attrubte_list=clean_data_attributes,  # 按 clean 数据的列顺序导出
        clean_data=clean_data
    )

    print(f"Results saved to {res_path}")

    # 记录结束时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Holoclean finished in {elapsed_time} seconds.")
    ori_empty_res_path = os.path.splitext(res_path)[0] + '_ori_empty.csv'
    # 测评性能
    print("测评性能开始：")
    inject_missing_values(
        csv_file=res_path,
        output_file=ori_empty_res_path,
        missing_value_in_ori_data='empty',
        missing_value_representation='',
        attributes_error_ratio=None
    )
    dirty_data = pd.read_csv(ori_empty_dirty_path)
    cleaned_data = pd.read_csv(ori_empty_res_path)

    # 根据规则定义的属性集合
    attributes = clean_data.columns.tolist()
    results = calculate_all_metrics(clean_data, dirty_data, cleaned_data, attributes, stra_path, args.task_name,
                                    index_attribute=index_attribute, mse_attributes=mse_attributes)

    # 输出评估结果到文件
    results_path = os.path.join(stra_path, f"{args.task_name}_total_evaluation.txt")
    original_stdout = sys.stdout
    with open(results_path, 'w', encoding='utf-8') as f:
        sys.stdout = f
        print("测试结果:")
        print(f"Accuracy: {results.get('accuracy')}")
        print(f"Recall: {results.get('recall')}")
        print(f"F1 Score: {results.get('f1_score')}")
        print(f"EDR: {results.get('edr')}")
        print(f"Hybrid Distance: {results.get('hybrid_distance')}")
        print(f"R-EDR: {results.get('r_edr')}")
        print(f"Time: {elapsed_time}")
        print(f"Speed: {100 * float(elapsed_time) / clean_data.shape[0]} seconds/100 records")
    sys.stdout = original_stdout

    # 打印测评结果到控制台
    print("测试结果:")
    print(f"Accuracy: {results.get('accuracy')}")
    print(f"Recall: {results.get('recall')}")
    print(f"F1 Score: {results.get('f1_score')}")
    print(f"EDR: {results.get('edr')}")
    print(f"Hybrid Distance: {results.get('hybrid_distance')}")
    print(f"R-EDR: {results.get('r_edr')}")
    print(f"Time: {elapsed_time}")
    print(f"Speed: {100 * float(elapsed_time) / clean_data.shape[0]} seconds/100 records")
    print("测评结束，详细测评日志见：" + str(stra_path))


if __name__ == "__main__":
    main()
