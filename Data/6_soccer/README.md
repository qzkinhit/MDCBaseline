
# 数据集：Soccer

## 属性集
```text
[name,surname,birthyear,birthplace,position,team,city,stadium,season,manager]
```

## 数据规模
**属性个数 × 条目数**：10 × 200000

## 干净版本
存在

## 原生错误种类及数量
### 错误种类：T, value swaps
### 错误数量：1.56%

## 数据规则集、标签、知识存放路径
- **FD 规则**：`../../Data/6_soccer/dc_rules-validate-fd-horizon.txt`
- **DC 规则**：`../../Data/6_soccer/dc_rules_dc_holoclean.txt`


## 数据集出处
### ED2: A Case for Active Learning in Error Detection

## 人工错误注入记录

## 主键属性集合：
```text
name,season,manager,city
```
1. **规则涉及**的属性中，保证**主键属性集合干净**的情况下，注入不同比例的混合错误。
   - 每个规则违反、非主键属性空缺值、非主键属性异常值的混合错误。
   - **错误注入比例**：
   
     - **a. 0.25%**  
       - 每个规则(不涉及主键属性)，每个规则涉及的属性总体 0.25% 的违反
       - 非主键属性0.25%的空缺值
       - 非主键属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=8921
       - **错误条目数** = 8134
       
    - **b. 0.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体0.5% 的违反
      - 非主键属性 0.5% 的空缺值
      - 非主键属性 0.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 17890
      - **错误条目数** = 15953
    
    - **c. 0.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 0.75% 的违反
      - 非主键属性 0.75% 的空缺值
      - 非主键属性 0.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 26664
      - **错误条目数** = 23389
    
    - **d. 1%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1% 的违反
      - 非主键属性 1% 的空缺值
      - 非主键属性 1% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 35595
      - **错误条目数** = 30718
    
    - **e. 1.25%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.25% 的违反
      - 非主键属性 1.25% 的空缺值
      - 非主键属性 1.25% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 44361
      - **错误条目数** = 37474
    
    - **f. 1.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.5% 的违反
      - 非主键属性 1.5% 的空缺值
      - 非主键属性 1.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 53253
      - **错误条目数** = 44653
    
    - **g. 1.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.75% 的违反
      - 非主键属性 1.75% 的空缺值
      - 非主键属性 1.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 61927
      - **错误条目数** = 51183
    
    - **h. 2%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 2% 的违反
      - 非主键属性 2% 的空缺值
      - 非主键属性 2% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 70630
      - **错误条目数** = 57247


### 数据存放路径
- **BART 脚本路径**：**0.25%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.25/soccer_mixed_all.xml`
                   **0.5%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.5/soccer_mixed_all.xml`
                   **0.75%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.75/soccer_mixed_all.xml`
                   **1%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1/soccer_mixed_all.xml`
                   **1.25%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.25/soccer_mixed_all.xml`
                   **1.5%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.5/soccer_mixed_all.xml`
                   **1.75%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.75/soccer_mixed_all.xml`
                   **2%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_2/soccer_mixed_all.xml`
- **数据存放路径**：**0.25%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_soccer_mix_0.25.csv`
                   **0.5%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_soccer_mix_0.5.csv`
                   **0.75%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_soccer_mix_0.75.csv`
                   **1%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1/dirty_soccer_mix_1.csv`
                   **1.25%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_soccer_mix_1.25.csv`
                   **1.5%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_soccer_mix_1.5.csv`
                   **1.75%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_soccer_mix_1.75.csv`
                   **2%**:`../6_soccer/noise_with_correct_primary_key/dirty_mixed_2/dirty_soccer_mix_2.csv`

---

2. **无条件**注入不同比例的错误。
   - 每个规则违反、每个属性空缺值、每个属性异常值的混合错误。
   - **错误注入比例**：
     - **a. 0.25%**  
       - 每个规则涉及的属性总体 0.25% 的违反
       - 每个属性0.25%的空缺值
       - 每个属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=13051
       - **错误条目数** = 12625

      - **b. 0.5%**  
        - 每个规则涉及的属性总体 0.5% 的违反
        - 每个属性 0.5% 的空缺值
        - 每个属性 0.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 25966
        - **错误条目数** = 23901
      
      - **c. 0.75%**  
        - 每个规则涉及的属性总体 0.75% 的违反
        - 每个属性 0.75% 的空缺值
        - 每个属性 0.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 38764
        - **错误条目数** = 34756
      
      - **d. 1%**  
        - 每个规则涉及的属性总体 1% 的违反
        - 每个属性 1% 的空缺值
        - 每个属性 1% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 51300
        - **错误条目数** = 44430
      
      - **e. 1.25%**  
        - 每个规则涉及的属性总体 1.25% 的违反
        - 每个属性 1.25% 的空缺值
        - 每个属性 1.25% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 64025
        - **错误条目数** = 54532
      
      - **f. 1.5%**  
        - 每个规则涉及的属性总体 1.5% 的违反
        - 每个属性 1.5% 的空缺值
        - 每个属性 1.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 76379
        - **错误条目数** = 62921
      
      - **g. 1.75%**  
        - 每个规则涉及的属性总体 1.75% 的违反
        - 每个属性 1.75% 的空缺值
        - 每个属性 1.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 89063
        - **错误条目数** = 71703
      
      - **h. 2%**  
        - 每个规则涉及的属性总体 2% 的违反
        - 每个属性 2% 的空缺值
        - 每个属性 2% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 101523
        - **错误条目数** = 79852

### 数据存放路径
- **BART 脚本路径**：**0.25%**:`../6_soccer/noise/dirty_mixed_0.25/soccer_mixed_all.xml`
                   **0.5%**:`../6_soccer/noise/dirty_mixed_0.5/soccer_mixed_all.xml`
                   **0.75%**:`../6_soccer/noise/dirty_mixed_0.75/soccer_mixed_all.xml`
                   **1%**:`../6_soccer/noise/dirty_mixed_1/soccer_mixed_all.xml`
                   **1.25%**:`../6_soccer/noise/dirty_mixed_1.25/soccer_mixed_all.xml`
                   **1.5%**:`../6_soccer/noise/dirty_mixed_1.5/soccer_mixed_all.xml`
                   **1.75%**:`../6_soccer/noise/dirty_mixed_1.75/soccer_mixed_all.xml`
                   **2%**:`../6_soccer/noise/dirty_mixed_2/soccer_mixed_all.xml`
- **数据存放路径**：**0.25%**:`../6_soccer/noise/dirty_mixed_0.25/dirty_soccer_mix_0.25.csv`
                   **0.5%**:`../6_soccer/noise/dirty_mixed_0.5/dirty_soccer_mix_0.5.csv`
                   **0.75%**:`../6_soccer/noise/dirty_mixed_0.75/dirty_soccer_mix_0.75.csv`
                   **1%**:`../6_soccer/noise/dirty_mixed_1/dirty_soccer_mix_1.csv`
                   **1.25%**:`../6_soccer/noise/dirty_mixed_1.25/dirty_soccer_mix_1.25.csv`
                   **1.5%**:`../6_soccer/noise/dirty_mixed_1.5/dirty_soccer_mix_1.5.csv`
                   **1.75%**:`../6_soccer/noise/dirty_mixed_1.75/dirty_soccer_mix_1.75.csv`
                   **2%**:`../6_soccer/noise/dirty_mixed_2/dirty_soccer_mix_2.csv`

### soccer 下目录结构说明
noise：存放纯随机噪声注入
noise with correct primary key：存放主键干净的噪声注入
