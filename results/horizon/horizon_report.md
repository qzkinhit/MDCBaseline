# 实验报告

## 1. 清洗系统名称：`Horizon`

**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)
**可视化结果**: `results/horizon/visualization.png`  
**说明**: 此结果包含了Horizon系统在输入数据上的清洗结果，并通过可视化展示了数据清洗前后的差异。

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 数据集: `parking` [下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)

#### 实验1-3 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                 | 本地输出路径             | 实际输出存放路径                  | 备注      |
|----------|--------------------------|--------------------------|--------------------------|---------------------------|-----------|
| 实验1    | `./Data/parking/input_parking_horizon.csv` | `baidupan/MDCBaseline-horizon/parking/input_parking_horizon.csv` | `./results/horizon/output_parking_horizon.csv`      | `/` | `备注内容1` |
### 实验 x 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty.csv --rule_path ../../Data/hospital/dc_rules_test.txt --clean_path ../../Data/hospital/hospital_clean.csv --task_name hospital_test --output_path ../../results/horizon/hospital_test
```




### 数据集: `hospital`[下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)

#### 实验2-4 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验2    | `./Data/hospital/input_hospital_horizon_E1.csv` | `baidupan/MDCBaseline-horizon/hospital/E1/input_hospital_horizon_E1.csv`         | `./results/horizon/output_hospital_horizon_E1.csv`      | `/`        | `备注内容` |
| 实验3    | `./Data/hospital/input_hospital_horizon_E2.csv` | `baidupan/MDCBaseline-horizon/hospital/E2/input_hospital_horizon_E2.csv`         | `./results/horizon/output_hospital_horizon_E2.csv`      | `/`        | `备注内容` |
### 实验 x 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty.csv --rule_path ../../Data/hospital/dc_rules_test.txt --clean_path ../../Data/hospital/hospital_clean.csv --task_name hospital_test --output_path ../../results/horizon/hospital_test
```

---

| 实验编号 | 本地输入路径                                                                                                                                                             | 实际输入存放路径                                                                                                                      | 本地输出路径                                       | 实际输出存放路径 | 备注                                  |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|------------------|-----------------------------------|
| 实验4  | `../../Data/hospital/dirty.csv`, `../../Data/hospital/dc_rules_test.txt`, `../../Data/hospital/hospital_clean.csv`                                                     | `/`   | `../../results/horizon/hospital_test`          | `/`              | 这个数据集是原生的错误，错误率3%    |

### 实验 4 运行命令：
```bash
python ../../CleanerRunScript/run_horizon/run_horizon_base.py --dirty_path ../../Data/hospital/dirty.csv --rule_path ../../Data/hospital/dc_rules_test.txt --clean_path ../../Data/hospital/hospital_clean.csv --task_name hospital_test --output_path ../../results/horizon/hospital_test
```

### 数据集: `tax`[下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)

#### 实验4-6 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验4    | `./Data/tax/input_tax_horizon_E1.csv` | `baidupan/MDCBaseline-horizon/tax/E1/input_tax_horizon_E1.csv`         | `./results/horizon/output_tax_horizon_E1.csv`      | `/`        | `备注内容` |
| 实验5    | `./Data/tax/input_tax_horizon_E2.csv` | `baidupan/MDCBaseline-horizon/tax/E2/input_tax_horizon_E2.csv`         | `./results/horizon/output_tax_horizon_E2.csv`      | `/`        | `备注内容` |
### 实验 x 运行命令：
```bash
python run_horizon_base.py --dirty_path ../../Data/hospital/input_hospital_horizon_E2.csv --rule_path ../../Data/hospital/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/hospital/input_hospital_horizon.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```
---

## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称      | 数值    | 备注      |
|----------|------------------|-----------|-------|-----------|
| 实验1-3  | `数据集名称1`     | Precision | `Precision` | `备注内容` |
|          |                  | F1        | `F1`  | `备注内容` |
|          |                  | EDR       | `EDR` | `备注内容` |
|          |                  | Recall    | `数值3` | `备注内容` |
| 实验4-6  | `数据集名称2`     | xx指标1     | `数值4` | `备注内容` |
|          |                  | xx指标2     | `数值5` | `备注内容` |
|          |                  | xx指标3     | `数值6` | `备注内容` |
| 实验7-9  | `数据集名称3`     | xx指标1     | `数值7` | `备注内容` |
|          |                  | xx指标2     | `数值8` | `备注内容` |
|          |                  | xx指标3     | `数值9` | `备注内容` |
| ...      | ...              | ...       | ...   | ...       |

---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。