#!/bin/bash
# 设置可执行权限： chmod +x CleanerRunScript/run_raha_baran/run_nwcpk.sh
# 运行方式：./CleanerRunScript/run_horizon/run_nwcpk.sh

# 定义数据集配置
# 解析dataset index_attr mse_attr noise_dir clean_path这几个参数，后续需要，根据你的系统配置自行修改
datasets=(
    #"1_hospitals:index:Score:Data/1_hospitals/noise_with_correct_primary_key:Data/1_hospitals/clean_index.csv:Data/1_hospitals/dc_rules-validate-fd-horizon.txt"
    #"2_flights:index::Data/2_flights/noise_with_correct_primary_key:Data/2_flights/clean_index.csv:Data/2_flights/dc_rules-validate-fd-horizon.txt"
    #"3_beers:id:abv ibu:Data/3_beers/noise_with_correct_primary_key:Data/3_beers/clean.csv:Data/3_beers/dc_rules-validate-fd-horizon.txt"
    #"4_rayyan:index::Data/4_rayyan/noise_with_correct_primary_key:Data/4_rayyan/clean_index.csv:Data/4_rayyan/dc_rules-validate-fd-horizon.txt"
    #"5_tax:tno:rate:Data/5_tax/subset_tax_10k/noise_with_correct_primary_key:Data/5_tax/subset_tax_10k/subset_tax_10k_clean_index.csv:Data/5_tax/dc_rules-validate-fd-horizon.txt"
    "6_soccer:index::Data/6_soccer/noise_with_correct_primary_key:Data/6_soccer/clean_index.csv:Data/6_soccer/dc_rules-validate-fd-horizon.txt"
)

# 定义错误比例集合
#error_ratios=("0.25" "0.5" "0.75" "1" "1.25" "1.5" "1.75" "2")
error_ratios=("1.75")

# 创建日志目录
log_dir="logs/horizon_nwcpk"
mkdir -p "${log_dir}"

# 遍历数据集和错误比例，生成并执行命令（根据各自的系统进行更改）
for dataset_config in "${datasets[@]}"; do
    # 使用分隔符解析键值对
    IFS=":" read -r dataset index_attr mse_attr noise_dir clean_path rule_path <<< "${dataset_config}"
    # 从第三个字符开始取数据集名称
    short_dataset_name="${dataset:2}"
    for ratio in "${error_ratios[@]}"; do
        task_name="${dataset}_nwcpk_${ratio//./}"
        dirty_path="${noise_dir}/dirty_mixed_${ratio}/dirty_${short_dataset_name}_mix_${ratio}.csv"
        #dirty_path="${noise_dir}/rayyan_${ratio}/dirty_${short_dataset_name}_mix_${ratio}.csv"
        output_path="results/horizon/nwcpk"
        log_file="${log_dir}/${dataset}_horizon_nwcpk_${ratio//./}.log"

        # 生成命令
        cmd="python CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ${dirty_path} --rule_path ${rule_path} --clean_path ${clean_path} --task_name ${task_name} --output_path ${output_path} --index_attribute ${index_attr}"

        if [ -n "${mse_attr}" ]; then
            cmd+=" --mse_attributes ${mse_attr}"
        fi

        # 打印命令用于调试
        echo "Generated command:"
        echo "${cmd}"

        # 执行命令
        eval "${cmd}" &> "${log_file}"

        if [ $? -ne 0 ]; then
            echo "Error: Command failed for task ${task_name}. Check ${log_file} for details."
            exit 1
        fi
        echo "Task ${task_name} completed successfully. Log saved to: ${log_file}"
    done
done

echo "All horizon tasks completed successfully."