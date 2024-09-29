# 运行脚本说明

## Horizon
**论文**: [Horizon: Scalable Dependency-Driven Data Cleaning](https://www.vldb.org/pvldb/vol14/p25)
### 脚本简介：
该脚本是基于 **Horizon** 方法的依赖驱动数据清洗脚本。Horizon 通过识别数据中的功能依赖（FD，Functional Dependency）违规来进行数据清洗。本脚本会读取指定的输入数据文件，应用约束规则（功能依赖规则），并生成清洗后的数据文件。


## 运行命令1:
```bash
python run_horizon_base.py --dirty_path data/input.csv --rule_path data/rules.txt --clean_path data/clean.csv --task_name task_name --output_path data/output.csv
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
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/1_hospital/dirty_hospital_E1.csv --rule_path ../../Data/1_hospital/dc_rules-vallidate-fd-horizon.txt --clean_path ../../Data/1_hospital/clean.csv --task_name hospital_horizon_E1 --output_path ../../results/horizon/hospital_horizon_E1
```
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/1_hospital/dirty_hospital_E2.csv --rule_path ../../Data/1_hospital/dc_rules-vallidate-fd-horizon.txt --clean_path ../../Data/1_hospital/clean.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/1_hospital/dirty.csv --rule_path ../../Data/1_hospital/dc_rules_test.txt --clean_path ../../Data/1_hospital/hospital_clean.csv --task_name hospital_test --output_path ../../results/horizon/hospital_test
```
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/5_tax/split_data/5_tax-dirty-original_error-0010k.csv --rule_path ../../Data/5_tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/5_tax/split-clean-clean_data_ori-0010k.csv --task_name tax_horizon_ori --output_path ../../results/horizon/tax_horizon_ori
```
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/5_tax/dirty_tax_E1.csv --rule_path ../../Data/5_tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/5_tax/clean.csv --task_name tax_horizon_E1 --output_path ../../results/horizon/tax_horizon_E1
```
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/5_tax/dirty_tax_E2.csv --rule_path ../../Data/5_tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/5_tax/clean.csv --task_name tax_horizon_E2 --output_path ../../results/horizon/tax_horizon_E2
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
