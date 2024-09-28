# 实验报告

## 1. 清洗系统名称：`Horizon`

**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)
**可视化结果**: `results/horizon/visualization.png`  
**说明**: 此结果包含了Horizon系统在输入数据上的清洗结果，并通过可视化展示了数据清洗前后的差异。

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 数据集: `hospital`
#### 实验1 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验1    | `../../Data/hospital/dirty_hospital_E1.csv`, `../../Data/hospital/dc-rules-validate-fd-horizon.txt`, `../../Data/hospital/clean.csv`| `/` | `../../results/horizon/hospital_horizon_E1.csv`      | `/`   | 规则违反MeasureCode ⇒ Stateavg比例为2%, 规则违反HospitalName ⇒ Address1比例为1%, 规则违反HospitalName ⇒ PhoneNumber比例为0.5%, 规则违反MeasureCode ⇒ Condition比例为1%|
### 实验1 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty_hospital_E1.csv --rule_path ../../Data/hospital/dc_rules-vallidate-fd-horizon.txt --clean_path ../../Data/hospital/clean.csv --task_name hospital_horizon_E1 --output_path ../../results/horizon/hospital_horizon_E1
```
####实验2 设置
| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验2    | `../../Data/hospital/dirty_hospital_E1.csv`, `../../Data/hospital/dc-rules-validate-fd-horizon.txt`, `../../Data/hospital/clean.csv` | `/` | `../../results/horizon/hospital_horizon_E2.csv`      | `/` | 注入随机错误 |

### 实验2 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty_hospital_E2.csv --rule_path ../../Data/hospital/dc_rules-vallidate-fd-horizon.txt --clean_path ../../Data/hospital/clean.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```
####实验3 设置
| 实验编号 | 本地输入路径                                                                                                                                                             | 实际输入存放路径                                                                                                                      | 本地输出路径                                       | 实际输出存放路径 | 备注                                  |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|------------------|-----------------------------------|
| 实验3  | `../../Data/hospital/dirty.csv`, `../../Data/hospital/dc_rules_test.txt`, `../../Data/hospital/hospital_clean.csv`                                                     | `/`   | `../../results/horizon/hospital_test`          | `/`              | 这个数据集是原生的错误，错误率3%    |

### 实验 3 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty.csv --rule_path ../../Data/hospital/dc_rules_test.txt --clean_path ../../Data/hospital/hospital_clean.csv --task_name hospital_test --output_path ../../results/horizon/hospital_test
```
---

### 数据集: `tax`

#### 实验4 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验4    | `../../Data/tax/split_data/tax-dirty-original_error-0010k.csv`, `../../Data/tax/dc_rulrs-validate-fd-horizon.txt`, `../../Data/tax/split_data/tax-clean-clean_data_ori-0010k.csv` | `/`  | `../../results/horizon/tax_horizon_ori.csv`      | `/`        | 这个数据集是原生的错误，错误率4% |
### 实验4 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/tax/split_data/tax-dirty-original_error-0010k.csv --rule_path ../../Data/tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/tax/split-clean-clean_data_ori-0010k.csv --task_name tax_horizon_ori --output_path ../../results/horizon/tax_horizon_ori
```

#### 实验5 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验5    | `../../Data/tax/dirty_tax_E1.csv`, `../../Data/tax/dc_rules-validate-fd-horizon.txt`, `../../Data/tax/clean.csv`  | `/` | `../../results/horizon/tax_horizon_E1.csv`      | `/`        | 规则违反zip ⇒ city比例为10%, 规则违反has_child ⇒ child_exemp比例为10%, 规则违反zip ⇒ child_exemp比例为10%|
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/tax/dirty_tax_E1.csv --rule_path ../../Data/tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/tax/clean.csv --task_name tax_horizon_E1 --output_path ../../results/horizon/tax_horizon_E1
```

#### 实验6 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验6    | `../../Data/tax/dirty_tax_E2.csv`, `../../Data/tax/dc_rules-validate-fd-horizon.txt`, `../../Data/tax/clean.csv`  | `/` | `../../results/horizon/tax_horizon_E2.csv`      | `/`        | `注入随机错误` |
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/tax/dirty_tax_E2.csv --rule_path ../../Data/tax/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/tax/clean.csv --task_name tax_horizon_E2 --output_path ../../results/horizon/tax_horizon_E2
```
---

## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称      | 数值    | 备注      |
|----------|------------------|-----------|-------|-----------|
| 实验1  | `hospital`     | Precision | `0.6923076923076923` | `/` |
|          |                  | F1        | `0.818181818133471`  | `/` |
|          |                  | Recall    | `1.0` | `/` |
| 实验2  | `hospital`     | Precision     | `0.34507042253521125` | `/` |
|          |                  | F1     | `0.42060085832149424` | `/` |
|          |                  | Recall     | `0.5384615384615384` | `/` |
| 实验3  | `hospital`     | Precision     | `0.7804295942720764` | `/` |
|          |                  | F1     | `0.7047413792608151` | `/` |
|          |                  | Recall     | `0.6424361493123772` | `/` |
| 实验4  | `tax`     | Precision     | `0.07362316061927815` | `/` |
|          |                  | F1     | `0.1134374653462553` | `/` |
|          |                  | Recall     | `0.24702476680604696` | `/` |
| 实验5  | `tax`     | Precision     | `0.1267171292402579` | `/` |
|          |                  | F1     | `0.22227686253068454` | `/` |
|          |                  | Recall     | `0.904` | `/` |
| 实验6  | `tax`     | Precision     | `0.07362316061927815` | `/` |
|          |                  | F1     | `0.1134374653462553` | `/` |
|          |                  | Recall     | `0.24702476680604696` | `/` |
---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。