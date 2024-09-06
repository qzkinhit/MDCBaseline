# 数据清洗脚本运行README
每个系统运行对脚本

## 目录
1. [Horizon](#horizon)
2. [Activeclean](#activeclean)
3. [Raha & Baran](#raha--baran)
4. [BoostClean](#boostclean)
5. [CPClean](#cpclean)
6. [BigDansing_Holistic](#bigdansing_holistic)
7. [Scared](#scared)
8. [Holoclean](#holoclean)

## 运行脚本说明

### Horizon
**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)  
**运行命令1**: 
```bash
python run_horizon.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，进行依赖驱动的数据清洗，并将结果保存到`data/output.csv`中。

**运行命令2**: 
```bash
python run_horizon.py --input data/input.csv --output data/output1.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，进行依赖驱动的数据清洗，并将结果保存到`data/output.csv`中。

### Activeclean
**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)  
**运行命令**: 
```bash
python run_activeclean.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用Activeclean框架进行交互式数据清洗，并将结果保存到`data/output.csv`中。

### Raha & Baran
**论文**:
- **Raha**: A configuration-free error detection system  
- **Baran**: Effective error correction via a unified context representation and transfer learning  
**运行命令**: 
```bash
python run_raha.py --input data/input.csv --output data/output.csv
python run_baran.py --input data/input.csv --output data/output.csv
```
**说明**: 这两个脚本分别用于运行Raha的错误检测和Baran的错误修正，将结果保存到`data/output.csv`中。

### BoostClean
**论文**: Automated Error Detection and Repair for Machine Learning  
**运行命令**: 
```bash
python run_boostclean.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用BoostClean进行自动错误检测和修复，并将结果保存到`data/output.csv`中。

### CPClean
**论文**: Nearest neighbor classifiers over incomplete information: From certain answers to certain predictions  
**运行命令**: 
```bash
python run_cpclean.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用CPClean处理不完整信息，并将结果保存到`data/output.csv`中。

### BigDansing_Holistic
**论文**: Holistic data cleaning: Putting violations into context  
**运行命令**: 
```bash
python run_bigdansing_holistic.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用BigDansing_Holistic进行整体数据清洗，并将结果保存到`data/output.csv`中。

### Scared
**论文**: Don't be scared: Use scalable automatic repairing with maximal likelihood and bounded changes  
**运行命令**: 
```bash
python run_scared.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用Scared进行自动修复，并将结果保存到`data/output.csv`中。

### Holoclean
**论文**: Holistic data repairs with probabilistic inference  
**运行命令**: 
```bash
python run_holoclean.py --input data/input.csv --output data/output.csv
```
**说明**: 此脚本将读取`data/input.csv`中的数据，使用Holoclean进行整体数据修复，并将结果保存到`data/output.csv`中。

---