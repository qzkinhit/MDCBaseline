# 数据集说明README，暂时不要把大于2M的数据集放放到git（太大了）
本文件记录了用于数据清洗系统复现的数据集的信息，包括属性、干净版本、脏版本及错误类型、数据规则集、标签、知识、下载链接和论文出处。

## 数据集目录
1. [Dataset 1](#dataset-1)
2. [Dataset 2](#dataset-2)
3. [Dataset 3](#dataset-3)
4. [Dataset 4](#dataset-4)
5. [Dataset 5](#dataset-5)
6. [Dataset 6](#dataset-6)
7. [Dataset 7](#dataset-7)

## 数据集说明

### Dataset 1
### parking
**属性**: [Summons Number, Plate ID, Registration State, Plate Type, Issue Date, Violation Code, Vehicle Body Type, Vehicle Make,
Issuing Agency, Street Code1, Street Code2, Street Code3, Vehicle Expiration Date, Violation Location, Violation Precinct, Issuer Precinct,
Issuer Code, Issuer Command, Issuer Squad, Violation Time, Time First Observed, Violation County, Violation In Front Of Or Opposite,
House Number, Street Name, Intersecting Street, Date First Observed, Law Section, Sub Division, Violation Legal Code, Days Parking In Effect,
From Hours In Effect, To Hours In Effect, Vehicle Color, Unregistered Vehicle?, Vehicle Year, Meter Number, Feet From Curb, Violation Post Code,
Violation Description, No Standing or Stopping Violation, Hydrant Violation, Double Parking Violation]    
**是否有干净版本**: 无  
**对应错误种类和数目**: 数据集本身包含自然错误，未进行注错处理   
**数据规则集、标签、知识**:存放路径：../../Data/parking/fd-horizon.txt     
Plate ID ⇒ Registration State   
Plate ID ⇒ Vehicle Make 
Violation location ⇒ Violation Precinct 
Violation location ⇒ Violation County   
Violation location ⇒ Street name    
Issuing Agency ⇒ Issuer Precinct    
Issuing Agency ⇒ Issuer Code    
Violation Code ⇒ Violation Description  
Violation Code ⇒ Violation Legal Code   
**数据集下载链接**: [下载链接](https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2021/kvfd-bves/about_data)   
**与论文中相同大小的数据集(100k)(input_parking_horizon.csv)下载链接**: [下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)     
**论文出处**: Horizon: Scalable Dependency-driven Data Cleaning

| 错误类型     | 数据存放路径（输入路径）          | 数据存放路径（输出路径）          | 数据量        | 错误量        | 备注        |
|----------|----------------------------------|----------------------------------|------------|------------|-----------|
| 原始数据集 | `./Data/parking/input_parking_horizon.csv` | `./results/horizon/output_parking_horizon.csv`| `100k条` | `/`  | `错误为数据集自然错误` |


### Dataset 2
### hospital
**属性**: [ProviderNumber, HospitalName, Address1, Address2, Address3, City, State, ZipCode, CountyName, PhoneNumber, HospitalType, HospitalOwner, EmergencyService, Condition, MeasureCode, MeasureName, Score, Sample, Stateavg]    
**是否有干净版本**: 有  
**对应错误种类和数目**: 包含以下错误类型：异常值、规则违反，分别8936个、500条     
**数据规则集、标签、知识**:存放路径：../../Data/hospital/dc_rules-validate-fd-horizon.txt     
HospitalName ⇒ ZipCode  
HospitalName ⇒ PhoneNumber  
MeasureCode ⇒ MeasureName   
MeasureCode ⇒ Stateavg  
MeasureName ⇒ MeasureCode   
ProviderNumber ⇒ HospitalName   
MeasureCode ⇒ Condition 
HospitalName ⇒ Address1 
HospitalName ⇒ HospitalOwner    
HospitalName ⇒ ProviderNumber   
City ⇒ CountyName   
ZipCode ⇒ EmergencyService  
HospitalName ⇒ City   
**数据集下载链接**: [下载链接](https://db.unibas.it/projects/bart/)    
**与论文中相同大小的数据集(100k)(input_hospital_horizon.csv)下载链接**:[下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)  
**论文出处**: Holistic Data Cleaning: Putting Violations Into Context

| 错误类型     | 数据存放路径（输入路径）          | 数据存放路径（输出路径）          | 数据量        | 错误量        | 备注        |
|----------|----------------------------------|----------------------------------|------------|------------|-----------|
| 异常值  | `./Data/hospital/input_hospital_horizon_E2.csv` | `./results/horizon/output_hospital_horizon_E2.csv` | `100k条` | `8936个单元格`      | `向不同属性注入随机错误` |
| ProviderNumber⇒HospitalName规则违反 | `./Data/hospital/input_hospital_horizion_E1.csv`  | `./results/horizon/output_hospital_horizon_E1.csv`| `100k条`     | `500条` | `由于bart运行时间过长，目前只对一条规则进行处理` |


### Dataset 3
### tax
**属性**: [index, fname, lname, gender, areacode, phone, city, state, zip, maritalstatus, haschild, salary, rate, singleexemp, marriedexemp, childexemp]    
**是否有干净版本**: 有  
**对应错误种类和数目**: 包含以下错误类型：异常值、规则违反，分别6041个、500条   
**数据规则集、标签、知识**:存放路径：../../Data/tax/dc_rules-validate-fd-horizon.txt     
zip ⇒ city  
zip ⇒ state     
zip,haschild ⇒ childexemp 
zip,maritalstatus ⇒ singleexemp   
zip,maritalstatus ⇒ marriedexemp  
fname ⇒ gender 
areacode ⇒ state   
phone, zip ⇒ areacode  
**数据集下载链接**: [下载链接](https://db.unibas.it/projects/bart/)    
**与论文中相同大小的数据集(100k)(input_tax_horizon.csv)下载链接**：[下载链接](https://pan.baidu.com/s/1-0epjUUe4SDlT6oNyqF9YA?pwd=2njy)    
**论文出处**: Conditional functional dependencies for capturing data inconsistencies    

| 错误类型     | 数据存放路径（输入路径）          | 数据存放路径（输出路径）          | 数据量        | 错误量        | 备注        |
|----------|----------------------------------|----------------------------------|------------|------------|-----------|
| 异常值  | `./Data/hospital/input_tax_horizon_E2.csv` | `./results/horizon/output_tax_horizon_E2.csv` | `100k条` | `6041个单元格` | `向不同属性注入随机错误` |
| zip ⇒ city规则违反 | `./Data/hospital/input_tax_horizon_E1.csv`  | `./results/horizon/output_tax_horizon_E1.csv`| `100k条` | `500条` | `由于bart运行时间过长，目前只对一条规则进行处理` |


### Dataset 4
### Titanic
**属性**: [PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked]    
**是否有干净版本**: 无  
**对应错误种类和数目**: 数据集本身包含缺失值和字符串格式错误，未进行注错处理。   
**数据规则集、标签、知识**:存放路径：../Data/Titanic/Titanic.csv    

**数据集下载链接**: [下载链接](https://storage.googleapis.com/kaggle-data-sets/1818188/2965537/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20240924%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240924T051242Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=bd294221720dd47652cc8b73be8feedf3c62ccf1716a6ae420eb4114a71c5c3d2c6ad85354c4184f92d29f5b681ea94d2e5b8c2c9d4b0f5172bb3586ab755d02dfb157d0bfc5b97910fa3c140e3640397c23ad98f949ab84304bb6d7bd49b82fd6b146ab3a964c0cff154b26ec20a174830240462d9cf5f32bb4b70bf142caed6846bf59ff0de7230bc36fec04db6579344200d948387e3d68ecaa470a2378880bfda2575dda36198067d6d78a7e56711536cee00f13a003f88c6020ce3bf87783bf7f5446c509c76fe9424f5263f170043f3d896c755e45aa171e3284a93a66d7efa6ea649877d3c25ff387a8fa486f6b1eac8dcdaf6854846fe55dccf268fc)   
  
**论文出处**: BoostClean: Automated Error Detection and Repair for Machine Learning


| 错误类型     | 数据存放路径（输入路径）          | 数据存放路径（输出路径）          | 数据量        | 错误量        | 备注        |
|----------|----------------------------------|----------------------------------|------------|------------|-----------|
| 原始数据集 | `./Data/Titanic/Titanic.csv` | `/`| `891条` | `/`  | `错误为数据集自然错误` |


### Dataset 5
### Emergency
**属性**: [lat, lng, desc, zip, title, timeStamp, twp, addr, e]    
**是否有干净版本**: 无  
**对应错误种类和数目**: 数据集包含缺失值以及911中心实际上不提供服务的虚假位置，未进行注错处理。   
**存放路径**:此数据集较大，暂不上传git。    

**数据集下载链接**: [下载链接](https://pan.baidu.com/s/1tUO7nQP-LSyGiMrPEXXI0A?pwd=gtpe)   
  
**论文出处**: BoostClean: Automated Error Detection and Repair for Machine Learning


### Dataset 6
### USCensus
**属性**: [age, workclass, fnlwgt, education, education.num, marital.status, occupation, relationship, race, sex, capital.gain, capital.loss, hours.per.week, native.country, income]    
**是否有干净版本**: 无  
**对应错误种类和数目**: 数据集包含缺失值和编码不一致错误，未进行注错处理。   
**存放路径**：此数据集较大，暂不上传git。    

**数据集下载链接**: [下载链接](https://pan.baidu.com/s/14iro2CuKO73nJ0lorSzKjQ?pwd=1pqp)   
  
**论文出处**: BoostClean: Automated Error Detection and Repair for Machine Learning

### Dataset 7
### Retail
**属性**: [InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country]    
**是否有干净版本**: 无  
**对应错误种类和数目**: 数据集包含数值错误，如一些购买数量为负数，未进行注错处理。   
**存放路径**：此数据集较大，暂不上传git。    

**数据集下载链接**: [下载链接](https://pan.baidu.com/s/1RSEZzmUvmh7OnxShrRTy3w?pwd=iglz)   
  
**论文出处**: BoostClean: Automated Error Detection and Repair for Machine Learning