"""
Example 1: 城市缩写数据集清洗.调试
"""

import environ
from util.self_test import Self_test

print("Logs saved in " + environ.logfilename);

data = [{'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NY'},
        {'a': 'New Yorks',     'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NYc'},

        ]

data1 = [{'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b':'NY'},
        {'a': 'New York',      'b': 'NY'},
        {'a': 'New Yorks',     'b': 'NY'},
        {'a': 'New Yorks',     'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NYc'},

        ]
"""
data = [{'a': 'New Yorks',     'b': 'NY'},
        {'a': 'New Yorks',      'b': 'NYc'},
        {'a': 'New Yorks',     'b': 'NYc'},
{'a': 'New Yorks',     'b': 'NYc'},


        ]
"""
import pandas as pd
df = pd.DataFrame(data)##将数据加载到一个Pandas DataFrame中
df1 = pd.DataFrame(data1)

from dataclean.constraint_languages.ic import OneToOne, OneDeterminedOne

constraint1 = OneToOne(["a"], ["b"])
test = Self_test(df,[],[constraint1])
print(test.score())

constraint2 = OneToOne(["a"], ["b"])
test1 = Self_test(df1,[],[constraint2])
print(test1.score())



from dataclean.search import solve, DEFAULT_SOLVER_CONFIG
config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 10
config['dependency']['similarity'] = {'a': 'jaccard'}


dcprogram, output ,eidt= solve(df, dependencies=[constraint1], config=config)

print(dcprogram)
print(dcprogram, output)

