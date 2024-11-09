#!/bin/bash
# chmod +x CleanerRunScript/run_horizon/run.sh
# ./CleanerRunScript/run_horizon/run.sh

# 定义horizon命令列表，并指定各数据集的mse_attributes，注意我这里在服务器上运行，所以是python3开头，你们本地可能只能识别python
horizon_commands=(
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/1_hospital/dirty_index.csv --rule_path Data/1_hospital/dc_rules-validate-fd-horizon.txt --clean_path Data/1_hospital/clean_index.csv --task_name 1_hospital_ori --output_path results/horizon/ --index_attribute index --mse_attributes Score"
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/2_flights/dirty_index.csv --rule_path Data/2_flights/dc_rules-validate-fd-horizon.txt --clean_path Data/2_flights/clean_index.csv --task_name 2_flights_ori --output_path results/horizon/ --index_attribute index"
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/3_beers/dirty_index.csv --rule_path Data/3_beers/dc_rules-validate-fd-horizon.txt --clean_path Data/3_beers/clean_index.csv --task_name 3_beers_ori --output_path results/horizon/ --index_attribute id --mse_attributes abv ibu"
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/4_rayyan/dirty_index.csv --rule_path Data/4_rayyan/dc_rules-validate-fd-horizon.txt --clean_path Data/4_rayyan/clean_index.csv --task_name 4_rayyan_ori --output_path results/horizon/ --index_attribute index"
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/5_tax/dirty_index_10k.csv --rule_path Data/5_tax/dc_rules-validate-fd-horizon.txt --clean_path Data/5_tax/clean_index_10k.csv --task_name 5_tax_ori --output_path results/horizon/ --index_attribute index --mse_attributes rate"
    "python3 CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/6_soccer/dirty_index_10k.csv --rule_path Data/6_soccer/dc_rules-validate-fd-horizon.txt --clean_path Data/6_soccer/clean_index_10k.csv --task_name 6_soccer_ori --output_path results/horizon/ --index_attribute index"
)


#python CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path Data/5_tax/dirty_index.csv --rule_path Data/5_tax/dc_rules-validate-fd-horizon.txt --clean_path Data/5_tax/clean_index.csv --task_name 5_tax_ori_50k --output_path results/horizon/ --index_attribute index --mse_attributes rate

# 定义日志文件名列表
log_files=(
    "logs/1_hospital_ori_horizon.log"
    "logs/2_flights_ori_horizon.log"
    "logs/3_beers_ori_horizon.log"
    "logs/4_rayyan_ori_horizon.log"
    "logs/5_tax_10k_ori_horizon.log"
    "logs/6_soccer_10k_ori_horizon.log"
)

# 创建日志目录
mkdir -p logs

# 逐条执行horizon命令并保存日志
for i in "${!horizon_commands[@]}"; do
    echo "Running: ${horizon_commands[$i]}"
    ${horizon_commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Command failed: ${horizon_commands[$i]}"
        exit 1
    fi
    echo "Output saved to: ${log_files[$i]}"
done

echo "All horizon tasks completed."
