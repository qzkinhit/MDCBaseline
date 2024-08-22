import numpy as np
import pandas as pd
from dataclean.search import DEFAULT_SOLVER_CONFIG
from dataclean.constraint_languages.ic import OneToOne
import time
import matplotlib.pylab as plt
from dataclean.search import *

from dataclean.constraint_languages.pattern import Date, Pattern

class Self_test(object):
    def __init__(self, df, patternlist = [],dependency_list = []):
        self.df = df
        self.cost = patternlist
        self.dependency_list = dependency_list

    def score(self):
        array_list = []
        N = self.df.shape[0]

        qfn_a = np.zeros((N,))

        for c in self.cost:
            if isinstance(c , Pattern):
                d = PatternCast(c.attr, c.pattern)
                self.df = d.run(self.df)
            elif isinstance(c , Float):
                d =  FloatCast(c.attr, c.range)
                self.df = d.run(self.df)
            elif isinstance(c,  Date):
                d = DatetimeCast(c.attr, c.pattern)
                self.df = d.run(self.df)

            q_array = c.qfn(self.df)

            array_list.append(q_array)


        for c in self.dependency_list:
            q_array2 = c.qfn(self.df)
            array_list.append(q_array2)
            print(q_array2)



        for a in array_list:
            qfn_a = qfn_a + a


        return np.sum(qfn_a)

    def edit_score(self,orig):
        config = DEFAULT_SOLVER_CONFIG
        editCostObj = CellEdit(orig, {}, config['dependency']['w2v'])
        efn = editCostObj.qfn
        return np.sum(efn(self.df))



"""
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


import pandas as pd
df = pd.DataFrame(data)##将数据加载到一个Pandas DataFrame中


from dataclean.constraint_languages.ic import OneToOne
constraint1 = OneToOne(["a"], ["b"])

from dataclean.search import solve, DEFAULT_SOLVER_CONFIG
config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 3
config['dependency']['similarity'] = {'a': 'jaccard'}
####

dcprogram, output = solve(df, dependencies=[constraint1], config=config)

print(dcprogram, output)

test1 = Self_test(df,[constraint1])
test1.score()

f = open('../testdata/airplane_small.txt', 'r')
data = []
for line in f.readlines():
    parsed = line.strip().split('\t')
    data.append({str(i): j for i, j in enumerate(parsed)})
df = pd.DataFrame(data)




patterns = [
            #Date("2", "%m/%d/%Y %I:%M %p"),
            #Date("3", "%m/%d/%Y %I:%M %p"),
            Pattern("4", '^[a-zA-Z][0-9]+'),
            #Date("5", "%m/%d/%Y %I:%M %p"),
            #Date("6", "%m/%d/%Y %I:%M %p"),
            Pattern("7", '^[a-zA-Z][0-9]+')
            ]

from dataclean.constraint_languages.ic import OneDeterminedOne

dependencies = [OneDeterminedOne(["1"], [str(i)]) for i in range(2, 8)]


from dataclean.search import *
pd.set_option('display.max_columns',10)
config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 5
config['pattern']['depth'] = 5
config['pattern']['edit'] = 0
config['dependency']['similarity'] = {'a':'jaccard'}
config['dependency']['operations'] = [Swap]
#print(df)
test = Self_test(df,patterns,[])
qfn_a0 = test.score()
#print(df.shape[0],df.shape[1])

time_start0=time.time()
operation, output, edit_score = solve(df, patterns, [], partitionOn="1",config= config)
#print(output)
time_end0=time.time()
test0 = Self_test(output,patterns,[])
qfn_a = test0.score()

config['dependency']['depth'] = 5
config['pattern']['depth'] = 5

time_start1=time.time()
operation1, output1, edit_score1 = solve(df, patterns, dependencies, partitionOn="1",config= config)
time_end1=time.time()
test1 = Self_test(output1,patterns,dependencies)
qfn_a1 = test1.score()

config['dependency']['depth'] = 8
config['pattern']['depth'] = 8
time_start2 = time.time()
operation2, output2, edit_score2 = solve(df, patterns, dependencies, partitionOn="1",config= config)
time_end2 = time.time()
test2 = Self_test(output2,patterns,dependencies)
qfn_a2 = test2.score()



time_start3 = time.time()
operation3, output3 ,edit_score3= solve(df, patterns, dependencies, partitionOn="1")
time_end3 = time.time()


test3 = Self_test(output3,patterns,dependencies)
qfn_a3 = test3.score()



print(np.sum(qfn_a0))

print(np.sum(qfn_a))
#print("编辑惩罚0  " + str(edit_score))
#print(np.sum(qfn_a1))
#print("编辑惩罚1  " + str(edit_score1))
#print(np.sum(qfn_a2))
#print(np.sum(qfn_a3))
print('time cost',time_end0-time_start0,'s')
#print('time cost',time_end1-time_start1,'s')
#print('time cost',time_end2-time_start2,'s')
#print('time cost',time_end3-time_start3,'s')
print(output)
print("11111111111111111111")
print(df)
print(operation)
"""