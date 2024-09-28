# 一些记录清洗结果和画图可视化的脚本
这是一些简单的Python脚本，用于记录清洗结果和可视化清洗，说明其用法。



### `inject_error.py`

------

`inject_error.py` 文件用于在adult和eeg的特征向量数据集上进行**错误注入**操作。错误注入的类型有两种：**随机错误（random errors）** 和 **系统错误（system errors）**。通过命令行参数，用户可以指定输入和输出文件路径、错误类型、以及注入错误的比例。

#### 主要函数说明

1. **`inject_random_error(df, percent)`**:
   - **作用**：注入随机错误。
   - **逻辑**：该函数随机选择一定比例（`percent`）的**行**，并将这些行的所有数值型特征替换为该列的最大值的 3 倍，模拟高幅度的异常值。
2. **`inject_system_error(df, percent, target_column)`**:
   - **作用**：注入系统错误。
   - **逻辑**：该函数基于训练的 **SGDClassifier** 模型，按照特征权重选择前 `x%` 的数据行，并将这些行中最重要的 3 个特征替换为该特征的均值。

#### 运行示例

##### 1.各个参数的作用以及命令行示例

命令行示例如下：

```
python inject_errors.py --input adult_data_vectorized.csv --output adult_with_random_errors.csv --error_type random --percent 5
```

1. **`--input`**：
   - 输入的 CSV 文件路径。
2. **`--output`**：
   - 输出的 CSV 文件路径。
3. **`--error_type`**：
   - 指定注入的错误类型：
     - `random`：注入随机错误，随机选择数据行，将行中的数值型特征替换为最大值的 3 倍。
     - `system`：注入系统错误，通过 SGD 模型的权重选择最重要的特征，对前 `x%` 的行中的重要特征进行均值替换。
4. **`--percent`**：
   - 注入错误的数据比例（百分比）。它决定了要对多少比例的行注入错误。

##### 2. **随机错误注入示例**：

假设你有一个向量化后的 **Adult 数据集**，并且想要对 5% 的数据行进行随机错误注入，命令如下：

```
python inject_error.py --input adult_vectorized.csv --output adult_with_random_errors.csv --error_type random --percent 5
```

##### 3. **系统错误注入示例**：

如果你想要对 10% 的数据行进行系统错误注入，命令如下：

```
python inject_error.py --input adult_vectorized.csv --output adult_with_system_errors.csv --error_type system --percent 10
```





### `eeg_vectorize.py`

------

 文件用于对 **EEG Eye State 数据集** 进行向量化处理，并提取每个时间步的统计特征，同时保留标签。通过命令行参数，用户可以指定输入和输出文件路径。

#### 主要函数说明

1. **`extract_statistical_features_by_time_step(df, label_column)`**:
   - **作用**：对 EEG 数据集中每个时间步的 14 个通道进行统计特征提取，并保留标签。

#### 命令行参数说明

- **`--input`**：
   - 输入的 `.arff` 文件路径，它包含 EEG 通道数据和标签。
   
- **`--output`**：
   - 输出的 CSV 文件路径，提取后的特征向量数据将被保存到此文件。

#### 运行示例

1. **运行示例**：
   假设有一个 `.arff` 格式的 **EEG Eye State 数据集**，希望将其转化为特征向量数据，同时保留标签，输出为 CSV 文件，命令如下：

   ```
   python vectorize_eeg.py --input eeg_eye_state.arff --output eeg_vectorized.csv
   ```

2. **各个参数的作用**：

   - `--input`：输入的 `.arff` 文件路径，包含 EEG 通道数据和眼睛状态标签。
     
   - `--output`：输出的 CSV 文件路径，保存提取的特征向量及其对应的标签。

#### 特征提取示例

该程序会将每个时间步的数据（14 个通道）提取成如下特征向量：
- **均值** (`mean`)：每个时间步的 14 个通道数据的平均值。
- **方差** (`variance`)：每个时间步的 14 个通道数据的方差，反映数值波动的幅度。
- **最大值** (`max`) 和 **最小值** (`min`)：每个时间步的 14 个通道数据中的最大值和最小值。
- **中位数** (`median`)：每个时间步的 14 个通道数据的中位数，用来平滑异常值的影响。
- **峰度** (`kurtosis`)：描述数据分布的尖峰程度，能够检测高幅度异常值。
- **偏度** (`skewness`)：描述数据分布的不对称性，检测信号的偏移。

这些特征将与最后的**标签列**（眼睛状态）一同被保留并输出到 CSV 文件中。





### `adult_vectorize.py`

------

文件用于对 **Adult 数据集** 进行向量化处理，针对数值型和类别型特征进行适当的编码，并将收入标签转换为二元值（0 和 1）。通过命令行参数，用户可以指定输入和输出文件路径。

#### 主要函数说明

1. `parse_arguments()`:
   - **作用**：解析命令行参数，用于获取输入和输出文件路径。
2. `main()`:
   - **作用**：读取数据集，按照数值型特征和类别型特征进行向量化处理，并将转换后的数据保存到输出文件中。

#### 命令行参数说明

- **`--input`**：
  - 输入的 `.csv` 文件路径，它包含 Adult 数据集的原始数据。
- **`--output`**：
  - 输出的 CSV 文件路径，向量化处理后的特征数据将被保存到此文件中。

#### 运行示例

1. **运行示例**：

   假设有一个 CSV 格式的 **Adult 数据集**，希望将其进行向量化处理，并保存为新的 CSV 文件，命令如下：

   ```
   python adult_vectorize.py --input adult.csv --output adult_vectorized.csv
   ```

2. **各个参数的作用**：

   - `--input`：输入的 `.csv` 文件路径，包含 Adult 数据集的原始数据。
   - `--output`：输出的 CSV 文件路径，保存向量化后的特征数据及其对应的标签。

#### 特征处理说明

该程序会对每个样本（行）的数据进行如下特征处理：

1. **数值型特征**：
   - 数值型特征包括 `age`, `fnlwgt`, `education-num`, `hours-per-week`。
   - 对这些特征使用 **标准化** (`Standardization`)，将它们的值转换为均值为 0，标准差为 1 的分布。
2. **类别型特征**：
   - 类别型特征包括 `workclass`, `education`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `native-country`。
   - 对这些特征使用 **独热编码** (`One-Hot Encoding`)，将每个类别值转换为二进制特征。每个类别对应一列，取值为 0 或 1，表示是否属于该类别。
3. **收入标签**：
   - 将标签列`income`进行二元编码：
     - `<=50K` 映射为 0。
     - `>50K` 映射为 1。
