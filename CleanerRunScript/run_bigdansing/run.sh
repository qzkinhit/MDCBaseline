#!/bin/bash
# chmod +x CleanerRunScript/run_bigdansing/run.sh
#./CleanerRunScript/run_bigdansing/run.sh
# 定义bigdansing命令列表
bigdansing_commands=(
    "python3 run_bigdansing_base.py --clean_path '../../Data/1_hospital/clean_index.csv' --dirty_path '../../Data/1_hospital/dirty_index.csv' --rule_path '../../Data/1_hospital/dc_rules_dc_holoclean.txt' --task_name 'bigdansing_hospital_test0'"
    "python3 run_bigdansing_base.py --clean_path '../../Data/2_flights/clean_index.csv' --dirty_path '../../Data/2_flights/dirty_index.csv' --rule_path '../../Data/2_flights/dc_rules_holoclean.txt' --task_name 'bigdansing_flights_test0'"
    "python3 run_bigdansing_base.py --clean_path '../../Data/3_beers/clean_index.csv' --dirty_path '../../Data/3_beers/dirty_index.csv' --rule_path '../../Data/3_beers/dc_rules_holoclean.txt' --task_name 'bigdansing_beers_test0' --index_attribute 'id'"
    "python3 run_bigdansing_base.py --clean_path '../../Data/4_rayyan/clean_index.csv' --dirty_path '../../Data/4_rayyan/dirty_index.csv' --rule_path '../../Data/4_rayyan/dc_rules_holoclean.txt' --task_name 'bigdansing_rayyan_test0'"
    "python3 run_bigdansing_base.py --clean_path '../../Data/5_tax/clean_index_10k.csv' --dirty_path '../../Data/5_tax/dirty_index_10k.csv' --rule_path '../../Data/5_tax/dc_rules_holoclean.txt' --task_name 'bigdansing_tax_test0' --mse_attributes 'rate'"
    "python3 run_bigdansing_base.py --clean_path '../../Data/6_soccer/clean_index_10k.csv' --dirty_path '../../Data/6_soccer/dirty_index_10k.csv' --rule_path '../../Data/6_soccer/dc_rules_holoclean.txt' --task_name 'bigdansing_soccer_test0'"
)

# 定义日志文件名列表
log_files=(
    "logs/bigdansing_hospital_test0.log"
    "logs/bigdansing_flights_test0.log"
    "logs/bigdansing_beers_test0.log"
    "logs/bigdansing_rayyan_test0.log"
    "logs/bigdansing_tax_test0.log"
    "logs/bigdansing_soccer_test0.log"
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
