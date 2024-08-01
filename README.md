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

## 系统调研与复现进度

### Horizon
**论文**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)  
**主讲人**: zekai  
**状态**: 进行中  
**摘要**: 该论文描述了一种可扩展的依赖驱动数据清洗方法。复现工作集中在实现文中描述的方法，并对提供的数据集进行验证。  
**错误处理方法（清洗信号）**: 依赖关系  
**处理的错误类型**: 依赖冲突、数据不一致  
**前置配置**: 依赖规则集  
**下游反馈内容**: 通用的系统，无特定下游  
**面向任务**: 通用任务的检测  
**清洗判别指标**: 准确率、召回率

### Activeclean
**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)  
**主讲人**: siying  
**语言**: Python  
**状态**: 进行中  
**摘要**: 使用Python复现Activeclean。重点在于复现交互式框架及其与机器学习工作流的集成。  
**错误处理方法（清洗信号）**: 用户交互反馈  
**处理的错误类型**: 噪声、缺失值  
**前置配置**: 用户反馈机制  
**下游反馈内容**: 凸损失模型  
**面向任务**: 凸损失模型的检测与修复  
**清洗判别指标**: 数据准确性、模型性能提升 

### Raha & Baran
**论文**:
- **Raha**: A configuration-free error detection system  
- **Baran**: Effective error correction via a unified context representation and transfer learning  
**主讲人**: zekai & siying  
**状态**: 计划中  
**摘要**: Raha和Baran将依次进行复现。Raha专注于错误检测，而Baran在此基础上通过迁移学习进行错误修正。  
**错误处理方法（清洗信号）**: 规则驱动、上下文表示  
**处理的错误类型**: 数据错误、不一致性  
**前置配置**: 无需配置（Raha），上下文规则集（Baran）  
**下游反馈内容**: 无特定下游  
**面向任务**: 错误检测和修复  
**清洗判别指标**: 错误检测率、修复精度

### BoostClean
**论文**: Automated Error Detection and Repair for Machine Learning  
**主讲人**: siying  
**状态**: 计划中  
**摘要**: BoostClean将被实现，以评估其在机器学习数据准备中的自动错误检测与修复能力。  
**错误处理方法（清洗信号）**: 统计分析、机器学习  
**处理的错误类型**: 噪声、异常值  
**前置配置**: 错误模式库  
**下游反馈内容**: 机器学习模型  
**面向任务**: 错误检测和修复  
**清洗判别指标**: 修复后模型性能提升

### CPClean
**论文**: Nearest neighbor classifiers over incomplete information: From certain answers to certain predictions  
**主讲人**: siying  
**语言**: Python  
**状态**: 计划中  
**摘要**: 实现将专注于使用最近邻分类器处理不完整信息。  
**错误处理方法（清洗信号）**: 最近邻分类  
**处理的错误类型**: 缺失值、不完整信息  
**前置配置**: 无  
**下游反馈内容**: 预测模型  
**面向任务**: 错误检测和修复  
**清洗判别指标**: 准确率、填充正确率

### BigDansing & Holistic
**论文**: Holistic data cleaning: Putting violations into context  
**主讲人**: zekai & siying  
**状态**: 计划中  
**摘要**: 将评估此方法在处理数据违规时的上下文处理能力。  
**错误处理方法（清洗信号）**: 上下文分析  
**处理的错误类型**: 数据违规、上下文冲突  
**前置配置**: 上下文规则集  
**下游反馈内容**: 无特定下游  
**面向任务**: 错误检测  
**清洗判别指标**: 准确率、召回率

### Scared
**论文**: Don't be scared: Use scalable automatic repairing with maximal likelihood and bounded changes  
**主讲人**: siying  
**状态**: 计划中  
**摘要**: 复现工作将集中于系统在受约束变化下自动修复数据的能力。  
**错误处理方法（清洗信号）**: 最大似然估计  
**处理的错误类型**: 噪声、错误值  
**前置配置**: 错误概率模型  
**下游反馈内容**: 无特定下游  
**面向任务**: 错误修复  
**清洗判别指标**: 修复精度、受约束变化量

### Holoclean
**论文**: Holistic data repairs with probabilistic inference  
**主负责人**: zekai  
**状态**: 计划中  
**摘要**: 将实现Holoclean，以测试其通过概率推理进行整体数据修复的方法。  
**错误处理方法（清洗信号）**: 概率推理  
**处理的错误类型**: 数据错误、不一致性  
**前置配置**: 先验概率、规则集  
**下游反馈内容**: 无特定下游  
**面向任务**: 错误修复  
**清洗判别指标**: 修复准确率、数据一致性
