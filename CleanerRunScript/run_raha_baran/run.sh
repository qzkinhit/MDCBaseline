#!/bin/bash
# chmod +x CleanerRunScript/run_raha_baran/run.sh
#./CleanerRunScript/run_raha_baran/run.sh
# 定义命令列表
commands=(
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --task_name hospital_3 --output_path ../result/baran --index_attribute index --mse_attributes Score"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --task_name flights_2 --output_path ../result/baran --index_attribute index"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --task_name beers_1 --output_path ../result/baran --index_attribute id --mse_attributes ounces abv ibu"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --task_name rayyan_1 --output_path ../result/baran --index_attribute id"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/5_tax/dirty_index_10k.csv --clean_path Data/5_tax/clean_index_10k.csv --task_name tax_10k_1 --output_path ../result/baran --index_attribute index --mse_attributes salary rate singleexemp marriedexemp childexemp"
    "python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/6_soccer/dirty_index_10k.csv --clean_path Data/6_soccer/clean_index_10k.csv --task_name soccer_10k_1 --output_path ../result/baran --index_attribute index"
)

# 定义日志文件名列表
log_files=(
    "logs/hospital_3_baran.log"
    "logs/flights_2_baran.log"
    "logs/beers_1_baran.log"
    "logs/rayyan_1_baran.log"
    "logs/tax_10k_1_baran.log"
    "logs/soccer_10k_1_baran.log"
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
