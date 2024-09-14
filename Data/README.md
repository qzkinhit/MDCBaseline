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
**对应错误种类和数目**: 包含以下错误类型：拼写错误、缺失值、重复记录，分别xx个
**数据规则集、标签、知识**: 提供了一组数据规则用于检测和修复错误，包含数据完整性和一致性规则  
**数据集下载链接**: [下载链接](https://example.com/dataset1)  
**论文出处**: 数据集最原始的论文出处


| 错误类型     | bart脚本代码（如果有）       | 数据存放路径（太大了则附网盘链接即可）      | 本地输出路径             | 实际输出存放路径                  | 备注      |
|----------|---------------------|--------------------------|--------------------------|---------------------------|-----------|
| 异常值      | `local/input/path1` | `github/baidupan/input1` | `local/output/path1`      | `github/baidupan/output1` | `备注内容1` |
|          | `local/input/path2` | `github/baidupan/input2` | `local/output/path2`      | `github/baidupan/output2` | `备注内容2` |
| 空缺值      | `local/input/path3` | `github/baidupan/input3` | `local/output/path3`      | `github/baidupan/output3` | `备注内容3` |
|          | `local/input/path4` | `github/baidupan/input4` | `local/output/path4`      | `github/baidupan/output4` | `备注内容4` |
|          | `local/input/path5` | `github/baidupan/input5` | `local/output/path5`      | `github/baidupan/output5` | `备注内容5` |
| xxx规则的违反 | `local/input/path6` | `github/baidupan/input6` | `local/output/path6`      | `github/baidupan/output6` | `备注内容6` |
|          | `local/input/path7` | `github/baidupan/input7` | `local/output/path7`      | `github/baidupan/output7` | `备注内容7` |
