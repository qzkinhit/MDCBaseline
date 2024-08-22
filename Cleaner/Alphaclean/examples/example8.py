import environ
print("Logs saved in " + environ.logfilename);
data = [{'title': 'Employee 1' , 'salary': 1000.0},
         {'title': 'Employee 2' , 'salary': 100.0},
         {'title': 'Employee 3' , 'salary': 100.0},
         {'title': 'Employee 4' ,'salary': 80.0},
         {'title': 'Manager 1' ,'salary': 500.0},
         {'title': 'Manager 2' ,'salary': 80.0}]

from dataclean.search import solve, DEFAULT_SOLVER_CONFIG
import pandas as pd
df = pd.DataFrame(data)


from dataclean.constraint_languages.ic import DenialConstraint, DCPredicate

#Employee is a manager
predicate1 = DCPredicate(local_attr='title', expression= lambda value, data_frame: 'Manager' in value)

#There exists an employee with a salary greater than the given manager's salary
predicate2 = DCPredicate(local_attr='salary', expression= lambda value, data_frame: \
                                                        data_frame[ (data_frame['salary'] > value) & \
                                                        data_frame['title'].str.contains("Employee", na=False) ].shape[0] > 0)

constraint = DenialConstraint([predicate1, predicate2])


from dataclean.search import solve

dcprogram, output,_ = solve(df, patterns=[] ,dependencies=[constraint])


print(dcprogram)
print("------------")
print(output)




"""""

from dataclean.search import DEFAULT_SOLVER_CONFIG
from dataclean.ops import Delete, Swap

config = DEFAULT_SOLVER_CONFIG
config['dependency']['operations'] = [Delete]

dcprogram2, output2 = solve(df, patterns=[] ,dependencies=[constraint], config=config)

print(dcprogram2, output2)




data = [{'title': 'Employee 1' , 'salary': 100.0}, 
         {'title': 'Employee 2' , 'salary': 100.0},
         {'title': 'Employee 3' , 'salary': 100.0},
         {'title': 'Employee 4' ,'salary': 100.0},
         {'title': 'Employee 5' ,'salary': 80.0},
         {'title': 'Manager 1' ,'salary': 500.0},
         {'title': 'Manager 2' ,'salary': 50.0}]

config = DEFAULT_SOLVER_CONFIG
config['dependency']['operations'] = [Swap, Delete]
config['dependency']['edit'] = 0

df = pd.DataFrame(data)

dcprogram3, output3 = solve(df, patterns=[] ,dependencies=[constraint], config=config)

print(dcprogram3, output3)
"""""