"""
Example 3: Election data.
"""

import environ
import pandas as pd
from dataclean.search import *

print("Logs saved in " + environ.logfilename)
df = pd.read_csv('../testdata/elections.txt', quotechar='\"', index_col=False)

from dataclean.misc import generateCodebook

codes = generateCodebook(df, 'contbr_occupation')
# print(codes)

config = DEFAULT_SOLVER_CONFIG
config['dependency']['similarity'] = {'contbr_occupation': 'semantic'}
config['dependency']['operations'] = [Swap, Delete]
config['dependency']['depth'] = 1

from dataclean.constraint_languages.ic import DictValue

operation, output,_= solve(df, [], dependencies=[DictValue('contbr_occupation', codes)],
                          partitionOn='contbr_occupation', config=config)

print(operation, output)
