# 数据清洗结果记录README

本文件记录了每个数据清洗系统的运行结果、结果存储位置、可视化结果以及不同系统在相同数据集下的对比结果。

## 目录
1. [Horizon](#horizon)
2. [Activeclean](#activeclean)
3. [Raha & Baran](#raha--baran)
4. [BoostClean](#boostclean)
5. [CPClean](#cpclean)
6. [BigDansing_Holistic](#bigdansing_holistic)
7. [Scared](#scared)
8. [Holoclean](#holoclean)
9. [对比结果](#对比结果)

## 结果记录

### Horizon
**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)  
**结果存储位置**: `results/horizon/output.csv`  
**可视化结果**: `results/horizon/visualization.png`  
**说明**: 此结果包含了Horizon系统在输入数据上的清洗结果，并通过可视化展示了数据清洗前后的差异。

### Activeclean
**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)  
**结果存储位置**: `results/activeclean/output.csv`  
**可视化结果**: `results/activeclean/visualization.png`  
**说明**: 此结果展示了Activeclean系统在输入数据上的清洗结果和相应的可视化对比。

### Raha & Baran
**论文**:
- **Raha**: A configuration-free error detection system  
- **Baran**: Effective error correction via a unified context representation and transfer learning  
**结果存储位置**: 
  - Raha: `results/raha/output.csv`
  - Baran: `results/baran/output.csv`  
**可视化结果**: 
  - Raha: `results/raha/visualization.png`
  - Baran: `results/baran/visualization.png`  
**说明**: 这些结果展示了Raha系统的错误检测结果和Baran系统的错误修正结果及其可视化。

### BoostClean
**论文**: Automated Error Detection and Repair for Machine Learning  
**结果存储位置**: `results/boostclean/output.csv`  
**可视化结果**: `results/boostclean/visualization.png`  
**说明**: 结果包含了BoostClean系统在输入数据上的自动错误检测和修复结果，并通过可视化进行展示。

### CPClean
**论文**: Nearest neighbor classifiers over incomplete information: From certain answers to certain predictions  
**结果存储位置**: `results/cpclean/output.csv`  
**可视化结果**: `results/cpclean/visualization.png`  
**说明**: 结果展示了CPClean系统处理不完整信息后的数据结果和相应的可视化对比。

### BigDansing_Holistic
**论文**: Holistic data cleaning: Putting violations into context  
**结果存储位置**: `results/bigdansing_holistic/output.csv`  
**可视化结果**: `results/bigdansing_holistic/visualization.png`  
**说明**: 此结果展示了BigDansing_Holistic系统在输入数据上的整体数据清洗结果和可视化展示。

### Scared
**论文**: Don't be scared: Use scalable automatic repairing with maximal likelihood and bounded changes  
**结果存储位置**: `results/scared/output.csv`  
**可视化结果**: `results/scared/visualization.png`  
**说明**: 结果展示了Scared系统在输入数据上的自动修复结果及其可视化对比。

### Holoclean
**论文**: Holistic data repairs with probabilistic inference  
**结果存储位置**: `results/holoclean/output.csv`  
**可视化结果**: `results/holoclean/visualization.png`  
**说明**: 结果展示了Holoclean系统在输入数据上的整体数据修复结果和相应的可视化展示。

## 对比结果
**存储位置**: `results/comparison`  
**说明**: 该文件夹包含了不同数据清洗系统在相同数据集上的清洗结果对比。对比结果包括清洗前后的数据对比、错误检测和修复的有效性分析，以及各系统的性能评估。每个对比结果均包含详细的分析报告和可视化图表。

---

确保每个系统的结果文件夹 (`results/horizon`, `results/activeclean`, `results/raha`, `results/baran`, `results/boostclean`, `results/cpclean`, `results/bigdansing_holistic`, `results/scared`, `results/holoclean`) 中包含相应的输出文件和可视化结果。对比结果文件夹 (`results/comparison`) 中应有综合对比分析和相应的报告。