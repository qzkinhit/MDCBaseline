# `TODOList`

[//]: # (最终目标设计的系统框架图如下：)

[//]: # ()
[//]: # (<img src="docs\final_frame_diagram.png"/></img>)

[//]: # ()
# `AlphaClean` `v1.0`文档

## 一、研究背景和项目概述

- 在许多数据科学应用中，数据清理实际上是通过临时的、局限性用途的清洗算子来进行手工操作。这种做法对于可重复性（在研究人员之间分享分析结果）、可解释性（解释特定分析的结果）和可扩展性（在更大的语料库中复制分析结果）来说是非常有问题的。
- 现在，研究人员关注的焦点逐渐从“针对特定种类的数据质量问题设计清洗方法”转变为“根据特定种类的数据清洗需求（比如同时清洗存在缺失值和错误值的数据）恰当地组合现有方法以便更高效、准确地清洗数据”。事实上，后者更符合实际应用场景，本课题也将聚焦于后者。
- 大多数现有的关系型数据清理解决方案被设计成独立的系统--通常与数据库管理系统结合在一起--对数据科学中广泛使用的语言（如Python和R）支持不足。 
 `AlphaClean`被赋予了一个质量规则（例如，数据必须符合的完整性约束或统计模型）和一种允许的数据转换语言，然后它搜索以找到一个最能满足质量规范的转换序列。
 所发现的转换序列定义了一个中间表示法，它可以很容易地在语言之间转移或用编译器优化。

`AlphaClean` v1.0的系统框架图如下图所示。

<img src="docs\frame_diagram.png"/></img>

## 二、运行环境

作为一个最初的研究原型，`AlphaClean`是一个包，研究人员可以在本地开发和测试，用以评估不同的数据清理方法和技术。
目前的运行环境是windows11下的python 3.6版本，可以通过从命令行运行以下代码来安装。

```
pip install -r requirements.txt
```
## 三、系统算法涉及相关定义
目前系统两大基础类设计图如下：

Operation:

<img src="docs\Operation.png"/></img>

Constraint:



<img src="docs\constraint.png"/></img>

### 0.代码各功能模块及功能说明

#### 基础类

1. ```constraint.py``` ： 内部定义了最基础的constraint父类，谓词类和编辑惩罚
2. ```ic.py``` : 内部定义了最常用且最表层的基础约束类型，是`constraint.py`中类型的子类，定义了最常用的`FunctionalDependency`(简单函数依赖)，`DenialConstraint`（复杂否定谓词依赖）
3. ```pattern.py```:内部定义了最常用的两种模式约束依赖：`Date`和`float`，主要判断格式错误。以及根据正则表达式判断数据格式的`Pattern`类
4. ```ops.py``` : 内部定义了操作算子，`swap`和`delete`, 是数据修复的高级表示，也是系统的直接排序对象 
5. ```statiscal.py``` :内部定义了三个衡量数值软关系的约束类型，可以用于检测离群值（需定义阈值），和函数软关系。

#### 核心算法

1. ```search.py``` : 序列搜索的表层核心算法，调用各种底层方法返回可选择的操作序列，对操作序列进行树搜索并进行评估。
2. ```generators.py``` : 操作生成器采样器，被`search.py`直接调用。即为当前数据集生成所有可能的操作参数（五元组），并将所有参数传递至`swap`或`delete`中，返回可使用的操作集合，作为搜索空间。
3. ```core.py``` :主要用于`predicate`参数生成，被`generators.py`直接调用。
4. ```learning.py```: 为`treesearch`的剪枝阶段提供更高级的机器学习方法，可由`treesearch`直接调用 。


#### 功能说明

本系统实现的功能：以`swap`和`delete`这两种修复方式为中间算子，对`swap`和`delete`构成的操作序列进行排序。

1. 简单函数依赖，一对多，多对多等错误识别；

2. 复杂函数依赖，以谓词表达式为判断方式：如：员工的收入不能比经理多。 可以是多个谓词表达式的组合；

3. 简单模式依赖：内置各种格式错误，如日期，时间，浮点数，可根据需求自行添加；

4. 复杂模式依赖：通过正则表达式判断格式的错误，自定义需求格式；

5. 质量函数模块化:可自定义编辑惩罚还是数据质量的权重，以决定倾向于哪种修复（`swap`还是`delete`）；

6. 支持更多剪枝方案：剪枝函数在本系统中为模块化，可自行定义剪枝方式；

7. 更多外置参数接口：`config`参数中可调节如:搜索深度，内置编辑惩罚的相似度计算方式；

8. 外接生成算子的算法库以减小搜索空间；

9. 形式多样的软约束：属性之间的正负相关、数字关联关系等；

   

### 1.主要数据结构说明
#### Constraint父类说明
`Constraint`用于表示本系统的核心--约束，通过父类`Constraint`及其内置函数的定义，能够具有复用性地表示各种数据库中常见的约束情况，以识别数据库中的各种错误。
constraint的重要函数有：

- ```qfn(df)``` :作为`constraint`的重要核心函数，该函数表示对`dataframe`该约束上的质量评估。主要的质量评估方式各有不同，取决于约束本身，但都大同小异。
- `qfn()`：函数内部:对传入的数据表进行逐行评估，检查该行的各种特征下的值是否满足对应的约束，如果不满足约束则该行打分>0反之，如果满足约束，则计数为0，这样就生成了一组List构成的打分。在后续的搜索过程中，我们认定qfn越小的数据表现越好，对应的操作序列越可行化。
- ```def __mul__(other)``` and`def __add__(other)`:将不同的Constrain进行合并，有助于自然分块。

##### 子类说明

`class Predicate(Constraint)`:这是常见类型的约束，即以谓词判断的约束类型,在本工作中作为常见格式错误（如Date,Float等）的父类使用。需要的输入如下：

- `attr`:往往在各种谓词指定的约束中用来表示其涉及到的列（或特征）。在`Predicate`类及其相似的约束类中，都设置了`hint`, `hint`等同于`attr`，目的是传达参数搜索序列（`getAllOperations`）,指定哪些列进行操作。这样减少了修复组合，大幅减少搜索空间。
- `expr`:则是一串布尔表达式，用以表示不同列之间可能存在的约束关系。

`class DCPredicate(Constraint)`: 以否定约束为主要判断模式的谓词约束，`local_attr`，以及`expression`参数的设置都分别代表着：涉及的列（特征）名，可以视作Predicate的一种延伸，而在后续的评估过程中以否定约束的方式去衡量数据集的质量。

`class DenialConstraint(Constraint)`: 由数个谓词构成的谓词`list`，将约束条件涉及到的所有约束谓词整合起来，逐行判断每行的单元格是否“不”满足所有的谓词约束。

- ```def qfn(df)``` :否定约束判断的核心，因为约束条件包含数个谓词约束，因此我们需要数据集每个谓词都“不”满足，因此采取否定约束的方式，初始化所有行的质量函数评分为1，如果有一个谓词不满足，则我们认为该行数据是满足要求的，那么将评分技数为0。
- 因此基于最终的结果，我们希望`qfn`返回的数值越小，数据的质量就越高

`class FunctionalDependency(Constraint)`:最常用的简单（一致性）函数依赖，输入参数为`source`和`target`用以代表一致性依赖对应的属性名称。

- ```def qfn(df)```  简单函数依赖的质量函数评估标准为，通过聚合查询（`groupby`）操作来逐行检查`source`的那些行没有满足一致性（一对多），没有满足一致性的行作分数处理，满足函数依赖的行，质量评估值为0。`qfn`结果越大，违反质量函数的行越多。

`class CellEdit(Constraint)`: 专门用于衡量编辑惩罚的类，并非用于表示某些约束。该类中内置了多种相似性判别方法。

- ```def qfn(df)``` 用于计算当前的数据表和原始的数据表（`source`）和当前数据表（`df`）的相似度，每列的相似度差异作为操作的编辑惩罚指标，相似度越高则`qfn`值越低，编辑惩罚越低。

`class Parameteric(Constraint)`:  该约束是用于规范数值区间的一种数值（均值）约束，将指定的属性的value全部提取并建模为高斯模型，以寻找离群值。

- ```def qfn(df)```  按照行依次判断该行处的value值与平均值是否相差超过tolerance个方差，如果超过，计qfn_a[i] = 1,视为离群值，在后续步骤中进行优化。否则计为0。

`class NonParameteric(Constraint)`:  该约束是用于规范数值区间的一种数值（中位数）约束，将指定的属性的value全部提取并建模为高斯模型，以寻找离群值。

- ```def qfn(df)```  按照行依次判断该行处的value值与中位数是否相差超过tolerance个方差，如果超过，计qfn_a[i] = 1,视为离群值，在后续步骤中进行优化。否则计为0。

`class NumericalRelationship(Constraint)`:   该约束用于衡量两个列（属性）的软关系：即：由用户外部定义属性a和b之间的函数映射关系，但是b需要在fn(a)的合理范围内。

- ```def qfn(df)```  给定两个属性a,b和软约束fn，计算|b - fn(a)| 的平均数mean，方差。再遍历每一行，查看该行的 |b - fn(a)|结果是否和平均值mean相近。若相差过多，记为离群值。

`class Correlation(Constraint)`:   该约束用于衡量两个列（属性）的软关系：正关系即：如果属性a的值高，那么属性b的值也应该高；负关系即：如果a高，b就应该低

- ```def qfn(df)```  分别计算属性a ，和b的中位数，逐行判断，正关系的条件下（positive）：如果当前a的值大于中位数，那么b的值也应该大于中位数。反之亦然。违反条件的行，qfn值直接做绝对值相加处理，否则计0。

#### Operation父类说明
`class(Operation)`是操作的父类，在当前的程序内由`swap`和`delete`函数继承，是本程序中的重要排序，输出对象。目前继承`Operation`的主要子类仅有`Swap`,和`Delete`类， 用以对应程序输出的中间表示语言。为了程序的复用化，`Operation`主要内置了如下的重要函数：

- ```def run(df): ```
  	`operation.run(df)`表示操作的执行，在搜索的过程中，我们需要将给定的五元组中间参数付诸实行，用以评估实行该操作后，得到数据的效果
- ```def __mul()__``` Operation类重新定义了乘法操作，`op1*op2`视为操作一之后进行操作二。
- ```def __str()__``` 用以输出操作的细节信息，在子类中分别重写该函数以输出操作信息。

##### 子类说明

`class ParametrizedOperation(Operation)`:

​		集成了`Operation`类，定义了五元组的参数，由于`swap`或`delete`需要的参数是该五元组的子集，如`swap`需要的参数为`(column,predicate,value)`,因此该类中定义了`paramDescriptor`类，以用于表示子类`swap`或`delete`到底需要五元组中的哪些参数和参数的标号。

`class Swap(ParametrizedOperation)`:
		这是一种替换操作，`paramDescriptor`将返回该操作所需要的参数：`column`,`predicate``value`.通过声明将该三种参数调用到Swap中来创建`Swap`实例。

- ```def __fn()__```   声明了`Swap`的运行本质：匹配所有满足`predicate[0:2]`的数据行，将该行`column`列的数值全部改为`value`。
- `class Delete(ParametrizedOperation)`：
  这是一种删除操作，`paramDescriptor`将返回该操作所需要的参数：`column,predicate`
   通过声明将该两种参数调用到Delete中来创建Delete实例。
- ```def __fn()__```   声明了`Delete`的运行本质：匹配所有满足`predicate[0:2]`的数据行，将该行`column`列的数值全部删除。

### 2.关键算法伪代码及解释

#### 搜索器算法

solve函数以数据表T,和模式约束列表和函数依赖列表的形式作为输入，并返回一个经过清理的数据表和一系列清理操作的中间表示语言（五元组或三元组）;

  ```   py
  solve(df, patterns=[], dependencies=[], partitionOn=None, config=DEFAULT_SOLVER_CONFIG)
     df:数据表T,扁平数据;
     patterns:由用户定义的模式约束，如日期格式，时间格式，文字格式等;
     dependencies: 由用户定义的函数依赖关系，可以为简单的一对一依赖或复杂布尔表达式;
     partitionOn: 分块，None表示数据直接运行，无分块。partitionOn = column 表示数据按照dataframe[column] 进行grouby聚合查询，以聚合分组后的结果进行分块运行，减少大规模数据的搜索时间;
     config：由用户定义的搜索参数，其中默认针对模式约束的修复操作为[delete],函数依赖的修复操作为[swap]。此外用户可以在此调节搜索深度，编辑惩罚等参数。
  ```
算法的伪代码如下：

    if needWord2Vec(config) then  #为了处理数据表中的文本，判断是否需要词袋模型
        word2vec.init()
    config <- new_config
    if partitionOn != None then#判断是否需要依照聚合查询分块
        for b ∈ blocks do:
            df_copy <- df.loc[partionOn == b].copy #将数据grouby操作
            op1 <- fun_1(treesearch(patternConstraints))     
            op2 <- fun_2(treesearch(dependencyConstraints))  #依次处理模式约束和函数依赖清洗
        return op1*op2
    else : #直接处理模式约束和函数依赖清洗
        op1 <- fun_1(treesearch(patternConstraints))     
            op2 <- fun_2(treesearch(dependencyConstraints))  
        return op1*op2 #返回排好序的修复操作中间表示。
    #搜索器进一步调用树搜索（treesearch）
#### 树搜索的算法解释

  `treeSearch()`以分块数据表`df`, 依赖对象`costFn`和其他外部定义参数为输入，经过树搜索生成一组最优的中间算子序列

  ```  python
  treeSearch(df, costFn, operations, evaluations, inflation, editCost,similarity, word2vec, pruningModel=None)
    df -- 数据表T 输入后不断遍历得到最优解
    costFn -- a cost function代价函数，等同于输入的函数依赖或模式约束
    operations -- a list of operations//swap或delete，或其他组合
    evaluation -- 搜索深度，外部定义决定树的搜索次数
    inflation -- 超参数：贪心值,用于决定搜索过程中的预剪枝
    editCost -- scaling on the edit cost 编辑惩罚，用于复杂情况下权衡swap和delete
    similarity -- 内置相似度计算方式
    word2vec -- 词袋模型
  ```
算法的伪代码如下：

   ```
   editCostObj <- CellEdit 
   best <- (value <- 2.0 , list(op), df)  #初始化迭代对象
   for i = 0 , 1 ....evaluations do:
        if judge_prune then :    #设置剪枝条件，提前退出循环
             return             
        p <- ParameterSampler(...) #初始化采样器，用于返回可能采样序列 
        ops <- p.getAllOperations() #针对当前的数据表T(output),采样器返回所有的
        for opbranch ∈ ops do:
            if  func_iscorrect() then: #设立多个用于判断的缓存或函数，如bad_op_cache等，检测坏操作，减少搜索时间
                continue
            if predict(pruningModel, opbranch, df) then: #外接剪枝判断模块，判断是否符合剪枝条件，如果当前操作无效，直接剪枝
                continue
            nextop <- nextop + opbranch #在修复序列中加入当前判断的分支操作
            df <- opbranch.run(opbranch) #将当前的数据表在该分支操作中运行，更新数据表结果，并判断是否存在异常
            costEval = costFn.qfn(df) #使用约束作为质量函数，输出当前数据表的评估值
            n <- (np.sum(costEval) + editCost * editfn) / output.shape[0]  #最终的n由约束评估值，和编辑惩罚两种方式做加和，如果不考虑swap和delete一同使用的复杂情况，则后者几乎可以忽略
            if n < best[0] then  #和当前最优序列的评分作比较，如果小于当前最优，则说明操作有效
                best <- (n, nextop , df) #将当前的序列和opbranch一同更新至最优序列内，同时更新打分和数据表。
            进入下一轮迭代
   ```

#### 评估函数设计
  ```python
costEval = constraint.qfn(output)  由函数依赖定义的_qfn评估函数
editCost = config[:]['edit'] 为外部定义的参数
editCostObj = CellEdit(df.copy(), similarity, word2vec) 编辑惩罚值

efn = editCostObj.qfn  efn是一个函数，不断在treesearch的遍历过程中评估当前output和原始dataframe的编辑距离
edictCostObj.qfn返回的是相似度，相似度可选择内置的jaccard，semantic等，比较df.copy和output的相似度以衡量编辑距离。
editfn = np.sum(efn(output))最终将操作序列产生的编辑惩罚加和 作为总的编辑惩罚指标

n = (np.sum(costEval) + editCost * editfn) / output.shape[0]
函数依赖惩罚和编辑惩罚共同构成了最后的评估函数，并在每轮search的过程中，评估opbranch.run(df)返回的output
  
  ```



#### 采样器算法
`class ParameterSampler`:为搜索过程中的参数采样器，负责为当前数据表生成并采样所有可能的operation.
` def getParameterGrid(self)` :参照当前依赖，为当前数据表提供提供所有参数并采样

   ```
      初始化paramset,为每一种操作分配排序过的五元组标号，和未排序标号，该标号表示这种操作需要哪些参数
      for op , p , orig ∈  paramset do: p为排序过的标号，orig为原生标号
            if p[0] = column then: 如果p[0]表示列
                orig <- orig.remove[p[0]]  orig数组删除表示列的标号
                for col ∈  columns 设计约束的每一列都进行遍历，以获取所有可能的操作参数
                     for pv ∈ orig: 针对每一种参数标号，我们通过子采样器来获得value,predicate参数，之后（column,value,predicate）作为三元组参数加入grid中                  
                        grid.append(sampler(pv,col))  pv = 3时，调用predicate子采样器获取predicate，pv = 1时，调用value子采样器获取value
                     至此，grid中储存着list(predicates) ,list(value) 
                     将两者作笛卡尔乘积匹配，再与column共同构成swap所需的三元组：（column,predicate,value）
                     将所有三元组存入parameters中，输出。
 def getAllOperations():
    在采样器中作为外部调用主要接口，返回一组可用的operations以支持treesearch的遍历
    parameterGrid <- self.getParameterGrid() 初始化参数网格，获取所有参数
    for op ∈ operationList 首先按照操作种类分配参数
        for param ∈  parameterGrid
            arg <- param   将grid中的{column,predicate,value}传递至arg
        operations.append(op(**arg))维护操作列表，定义操作并将参数传给操作
    return operations 返回所有操作

   ```
## 四、项目使用指南和测试分析

关于如何使用`AlphaClean`，以及设计了相关实例进行测试，下面将总结如下。

### 0. 城市名称和缩略语数据集

这个例子是为了说明`AlphaClean`的基本功能和概念。你可以自己运行这个例子，在`AlphaClean`目录下运行`python examples/example1.py`。
让我们从一个简单的城市名称和缩写的例子开始。

```
data = [{'a': 'New Yorks',     'b': 'NY'},
        {'a': 'New York',      'b': 'NY'},
        {'a': 'San Francisco', 'b': 'SF'},
        {'a': 'San Francisco', 'b': 'SF'},
        {'a': 'San Jose',      'b': 'SJ'},
        {'a': 'New York',      'b': 'NY'},
        {'a': 'San Francisco', 'b': 'SFO'},
        {'a': 'Berkeley City', 'b': 'Bk'},
        {'a': 'San Mateo',     'b': 'SMO'},
        {'a': 'Albany',        'b': 'AB'},
        {'a': 'San Mateo',     'b': 'SM'}]

```
请注意，城市名称是不一致的 (<b>New York</b> vs. <b>New Yorks</b>), 
缩写也是不一致的 (<b>SF</b> vs. <b>SFO</b>, and <b>SM</b> vs. <b>SMO</b>). 
对于一个小的数据集，有可能通过直观的检查来列举所有的修正，但如果数据集非常大呢？


#### 加载数据
`AlphaClean`是在Pandas上操作的，`Pandas`给了我们一个轻量级的表的抽象，叫做`DataFrame`。
首先，我们将数据加载到一个`Pandas DataFrame`中。

```
import pandas as pd
df = pd.DataFrame(data)
```
可以用`python`代码查询这个`DataFrame`。
```
>>> df['a'].values
array(['New Yorks', 'New York', 'San Francisco', 'San Francisco',
       'San Jose', 'New York', 'San Francisco', 'Berkeley City',
       'San Mateo', 'Albany', 'San Mateo'], dtype=object)
```

#### 指定数据清洗规则

为了自动化进行数据清洗，AlphaClean的需要定义一个清洗规则，
使得用户不应该用手写代码来纠正所有的错误。相反，用户应该指定一个高层次的数据模型，而系统会自动生成代码来最好地满足这个模型。
例如，在这个数据集中，我们知道属性 "a "和 "b "应该有一个一对一的关系。 
在代码中表示为一个`OneToOne`约束，强制要求键 "a "与 "b "进行双向映射。

```python
from AlphaClean.constraint_languages.ic import OneToOne
constraint = OneToOne(["a"], ["b"])
```

#### 通过编排中间算子证据集的搜索

接下来，调用搜索器来寻找一个能满足这个约束的中间算子序列。
AlphaClean将这些约束条件转换成质量评估函数。
一个最优搜索会利用爬山法根据质量评估函数选择的最有希望的节点。 
搜索器（solve）接受了一个模式约束（单属性约束，表示基于统计特征的清洗）
和依赖关系（包括条件依赖和外部字典）的列表。
模式约束具有更高的优先级，因为它们通常是像强制执属性是一个浮点型这种清洗。

```python
from AlphaClean.search import solve
dcprogram, clean_instance = solve(df, patterns=[], dependencies=[constraint])
```
`dcprogram` 是一个对象，代表搜索器找到中间算子序列。
```
>>> print(dcprogram)
df = swap(df,'a','New York',('a', set(['New Yorks'])))
df = swap(df,'b','SF',('a', set(['San Francisco'])))
df = swap(df,'b','SMO',('a', set(['San Mateo'])))
```
有三个swap算子，通过`clean_instance`(`output`) 显示清理后的数据集。
```
>>> print(output)

                a    b
0        New York   NY
1        New York   NY
2   San Francisco   SF
3   San Francisco   SF
4        San Jose   SJ
5        New York   NY
6   San Francisco   SF
7   Berkeley City   Bk
8       San Mateo  SMO
9          Albany   AB
10      San Mateo  SMO

print(dcprogram.run(df))
                a    b
0        New York   NY
1        New York   NY
2   San Francisco   SF
3   San Francisco   SF
4        San Jose   SJ
5        New York   NY
6   San Francisco   SF
7   Berkeley City   Bk
8       San Mateo  SMO
9          Albany   AB
10      San Mateo  SMO
```

#### 搜索器配置

事实上，即使在一个相对简单的问题上，搜索算法也需要30秒左右的时间来运行。下面从两个角度进行分析。

首先，在设计的流水线中，可以人为的设置搜索深度。
如果我们知道清洁问题相对容易，我们可以通过限制搜索深度来优化算法的性能。
`solve`命令可以选择接收一个配置对象。人们可以这样查询默认的配置:

```
from AlphaClean.search import DEFAULT_SOLVER_CONFIG
config = DEFAULT_SOLVER_CONFIG
print(config['dependency']['depth'])

>>10
```
下面配置参数设置为3:
```py
config['dependency']['depth'] = 3
```
另一个低效率的来源是用修复于惩罚的相似度指标计算了过多数据。
默认情况下，这是一个`Levenstein`距离计算。在更简单的问题上，
我们可以使用更有效的`Jaccard`相似度:
```py
config['dependency']['similarity'] = {'a': 'jaccard'}
```
如果你用这些参数调用搜索器，搜索的优化速度会快一点:
```py
dcprogram = solve(df, patterns=[], dependencies=[constraint], config=config)
```

#### 更复杂的情况

`example`文件夹包含了一些更复杂的场景。
可以用`python examples/examplex.py`
来运行`AlphaClean`文件夹中的所有例子。
这是为了保持`sklearn`中的`toy datasets`和模型的默认路径一致，
可以自由修改这些路径。

### 1. 通过定义约束添加多种清洗方式

这个例子是为了说明更复杂的功能和`AlphaClean`中的概念。不是所有的数据模型都像一对一的关系那样简单。有时我们会有更复杂的约束，我们想强制执行。这个例子在 `examples/example8.py`.

让我们考虑以下数据。

```python
data = [{'title': 'Employee 1' , 'salary': 100.0}, 
         {'title': 'Employee 2' , 'salary': 100.0},
         {'title': 'Employee 3' , 'salary': 100.0},
         {'title': 'Employee 4' ,'salary': 100.0},
         {'title': 'Manager 1' ,'salary': 500.0},
         {'title': 'Manager 2' ,'salary': 80.0}]
```

在这个表中有两类记录：雇员和经理。
假设我们想强制要求不存在一个收入低于雇员的经理。
这种类型的约束可以用一种形式化的语言来表达，叫做**拒绝约束**（一组不能全部为真的数据库谓词）。

`AlphaClean` 提供了一个API，用于在`DataFrame`上指定这种约束。

一个谓词的基本结构如下。

* 这个谓词被应用于`dataframe`的每一行。
* 对于每一行，我们可以查询一个叫做 `local attribute`的属性
* 然后，我们可以在这个值上和整个数据框架上评估一个布尔表达式

```python
from AlphaClean.constraint_languages.ic import DenialConstraint, DCPredicate

# Employee is a manager
predicate1 = DCPredicate(local_attr='title', expression=lambda value, data_frame: 'Manager' in value)

# There exists an employee with a salary greater than the given manager's salary
predicate2 = DCPredicate(local_attr='salary', expression=lambda value, data_frame:
    data_frame[(data_frame['salary'] > value) &
               data_frame['title'].str.contains("Employee", na=False)].shape[0] > 0)

constraint = DenialConstraint([predicate1, predicate2])                                                    
```

和以前一样，我们可以通过`solve`来找到一个能满足修复约束的中间算子:

```python
from AlphaClean.search import solve

dcprogram, output = solve(df, patterns=[], dependencies=[constraint])
```

可以看到这样的输出:

```
print(dcprogram)
df = swap(df,'salary','500.0',('salary', set([80.0])))

print(output)
salary       title
0   100.0  Employee 1
1   100.0  Employee 2
2   100.0  Employee 3
3   100.0  Employee 4
4   500.0   Manager 1
5   500.0   Manager 2
```

#### 改变搜索参数，添加Delete算子

这里的一个问题是，虽然约束被强制执行，
但这样做可能在语义上没有意义。将经理的工资设置为500可能并不准确。假设，我们只是想删除那些导致这些违规的单元格。我们可以在`AlphaClean`中非常容易地做到这一点，我们切换搜索语言，只考虑删除操作，不考虑对数据的修改。

```py
from AlphaClean.search import DEFAULT_SOLVER_CONFIG
from AlphaClean.ops import Delete

config = DEFAULT_SOLVER_CONFIG
config['dependency']['operations'] = [Delete]
```

上述配置对象将操作限制为只考虑删除。 其结果是:

```
dcprogram2, output2 = solve(df, patterns=[] ,dependencies=[constraint], config=config)

print(dcprogram2)
df = delete(df,'title',('salary', set([80.0]))

print(output2)
0   100.0  Employee 1
1   100.0  Employee 2
2   100.0  Employee 3
3   100.0  Employee 4
4   500.0   Manager 1
5    80.0        None)
```

编辑惩罚

我们可能想在删除和替换之间灵活地移动，这取决于我们认为错误有多严重。
考虑一下第二位经理的工资为50.0的表格:


```
    salary       title
0   100.0  Employee 1
1   100.0  Employee 2
2   100.0  Employee 3
3   100.0  Employee 4
4   500.0   Manager 1
5    50.0   Manager 2
```

也许一个合理的假设是，这是一个异常值， 可以安全地更新到500.0。
我们可以在`AlphaClean`中通过改变编辑成本来表达这样的逻辑，
即对修改数据的惩罚。让我们首先创建一个新的数据集:

```python
data = [{'title': 'Employee 1' , 'salary': 100.0}, 
         {'title': 'Employee 2' , 'salary': 100.0},
         {'title': 'Employee 3' , 'salary': 100.0},
         {'title': 'Employee 4' ,'salary': 100.0},
         {'title': 'Manager 1' ,'salary': 500.0},
         {'title': 'Manager 2' ,'salary': 50.0}]

df = pd.DataFrame(data)
```

并将搜索器配置为同时使用Swap和Delete算子:

```python
from AlphaClean.search import DEFAULT_SOLVER_CONFIG
from AlphaClean.ops import Delete, Swap

config = DEFAULT_SOLVER_CONFIG
config['dependency']['operations'] = [Swap, Delete]
```

编辑惩罚可以通过以下配置选项来修改，先把它设置为0:

```python
config['dependency']['edit'] = 0
```

此时我们运行搜索器，我们可以看到，搜索器倾向于替换元素:

```
dcprogram3, output3 = solve(df, patterns=[] ,dependencies=[constraint], config=config)

print(dcprogram3)
df = swap(df,'salary','500.0',('salary', set([50.0])))   

print(output3)
salary       title
0   100.0  Employee 1
1   100.0  Employee 2
2   100.0  Employee 3
3   100.0  Employee 4
4   500.0   Manager 1
5   500.0   Manager 2
```

如果我们让编辑的成本为10:

```python
config['dependency']['edit'] = 10
```

我们可以得到被删除的结果:

```
df = delete(df,'title',('salary', set([80.0]))

0   100.0  Employee 1
1   100.0  Employee 2
2   100.0  Employee 3
3   100.0  Employee 4
4   500.0   Manager 1
5    80.0        None)
```

#### 调试

每次执行示例文件都会创建一个随机的日志文件，文件名包括一个随机的字符串和当前程序开始运行的时间序列号，你可以通过查看每个示例顶部的environ导入来配置日志：

```python
import logging 
import string
import random
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
logfilename =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) +'_'+timestr+ '.log'

logging.basicConfig(level=logging.DEBUG, filename=logfilename) 

logging.warn("Logs saved in " + logfilename)
```

如果你把它改为logging.DEBUG，你会得到更多关于算法所做决定的详细日志。同时在对应的`example`中，我也添加了相应的输出，帮助用户更快的查看日志在哪里。

### 2.`AlphaClean`的分块策略和基于模式匹配的修复

这个例子将展示如何将通过分块策略将搜索算法扩展到更大的数据集，
并在一些真实的数据运行清洗。

从不同的网络来源获得的数据往往存在差异，
一个常见的数据清理任务是将这些差异利用统计修复的策略修复为同一种格式。
实例2` examples/example2.py`将利用与小规模例子相同的基本工具，
展示了如何在我们的框架中完成这个任务。


该实例中加载了一家航空公司1000个到达和离开时间的数据集：

```python
import pandas as pd
f = open('../testdata/airplane.txt','r')
data = [  { str(i):j for i,j in enumerate(l.strip().split('\t')) } for l in f.readlines()]
df = pd.DataFrame(data)
```

我们把它加载到pandas数据框架中，会得到一个在格式、取值和完整性方面有大量不一致的数据集:

```pyhon
                0                1                    2                3  \
10         panynj  AA-1007-TPA-MIA                         2:07 PMDec 01   
11          gofox  AA-1007-TPA-MIA                         2:07 PMDec 01   
12    foxbusiness  AA-1007-TPA-MIA                         2:07 PMDec 01   
13   allegiantair  AA-1007-TPA-MIA                         2:07 PMDec 01   
14         boston  AA-1007-TPA-MIA                         2:07 PMDec 01   
15    travelocity  AA-1007-TPA-MIA      Dec 01 - 1:55pm  Dec 01 - 1:57pm   
16         orbitz  AA-1007-TPA-MIA           1:55pDec 1       1:57pDec 1   
17        weather  AA-1007-TPA-MIA  2011-12-01 01:55 PM                    
18            mia  AA-1007-TPA-MIA                                         
19  mytripandmore  AA-1007-TPA-MIA           1:55pDec 1       1:57pDec 1   

       4                    5                  6    7  
10                                 2:57 PMDec 01  NaN  
11                                 2:57 PMDec 01  NaN  
12                                 2:57 PMDec 01  NaN  
13                                 2:57 PMDec 01  NaN  
14                                 2:49 PMDec 01  NaN  
15   F78      Dec 01 - 3:00pm    Dec 01 - 2:57pm   D5  
16   F78           3:00pDec 1         2:57pDec 1   D5  
17        2011-12-01 03:00 PM                NaN  NaN  
18             3:00P 12-01-11  2011-12-01  2:57P  NaN  
19   F78           3:00pDec 1         2:57pDec 1   D5 
```

#### 创建数据模型

我们可以用`AlphaClean`来解决这个问题。
首先，我们把所有的日期/时间属性2、3、5、6选择出来。
我们有一个特殊的约束条件，
对标准strftime格式的日期/时间属性执行模式。

```python
from AlphaClean.constraint_languages.pattern import Date

patterns = [Date("2", "%m/%d/%Y %I:%M %p"), Date("3", "%m/%d/%Y %I:%M %p"), Date("5", "%m/%d/%Y %I:%M %p"),
            Date("6", "%m/%d/%Y %I:%M %p")]
```

这使得数值应该是 `MM-DD-YYY HH:MM {AM,PM}`的形式。

接下来，我们必须对属性4（型号）执行一个`Pattern`：

```python
from AlphaClean.constraint_languages.pattern import Pattern

patterns += [Pattern("4", '^[a-zA-Z][0-9]+'), Pattern("7", '^[a-zA-Z][0-9]+')]
```

然后，我们在航班代码（属性1）和所有其他属性之间引入一个一对一的约束，加入最小化规则违反的修复：

```python
from AlphaClean.constraint_languages.ic import OneToOne
dependencies = []
for i in range(2, 8):
    dependencies.append(OneToOne(["1"], [str(i)]))
```

#### 数据的分块策略

因为这个数据集大大的大了，我们要用块来解决它。块划分解耦的数据单元，以加快搜索算法的速度。
在这种情况下，代码是一个合理的块状规则：

```python
from AlphaClean.search import solve

operation = solve(df, patterns, dependencies, partitionOn="1")
```

这意味着搜索器将采用分而治之的策略，
以属性'1'（航班代码）划分的块来解算问题。
这应该需要5分钟左右的时间来运行，并将输出一个很长的中间算子序列
来修复所有的数据，这里是一个结果的样本：

```
10                panynj  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
11                 gofox  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
12           foxbusiness  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
13          allegiantair  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
14                boston  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
15           travelocity  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
16                orbitz  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
17               weather  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
18                   mia  AA-1007-TPA-MIA  12/01/2011 01:55 PM   
19         mytripandmore  AA-1007-TPA-MIA  12/01/2011 01:55 PM


10  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
11  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
12  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
13  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
14  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
15  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
16  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
17  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
18  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
19  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5  
20  12/01/2011 02:07 PM  F78  12/01/2011 03:00 PM  12/01/2011 02:51 PM    D5
```

合成的操作序列的一个片段如下：

```python
...

df = delete(df,'6',('6', set([nan])))
df = delete(df,'6',('6', set(['2:57pDec 1'])))
df = pattern(df,'7','^[a-zA-Z][0-9]+')

df = delete(df,'7',('7', set([None])))


df = swap(df,'2','12/01/2011 12:10 PM',('1', set(['AA-1518-DFW-SDF'])))

df = swap(df,'3','12/01/2011 12:18 PM',('1', set(['AA-1518-DFW-SDF'])))

df = swap(df,'4','C20',('1', set(['AA-1518-DFW-SDF'])))

df = swap(df,'5','12/01/2011 03:10 PM',('1', set(['AA-1518-DFW-SDF'])))

df = swap(df,'6','12/01/2011 02:57 PM',('1', set(['AA-1518-DFW-SDF'])))

df = swap(df,'7','A15',('1', set(['AA-1518-DFW-SDF'])))

df = dateparse(df,'2','%m/%d/%Y %I:%M %p')

...

```

### 3. 通过外部字典进行匹配依赖修复

在这个例子中，我们有一个由1000个美国2016年总统选举捐款组成的数据集，
想把捐款人的职业归为一组。 
 例子3 `examples/example3.py`展示了如何在我们的框架中完成这一工作。这个例子要求至少有8GB的可用内存。

#### 加载数据和初步数据分析

首先，把数据加载到系统中:

```python
import pandas as pd

df = pd.read_csv('testdata/elections.txt', quotechar='\"', index_col=False)
```
打印一个样本记录:

```
print(df.iloc[0,:])

cmte_id                                          C00458844
cand_id                                          P60006723
cand_nm                                       Rubio, Marco
contbr_nm                                    BLUM, MAUREEN
contbr_city                                     WASHINGTON
contbr_st                                               20
contbr_zip                                              DC
contbr_employer      STRATEGIC COALITIONS & INITIATIVES LL
contbr_occupation                        OUTREACH DIRECTOR
contb_receipt_amt                                      175
contb_receipt_dt                                 15-MAR-16
receipt_desc                                           NaN
memo_cd                                                NaN
memo_text                                              NaN
form_tp                                              SA17A
file_num                                           1082559
tran_id                                       SA17.1152124
election_tp                                          P2016
```

值得关注的属性是`contbr_occupation`--按职业来分析贡献 

如果想对这个数据库中的人进行分类，就必须对这些不同的属性值进行标准化处理。
在的`misc.py`中，有一个帮助方法可以建立一个 `Codebook`。

```py
from AlphaClean.misc import generateCodebook

codes = generateCodebook(df, 'contbr_occupation')
print(codes)
```

外部字典看起来是这样的:

```py
set(['CPA', 'LAWYER', 'WEALTH MANAGEMENT ADVISOR', 'SEMI-RETIRED PHYSICIAN', 'CHAIRMAN/CEO', 'RETIRED', 'FRANCHISEE', 'EDUCATION CHIEF', 'SHERIFF OF ETOWAH CO', 'VICE PRESIDENT/OWNER', 'UBI', 'HOMEMAKER', 'ATTORNEY', 'TRANSPORTATION', 'HEALTH CARE', 'E.E.', 'SUPPORTED LIVING SPECIALIST... RETIRED', 'ATHLETICS COMMUNICATIONS ASSOCIATE', 'CEO', 'PRESIDENT AND CEO', 'VP FOR GOVERNMENT AFFAIRS & SPECIAL CO', 'DIRECTOR OF FINANCE', 'CONTRACTOR', 'MANAGER', 'BUSINESS OWNER', 'M.D.', 'KBR', 'ADMIN ASSISTANT', 'YMCA', 'BDC', 'EXPERIANCED HOSPITAL CEO', 'FUNERAL DIRECTOR', 'THEATRE OWNER', 'HOUSEWIFE', 'MEDICAL TRANSCRIPTIONIST', 'OWNER', 'INSURANCE AGENT', 'REAL ESTATE BROKER', 'ACCOUNTANT', 'CUSTOMER SERVICE', 'PARTNER', 'TEACHER', 'VOLUNTEER', 'BUSINESS FARMS SALES', 'SMALL BUSINESS OWNER', 'FINANCIAL ADVISOR', 'ENGINEER', 'MULTIFAMILY REAL ESTATE', 'MANAGEMENT', 'FINANCE', 'VICE PRESIDENT', 'EXECUTIVE', 'CARPENTER', 'NORTH SLOPE BOROUGH SCHOOL DISTRICT', 'CAMPAIGN COORDINATOR', 'PRESIDENT', 'PHARMACIST', 'ANALYST', 'STATE REPRESENTATIVE', 'KFC FRANCHISEE', 'CONSTRUCTION', 'HUMAN RESOURCE OFFICER', 'INFORMATION REQUESTED PER BEST EFFORTS', 'SELF EMPLOYED', 'US GOVERNMENT', 'PND ENGINEERS', 'CONSULTANT', 'CLERK', 'WRITER', 'COMMUNICATIONS', 'STUDENT', 'R.N.', 'REAL ESTATE/OWNER', 'CONSULTING', 'SYSTEMS ANALYST', 'SALES REPRESENTATIVE', 'FARM', 'DAVIS HEATING & COOLING', 'SPEECH PATHALOGIST', 'ATTORNEY/REAL ESTATE DEVELOPER', 'CARDIOTHORACIC SURGEONS PC', 'SECRETARY', 'FURRIER', 'FARMER', 'AVIATOR', 'PILOT', 'COMMERCIAL REAL ESTATE BROKER', 'PHYSICIAN', 'IT', 'SUPERVISORY ADMINISTRATIVE OFFICER', 'FIELD REP', 'REAL ESTATE APPRAISER', 'CFO', 'REAL-ESTATE INVESTOR', 'SELF-EMPLOYED', 'SELF', 'SALES', 'HVAC TECH', 'SALES DIRECTOR'])
```

#### 定义约束条件

我们想强制要求该属性的所有值都存在于外部字典中。
这可以通过我们称之为`DictValue`的约束来指定:

```py
DictValue('contbr_occupation', codes)
```

用`AlphaClean`来找到最小成本的来满足这个约束条件。 
然而，对如何定义代价函数有一个技巧。 例如，`MEDICAL DOCTOR`和`PHYSICIAN`这两个值非常相似，
但在大多数字符串相似度指标上会有很大差异。
因此`AlphaClean`提供了一个在谷歌新闻语料库上预先训练好的100B实体的编辑成本函数。

```
mkdir -p resources
wget http://automation.berkeley.edu/archive/GoogleNews-vectors-negative300.bin
mv GoogleNews-vectors-negative300.bin resources
```

为了使用这个成本函数，以如下方式修改约束条件:

```python
config = DEFAULT_SOLVER_CONFIG
config['dependency']['similarity'] = {'contbr_occupation':'semantic'}
```

还可能希望允许搜索器使用“Delete”中间算子（那些似乎与代码书中的任何内容不匹配的记录）:

```python
config['dependency']['operations'] = [Swap, Delete]
```

#### 运行搜索器

需要一段时间来运行，因为它必须将整个`Word2Vec`模型加载到内存中。

```python
operation = solve(df, [], dependencies=[DictValue('contbr_occupation', codes)], partitionOn='contbr_nm', config=config)
```

结果将看起来像这样:

```python
df = delete(df,'contbr_occupation',('contbr_occupation', set(['PHYSICAL THERAPIST'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INVESTMENT BUSINESS'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['A PRINCIPAL'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CITY PLANNER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CHAIRMAN & CEO'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['PROPERTY INVESTMENT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CHIEF FINANCIAL OFFICER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EVP'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INVESTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INSURANCE & REAL ESTATE'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CIO'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['C.E.O.'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ENVIRONMENTAL ADVISOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['NURSE PRACTITIONER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['PRIVATE MORTGAGE BANKING'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EXECUTIVE INSURANCE BROKER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INVESTMENTS'])))
df = swap(df,'contbr_occupation','BUSINESS OWNER',('contbr_occupation', set(['BUSINESS'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['C.E.O./OWNER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['FINANCIAL CONSULATANT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['REAL ESTATE/CEO'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['AUTO DEALER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['FINANCIAL ADVISORS'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['OPERATIONS DIRECTOR'])))
df = swap(df,'contbr_occupation','COMMUNICATIONS',('contbr_occupation', set(['COMMUNICATIONS DIRECTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ORTHODONTIST'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['MILITARY'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['PRESIDENT/CEO'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ENGINEER (RET.)'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['GEOLOGIST'])))
df = swap(df,'contbr_occupation','MANAGEMENT',('contbr_occupation', set(['INVESTMENT MANAGEMENT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['OWNER CEO'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EXECUTIVE SENIOR VP'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['GOVERNMENTAL AFFAIRS'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['DERMATOLOGIST'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EDUCATOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['REAL ESTATE INVESTMENT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CHIEF HUMAN RELATIONS OFFICER'])))
df = swap(df,'contbr_occupation','ENGINEER',('contbr_occupation', set(['CIVIL ENGINEER'])))
df = swap(df,'contbr_occupation','EXECUTIVE',('contbr_occupation', set(['EXECUTIVE DIRECTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['PRODUCTION'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['MANUFACTURER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['BENNETT LUMBER COMPANY PIEDMONT AL'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['BENNETT LUMBER COMPANY'])))
df = swap(df,'contbr_occupation','CLERK',('contbr_occupation', set(['GROCERY CLERK'])))
df = swap(df,'contbr_occupation','CONSTRUCTION',('contbr_occupation', set(['ELECTRICAL CONSTRUCTION'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INS SALES'])))
df = swap(df,'contbr_occupation','PHYSICIAN',('contbr_occupation', set(['DOCTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['LAW CLERK'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['CIVIL SERVANT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['LIFE SAVVY WEIGHT LOSS CLINIC'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['COA'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EXEUCTIVE'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['COMPUTER PROGRAMMER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ADVISOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['OUTREACH DIRECTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['BOOKEEPER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['INSURANCE'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['DEVELOPMENT OFFICER'])))
df = swap(df,'contbr_occupation','PHYSICIAN',('contbr_occupation', set(['MEDICAL DOCTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ASTROPHYSICIST'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['EQUIPMENT OPERATOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ATTORNEY/SHAREHOLDER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['AUTHOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['POLICE OFFICER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['FOREIGN SERVICE OFFICER'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['ADMINISTRATION'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['FIRE DEPARTMENT'])))
df = swap(df,'contbr_occupation','CONTRACTOR',('contbr_occupation', set(['CONSTRUCTION CONTRACTOR'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['LAW ENFORCEMENT'])))
df = delete(df,'contbr_occupation',('contbr_occupation', set(['COMMUNITY BUSINESS DEVELOPER'])))
df = swap(df,'contbr_occupation','HEALTH CARE',('contbr_occupation', set(['HEALTH'])))
```

在配置参数上做文章，使下面的参数变大或变小，改变Swap和Delete的倾向：

```python
config['dependency']['edit'] = 1
```

### 4. `AlphaClean`加入处理 "简单 "异常值的清洗方法

在下一个例子`example4`中，我们考虑 "简单 "的离群值。
也就是说，明显偏离分布中正常值的单一属性。

#### 天气数据集

天气数据集包含30个城市的6030条天气读数记录:

```
0          Fri Jan 29 08:38:52 2010
1                    Austin, Texas 
2      Heavy Thunderstorms and Rain
3                                55
4                               WNW
5                                 8
6                                54
7                             29.95
8                                  
9                                94
10                              1.5
```

这个数据集有一个数字和分类值的混合体。
 首先，加载数据集:

```python
f = open('testdata/weather.txt', 'r')
data = [{str(i): j for i, j in enumerate(l.strip().split('\t'))} for l in f.readlines()]
df = pd.DataFrame(data)
```

#### 创建约束条件

接下来，把每一列数字解析为一个浮点数字:

```python
from AlphaClean.constraint_languages.pattern import Float

patterns = [Float("3"), Float("5"), Float("6"), Float("7"), Float("8"), Float("9"), Float("10")]
```

最后运行搜索器：

```python
operation = solve(df, patterns,[])

output = operation.run(df)
```

把结果绘制出来:

```python
import matplotlib.pyplot as plt

plt.hist(output["5"].dropna().values)

plt.show()
```

可以看到有很大的离群值污染了数据。
可以进一步添加一个 "模型 "限制，给系统一个提示，
即该列代表一个统计分布，应该集中在中心值周围。

```python
from AlphaClean.constraint_languages.statistical import Parametric

models = [Parameteric("5")]
```

#### 结果形成的方案:

```python
df = numparse(df,'3')
df = numparse(df,'5')
df = numparse(df,'6')
df = numparse(df,'7')
df = numparse(df,'8')
df = numparse(df,'9')
df = numparse(df,'10')
df = delete(df,'5',('5', set([-9999.0])))
df = delete(df,'5',('5', set([33.0])))
```



### 5. 更高级的数字清洗

本节主要集中在`AlphaClean.constraint_languages.statistics`的模块上。
这个模块中的大多数类都定义了软约束
（即基于违反程度的质量函数，硬约束之间如果存在矛盾，那么搜索器将失败，
软约束仅表示对一种解决方案的偏好，当软约束与其他硬约束相矛盾时，软约束将被放弃）。

相关性约束是对两个属性之间的正负关系的一种软性提示。两个属性之间的正负关系的软提示。
例如，如果我们期望两个属性之间有正相关关系，我们可以写下面的约束。

```python
from AlphaClean.constraint_languages.statistical import Correlation

Correlation(["attr1", "attr2"], ctype="positive")
```

这意味着`attr2`的值如果高于平均值，就意味着`att1`的相应值也高于平均值。
这个约束创造了一个质量函数，对不遵守这种关系的行为进行惩罚。

数字关系（`NumericalRelationship`）约束是另一种软约束。
数字关系是对两个数字属性之间关系的一个软性提示属性之间的关系。 可以写一个函数，当数值与该函数的偏差较大时，该约束就会更强烈地发射。
例如，如果我们期望两个属性应该是接近的，我们可以写：

```python
from AlphaClean.constraint_languages.statistical import NumericalRelationship

NumericalRelationship(["attr1", "attr2"], lambda x: x)
```
这将对两个属性之间的差异进行惩罚。
