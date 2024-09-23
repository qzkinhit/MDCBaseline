# 运行脚本说明

## ActiveClean
**论文**: [Activeclean: An interactive data cleaning framework for modern machine learning](https://arxiv.org/pdf/1601.03797.pdf)
### 脚本简介：
该脚本是基于 **ActiveClean** 方法的数据清洗脚本。ActiveClean以梯度下降的形式，逐步清洗数据并更新数据下游模型的参数，最终得到干净数据对应的模型。


## 运行命令:
```bash
python runActiveclean.py --input IMDB/imdb_features.p --output output.txt
```

### 命令行参数说明：
- `--input`: **必需参数**。指定输入的文件数据
- `--output`: **必需参数**。指定清洗过程中模型效果变化的存放位置。

### 命令将执行以下操作：
1. **读取输入数据**：
   - 输入文件路径通过 `--input` 参数指定，例如 `IMDB/imdb_features.p`。
   - 该文件应为 **CSV 格式**，包含需要清洗的数据。

2. **读取功能依赖规则**：
   - 输出文件路径通过 `--output` 参数指定，例如 `output.txt`。
   - 该文件应为 **txt 格式**，包含模型训练过程中效果的变化。
