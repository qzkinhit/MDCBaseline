#!/bin/bash
# chmod +x CleanerRunScript/run_bigdansing/run.sh
#./CleanerRunScript/run_bigdansing/run.sh
# 定义bigdansing命令列表
bigdansing_commands=(
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/1_hospital/clean_index.csv' --dirty_path 'Data/1_hospital/dirty_index.csv' --rule_path 'Data/1_hospital/dc_rules_dc_holoclean.txt' --task_name '1_hospital_ori'"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/2_flights/clean_index.csv' --dirty_path 'Data/2_flights/dirty_index.csv' --rule_path 'Data/2_flights/dc_rules_holoclean.txt' --task_name '2_flights_ori'"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/3_beers/clean_index.csv' --dirty_path 'Data/3_beers/dirty_index.csv' --rule_path 'Data/3_beers/dc_rules_holoclean.txt' --task_name '3_beers_ori' --index_attribute 'id'"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/4_rayyan/clean_index.csv' --dirty_path 'Data/4_rayyan/dirty_index.csv' --rule_path 'Data/4_rayyan/dc_rules_holoclean.txt' --task_name '4_rayyan_ori'"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/5_tax/clean_index_10k.csv' --dirty_path 'Data/5_tax/dirty_index_10k.csv' --rule_path 'Data/5_tax/dc_rules_holoclean.txt' --task_name '5_tax_ori' --mse_attributes 'rate'"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --clean_path 'Data/6_soccer/clean_index_10k.csv' --dirty_path 'Data/6_soccer/dirty_index_10k.csv' --rule_path 'Data/6_soccer/dc_rules_holoclean.txt' --task_name '6_soccer_ori'"
)

# 定义日志文件名列表
log_files=(
    "logs/1_hospital_ori_bigdansing.log"
    "logs/2_flights_ori_bigdansing.log"
    "logs/3_beers_ori_bigdansing.log"
    "logs/4_rayyan_ori_bigdansing.log"
    "logs/5_tax_10k_ori_bigdansing.log"
    "logs/6_soccer_10k_ori_bigdansing.log"
)

# 创建日志目录
mkdir -p logs

# 逐条执行bigdansing命令并保存日志
for i in "${!bigdansing_commands[@]}"; do
    echo "Running: ${bigdansing_commands[$i]}"
    ${bigdansing_commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Command failed: ${bigdansing_commands[$i]}"
        exit 1
    fi
    echo "Output saved to: ${log_files[$i]}"
done

echo "All bigdansing tasks completed."
