# 数据集说明README，暂时不要把大于2M的数据集放放到git（太大了）
本文件记录了用于数据清洗系统复现的数据集的信息，包括属性、干净版本、脏版本及错误类型、数据规则集、标签、知识、下载链接和论文出处。

## 数据集目录
1. [Dataset 1](#dataset-1)
2. [Dataset 2](#dataset-2)
3. [Dataset 3](#dataset-3)
4. [Dataset 4](#dataset-4)
5. [Dataset 5](#dataset-5)

## 数据集说明

### Dataset 1
**属性**: [用户ID、姓名、年龄、地址、电子邮件]    
**是否有干净版本**: 有  
**是否有原生脏版本及对应错误**: 有，包含以下错误类型：拼写错误、缺失值、重复记录  
**数据规则集、标签、知识**: 提供了一组数据规则用于检测和修复错误，包含数据完整性和一致性规则  
**数据集下载链接**: [下载链接](https://example.com/dataset1)  
**论文出处**: [Horizon: scalable dependency-driven data cleaning](https://www.vldb.org/pvldb/vol14/p25)  

### Dataset 2
**属性**: [用户ID、姓名、年龄、地址、电子邮件]   
**是否有干净版本**: 有  
**是否有原生脏版本及对应错误**: 有，包含以下错误类型：价格错误、库存数量负值、供应商信息不完整  
**数据规则集、标签、知识**: 提供了错误检测的规则和标签，包含数据范围和一致性检查  
**数据集下载链接**: [下载链接](https://example.com/dataset2)  
**论文出处**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)  

### Dataset 3
**属性**: [用户ID、姓名、年龄、地址、电子邮件]   
**是否有干净版本**: 有  
**是否有原生脏版本及对应错误**: 有，包含以下错误类型：日期格式错误、订单重复、客户ID不存在  
**数据规则集、标签、知识**: 提供了错误检测和修复的规则，包含日期格式验证和唯一性检查  
**数据集下载链接**: [下载链接](https://example.com/dataset3)  
**论文出处**: 
- **Raha**: [A configuration-free error detection system](https://example.com/raha)
- **Baran**: [Effective error correction via a unified context representation and transfer learning](https://example.com/baran)

### Dataset 4
**属性**: [用户ID、姓名、年龄、地址、电子邮件]   
**是否有干净版本**: 有  
**是否有原生脏版本及对应错误**: 有，包含以下错误类型：成绩超出范围、姓名拼写错误、重复学生记录  
**数据规则集、标签、知识**: 提供了检测和修复规则，包含数据范围验证和重复记录检查  
**数据集下载链接**: [下载链接](https://example.com/dataset4)  
**论文出处**: [BoostClean: Automated Error Detection and Repair for Machine Learning](https://example.com/boostclean)  

### Dataset 5
**属性**: [用户ID、姓名、年龄、地址、电子邮件]   
**是否有干净版本**: 有  
**是否有原生脏版本及对应错误**: 有，包含以下错误类型：诊断信息错误、治疗方案缺失、重复记录  
**数据规则集、标签、知识**: 提供了数据规则和标签，包含数据一致性和完整性检查  
**数据集下载链接**: [下载链接](https://example.com/dataset5)  
**论文出处**: [Holistic data cleaning: Putting violations into context](https://example.com/holistic)