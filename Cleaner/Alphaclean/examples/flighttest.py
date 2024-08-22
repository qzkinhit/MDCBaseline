"""
Example 2: Flight data.
Run this example with `python examples/flight_ramdon_clean.py` from the `dataclean`
directory.
"""

import environ
import pandas as pd

from dataclean.constraint_languages.ic import OneDeterminedOne
from dataclean.ops import Swap
from dataclean.search import solve, DEFAULT_SOLVER_CONFIG
from util.getNum import getErrorNum, getCorrectRepairs
import time

df_clean = pd.read_csv('../testdata/baddata/flights/flights_clean.csv')
df_dirty = pd.read_csv('../testdata/baddata/flights/dirty_dependencies_0.5/dirty_flights.csv')
df_dirty1 = df_dirty.iloc[:].copy(deep=True)
df_clean1 = df_clean.iloc[:].copy(deep=True)
set = [ "sched_dep_time", "act_dep_time", "sched_arr_time", "act_arr_time"]
# set=["flight"]
error_num0 = getErrorNum(df_dirty1, df_clean1, set)
print(error_num0)

config = DEFAULT_SOLVER_CONFIG
config['dependency']['depth'] = 5
config['pattern']['depth'] = 0
# config['dependency']['similarity'] = {'a': 'jaccard'}
config['dependency']['operations'] = [Swap]

from dataclean.constraint_languages.pattern import Date, Pattern

patterns = [Date("sched_dep_time", "%I:%M %p"),
            Date("act_dep_time", "%I:%M %p"),
            Date("sched_arr_time", "%I:%M %p"),
            Date("act_arr_time", "%I:%M %p")]
time_start = time.time()
dependencies=[OneDeterminedOne(["flight"], [str(i)]) for i in ["sched_dep_time", "act_dep_time", "sched_arr_time", "act_arr_time"]]


operation, output,_ = solve(df_dirty1, patterns, dependencies,partitionOn="flight",config=config)
time_end= time.time()

total_repair = getErrorNum(output,df_dirty,set)
now_error = getErrorNum(output, df_clean1, set)
total_error = getErrorNum( df_dirty, df_clean1, set)
correct_repairs =  getCorrectRepairs(df_clean1,output,df_dirty,set)

precision = correct_repairs / total_repair
recall = correct_repairs / total_error

print(operation, output)
print("total_repair",total_repair)
print("correct_repair",correct_repairs)
print("now_error",now_error)
print("total_error",total_error)

print("precision",precision)
print("recall",recall)
t = time_end - time_start
print("time:", t)
output.to_csv('../testdata/flight/flights_repair0.csv')