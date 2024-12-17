#!/bin/bash
# chmod +x CleanerRunScript/run_holistic/run.sh
# ./CleanerRunScript/run_holistic/run.sh

# 定义holistic命令列表，包含每个数据集的mse_attributes，注意我这里在服务器上运行，所以是python3开头，你们本地可能只能识别python
commands=(
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 1_hospital_ori --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --output_path results/holistic --mse_attributes Score"
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 2_flights_ori --rule_path Data/2_flights/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 3_beers_ori --rule_path Data/3_beers/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --output_path results/holistic --index_attribute id --mse_attributes abv ibu"
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 4_rayyan_ori --rule_path Data/4_rayyan/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 5_tax_ori --rule_path Data/5_tax/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/5_tax/subset_dirty_index_10k.csv --clean_path Data/5_tax/subset_clean_index_10k --output_path results/holistic --mse_attributes rate"
    "python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name 6_soccer_ori --rule_path Data/6_soccer/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/6_soccer/subset_dirty_index_10k.csv --clean_path Data/6_soccer/subset_clean_index_10k.csv --output_path results/holistic"
)

#python CleanerRunScript/run_holistic/run_holistic_base.py --task_name 5_tax_ori --rule_path Data/5_tax/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/5_tax/subset_dirty_index_10k.csv --clean_path Data/5_tax/subset_clean_index_10k.csv --output_path results/holistic --mse_attributes rate

# 定义日志文件名列表
log_files=(
    "logs/1_hospital_ori_holistic.log"
    "logs/2_flights_ori_holistic.log"
    "logs/3_beers_ori_holistic.log"
    "logs/4_rayyan_ori_holistic.log"
    "logs/5_tax_10k_ori_holistic.log"
    "logs/6_soccer_10k_ori_holistic.log"
)

# 创建日志目录
mkdir -p logs

# 逐条执行holistic命令并保存日志
for i in "${!commands[@]}"; do
    echo "Running command for task ${i+1}..."
    echo "${commands[$i]}"
    ${commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Command failed for task ${i+1}. See ${log_files[$i]} for details."
        exit 1
    fi
    echo "Command for task ${i+1} completed successfully. Output saved to: ${log_files[$i]}"
done

echo "All holistic tasks completed."
