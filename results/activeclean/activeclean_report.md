# 实验报告

## 1. 清洗系统名称：`ActiveClean`

**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)
**说明**: 此结果包含了ActiveClean系统在不同输入数据上的模型效果。

---

## 2. 数据集上的实验设置
`备注：本地路径的文件如果大于5M，请使用百度网盘进行上传，在本地输入路径位置留下链接；否则直接存在本地输入路径上传github即可`

### 将数据集转化为向量
选择一种编码形式，将数据集中的数据集全部转化为向量形式。

### 对数据集插入错误
`随机错误`: 随机选择5%的数据，将值替换为最大值的3倍，模拟高幅度随机异常值。

`系统错误`: 使用在干净数据上训练的模型，通过三个最高加权特征对训练数据进行排序，然后将前5%数据中这些特征值替换为整个训练集中相应特征的平均值。


### 数据集: `Adult`[下载链接](https://archive.ics.uci.edu/dataset/2/adult)

#### 实验1

| 实验编号 | 本地输入路径                        | 实际输入存放路径                 | 本地输出路径                        | 实际输出存放路径                  | 备注      |
|------|-------------------------------|--------------------------|-------------------------------|---------------------------|-----------|
| 1.1  | `Adult/adult_random_5.p`      | `github/baidupan/input1` | `Adult/adult_random_5.txt`    | `github/baidupan/output1` | `备注内容1` |
| 1.2  | `Adult/adult_random_10.p`     | `github/baidupan/input2` | `Adult/adult_random_10.txt`     | `github/baidupan/output2` | `备注内容2` |
| 1.3  | `Adult/adult_random_15.p`     | `github/baidupan/input3` | `Adult/adult_random_15.txt`     | `github/baidupan/output3` | `备注内容3` |
| 1.4  | `Adult/adult_random_20.p`     | `github/baidupan/input4` | `Adult/adult_random_20.txt`     | `github/baidupan/output4` | `备注内容4` |
| 1.5  | `Adult/adult_random_25.p`     | `github/baidupan/input5` | `Adult/adult_random_25.txt`     | `github/baidupan/output5` | `备注内容5` |
| 1.6  | `Adult/adult_systematic_5.p`  | `github/baidupan/input6` | `Adult/adult_systematic_5.txt`  | `github/baidupan/output6` | `备注内容6` |
| 1.7  | `Adult/adult_systematic_10.p` | `github/baidupan/input7` | `Adult/adult_systematic_10.txt` | `github/baidupan/output7` | `备注内容7` |
| 1.8  | `Adult/adult_systematic_15.p` | `github/baidupan/input6` | `Adult/adult_systematic_15.txt` | `github/baidupan/output6` | `备注内容6` |
| 1.9  | `Adult/adult_systematic_20.p` | `github/baidupan/input7` | `Adult/adult_systematic_20.txt` | `github/baidupan/output7` | `备注内容7` |
| 1.10 | `Adult/adult_systematic_25.p` | `github/baidupan/input7` | `Adult/adult_systematic_25.txt` | `github/baidupan/output7` | `备注内容7` |

---

### 数据集: `EEG`[下载链接](https://archive.ics.uci.edu/dataset/121/eeg+database)

#### 实验2

| 实验编号 | 本地输入路径                     | 实际输入存放路径                 | 本地输出路径                        | 实际输出存放路径                  | 备注      |
|------|----------------------------|--------------------------|-------------------------------|---------------------------|-----------|
| 2.1  | `EEG/EEG_random_5.p`       | `github/baidupan/input1` | `EEG/EEG_random_5.txt`    | `github/baidupan/output1` | `备注内容1` |
| 2.2  | `EEG/EEG_random_10.p`      | `github/baidupan/input2` | `EEG/EEG_random_10.txt`     | `github/baidupan/output2` | `备注内容2` |
| 2.3  | `EEG/EEG_random_15.p`     | `github/baidupan/input3` | `EEG/EEG_random_15.txt`     | `github/baidupan/output3` | `备注内容3` |
| 2.4  | `EEG/EEG_random_20.p`     | `github/baidupan/input4` | `EEG/EEG_random_20.txt`     | `github/baidupan/output4` | `备注内容4` |
| 2.5  | `EEG/EEG_random_25.p`    | `github/baidupan/input5` | `EEG/EEG_random_25.txt`     | `github/baidupan/output5` | `备注内容5` |
| 2.6  | `EEG/EEG_systematic_5.p` | `github/baidupan/input6` | `EEG/EEG_systematic_5.txt`  | `github/baidupan/output6` | `备注内容6` |
| 2.7  | `EEG/EEG_systematic_10.p` | `github/baidupan/input7` | `EEG/EEG_systematic_10.txt` | `github/baidupan/output7` | `备注内容7` |
| 2.8  | `EEG/EEG_systematic_15.p` | `github/baidupan/input6` | `EEG/EEG_systematic_15.txt` | `github/baidupan/output6` | `备注内容6` |
| 2.9  | `EEG/EEG_systematic_20.p` | `github/baidupan/input7` | `EEG/EEG_systematic_20.txt` | `github/baidupan/output7` | `备注内容7` |
| 2.10 | `EEG/EEG_systematic_25.p` | `github/baidupan/input7` | `EEG/EEG_systematic_25.txt` | `github/baidupan/output7` | `备注内容7` |

---

## 3. 实验结果汇总

| 实验编号 | 数据集                           | 初始准确率 | 清洗后准确率 |
|------|-------------------------------|-------|--------|
| 1.1  | `Adult/adult_random_5.p`      |       |        |
| 1.2  | `Adult/adult_random_10.p`     |       |        |
| 1.3  | `Adult/adult_random_15.p`     |       |        |
| 1.4  | `Adult/adult_random_20.p`     |       |        |
| 1.5  | `Adult/adult_random_25.p`     |       |        |
| 1.6  | `Adult/adult_systematic_5.p`  |       |        |
| 1.7  | `Adult/adult_systematic_10.p` |       |        |
| 1.8  | `Adult/adult_systematic_15.p` |       |        |
| 1.9  | `Adult/adult_systematic_20.p` |       |        |
| 1.10 | `Adult/adult_systematic_25.p` |       |        |
| 2.1  | `EEG/EEG_random_5.p`  |       |        |
| 2.2  | `EEG/EEG_random_10.p` |       |        |
| 2.3  | `EEG/EEG_random_15.p` |       |        |
| 2.4  | `EEG/EEG_random_20.p` |       |        |
| 2.5  | `EEG/EEG_random_25.p` |       |        |
| 2.6  | `EEG/EEG_systematic_5.p` |       |        |
| 2.7  | `EEG/EEG_systematic_10.p` |       |        |
| 2.8  | `EEG/EEG_systematic_15.p` |       |        |
| 2.9  | `EEG/EEG_systematic_20.p` |       |        |
| 2.10 | `EEG/EEG_systematic_25.p` |       |        |

---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。