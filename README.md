# 数据清洗系统复现

本仓库包含了对多个数据清洗系统的复现工作，这些系统描述于各类研究论文中。目标是复现这些系统，并在受控环境中验证其有效性。

## 目录
1. [Horizon](#horizon)
2. [Activeclean](#activeclean)
3. [Raha & Baran](#raha--baran)
4. [BoostClean](#boostclean)
5. [CPClean](#cpclean)
6. [BigDansing_Holistic](#bigdansing_holistic)
7. [Scared](#scared)
8. [Holoclean](#holoclean)

## 复现进度

### Horizon
**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)  
**重要度**: 绿色 (zk)  
**状态**: 进行中  
**备注**: 该论文描述了一种可扩展的依赖驱动数据清洗方法。复现工作集中在实现文中描述的方法，并对提供的数据集进行验证。

### Activeclean
**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)  
**重要度**: 绿色 (zk)  
**语言**: Python  
**状态**: 进行中  
**备注**: 使用Python复现Activeclean。重点在于复现交互式框架及其与机器学习工作流的集成。

### Raha & Baran
**论文**:
- **Raha**: A configuration-free error detection system  
- **Baran**: Effective error correction via a unified context representation and transfer learning  
**重要度**: 
- Raha: 红色 (sy)  
- Baran: 红色 (sy)  
**状态**: 计划中  
**备注**: Raha和Baran将依次进行复现。Raha专注于错误检测，而Baran在此基础上通过迁移学习进行错误修正。

### BoostClean
**论文**: Automated Error Detection and Repair for Machine Learning  
**重要度**: 红色 (sy)  
**状态**: 计划中  
**备注**: BoostClean将被实现，以评估其在机器学习数据准备中的自动错误检测与修复能力。

### CPClean
**论文**: Nearest neighbor classifiers over incomplete information: From certain answers to certain predictions  
**重要度**: 红色 (sy)  
**语言**: Python  
**状态**: 计划中  
**备注**: 实现将专注于使用最近邻分类器处理不完整信息。

### BigDansing_Holistic
**论文**: Holistic data cleaning: Putting violations into context  
**重要度**: 红色 (sy)  
**状态**: 计划中  
**备注**: 将评估此方法在处理数据违规时的上下文处理能力。

### Scared
**论文**: Don't be scared: Use scalable automatic repairing with maximal likelihood and bounded changes  
**重要度**: 红色 (sy)  
**状态**: 计划中  
**备注**: 复现工作将集中于系统在受约束变化下自动修复数据的能力。

### Holoclean
**论文**: Holistic data repairs with probabilistic inference  
**重要度**: 红色 (sy)  
**状态**: 计划中  
**备注**: 将实现Holoclean，以测试其通过概率推理进行整体数据修复的方法。

## 贡献
欢迎对本复现工作做出贡献。请提交pull request以包含您的更改或改进。

## 许可证
本项目基于MIT许可证 - 详情参见[LICENSE](LICENSE)文件。

---
