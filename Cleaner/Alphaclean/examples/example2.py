"""
Example 2: Flight data.
验证分块策略和模式匹配修复
"""

import environ
import pandas as pd
print("Logs saved in " + environ.logfilename);
f = open('../testdata/airplane_small.txt', 'r')
data = []
for line in f.readlines():
    parsed = line.strip().split('\t')
    data.append({str(i): j for i, j in enumerate(parsed)})
df = pd.DataFrame(data)


from dataclean.constraint_languages.pattern import Date, Pattern

patterns = [Date("2", "%m/%d/%Y %I:%M %p"),
            Date("3", "%m/%d/%Y %I:%M %p"),
            Pattern("4", '^[a-zA-Z][0-9]+'),
            Date("5", "%m/%d/%Y %I:%M %p"),
            Date("6", "%m/%d/%Y %I:%M %p"),
            Pattern("7", '^[a-zA-Z][0-9]+')]

from dataclean.constraint_languages.ic import OneDeterminedOne

dependencies = [OneDeterminedOne(["1"], [str(i)]) for i in range(2, 8)]


from dataclean.search import *
pd.set_option('display.max_columns',10)
config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 1
config['dependency']['similarity'] = {'a':'jaccard'}
config['dependency']['operations'] = [Swap]
print(df)
operation, output ,_ = solve(df, patterns, [], partitionOn="1")

print(operation, output)
