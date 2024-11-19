# 实验报告

## 1. 清洗系统名称：`Baran`

**论文**: [Baran: Effective Error Correction via a Unified Context Representation and Transfer Learning](https://www.vldb.org/pvldb/vol13/p1948-mahdavi.pdf)
**结果路径**: `results/raha_baran/`  
**说明**: 此结果包含了Baran系统在输入数据上的清洗结果,数值为三次实验取平均。

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 数据集: `hospital`

用于计算mse的属性：Score

#### 实验1 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                 | 本地输出路径             | 实际输出存放路径                  | 备注      |
|----------|--------------------------|--------------------------|--------------------------|---------------------------|-----------|
| 实验1    | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `/results/raha_baran/` | `/results/raha_baran/results-1_hospital_ori` | `备注内容1` |
### 实验 1 运行命令：
```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/1_hospitals/dirty_index.csv --clean_path Data/1_hospitals/clean_index.csv --task_name 1_hospital_ori --output_path results/raha_baran/ --index_attribute index --mse_attributes Score
```

### 数据集: `flights`

用于计算mse的属性：无

#### 实验2 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径           | 实际输出存放路径                            | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ------------------------------------------- | ----------- |
| 实验2    | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `/results/raha_baran/` | `/results/raha_baran/results-2_flights_ori` | `备注内容1` |

---

### 实验 2 运行命令：

```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --task_name 2_flights_ori --output_path results/raha_baran/ --index_attribute index
```

### 数据集: `beers`

用于计算mse的属性：abv、ibu

#### 实验3 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径           | 实际输出存放路径                          | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ----------------------------------------- | ----------- |
| 实验3    | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `/results/raha_baran/` | `/results/raha_baran/results-3_beers_ori` | `备注内容1` |

---

### 实验 3 运行命令：

```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --task_name 3_beers_ori --output_path results/raha_baran/ --index_attribute id --mse_attributes abv ibu
```

### 数据集: `rayyan`

用于计算mse的属性：无

#### 实验4 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径           | 实际输出存放路径                           | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ------------------------------------------ | ----------- |
| 实验4    | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `/results/raha_baran/` | `/results/raha_baran/results-4_rayyan_ori` | `备注内容1` |

---

### 实验 4 运行命令：

```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --task_name 4_rayyan_ori --output_path results/raha_baran/ --index_attribute index
```



### 数据集: `tax`

用于计算mse的属性：rate

#### 实验5 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径           | 实际输出存放路径                            | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ------------------------------------------- | ----------- |
| 实验5    | `Data/5_tax/dirty_index_10k.csv`<br />`Data/5_tax/clean_index_10k.csv` | `Data/5_tax/dirty_index_10k.csv`<br />`Data/5_tax/clean_index_10k.csv` | `/results/raha_baran/` | `/results/raha_baran/results-5_tax_10k_ori` | `备注内容1` |

---

### 实验 5 运行命令：

```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/5_tax/dirty_index_10k.csv --clean_path Data/5_tax/clean_index_10k.csv --task_name 5_tax_10k_ori --output_path results/raha_baran/ --index_attribute index --mse_attributes rate
```



### 数据集: `soccer`

用于计算mse的属性：无

#### 实验6 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径           | 实际输出存放路径                               | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ---------------------------------------------- | ----------- |
| 实验6    | `Data/6_soccer/dirty_index_10k.csv`<br />`Data/6_soccer/clean_index_10k.csv` | `Data/6_soccer/dirty_index_10k.csv`<br />`Data/6_soccer/clean_index_10k.csv` | `/results/raha_baran/` | `/results/raha_baran/results-6_soccer_10k_ori` | `备注内容1` |

---

### 实验 6 运行命令：

```bash
python3 CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/6_soccer/dirty_index_10k.csv --clean_path Data/6_soccer/clean_index_10k.csv --task_name 6_soccer_10k_ori --output_path results/raha_baran/ --index_attribute index
```



## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称  | 数值  | 备注      |
|----------|------------------|-------|-------|----------|
| 实验1 | `hospital` | acc | 0.9298245614035088 | `备注内容` |
|  |            | rec | 0.4165029469548134 | `备注内容` |
|  |            | EDR | 0.4165029469548134 | `备注内容` |
|  |            | hybrid | 0.13039368009625718 | `备注内容` |
|  |            | R-EDR | 0.36117936117936117 | `备注内容` |
| | | F1 | 0.5753052916804707 | `备注内容` |
| | | time | 431.0772750377655 | `备注内容` |
| 实验2 | `flights` | acc | 0.8576687116564418 | `备注内容` |
|           |            | rec      | 0.5682926829268292 | `备注内容` |
|           |            | EDR      | 0.516869918699187 | `备注内容` |
|           |            | hybrid   | 0.11865335019431696 | `备注内容` |
|           |            | R-EDR    | 0.12710084033613445 | `备注内容` |
| | | F1 | 0.6836185818591496 | `备注内容` |
| | | time | 391.8582489490509 | `备注内容` |
| 实验3 | `beers`    | acc      | 0.8086929905111724 | `备注内容` |
|           |            | rec      | 0.7867778439547349 | `备注内容` |
|           |            | EDR      | 0.7867778439547349 | `备注内容` |
|           |            | hybrid   | 0.053763122861445495 | `备注内容` |
|           |            | R-EDR    | 0.7224066390041494 | `备注内容` |
| | | F1 | 0.7975849056103869 | `备注内容` |
| | | time | 597.5746324062347 | `备注内容` |
| 实验4 | `rayyan`      | acc | 0.25741399762752076 | `备注内容` |
|           |            | rec      | 0.21852970795568982 | `备注内容` |
|           |            | EDR      | -0.23967774420946628 | `备注内容` |
|           |            | hybrid   | 0.053628215233389086 | `备注内容` |
|           |            | R-EDR    | 0.061224489795918366 | `备注内容` |
|  |  | F1 | 0.23638344221612895 | `备注内容` |
| | | time | 296.1245415210724 | `备注内容` |
| 实验5 | `tax`      | acc      |                       | `备注内容` |
|  |  | rec |                       | `备注内容` |
|          |            | EDR      |                       | `备注内容` |
|          |            | hybrid   |                       | `备注内容` |
|          |            | R-EDR |  | `备注内容` |
|  |  | F1 |  | `备注内容` |
|  |  | time |  | `备注内容` |
| 实验6 | `soccer` | acc | 0.5 | `备注内容` |
|  |  | rec | 0.24361493123772102 | `备注内容` |
|  |  | EDR | 0.2337917485265226 | `备注内容` |
|  |  | hybrid | 0.0070558120322061265 | `备注内容` |
|  |  | R-EDR | 0.2337917485265226 | `备注内容` |
|  |  | F1 | 0.3276089827828922 | `备注内容` |
|  |  | time | 2378.475999355316 | `备注内容` |
|  |  |  |  |  |

---

## 4. 结论

部分edr与recall相同的原因：

recall的值为清洗后数据正确修复的错误数量/所有本应修复的错误数量

edr计算为（Distance (Dirty to Clean)-Distance (Repaired to Clean)）/Distance (Dirty to Clean) 

- Distance (Dirty to Clean) 是脏数据与干净数据的距离，即脏数据与干净数据不一致的条目数。
- Distance (Repaired to Clean) 是清洗后数据与干净数据的距离，即清洗后的数据与干净数据不一致的条目数。

其中，两个指标的分母计算是一样的

因此当 清洗后数据正确修复的错误数量 =Distance (Dirty to Clean)-Distance (Repaired to Clean)时，edr和recall就相同。

 清洗后数据正确修复的错误数量：true_positives = ((cleaned_values == clean_values) & (dirty_values != cleaned_values)).sum()

这种情况可能的原因是：若清洗后的数据**准确地修复了所有脏数据中与干净数据不一致的项**，并且没有引入新的错误

