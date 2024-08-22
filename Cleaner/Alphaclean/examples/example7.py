import environ
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
print("Logs saved in " + environ.logfilename);
#Load the rain fall data
f = open('../testdata/all_villages_2010-16.csv', 'r')
datafile = f.readlines()

data = [  { str(i):j for i,j in enumerate(l.strip().split(',')) } for l in datafile[2:]]
locations = [  { str(i):j for i,j in enumerate(l.strip().split(',')) if i >= 3} for l in datafile[0:2]]

df = pd.DataFrame(data)



from dataclean.constraint_languages.pattern import Float

from dataclean.constraint_languages.statistical import Correlation, NumericalRelationship

# 属性约束为正浮点型
patterns = []
for i in range(3,84):
    patterns.append(Float(str(i), [0, np.inf]))#Float的约束正浮点数


models = []

#计算邻近村庄之间的距离并确保附近村庄之间存在正相关关系
for l in locations[0]:
    lat_long = np.array([float(locations[0][l]), float(locations[1][l])])
    distances = [ 
                    (np.linalg.norm( np.array([float(locations[0][other]), \
                                      float(locations[1][other])])\
                   -lat_long), other) \

                    for other in locations[0] if l != other\
                ]

    distances = sorted(distances)

    if distances[0][0] == 0.0:
      models.append(NumericalRelationship([l, distances[0][1]], lambda x: x))



#Solve
from dataclean.search import *

config = DEFAULT_SOLVER_CONFIG

#无需对pattern约束搜索，直接强制执行Float约束
config['pattern']['depth'] = 0

#only delete
config['dependency']['operations'] = [Delete]
config['dependency']['depth'] = 1

operation, output,_ = solve(df, patterns, models)

print(operation)
print("------------")
print(output)

