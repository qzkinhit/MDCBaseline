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
python .\CleanerRunScript\run_activeclean\runActiveclean.py --correct_data "C:\Users\lzfd\Desktop\work\handle_data\adult_1\adult_data_vectorized.csv" --injected_data "C:\Users\lzfd\Desktop\work\handle_data\adult_1\adult_systematic_25.csv" --output "C:\Users\lzfd\Desktop\work\result\adult\adult_system_25_1.txt"
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
python .\CleanerRunScript\run_activeclean\runActiveclean.py --correct_data "C:\Users\lzfd\Desktop\work\handle_data\eeg\eeg_data_vectorized.csv" --injected_data "C:\Users\lzfd\Desktop\work\handle_data\eeg\eeg_random_5.csv" --output "C:\Users\lzfd\Desktop\work\MDCBaseline\results\activeclean\eeg\eeg_random_5_1.txt"
```
## 3. 实验结果汇总

| 实验编号 | 数据集                           | 1-初始准确率 | 1-清洗后准确率 | 2-初始准确率 | 2-清洗后准确率 | 3-初始准确率 | 3-清洗后准确率 |
|------|-------------------------------|-------|--------|--------|--------|--------|--------|
| 1.1  | `Adult/adult_random_5.p`      | 0.5215681601525262  | 0.5337225929456625 | 0.5631056346452925  | 0.6073693025481517 | 0.534847764034253 | 0.5407944814462416 |
| 1.2  | `Adult/adult_random_10.p`     | 0.5909147948299661 | 0.4892709248337307 | 0.528270998614784 | 0.5776350585568568 | 0.5299736081437728 | 0.6012316199572704 |
| 1.3  | `Adult/adult_random_15.p`     | 0.5579045339715464 | 0.5656162744315916 | 0.5383268220396066 | 0.5522026134985855 | 0.553330663462822 | 0.4916566546522494 |
| 1.4  | `Adult/adult_random_20.p`     | 0.595322466335932 | 0.605669737774628 | 0.5055350553505535 | 0.5851546977008232 | 0.5034756703078451 | 0.5458930344729749 |
| 1.5  | `Adult/adult_random_25.p`     | 0.5659382064807837 | 0.5062547098718915 | 0.5781578157815782 | 0.6255625562556255 | 0.5563052931473984 | 0.5823961613435298 |
| 1.6  | `Adult/adult_systematic_5.p`  | 0.5539872971065631 | 0.5741002117148906 | 0.525067512034754 | 0.5417400493131385 | 0.5249705535924617 | 0.6257950530035336 |
| 1.7  | `Adult/adult_systematic_10.p` | 0.5731132075471698 | 0.5052135054617676 | 0.5258407517309595 | 0.5636745796241345 | 0.5650006232082762 | 0.5777140720428767 |
| 1.8  | `Adult/adult_systematic_15.p` | 0.5727140399629482 | 0.5463808389572582 | 0.49868697478991597 | 0.5110294117647058 | 0.48812803358257906 | 0.5913682277318641 |
| 1.9  | `Adult/adult_systematic_20.p` | 0.5724708853655114 | 0.5016135821523783 | 0.5554469273743017 | 0.5636871508379888 | 0.5669038649365146 | 0.5526719687456397 |
| 1.10 | `Adult/adult_systematic_25.p` | 0.5192421551213736 | 0.5951746595618709 | 0.4900820283370619 | 0.5321401938851603 | 0.535449421536636 | 0.5636309700385642 |
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