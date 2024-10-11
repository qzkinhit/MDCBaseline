# 数据集：Flights

## 属性集

```text
[tuple_id, src, flight, sched_dep_time, act_dep_time, sched_arr_time, act_arr_time]
```

## 数据规模

**属性个数 × 条目数**：7*2376

## 干净版本

存在

## 原生错误种类及数量

### 错误种类：MV(缺失值)，FI（格式不一致），VAD（违反属性依赖关系）

### 错误数量：30%

## 数据规则集、标签、知识存放路径

- **FD 规则**：`../../Data/flight/dc_rules-validate-fd-horizon.txt`
- **DC 规则**：`../../Data/flight/dc_rules_dc_holoclean.txt`


## 数据集出处

### Theodoros Rekatsinas, Xu Chu, Ihab F. Ilyas, and Christopher Ré. 2017. HoloClean: Holistic data repairs with probabilistic inference. *Proceedings of the VLDB Endowment 10, 11 (2017), 1190–1201.

## 人工错误注入记录

## 主键属性集合：

```text
[flight]
```

1. **规则涉及**的属性中，保证**主键属性集合干净**的情况下，注入不同比例的混合错误。
   
   - 每个规则违反、非主键属性空缺值、非主键属性异常值的混合错误。
   
   - **错误注入比例**：
     - **a. 0.25%**  
       - 每个规则0.25%的违反
       - 非主键属性0.25%的空缺值
       - 非主键属性0.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=74
       - **错误条目数** = 72
     - **b. 0.5%**  
       - 每个规则0.5%的违反
       - 非主键属性0.5%的空缺值
       - 非主键属性0.5%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=132
       - **错误条目数** = 117
     - **c. 0.75%**  
       - 每个规则0.75%的违反
       - 非主键属性0.75%的空缺值
       - 非主键属性0.75%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=203
       - **错误条目数** = 182
     - **d. 1%**  
       - 每个规则1%的违反
       - 非主键属性1%的空缺值
       - 非主键属性1%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=269
       - **错误条目数** = 237
     - **e. 1.25%**  
       - 每个规则1.25%的违反
       - 非主键属性1.25%的空缺值
       - 非主键属性1.25%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=344
       - **错误条目数** = 282
     - **f. 1.5%**  
       - 每个规则1.5%的违反
       - 非主键属性1.5%的空缺值
       - 非主键属性1.5%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=433
       - **错误条目数** = 371
     - **g. 1.75%**  
       - 每个规则1.75%的违反
       - 非主键属性1.75%的空缺值
       - 非主键属性1.75%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=500
       - **错误条目数** = 399
     - **h. 2%**  
       - 每个规则2%的违反
       - 非主键属性2%的空缺值
       - 非主键属性2%的异常值
       - **Original Error Count (OEC)** = 总错误单元格数=558
       - **错误条目数** = 457
     
     
     ### 数据存放路径
     
     - **BART 脚本路径**：
     
       ​	**0.25%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.25/flights__with_correct_primary_key.xml`
       ​    **0.5%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.5/flights__with_correct_primary_key.xml`
       ​    **0.75%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.75/flights__with_correct_primary_key.xml`
       ​    **1%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1/flights__with_correct_primary_key.xml`
       ​    **1.25%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.25/flights__with_correct_primary_key.xml`
       ​    **1.5%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.5/flights__with_correct_primary_key.xml`
       ​    **1.75%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.75/flights__with_correct_primary_key.xml`
          **2%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_2/flights__with_correct_primary_key.xml`
     
     - **数据存放路径**：`
     
       ​	**0.25%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.25/dirty_flights_null.csv`
       ​    **0.5%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.5/dirty_flights_null.csv`
       ​    **0.75%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_0.75/dirty_flights_null.csv`
       ​    **1%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1/dirty_flights_null.csv`
       ​    **1.25%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.25/dirty_flights_null.csv`
       ​    **1.5%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.5/dirty_flights_null.csv`
       ​    **1.75%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_1.75/dirty_flights_null.csv`
       ​    **2%**:`../2_flights/noise_with_correct_primary_key/dirty_mixed_2/dirty_flights_null.csv`
     
     ---
     
     2. **无条件**注入不同比例的错误。
        - 每个规则违反、每个属性空缺值、每个属性异常值的混合错误。
        - **错误注入比例**：
          - **a. 0.25%**  
            - 每个规则涉及的属性总体 0.25% 的违反
            - 每个属性0.25%的空缺值
            - 每个属性0.25%的异常值
            - **Original Error Count (OEC)** = 总错误单元格数=71
            - **错误条目数** = 71
     
           - **b. 0.5%**  
             - 每个规则涉及的属性总体 0.5% 的违反
             - 每个属性 0.5% 的空缺值
             - 每个属性 0.5% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 155
             - **错误条目数** = 149
     
           - **c. 0.75%**  
             - 每个规则涉及的属性总体 0.75% 的违反
             - 每个属性 0.75% 的空缺值
             - 每个属性 0.75% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 247
             - **错误条目数** = 233
     
           - **d. 1%**  
             - 每个规则涉及的属性总体 1% 的违反
             - 每个属性 1% 的空缺值
             - 每个属性 1% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 321
             - **错误条目数** = 298
     
           - **e. 1.25%**  
             - 每个规则涉及的属性总体 1.25% 的违反
             - 每个属性 1.25% 的空缺值
             - 每个属性 1.25% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 399
             - **错误条目数** = 362
     
           - **f. 1.5%**  
             - 每个规则涉及的属性总体 1.5% 的违反
             - 每个属性 1.5% 的空缺值
             - 每个属性 1.5% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 488
             - **错误条目数** = 445
          
           - **g. 1.75%**  
             - 每个规则涉及的属性总体 1.75% 的违反
             - 每个属性 1.75% 的空缺值
             - 每个属性 1.75% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 564
             - **错误条目数** = 515
          
           - **h. 2%**  
             - 每个规则涉及的属性总体 2% 的违反
             - 每个属性 2% 的空缺值
             - 每个属性 2% 的异常值
             - **Original Error Count (OEC)** = 总错误单元格数 = 652
             - **错误条目数** = 575
     
     ### 数据存放路径
     
     - **BART 脚本路径**：
     
       ​	**0.25%**:`../2_flights/noise/dirty_mixed_0.25/flights_mixed_all.xml`
       ​    **0.5%**:`../2_flights/noise/dirty_mixed_0.5/flights_mixed_all.xml`
       ​    **0.75%**:`../2_flights/noise/dirty_mixed_0.75/flights_mixed_all.xml`
       ​    **1%**:`../2_flights/noise/dirty_mixed_1/flights_mixed_all.xml`
       ​    **1.25%**:`../2_flights/noise/dirty_mixed_1.25/flights_mixed_all.xml`
       ​    **1.5%**:`../2_flights/noise/dirty_mixed_1.5/flights_mixed_all.xml`
       ​    **1.75%**:`../2_flights/noise/dirty_mixed_1.75/flights_mixed_all.xml`
          **2%**:`../2_flights/noise/dirty_mixed_2/flights_mixed_all.xml`
     - **数据存放路径**：`
     
       ​	**0.25%**:`../2_flights/noise/dirty_mixed_0.25/dirty_flights_null.csv`
       ​    **0.5%**:`../2_flights/noise/dirty_mixed_0.5/dirty_flights_null.csv`
       ​    **0.75%**:`../2_flights/noise/dirty_mixed_0.75/dirty_flights_null.csv`
       ​    **1%**:`../2_flights/noise/dirty_mixed_1/dirty_flights_null.csv`
       ​    **1.25%**:`../2_flights/noise/dirty_mixed_1.25/dirty_flights_null.csv`
       ​    **1.5%**:`../2_flights/noise/dirty_mixed_1.5/dirty_flights_null.csv`
       ​    **1.75%**:`../2_flights/noise/dirty_mixed_1.75/dirty_flights_null.csv`
       ​    **2%**:`../2_flights/noise/dirty_mixed_2/dirty_flights_null.csv`
     
     ### hospital 下目录结构说明
     
     noise：存放无条件噪声注入
     noise with correct primary key：存放主键干净的噪声注入
