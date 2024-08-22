import environ
import pandas as pd
from dataclean.search import *

df = pd.read_csv('../testdata/pcari_csv.csv', quotechar='\"', index_col=False)
df1 = pd.read_csv('../testdata/pcari_csv.csv', quotechar='\"', index_col=False)
print("Logs saved in " + environ.logfilename);
from dataclean.constraint_languages.ic import DictValue

from dataclean.constraint_languages.pattern import Float, Pattern


patterns = []

# M or F based on the interface
patterns += [DictValue('Gender', set(['M', 'F']))]

#18 years old to 100, remove under 18 since that violates IRB anyways
patterns += [Float('Age', [18, 100])]

#Only alpha numeric values
patterns += [Pattern('Comment', "^[a-zA-Z0-9_]*$")]


#generate a code book
from dataclean.misc import generateCodebook
codes = generateCodebook(df,'Barangay', size=100)
codes = [c for c in codes if not 'x' in c.lower() and not '--' in c.lower()] #remove some messy string artifacts


config = DEFAULT_SOLVER_CONFIG
config["pattern"]["depth"] = 2
config['dependency']['similarity'] = {'Barangay': 'jaccard'}
config['dependency']['operations'] = [Swap]
config['dependency']['edit'] = 7


operation ,output,_= solve(df, patterns, [DictValue('Barangay', codes)], partitionOn="Barangay")

print(operation)
print("------------")
print(output)







