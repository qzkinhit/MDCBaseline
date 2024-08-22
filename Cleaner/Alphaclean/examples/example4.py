import environ
import pandas as pd

print("Logs saved in " + environ.logfilename);
f = open('../testdata/weather.txt', 'r')
data = [{str(i): j for i, j in enumerate(l.strip().split('\t'))} for l in f.readlines()]
df = pd.DataFrame(data)

print(df.iloc[0, :])

from dataclean.constraint_languages.pattern import Float

patterns = [Float("3"), Float("5"), Float("6"), Float("7"), Float("8"), Float("9"), Float("10")]

from dataclean.constraint_languages.statistical import Parameteric  ##repair:修改

models = [Parameteric("5")]

from dataclean.search import *

config = DEFAULT_SOLVER_CONFIG

config['dependency']['operations'] = [Delete]

operation, output,_ = solve(df, patterns, models)

print(operation)
print("------------")
print(output)
import matplotlib.pyplot as plt

plt.hist(output["5"].dropna().values)

plt.show()
