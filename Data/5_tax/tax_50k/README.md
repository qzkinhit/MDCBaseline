
# 数据集：tax_50k

## 属性集
```text
[fname, lname, gender, areacode, phone, city, 
state, zip, maritalstatus, haschild, salary, 
rate, singleexemp, marriedexemp, childexemp]
```

## 数据规模
**属性个数 × 条目数**：15 × 500000

## 干净版本
存在

## 原生错误种类及数量
### 错误种类：T(typo), FI(formatting issue), VAD(violate attribute dependency)
### 错误数量：4%

## 数据规则集、标签、知识存放路径
- **FD 规则**：`../../Data/hospital/dc_rules-validate-fd-horizon.txt`
- **DC 规则**：`../../Data/hospital/dc_rules_dc_holoclean.txt`


## 数据集出处
### Fan W, Geerts F, Jia X, et al. Conditional functional dependencies for capturing data inconsistencies[J]. ACM Transactions on Database Systems (TODS), 2008, 33(2): 1-48.

## 人工错误注入记录

## 主键属性集合：
```text
[fname, lname, areacode, phone, zip, maritalstatus, haschild, salary, rate]
```
1. **规则涉及**的属性中，保证**主键属性集合干净**的情况下，注入不同比例的混合错误。
   - 每个规则违反、非主键属性空缺值、非主键属性异常值的混合错误。
   - **错误注入比例**：
   
     - **a. 0.25%**  
       - 每个规则(不涉及主键属性)，每个规则涉及的属性总体 0.25% 的违反
       - 非主键属性0.25%的空缺值
       - 非主键属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数 = 2337
       - **错误条目数** = 2290
       
    - **b. 0.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体0.5% 的违反
      - 非主键属性 0.5% 的空缺值
      - 非主键属性 0.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 4731
      - **错误条目数** = 4516
    
    - **c. 0.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 0.75% 的违反
      - 非主键属性 0.75% 的空缺值
      - 非主键属性 0.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 7085
      - **错误条目数** = 6479
    
    - **d. 1%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1% 的违反
      - 非主键属性 1% 的空缺值
      - 非主键属性 1% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 9391
      - **错误条目数** = 8421
    
    - **e. 1.25%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.25% 的违反
      - 非主键属性 1.25% 的空缺值
      - 非主键属性 1.25% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 11684
      - **错误条目数** = 10217
    
    - **f. 1.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.5% 的违反
      - 非主键属性 1.5% 的空缺值
      - 非主键属性 1.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 13970
      - **错误条目数** = 12098
    
    - **g. 1.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.75% 的违反
      - 非主键属性 1.75% 的空缺值
      - 非主键属性 1.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 16473
      - **错误条目数** = 13922
    
    - **h. 2%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 2% 的违反
      - 非主键属性 2% 的空缺值
      - 非主键属性 2% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 18502
      - **错误条目数** = 15484


### 数据存放路径
- **BART 脚本路径**：`../../Data/5_tax/tax_50k/tax_50k_mixed_with_c.xml`
- **数据存放路径**：`../../Data/5_tax/tax_50k/noise_with_correct_primary_key/dirty_mix_ratio/`

---

2. **无条件**注入不同比例的错误。
   - 每个规则违反、每个属性空缺值、每个属性异常值的混合错误。
   - **错误注入比例**：
     - **a. 0.25%**  
       - 每个规则涉及的属性总体 0.25% 的违反
       - 每个属性0.25%的空缺值
       - 每个属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数 = 4571
       - **错误条目数** = 4390

      - **b. 0.5%**  
        - 每个规则涉及的属性总体 0.5% 的违反
        - 每个属性 0.5% 的空缺值
        - 每个属性 0.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 9199
        - **错误条目数** = 8491
      
      - **c. 0.75%**  
        - 每个规则涉及的属性总体 0.75% 的违反
        - 每个属性 0.75% 的空缺值
        - 每个属性 0.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 13781
        - **错误条目数** = 12230
      
      - **d. 1%**  
        - 每个规则涉及的属性总体 1% 的违反
        - 每个属性 1% 的空缺值
        - 每个属性 1% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 18005
        - **错误条目数** = 15320
      
      - **e. 1.25%**  
        - 每个规则涉及的属性总体 1.25% 的违反
        - 每个属性 1.25% 的空缺值
        - 每个属性 1.25% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 22743
        - **错误条目数** = 18589
      
      - **f. 1.5%**  
        - 每个规则涉及的属性总体 1.5% 的违反
        - 每个属性 1.5% 的空缺值
        - 每个属性 1.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 27446
        - **错误条目数** = 21414
      
      - **g. 1.75%**  
        - 每个规则涉及的属性总体 1.75% 的违反
        - 每个属性 1.75% 的空缺值
        - 每个属性 1.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 32045
        - **错误条目数** = 23688
      
      - **h. 2%**  
        - 每个规则涉及的属性总体 2% 的违反
        - 每个属性 2% 的空缺值
        - 每个属性 2% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 36200
        - **错误条目数** = 26252

### 数据存放路径
- **BART 脚本路径**：`../../Data/5_tax/tax_50k/tax_50k_mixed_all.xml`
- **数据存放路径**：`../../Data/5_tax/tax_50k/noise/dirty_mix_ratio/`

### tax_50k 下目录结构说明
noise：存放纯随机噪声注入
noise with correct primary key：存放主键干净的噪声注入
xxxx待填写