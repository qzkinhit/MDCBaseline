# 运行脚本说明

## Horizon
**论文**: [Horizon: Scalable Dependency-Driven Data Cleaning](https://www.vldb.org/pvldb/vol14/p25)
### 脚本简介：
该脚本是基于 **Horizon** 方法的依赖驱动数据清洗脚本。Horizon 通过识别数据中的功能依赖（FD，Functional Dependency）违规来进行数据清洗。本脚本会读取指定的输入数据文件，应用约束规则（功能依赖规则），并生成清洗后的数据文件。

## 运行命令1:
```bash
python run_horizon.py --input data/input.csv --rule_text data/rules.txt --output data/output.csv
```
### 命令行参数说明：
- `--input`: **必需参数**。指定待清洗数据的 CSV 文件路径。
- `--rule_text`: **必需参数**。指定包含功能依赖规则的文件路径。
- `--output`: **必需参数**。指定清洗后数据的保存路径。

### 命令将执行以下操作：
1. **读取输入数据**：
   - 输入文件路径通过 `--input` 参数指定，例如 `data/input.csv`。
   - 该文件应为 **CSV 格式**，包含需要清洗的数据。
2. **读取功能依赖规则**：
   - 功能依赖规则文件路径通过 `--rule_text` 参数指定，例如 `data/rules.txt`。
   - 该文件应包含功能依赖规则，例如 `A ⇒ B`，表示属性 A 功能依赖于属性 B。

3.**输出清洗结果**：
   - 清洗后的结果将保存到通过 `--output` 参数指定的路径，例如 `data/output.csv`。
   - 输出文件也是 **CSV 格式**，包含清洗后的数据。



### 运行示例：
```bash
python run_horizon.py --input data/hospital_test.csv --rule_text data/hospital_rules.txt --output data/hospital_cleaned.csv
```

## 运行命令2:
```bash
python xx
```
### 命令行参数说明：
xx
### 命令将执行以下操作：
xx