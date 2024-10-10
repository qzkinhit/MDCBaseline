import os
import sys
import pandas as pd

# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')

from util.get_error_num import count_inconsistent_entries,generate_change_report

dirty_df = pd.read_csv('dirty_hospitals_null.csv')
clean_df = pd.read_csv('../../clean_index.csv')

num_entry = count_inconsistent_entries(
    dirty_df=dirty_df,
    clean_df=clean_df,
    index_column="index"
)
num_cell = generate_change_report(
    dirty_df=dirty_df,
    clean_df=clean_df,
    index_column="index"
)
print("不一致的条目总数：",num_entry)
print("不一致的单元格总数：",num_cell)

