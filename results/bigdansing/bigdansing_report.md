# 实验报告

## 1. 清洗系统名称：`BigDansing`

**论文**: [BigDansing: A System for Big Data Cleansing](https://dl.acm.org/doi/10.1145/2723372.2747646) 

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 数据集: `hospital`
#### 实验1 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验1    | `../../Data/hospital/noise/hospital-inner_outer_error-10.csv`, `../../Data/hospital/dc_rules_holoclean.txt`, `../../Data/hospital/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_hospital/all_computed_bigdansing_hospital1-inner_outer_error-10.txt`,`../../results/bigdansing/Repaired_res/bigdansing_hospital/repaired_bigdansing_hospital1-inner_outer_error-10.csv`  | `/`   | `/` |
### 实验1 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/hospital/noise/hospital-inner_outer_error-10.csv" --rule_path "../../Data/hospital/dc_rules_holoclean.txt" --clean_path "../../Data/hospital/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_hospital1"
```

#### 实验2 设置
| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验2    | `../../Data/hospital/noise/hospital-inner_outer_error-20.csv`, `../../Data/hospital/dc_rules_holoclean.txt`, `../../Data/hospital/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_hospital/all_computed_bigdansing_hospital2-inner_outer_error-20.txt`,`../../results/bigdansing/Repaired_res/bigdansing_hospital/repaired_bigdansing_hospital2-inner_outer_error-20.csv`  | `/`   | `/` |
### 实验2 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/hospital/noise/hospital-inner_outer_error-20.csv" --rule_path "../../Data/hospital/dc_rules_holoclean.txt" --clean_path "../../Data/hospital/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_hospital2"
```

#### 实验3 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验3    | `../../Data/hospital/noise/hospital-inner_outer_error-30.csv`, `../../Data/hospital/dc_rules_holoclean.txt`, `../../Data/hospital/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_hospital/all_computed_bigdansing_hospital3-inner_outer_error-30.txt`,`../../results/bigdansing/Repaired_res/bigdansing_hospital/repaired_bigdansing_hospital3-inner_outer_error-30.csv`  | `/`   | `/` |
### 实验3 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/hospital/noise/hospital-inner_outer_error-30.csv" --rule_path "../../Data/hospital/dc_rules_holoclean.txt" --clean_path "../../Data/hospital/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_hospital3"
```
---

### 数据集: `flights`

#### 实验4 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验4    | `../../Data/flights/noise/flights-outer_error-10.csv`, `../../Data/flights/dc_rules_holoclean.txt`, `../../Data/flights/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_flights/all_computed_bigdansing_flights1-inner_outer_error-10.txt`,`../../results/bigdansing/Repaired_res/bigdansing_flights/repaired_bigdansing_flights1-inner_outer_error-10.csv`  | `/`   | `/` |
### 实验4 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/flights/noise/flights-inner_outer_error-10.csv" --rule_path "../../Data/flights/dc_rules_holoclean.txt" --clean_path "../../Data/flights/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_flights1"
```

#### 实验5 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验5    | `../../Data/flights/noise/flights-outer_error-20.csv`, `../../Data/flights/dc_rules_holoclean.txt`, `../../Data/flights/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_flights/all_computed_bigdansing_flights2-inner_outer_error-20.txt`,`../../results/bigdansing/Repaired_res/bigdansing_flights/repaired_bigdansing_flights2-inner_outer_error-20.csv`  | `/`   | `/` |
### 实验5 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/flights/noise/flights-inner_outer_error-20.csv" --rule_path "../../Data/flights/dc_rules_holoclean.txt" --clean_path "../../Data/flights/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_flights2"
```

#### 实验6 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验6    | `../../Data/flights/noise/flights-outer_error-30.csv`, `../../Data/flights/dc_rules_holoclean.txt`, `../../Data/flights/clean.csv`| `/` | `../../results/bigdansing/Exp_result/bigdansing_flights/all_computed_bigdansing_flights3-inner_outer_error-30.txt`,`../../results/bigdansing/Repaired_res/bigdansing_flights/repaired_bigdansing_flights3-inner_outer_error-30.csv`  | `/`   | `/` |
### 实验6 运行命令：
```bash
python3 bigdansing.py --dirty_path "../../Data/flights/noise/flights-inner_outer_error-30.csv" --rule_path "../../Data/flights/dc_rules_holoclean.txt" --clean_path "../../Data/flights/clean.csv" --onlyed 0 --perfected 0 --task_name "bigdansing_flights3"
```
---

## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称      | 数值    | 备注      |
|----------|------------------|-----------|-------|-----------|
| 实验1  | `hospital`     | Precision | `0.49564873417719557` | `/` |
|          |                  | F1        | `0.5861517550018409`  | `/` |
|          |                  | Recall    | `0.7170886075948913` | `/` |
| 实验2  | `hospital`     | Precision     | `0.49706744868033975` | `/` |
|          |                  | F1     | `0.5390857045945548` | `/` |
|          |                  | Recall     | `0.5888637099384724` | `/` |
| 实验3  | `hospital`     | Precision     | `0.4511053574984973` | `/` |
|          |                  | F1     | `0.45871043419125546` | `/` |
|          |                  | Recall     | `0.4665763324299804` | `/` |
| 实验4  | `flights`     | Precision     | `0.28330058939095154` | `/` |
|          |                  | F1     | `0.37328501160400257` | `/` |
|          |                  | Recall     | `0.5470409711683955` | `/` |
| 实验5  | `flights`     | Precision     | `0.3009753831862447` | `/` |
|          |                  | F1     | `0.380908477747561` | `/` |
|          |                  | Recall     | `0.5186522262334329` | `/` |
| 实验6  | `flights`     | Precision     | `0.3392589419575854` | `/` |
|          |                  | F1     | `0.38199335283711566` | `/` |
|          |                  | Recall     | `0.4370453273642855` | `/` |
---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。