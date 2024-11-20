
# 数据集：Hospital

## 属性集
```text
[ProviderNumber, HospitalName, Address1, Address2, Address3, City, State, ZipCode, CountyName, 
PhoneNumber, HospitalType, HospitalOwner, EmergencyService, Condition, MeasureCode, MeasureName, 
Score, Sample, Stateavg]
```

## 数据规模
**属性个数 × 条目数**：19 × 1000

## 干净版本
存在

## 原生错误种类及数量
### 错误种类：typo(拼写错误),violated attribute dependency(规则违反)
### 错误数量：1000*0.3%

## 数据规则集、标签、知识存放路径
- **FD 规则**：`../../Data/hospital/fd_rules-validate-fd-horizon.txt`
- **DC 规则**：`../../Data/hospital/dc_rules_dc_holoclean.txt`


## 数据集出处
### Holistic Data Cleaning: Putting Violations Into Context

## 人工错误注入记录

## 主键属性集合：
```
ProviderNumber、MeasureCode
注：ProviderNumber和HospitalName构成循环依赖，这里选择ProviderNumber作为主键  
MeasureCode和MeasureName构成循环依赖，这里选择MeasureCode作为主键
```
1. **规则涉及**的属性中，保证**主键属性集合干净**的情况下，注入不同比例的混合错误。
   - 每个规则违反、非主键属性空缺值、非主键属性异常值的混合错误。
   - **错误注入比例**：
   
     - **a. 0.25%**  
       - 每个规则(不涉及主键属性)，每个规则涉及的属性总体 0.25% 的违反
       - 非主键属性0.25%的空缺值
       - 非主键属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数 = 83
       - **错误条目数** = 83
       
    - **b. 0.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体0.5% 的违反
      - 非主键属性 0.5% 的空缺值
      - 非主键属性 0.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 176
      - **错误条目数** = 162
    
    - **c. 0.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 0.75% 的违反
      - 非主键属性 0.75% 的空缺值
      - 非主键属性 0.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 242
      - **错误条目数** = 222
    
    - **d. 1%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1% 的违反
      - 非主键属性 1% 的空缺值
      - 非主键属性 1% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 364
      - **错误条目数** = 308
    
    - **e. 1.25%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.25% 的违反
      - 非主键属性 1.25% 的空缺值
      - 非主键属性 1.25% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 422
      - **错误条目数** = 341
    
    - **f. 1.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.5% 的违反
      - 非主键属性 1.5% 的空缺值
      - 非主键属性 1.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 532
      - **错误条目数** = 412
    
    - **g. 1.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.75% 的违反
      - 非主键属性 1.75% 的空缺值
      - 非主键属性 1.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 608
      - **错误条目数** = 443
    
    - **h. 2%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 2% 的违反
      - 非主键属性 2% 的空缺值
      - 非主键属性 2% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 694
      - **错误条目数** = 509


### 数据存放路径
- **BART 脚本路径**：**0.25%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.25/hospitals_mixed_correct_primary_key.xml`
                   **0.5%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.5/hospitals_mixed_correct_primary_key.xml`
                   **0.75%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.75/hospitals_mixed_correct_primary_key.xml`
                   **1%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1/hospitals_mixed_correct_primary_key.xml`
                   **1.25%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.25/hospitals_mixed_correct_primary_key.xml`
                   **1.5%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.5/hospitals_mixed_correct_primary_key.xml`
                   **1.75%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.75/hospitals_mixed_correct_primary_key.xml`
                   **2%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_2/hospitals_mixed_correct_primary_key.xml`
- **数据存放路径**：**0.25%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_hospitals_null.csv`
                  **0.5%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_hospitals_null.csv`
                  **0.75%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_hospitals_null.csv`
                  **1%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1/dirty_hospitals_null.csv`
                  **1.25%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_hospitals_null.csv`
                  **1.5%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_hospitals_null.csv`
                  **1.75%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_hospitals_null.csv`
                  **2%**:`../1_hospital/noise_with_correct_primary_key/dirty_mixed_2/dirty_hospitals_null.csv`
                  

---

2. **无条件**注入不同比例的错误。
   - 每个规则违反、每个属性空缺值、每个属性异常值的混合错误。
   - **错误注入比例**：
     - **a. 0.25%**  
       - 每个规则涉及的属性总体 0.25% 的违反
       - 每个属性0.25%的空缺值
       - 每个属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=99
       - **错误条目数** = 93

      - **b. 0.5%**  
        - 每个规则涉及的属性总体 0.5% 的违反
        - 每个属性 0.5% 的空缺值
        - 每个属性 0.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 244
        - **错误条目数** = 212
      
      - **c. 0.75%**  
        - 每个规则涉及的属性总体 0.75% 的违反
        - 每个属性 0.75% 的空缺值
        - 每个属性 0.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 319
        - **错误条目数** = 264
      
      - **d. 1%**  
        - 每个规则涉及的属性总体 1% 的违反
        - 每个属性 1% 的空缺值
        - 每个属性 1% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 448
        - **错误条目数** = 353
      
      - **e. 1.25%**  
        - 每个规则涉及的属性总体 1.25% 的违反
        - 每个属性 1.25% 的空缺值
        - 每个属性 1.25% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 572
        - **错误条目数** = 425
      
      - **f. 1.5%**  
        - 每个规则涉及的属性总体 1.5% 的违反
        - 每个属性 1.5% 的空缺值
        - 每个属性 1.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 701
        - **错误条目数** = 516
      
      - **g. 1.75%**  
        - 每个规则涉及的属性总体 1.75% 的违反
        - 每个属性 1.75% 的空缺值
        - 每个属性 1.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 784
        - **错误条目数** = 547
      
      - **h. 2%**  
        - 每个规则涉及的属性总体 2% 的违反
        - 每个属性 2% 的空缺值
        - 每个属性 2% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 951
        - **错误条目数** = 611

### 数据存放路径
- **BART 脚本路径**：**0.25%**:`../1_hospital/noise/dirty_mixed_0.25/hospitals_mixed_all.xml`
                   **0.5%**:`../1_hospital/noise/dirty_mixed_0.5/hospitals_mixed_all.xml`
                   **0.75%**:`../1_hospital/noise/dirty_mixed_0.75/hospitals_mixed_all.xml`
                   **1%**:`../1_hospital/noise/dirty_mixed_1/hospitals_mixed_all.xml`
                   **1.25%**:`../1_hospital/noise/dirty_mixed_1.25/hospitals_mixed_all.xml`
                   **1.5%**:`../1_hospital/noise/dirty_mixed_1.5/hospitals_mixed_all.xml`
                   **1.75%**:`../1_hospital/noise/dirty_mixed_1.75/hospitals_mixed_all.xml`
                   **2%**:`../1_hospital/noise/dirty_mixed_2/hospitals_mixed_all.xml`
- **数据存放路径**：**0.25%**:`../1_hospital/noise/dirty_mixed_0.25/hospitals_mixed_all.xml`
                  **0.5%**:`../1_hospital/noise/dirty_mixed_0.5/hospitals_mixed_all.xml`
                  **0.75%**:`../1_hospital/noise/dirty_mixed_0.75/hospitals_mixed_all.xml`
                  **1%**:`../1_hospital/noise/dirty_mixed_1/hospitals_mixed_all.xml`
                  **1.25%**:`../1_hospital/noise/dirty_mixed_1.25/hospitals_mixed_all.xml`
                  **1.5%**:`../1_hospital/noise/dirty_mixed_1.5/hospitals_mixed_all.xml`
                  **1.75%**:`../1_hospital/noise/dirty_mixed_1.75/hospitals_mixed_all.xml`
                  **2%**:`../1_hospital/noise/dirty_mixed_2/hospitals_mixed_all.xml`
                  

### hospital 下目录结构说明
noise：存放纯随机噪声注入
noise with correct primary key：存放主键干净的噪声注入