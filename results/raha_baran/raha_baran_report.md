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

#### 实验1-3 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                 | 本地输出路径             | 实际输出存放路径                  | 备注      |
|----------|--------------------------|--------------------------|--------------------------|---------------------------|-----------|
| 实验1    | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-hospital_1` | `备注内容1` |
| 实验2    | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-hospital_2` | `备注内容3` |
| 实验3    | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `Data/1_hospital/dirty_index.csv`<br />`Data/1_hospital/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-hospital_3` | `备注内容6` |
### 实验 1-3 运行命令：
```bash
python CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/1_hospital/dirty_index.csv --clean_path Data/1_hospital/clean_index.csv --task_name hospital_1 --output_path ../result/baran --index_attribute index --mse_attributes Score
```

### 数据集: `flights`

用于计算mse的属性：无

#### 实验4-6 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径      | 实际输出存放路径                        | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- | --------------------------------------- | ----------- |
| 实验4    | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-flights_1` | `备注内容1` |
| 实验5    | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-flights_2` | `备注内容3` |
| 实验6    | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `Data/2_flights/dirty_index.csv`<br />`Data/2_flights/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-flights_3` | `备注内容6` |

---

### 实验 4-6 运行命令：

```bash
python CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/2_flights/dirty_index.csv --clean_path Data/2_flights/clean_index.csv --task_name flights_2 --output_path ../result/baran --index_attribute index
```

### 数据集: `beers`

用于计算mse的属性：ounces、abv、ibu

#### 实验7-9 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径      | 实际输出存放路径                      | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- | ------------------------------------- | ----------- |
| 实验7    | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-beers_1` | `备注内容1` |
| 实验8    | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-beers_2` | `备注内容3` |
| 实验9    | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `Data/3_beers/dirty_index.csv`<br />`Data/3_beers/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-beers_3` | `备注内容6` |

---

### 实验 7-9 运行命令：

```bash
python CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/3_beers/dirty_index.csv --clean_path Data/3_beers/clean_index.csv --task_name beers_1 --output_path ../result/baran --index_attribute id --mse_attributes ounces abv ibu
```

### 数据集: `rayyan`

用于计算mse的属性：无

#### 实验10-12 设置

| 实验编号 | 本地输入路径                                                 | 实际输入存放路径                                             | 本地输出路径      | 实际输出存放路径                       | 备注        |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- | -------------------------------------- | ----------- |
| 实验7    | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-rayyan_1` | `备注内容1` |
| 实验8    | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-rayyan_2` | `备注内容3` |
| 实验9    | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `Data/4_rayyan/dirty_index.csv`<br />`Data/4_rayyan/clean_index.csv` | `../result/baran` | `/results/raha_baran/results-rayyan_3` | `备注内容6` |

---

### 实验 10-12 运行命令：

```bash
python CleanerRunScript/run_raha_baran/repair_with_raha.py --dirty_path Data/4_rayyan/dirty_index.csv --clean_path Data/4_rayyan/clean_index.csv --task_name rayyan_1 --output_path ../result/baran --index_attribute index
```



## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称  | 数值  | 备注      |
|----------|------------------|-------|-------|-----------|
| 实验1-3 | `hospital` | acc | 0.8732 | `备注内容` |
|  |            | rec | 0.5801 | `备注内容` |
|  |            | EDR | 0.5723 | `备注内容` |
|  |            | hybrid | 0.0817 | `备注内容` |
|  |            | R-EDR | 0.5151 | `备注内容` |
| 实验4-6 | `flights` | acc | 0.8368 | `备注内容` |
|           |            | rec      | 0.5190 | `备注内容` |
|           |            | EDR      | 0.4891 | `备注内容` |
|           |            | hybrid   | 0.1311 | `备注内容` |
|           |            | R-EDR    | 0.1153 | `备注内容` |
| 实验7-9 | `beers`    | acc      | 0.8257 | `备注内容` |
|           |            | rec      | 0.7651 | `备注内容` |
|           |            | EDR      | 0.7631 | `备注内容` |
|           |            | hybrid   | 0.0560 | `备注内容` |
|           |            | R-EDR    | 0.7050 | `备注内容` |
| 实验10-12 | `rayyan`      | acc | 0.8417 | `备注内容` |
|           |            | rec      | 0.2505 | `备注内容` |
|           |            | EDR      | 0.2491 | `备注内容` |
|           |            | hybrid   | 0.1659 | `备注内容` |
|           |            | R-EDR    | 0.2342 | `备注内容` |
|  |  |  |  |  |

---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。