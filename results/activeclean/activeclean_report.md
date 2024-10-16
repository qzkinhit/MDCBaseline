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
### 实验 x 运行命令：
```bash
python run_horizon_base.py --dirty_path ../../Data/1_hospital/input_hospital_horizon_E2.csv --rule_path ../../Data/1_hospital/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/1_hospital/input_hospital_horizon.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```
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
### 实验 x 运行命令：
```bash
python run_horizon_base.py --dirty_path ../../Data/1_hospital/input_hospital_horizon_E2.csv --rule_path ../../Data/1_hospital/dc_rules-validate-fd-horizon.txt --clean_path ../../Data/1_hospital/input_hospital_horizon.csv --task_name hospital_horizon_E2 --output_path ../../results/horizon/hospital_horizon_E2
```
## 3. 实验结果汇总

| 实验编号 | 数据集                           | 1-初始准确率 | 1-清洗后准确率 | 2-初始准确率 | 2-清洗后准确率 | 3-初始准确率 | 3-清洗后准确率 |
|------|-------------------------------|-------|--------|--------|--------|--------|--------|
| 1.1  | `Adult/adult_random_5.p`      | 0.5371312309257376 | 0.5935910478128179 | 0.47956989247311826 | 0.5526881720430108 | 0.5186351706036746 | 0.6125984251968504 |
| 1.2  | `Adult/adult_random_10.p`     | 0.6060267857142857 | 0.5022321428571429 | 0.5643454038997214 | 0.5949860724233983 | 0.43799323562570464 | 0.5704622322435174 |
| 1.3  | `Adult/adult_random_15.p`     | 0.5881642512077294 | 0.6092995169082126 | 0.6593860684769776 | 0.5336481700118064 | 0.6016451233842538 | 0.5887191539365453 |
| 1.4  | `Adult/adult_random_20.p`     | 0.5510817307692307 | 0.5835336538461539 | 0.5369674185463659 | 0.618421052631579 | 0.6214925373134328 | 0.5982089552238806 |
| 1.5  | `Adult/adult_random_25.p`     | 0.6478405315614618 | 0.6079734219269103 | 0.6226790450928382 | 0.6273209549071618 | 0.5198606271777003 | 0.6 |
| 1.6  | `Adult/adult_systematic_5.p`  | 0.4277067921990585 | 0.5924680564895763 | 0.5744975744975745 | 0.6098406098406098 | 0.4785714285714286 | 0.5771428571428572 |
| 1.7  | `Adult/adult_systematic_10.p` | 0.5965116279069768 | 0.5901162790697675 | 0.5639470782800441 | 0.6085997794928335 | 0.5995462280204198 | 0.6097560975609756 |
| 1.8  | `Adult/adult_systematic_15.p` | 0.5906674542232723 | 0.5440047253396337 | 0.5697530864197531 | 0.5944444444444444 | 0.6133988936693301 | 0.5064535955746773 |
| 1.9  | `Adult/adult_systematic_20.p` | 0.516012084592145 | 0.5613293051359517 | 0.6251518833535844 | 0.5801944106925881 | 0.4893479664299548 | 0.5739186571981924 |
| 1.10 | `Adult/adult_systematic_25.p` | 0.6213793103448276 | 0.5786206896551724 | 0.48035837353549277 | 0.6271536871123363 | 0.465244322092223 | 0.5498967653131452 |
| 2.1  | `EEG/EEG_random_5.p`  | 0.4392755681818182 | 0.5326704545454546 | 0.5054443273621356 | 0.5763962065331928 | 0.5447839831401475 | 0.5834211450649807 |
| 2.2  | `EEG/EEG_random_10.p` | 0.5269970414201184 | 0.5887573964497042 | 0.46684053651266766 | 0.599478390461997 | 0.5677777777777778 | 0.5714814814814815 |
| 2.3  | `EEG/EEG_random_15.p` | 0.5176517255057517 | 0.57159857199524 | 0.5650454725187821 | 0.6022143139580862 | 0.5334637964774951 | 0.5600782778864971 |
| 2.4  | `EEG/EEG_random_20.p` | 0.5694675540765392 | 0.5262063227953411 | 0.5136702568351285 | 0.5571665285832643 | 0.5881612090680101 | 0.5453400503778337 |
| 2.5  | `EEG/EEG_random_25.p` | 0.5815602836879432 | 0.5625 | 0.5232350312779267 | 0.47229669347631814 | 0.5339547270306259 | 0.45894363071460276 |
| 2.6  | `EEG/EEG_systematic_5.p` | 0.5626535626535627 | 0.5812565812565813 | 0.5557887373207415 | 0.5764253235396992 | 0.432536893886156 | 0.5411103302881237 |
| 2.7  | `EEG/EEG_systematic_10.p` | 0.5572065378900446 | 0.5044576523031203 | 0.5512249443207127 | 0.5694135115070527 | 0.5370577281191806 | 0.5832402234636872 |
| 2.8  | `EEG/EEG_systematic_15.p` | 0.5897736143637783 | 0.5300546448087432 | 0.512185534591195 | 0.44693396226415094 | 0.5408682049276496 | 0.5670707860774344 |
| 2.9  | `EEG/EEG_systematic_20.p` | 0.43880972338642077 | 0.5461022632020117 | 0.5557439593047901 | 0.532852903772785 | 0.5803387030152829 | 0.5832300702189178 |
| 2.10 | `EEG/EEG_systematic_25.p` | 0.4928571428571429 | 0.5741071428571428 | 0.519137703475583 | 0.40607127144742633 | 0.5267415730337078 | 0.5123595505617977 |

---

## 4. 结论

在此部分总结实验的总体结果，并讨论实验结果相比于论文描述的优劣。根据实验结果，可以讨论该系统的优势、不足之处，以及未来可能的改进方向。