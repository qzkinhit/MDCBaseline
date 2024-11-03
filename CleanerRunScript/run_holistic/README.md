# 运行脚本说明

## Holistic
**论文**: [Holistic Data Cleaning: Putting Violations Into
Context](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=c4221a899528798105ca94e509027e7210a87d6b)
### 脚本简介：
该脚本是基于 **Holistic** 方法的依赖驱动数据清洗脚本。Holistic 以拒绝约束（DC, Denial Constraint）为输入，检测规则违反并构建冲突超图，使用修复上下文修复对数据集进行整体修复，并生成清洗后的数据文件。


## 运行命令1:
```bash
python CleanerRunScript/run_holistic/run_holistic_base.py --task_name task_name1 --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --output_path results/hospital/
```

### 命令行参数说明：
- `--dirty_path`: **必需参数**。指定待清洗数据的 CSV 文件路径
- `--rule_path`: **必需参数**。指定包含功能依赖规则的文件路径
- `--clean_path`: **必需参数**。指定清洗数据的真值 CSV 文件路径
- `--task_name`: **必需参数**。指定清洗任务的名称
- `--output_path`: **必需参数**。指定清洗后数据的保存路径

### 命令将执行以下操作：
1. **读取输入数据**：
   - 输入文件路径通过 `--dirty_path` 参数指定，例如 `data/input.csv`。
   - 该文件应为 **CSV 格式**，包含需要清洗的数据。

2. **读取功能依赖规则**：
   - 功能依赖规则文件路径通过 `--rule_path` 参数指定，例如 `data/rules.txt`。
   - 该文件应包含功能依赖规则，例如 `A ⇒ B`，表示属性 A 功能依赖于属性 B。

3. **读取真值数据**：
   - 真值文件路径通过 `--clean_path` 参数指定，例如 `data/clean.csv`。这个文件是干净的参考数据，用于验证清洗结果。

4. **输出清洗结果**：
   - 清洗后的结果将保存到通过 `--output_path` 参数指定的路径，例如 `data/output.csv`。
   - 输出文件也是 **CSV 格式**，包含清洗后的数据。

### 运行示例：
```bash
python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name hospital_dirty1 --rule_path Data/1_hospital/dc_rules_dc_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --output_path results/holistic
```
```bash
python CleanerRunScript/run_holistic/run_holistic_base.py --task_name flights_dirty1 --rule_path Data/2_flights/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --output_path results/holistic
```
```bash
python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name beers_dirty1 --rule_path Data/3_beers/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --output_path results/holistic
```
```bash
python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name rayyan_dirty1 --rule_path Data/4_rayyan/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --output_path results/holistic
```
```bash
python3 CleanerRunScript/run_holistic/run_holistic_base.py --task_name tax_dirty1 --rule_path Data/5_tax/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/5_tax/tax_50k/tax-dirty-original_error-0050k.csv --clean_path Data/5_tax/tax_50k/tax_50k_clean_id.csv --output_path results/holistic
```
```bash
python CleanerRunScript/run_holistic/run_holistic_base.py --task_name soccer_dirty1 --rule_path Data/6_soccer/dc_rules_holoclean.txt --onlyed 0 --perfected 0 --dirty_path Data/6_soccer/dirty_index.csv --clean_path Data/6_soccer/clean_index.csv --output_path results/holistic
```

## 运行命令2:
```bash
python xx
```
### 命令行参数说明：
xx
### 命令将执行以下操作：
xx
### 运行示例：
