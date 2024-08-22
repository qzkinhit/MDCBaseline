
import pandas as pd
import numpy as np
def celltoalldata():
    # Load the rain fall data
    f = open('clean_unform_data.csv', 'r')
    datafile = f.readlines()

    data = [{str(i): j for i, j in enumerate(l.strip().split(','))} for l in datafile[1:]]
    locations = [{str(i): j for i, j in enumerate(l.strip().split(',')) if i >= 3} for l in datafile[0:2]]
    ##print(data)
    # only put the data into a dataframe
    df = pd.DataFrame(data)
    pd.set_option('display.max_rows',100)
    pd.set_option('display.max_columns',100)
    data=pd.DataFrame(df['2'])
    data=pd.DataFrame(data.unstack())
    data1=pd.DataFrame(data.to_numpy().reshape(int(data.to_numpy().shape[0]/8),8))
    data1.to_csv ("clean_form_data.csv", mode="a" ,index = False, header=False,encoding='gb18030')
    print(data)

    # print(zip(df))
    # print(df.pivot(index='0',columns='1',values='2'))
