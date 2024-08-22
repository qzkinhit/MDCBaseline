"""
Example 1: 城市缩写数据集清洗.
"""

import environ
print("Logs saved in " + environ.logfilename);
data = [{'a': 'New Yorks',     'b': 'NY'},#脏元组
        {'a': 'New York',      'b': 'NY'},
        {'a': 'San Francisco', 'b': 'SF'},
        {'a': 'San Francisco', 'b': 'SF'},
        {'a': 'San Jose',      'b': 'SJ'},
        {'a': 'New York',      'b': 'NY'},
        {'a': 'San Francisco', 'b': 'SFO'},#脏元组
        {'a': 'Berkeley City', 'b': 'Bk'},
        {'a': 'San Mateo',     'b': 'SMO'},#脏元组
        {'a': 'Albany',        'b': 'AB'},
        {'a': 'San Mateo',     'b': 'SM'}]

import pandas as pd
df = pd.DataFrame(data)##将数据加载到一个Pandas DataFrame中


from dataclean.constraint_languages.ic import OneToOne
constraint1 = OneToOne(["a"], ["b"]) #一对一约束
from dataclean.search import solve, DEFAULT_SOLVER_CONFIG
config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 3
config['dependency']['similarity'] = {'a': 'jaccard'}


dcprogram, output,_ = solve(df, dependencies=[constraint1], config=config)

print(dcprogram)
print(output)

