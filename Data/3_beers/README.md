
# 数据集：Beers

## 属性集
```text
[id,brewery_id,brewery_name,beer_name,style,ounces,abv,ibu,city,state]
```

## 数据规模
**属性个数 × 条目数**：11 × 2410

## 干净版本
存在

## 原生错误种类及数量
### 错误种类：MV,FI,VAD
### 错误数量：16%

## 数据规则集、标签、知识存放路径
- **FD 规则**：`../../Data/3_beers/dc_rules-validate-fd-horizon.txt`
- **DC 规则**：`../../Data/3_beers/dc_rules_dc_holoclean.txt`


## 数据集出处
### J.-N. Hould. Craft beers dataset. https://www.kaggle.com/nickhould/craft-cans, 2017. Version 1.

## 人工错误注入记录

## 主键属性集合：
```text
brewery_id
```
1. **规则涉及**的属性中，保证**主键属性集合干净**的情况下，注入不同比例的混合错误。
   - 每个规则违反、非主键属性空缺值、非主键属性异常值的混合错误。
   - **错误注入比例**：
   
     - **a. 0.25%**  
       - 每个规则(不涉及主键属性)，每个规则涉及的属性总体 0.25% 的违反
       - 非主键属性0.25%的空缺值
       - 非主键属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=65
       - **错误条目数** = 65
       
    - **b. 0.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体0.5% 的违反
      - 非主键属性 0.5% 的空缺值
      - 非主键属性 0.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 110
      - **错误条目数** = 108
    
    - **c. 0.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 0.75% 的违反
      - 非主键属性 0.75% 的空缺值
      - 非主键属性 0.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 168
      - **错误条目数** = 158
    
    - **d. 1%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1% 的违反
      - 非主键属性 1% 的空缺值
      - 非主键属性 1% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 226
      - **错误条目数** = 224
    
    - **e. 1.25%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.25% 的违反
      - 非主键属性 1.25% 的空缺值
      - 非主键属性 1.25% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 264
      - **错误条目数** = 239
    
    - **f. 1.5%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.5% 的违反
      - 非主键属性 1.5% 的空缺值
      - 非主键属性 1.5% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 327
      - **错误条目数** = 308
    
    - **g. 1.75%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 1.75% 的违反
      - 非主键属性 1.75% 的空缺值
      - 非主键属性 1.75% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 371
      - **错误条目数** = 321
    
    - **h. 2%**  
      - 每个规则（不涉及主键属性），每个规则涉及的属性总体 2% 的违反
      - 非主键属性 2% 的空缺值
      - 非主键属性 2% 的异常值
      - **Original Error Count (OEC)** = 总错误单元格数 = 426
      - **错误条目数** = 363


### 数据存放路径
- **BART 脚本路径**：`待填写`
- **数据存放路径**：`待填写`

---

2. **无条件**注入不同比例的错误。
   - 每个规则违反、每个属性空缺值、每个属性异常值的混合错误。
   - **错误注入比例**：
     - **a. 0.25%**  
       - 每个规则涉及的属性总体 0.25% 的违反
       - 每个属性0.25%的空缺值
       - 每个属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=65
       - **错误条目数** = 64

      - **b. 0.5%**  
        - 每个规则涉及的属性总体 0.5% 的违反
        - 每个属性 0.5% 的空缺值
        - 每个属性 0.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 121
        - **错误条目数** = 120
      
      - **c. 0.75%**  
        - 每个规则涉及的属性总体 0.75% 的违反
        - 每个属性 0.75% 的空缺值
        - 每个属性 0.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 188
        - **错误条目数** = 180
      
      - **d. 1%**  
        - 每个规则涉及的属性总体 1% 的违反
        - 每个属性 1% 的空缺值
        - 每个属性 1% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 233
        - **错误条目数** = 221
      
      - **e. 1.25%**  
        - 每个规则涉及的属性总体 1.25% 的违反
        - 每个属性 1.25% 的空缺值
        - 每个属性 1.25% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 294
        - **错误条目数** = 281
      
      - **f. 1.5%**  
        - 每个规则涉及的属性总体 1.5% 的违反
        - 每个属性 1.5% 的空缺值
        - 每个属性 1.5% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 348
        - **错误条目数** = 319
      
      - **g. 1.75%**  
        - 每个规则涉及的属性总体 1.75% 的违反
        - 每个属性 1.75% 的空缺值
        - 每个属性 1.75% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 426
        - **错误条目数** = 396
      
      - **h. 2%**  
        - 每个规则涉及的属性总体 2% 的违反
        - 每个属性 2% 的空缺值
        - 每个属性 2% 的异常值
        - **Original Error Count (OEC)** = 总错误单元格数 = 499
        - **错误条目数** = 460

### 数据存放路径
- **BART 脚本路径**：`待填写`
- **数据存放路径**：`待填写`

### beer 下目录结构说明
noise：存放纯随机噪声注入
noise with correct primary key：存放主键干净的噪声注入
