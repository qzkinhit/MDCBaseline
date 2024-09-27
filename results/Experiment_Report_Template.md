# 实验报告

## 1. 清洗系统名称：`Horizon`

**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)
**可视化结果**: `results/horizon/visualization.png`  
**说明**: 此结果包含了Horizon系统在输入数据上的清洗结果，并通过可视化展示了数据清洗前后的差异。

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 数据集: `数据集名称1`

#### 实验1-3 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                 | 本地输出路径             | 实际输出存放路径                  | 备注      |
|----------|--------------------------|--------------------------|--------------------------|---------------------------|-----------|
| 实验1    | `local/input/path1`       | `github/baidupan/input1` | `local/output/path1`      | `github/baidupan/output1` | `备注内容1` |
|          | `local/input/path2`       | `github/baidupan/input2` | `local/output/path2`      | `github/baidupan/output2` | `备注内容2` |
| 实验2    | `local/input/path3`       | `github/baidupan/input3` | `local/output/path3`      | `github/baidupan/output3` | `备注内容3` |
|          | `local/input/path4`       | `github/baidupan/input4` | `local/output/path4`      | `github/baidupan/output4` | `备注内容4` |
|          | `local/input/path5`       | `github/baidupan/input5` | `local/output/path5`      | `github/baidupan/output5` | `备注内容5` |
| 实验3    | `local/input/path6`       | `github/baidupan/input6` | `local/output/path6`      | `github/baidupan/output6` | `备注内容6` |
|          | `local/input/path7`       | `github/baidupan/input7` | `local/output/path7`      | `github/baidupan/output7` | `备注内容7` |
### 实验 x 运行命令：
```bash
python run_horizon_base.py --dirty_path ../../Data/hospital/input_hospital_horizon_E2.csv --rule_path ../../Data/hospital/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/hospital/input_hospital_horizon.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```

### 数据集: `数据集名称2`

#### 实验4-6 设置

| 实验编号 | 本地输入路径             | 实际输入存放路径                         | 本地输出路径             | 实际输出存放路径                        | 备注      |
|----------|--------------------------|----------------------------------|--------------------------|----------------------------------|-----------|
| 实验4    | `local/input/path1`       | `github/baidupan/input1`         | `local/output/path1`      | `github/baidupan/output1`        | `备注内容1` |
|          | `local/input/path2`       | `github/baidupan/input2`         | `local/output/path2`      | `github/baidupan/output2`        | `备注内容2` |
| 实验5    | `local/input/path3`       | `github/baidupan/input3`         | `local/output/path3`      | `github/baidupan/output3`        | `备注内容3` |
|          | `local/input/path4`       | `github/baidupan/input4`         | `local/output/path4`      | `github/baidupan/output4`        | `备注内容4` |
|          | `local/input/path5`       | `github/baidupan/input5`         | `local/output/path5`      | `github/baidupan/output5`        | `备注内容5` |
| 实验6    | `local/input/path6`       | `github/baidupan/input6`         | `local/output/path6`      | `github/baidupan/output6`        | `备注内容6` |
|          | `local/input/path7`       | `github/baidupan/input7`         | `local/output/path7`      | `github/baidupan/output7`        | `备注内容7` |

---

## 3. 实验结果汇总

| 实验编号 | 数据集名称       | 指标名称  | 数值  | 备注      |
|----------|------------------|-------|-------|-----------|
| 实验1-3  | `数据集名称1`     | xx指标1 | `数值1` | `备注内容` |
|          |                  | xx指标2 | `数值2` | `备注内容` |
|          |                  | xx指标3 | `数值3` | `备注内容` |
| 实验4-6  | `数据集名称2`     | xx指标1 | `数值4` | `备注内容` |
|          |                  | xx指标2 | `数值5` | `备注内容` |
|          |                  | xx指标3 | `数值6` | `备注内容` |
| 实验7-9  | `数据集名称3`     | xx指标1 | `数值7` | `备注内容` |
|          |                  | xx指标2 | `数值8` | `备注内容` |
|          |                  | xx指标3 | `数值9` | `备注内容` |
| ...      | ...              | ...   | ...   | ...       |

---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。