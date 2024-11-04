# chmod +x CleanerRunScript/run_bigdansing/run_nwcpk.sh
# ./CleanerRunScript/run_bigdansing/run_nwcpk.sh


bigdansing_commands=(
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_hospital_mix_0.25.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_025 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_hospital_mix_0.5.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_050 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_hospital_mix_0.75.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_075 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_1/dirty_hospital_mix_1.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_100 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_hospital_mix_1.25.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_125 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_hospital_mix_1.5.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_150 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_hospital_mix_1.75.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_175 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/1_hospital/clean_index.csv --dirty_path Data/1_hospital/noise_with_correct_primary_key/dirty_mixed_2/dirty_hospital_mix_2.csv --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --task_name 1_hospital_nwcpk_200 --mse_attributes Score"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_flights_mix_0.25.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_025"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_flights_mix_0.5.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_050"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_flights_mix_0.75.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_075"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_1/dirty_flights_mix_1.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_100"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_flights_mix_1.25.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_125"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_flights_mix_1.5.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_150"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_flights_mix_1.75.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_175"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/2_flights/clean_index.csv --dirty_path Data/2_flights/noise_with_correct_primary_key/dirty_mixed_2/dirty_flights_mix_2.csv --rule_path Data/2_flights/dc_rules_holoclean.txt --task_name 2_flights_nwcpk_200"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_beers_mix_0.25.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_025 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_beers_mix_0.5.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_050 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_beers_mix_0.75.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_075 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_1/dirty_beers_mix_1.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_100 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_beers_mix_1.25.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_125 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_beers_mix_1.5.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_150 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_beers_mix_1.75.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_175 --index_attribute id --mse_attributes abv ibu"
    # "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/3_beers/clean_index.csv --dirty_path Data/3_beers/noise_with_correct_primary_key/dirty_mixed_2/dirty_beers_mix_2.csv --rule_path Data/3_beers/dc_rules_holoclean.txt --task_name 3_beers_nwcpk_200 --index_attribute id --mse_attributes abv ibu"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_0.25/dirty_rayyan_mix_0.25.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_025"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_0.5/dirty_rayyan_mix_0.5.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_050"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_0.75/dirty_rayyan_mix_0.75.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_075"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_1/dirty_rayyan_mix_1.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_100"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_1.25/dirty_rayyan_mix_1.25.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_125"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_1.5/dirty_rayyan_mix_1.5.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_150"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_1.75/dirty_rayyan_mix_1.75.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_175"
    "python3 CleanerRunScript/run_bigdansing/run_bigdansing_base.py --output_path results/bigdansing/nwcpk --clean_path Data/4_rayyan/clean_index.csv --dirty_path Data/4_rayyan/noise_with_correct_primary_key/rayyan_2/dirty_rayyan_mix_2.csv --rule_path Data/4_rayyan/dc_rules_holoclean.txt --task_name 4_rayyan_nwcpk_200"
)

# 定义日志文件名列表
log_files=(
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_025.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_050.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_075.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_100.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_125.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_150.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_175.log"
    # "logs/bigdansing_nwcpk/1_hospital_bigdansing_nwcpk_200.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_025.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_050.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_075.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_100.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_125.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_150.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_175.log"
    # "logs/bigdansing_nwcpk/2_flights_bigdansing_nwcpk_200.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_025.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_050.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_075.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_100.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_125.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_150.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_175.log"
    # "logs/bigdansing_nwcpk/3_beers_bigdansing_nwcpk_200.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_025.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_050.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_075.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_100.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_125.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_150.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_175.log"
    "logs/bigdansing_nwcpk/4_rayyan_bigdansing_nwcpk_200.log"
)

# 创建日志目录
mkdir -p logs/bigdansing_nwcpk


# 逐条执行bigdansing命令并保存日志
for i in "${!bigdansing_commands[@]}"; do
    echo "Running command for task ${i+1}..."
    echo "${bigdansing_commands[$i]}"
    ${bigdansing_commands[$i]} &> "${log_files[$i]}"
    if [ $? -ne 0 ]; then
        echo "Command failed for task ${i+1}. See ${log_files[$i]} for details."
        exit 1
    fi
    echo "Command for task ${i+1} completed successfully. Output saved to: ${log_files[$i]}"
done

echo "All bigdansing tasks completed."