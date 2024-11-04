#!/bin/bash
# 设置可执行权限： chmod +x CleanerRunScript/run_raha_baran/run.sh
# 运行方式：./CleanerRunScript/run_raha_baran/run.sh

# 定义命令列表，每个命令用于不同的数据集
commands=(
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --task_name 1_hospital_ori --output_path result/baran --index_attribute index --mse_attributes Score"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --task_name 2_flights_ori --output_path result/baran --index_attribute index"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --task_name 3_beers_ori --output_path result/baran --index_attribute id --mse_attributes ounces abv ibu"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --task_name 4_rayyan_ori --output_path result/baran --index_attribute id"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/5_tax/dirty_index_10k.csv --clean_path Data/5_tax/clean_index_10k.csv --task_name 5_tax_10k_ori --output_path result/baran --index_attribute index --mse_attributes rate"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/6_soccer/dirty_index_10k.csv --clean_path Data/6_soccer/clean_index_10k.csv --task_name 6_soccer_10k_ori --output_path result/baran --index_attribute index"
)

# 定义日志文件名列表
log_files=(
    "logs/1_hospital_ori_baran.log"
    "logs/2_flights_ori_baran.log"
    "logs/3_beers_ori_baran.log"
    "logs/4_rayyan_ori_baran.log"
    "logs/5_tax_10k_ori_baran.log"
    "logs/6_soccer_10k_ori_baran.log"
)

# 创建日志目录
mkdir -p logs

# 逐条执行命令并保存日志
for i in "${!commands[@]}"; do
    echo "Running command for task ${i+1}:"
    echo "${commands[$i]}"
    ${commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Error: Command failed for task ${i+1}. Check ${log_files[$i]} for details."
        exit 1
    fi
    echo "Task ${i+1} completed successfully. Log saved to: ${log_files[$i]}"
done

echo "All Raha Baran tasks completed successfully."
