import environ
import pandas as pd
from dataclean.constraint_languages.ic import *
from dataclean.constraint_languages.ic import DictValue
from dataclean.constraint_languages.pattern import Float, Pattern
import time
import numpy as np
from dataclean.search import *
import matplotlib.pyplot as plt
# Load the rain fall data
from util.getNum import getErrorNum

df_merge = pd.read_csv('../testdata/bartdata/hospitals/dirty_mix_0.5/dirty_hospitals.csv')
df_clean_merge = pd.read_csv('../testdata/bartdata/hospitals/hospitals_clean.csv')

"""
for x in range(50):
    df_merge = pd.concat([df_merge, df1], axis=0, ignore_index=True)
    df_clean_merge = pd.concat([df_clean_merge,df_clean1],axis=0,ignore_index=True)
df_merge.to_csv('../testdata/hospital_big.csv')
df_clean_merge.to_csv('../testdata/hospital_clean_big.csv')
"""
# 将pandas自动识别成int类型的干净数据，改为字符串型，方便比对
df_clean_merge['providernumber'] = df_clean_merge['providernumber'].astype(str)
df_merge['providernumber'] = df_merge['providernumber'].astype(str)
df_clean_merge['zipcode'] = df_clean_merge['zipcode'].astype(str)
df_merge['zipcode'] = df_merge['zipcode'].astype(str)
df_clean_merge['phonenumber'] = df_clean_merge['phonenumber'].astype(str)
df_merge['phonenumber'] = df_merge['phonenumber'].astype(str)
##print(data)
p=[]
t=[]

df=df_merge.copy(deep=True)
df_clean=df_clean_merge.copy(deep=True)

set = [ "address1", "city", "state", "zipcode","countyname","phonenumber","hospitaltype","hospitalowner","emergencyservice","measurecode","measurename"]
# 计算初始的错误数据个数
error_num0 = getErrorNum(df_merge, df_clean, set)
print(error_num0)


print("Logs saved in " + environ.logfilename);
# df.compare(df_clean).to_csv("clean_form_data.csv", mode="a" ,index = False, header=False,encoding='gb18030')
# 开始定义patterns
# patterns = []
# ##定义正则和字典
# # ProviderNumber以5位数字组成
# patterns += [Pattern('ProviderNumber', "[0-9][0-9][0-9][0-9][0-9]")]
# patterns += [Pattern('Address1', "^[0-9].*")]
# patterns += [Pattern('ZipCode', "[0-9][0-9][0-9][0-9][0-9]")]
# patterns += [Pattern('PhoneNumber', "[0-9]{10}")]
# #patterns += [Pattern('MeasureCode', "^([a-z]+-)([^-]+-[^-]+|[^-]*+")]
# patterns += [Pattern('Stateavg', "^(al_[a-z]+-|ak_[a-z]+-)([^-]+-[^-]+|[^-]+)")]
#patterns += [Pattern('Score', "[1-9][0-9]?%$|100%$|0$%")]
#patterns += [Pattern('Sample', "^[0-9]+ patients")]
# patterns += [DictValue('HospitalType', {'acute care hospitals'})]
# patterns += [DictValue('EmergencyService', {'no', 'yes'})]
# patterns += [DictValue('State', {'ak', 'al'})]
# patterns += [DictValue('Condition', {'pneumonia', 'heart attack', 'surgical infection prevention', 'heart failure',
#                                    'children s asthma care'})]
# patterns += [DictValue('HospitalOwner', {'voluntary non-profit - church', 'government - local', 'government - federal',
#                                        'voluntary non-profit - private', 'voluntary non-profit - other',
#                                        'proprietary', 'government - state',
#                                        'government - hospital district or authority'})]

models = []

##定义字典
# models += [DictValue('hospitaltype', {'acute care hospitals'})]
# models += [DictValue('emergencyservice', {'no', 'yes'})]
#
# models += [DictValue('state', {'ak', 'al'})]
# models += [DictValue('condition', {'pneumonia', 'heart attack', 'surgical infection prevention', 'heart failure',
#                                    'children s asthma care'})]
# models += [DictValue('hospitalowner', {'voluntary non-profit - church', 'government - local', 'government - federal',
#                                        'voluntary non-profit - private', 'voluntary non-profit - other',
#                                        'proprietary', 'government - state',
#                                        'government - hospital district or authority'})]
#
#
#



models.append(OneToOne(["hospitalname"], ["providernumber"]))
models.append(OneToOne(["hospitalname"], ["phonenumber"]))
models.append(OneDeterminedOne(["hospitalname"], ["address1"]))
models.append(OneDeterminedOne(["hospitalname"], ["hospitalowner"]))
models.append(OneDeterminedOne(["hospitalname"], ["city"]))
models.append(OneDeterminedOne(["hospitalname"], ["zipcode"]))
models.append(OneDeterminedOne(["hospitalname", "phonenumber", "hospitalowner"], ["state"]))
models.append(OneDeterminedOne(["condition", "measurename"], ["hospitaltype"]))



config = DEFAULT_SOLVER_CONFIG

# config['pattern']['depth'] = 0
# config['dependency']['operations'] = [Swap]
config['dependency']['depth'] = 1
time_start = time.time()
operation, output  = solve(df, [], models, partitionOn="hospitalname", config=config)





"""
models1 = []
models1.append(OneToOne(["measurecode"], ["measurename"]))

operation, output , _ = solve(output, [], models1, partitionOn="measurecode", config=config)

models2 = []

models2.append(OneDeterminedOne(["city"], ["countyname"]))
operation, output , _ = solve(output, [], models2,  partitionOn="city",config=config)

models3 = []
models3.append(OneDeterminedOne(["zipcode"], ["emergencyservice"]))
operation, output , _ = solve(output, [], models3,  partitionOn="zipcode",config=config)

models4 = []
models4.append(OneToOne(["providernumber"], ["hospitalname"]))
operation, output , _ = solve(output, [], models4,  partitionOn="providernumber",config=config)

"""
# output.to_csv("../testdata/hospital/hospital_repair_mix.csv")



time_end = time.time()


print('time cost', time_end - time_start, 's')


error_num1 = getErrorNum(output, df_clean, set)


t.append(time_end - time_start)



print(operation)
print(error_num1)