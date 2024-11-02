#!/bin/bash
# chmod +x CleanerRunScript/run_raha_baran/run.sh
#./CleanerRunScript/run_holistic/run.sh
# 定义命令列表
commands=(
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 1_hospital_ori --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 2_flights_ori --rule_path Data/2_flights/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 3_beers_ori --rule_path Data/3_beers/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --output_path results/holistic  --index_attribute id"
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 4_rayyan_ori --rule_path Data/4_rayyan/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 5_tax_ori --rule_path Data/5_tax/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/5_tax/dirty_index_10k.csv --clean_path Data/5_tax/clean_index_10k.csv --output_path results/holistic"
    "python3 CleanerRunScript/run_holistic/run_holistic.py --task_name 6_soccer_ori --rule_path Data/6_soccer/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/6_soccer/dirty_index.csv --clean_path Data/6_soccer/clean_index.csv --output_path results/holistic"
)

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

# 逐条执行命令并保存日志
for i in "${!commands[@]}"; do
    echo "Running: ${commands[$i]}"
    ${commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Command failed: ${commands[$i]}"
        exit 1
    fi
    echo "Output saved to: ${log_files[$i]}"
done

echo "All tasks completed."