import matplotlib.pyplot as plt
import numpy as np

# 第一张图数据
data_sizes = [1, 5, 20, 200]  # 数据规模 n(k)
recall_abnormal = [0.72, 0.6, 0.5, 0.45]  # 异常值错误的召回率 F1
recall_missing = [0.94, 0.93, 0.91, 0.88]  # 空缺值错误的召回率 F1
recall_violation = [0.99, 0.99, 0.85, 0.80]  # 规则违反错误的召回率 F1
recall_mixed = [0.91, 0.87, 0.88, 0.8]  # 混合错误的召回率 F1
# 第二张图数据
data_sizes_2 = [1, 5, 20, 200]  # 数据规模 n(k)
time_abnormal = [3.0,13, 35, 200]  # 异常值错误的时间 t (min)
time_missing = [2.8, 10, 30, 180]  # 空缺值错误的时间 t (min)
time_violation = [3, 16, 40, 240]  # 规则违反错误的时间 t (min)
time_mixed = [2.5, 12, 35, 216]  # 混合错误的时间 t (min)

# 第三张图数据
error_types = ['Abnormal Value', 'Missing Value', 'Rule Violation', 'Mixed Error']
recall_this_system = [0.6, 0.91, 0.89, 0.87]  # 本系统的召回率 F1
recall_holoclean = [0.77, 0.95, 0.69, 0.76]  # Holoclean系统的召回率 F1

# 第四张图数据
error_types_2 = ['Abnormal Value', 'Missing Value', 'Rule Violation', 'Mixed Error']
time_this_system = [600, 160, 180, 157]  # 本系统的时间 t (s)
time_holoclean = [125, 103, 105, 120]  # Holoclean系统的时间 t (s)

# 创建一个包含四个子图的大图
fig, axs = plt.subplots(1, 3, figsize=(20, 6))

# 绘制第一张图
axs[0].plot(data_sizes, recall_abnormal, marker='o', label='Abnormal Value')
axs[0].plot(data_sizes, recall_missing, marker='o', label='Missing Value')
axs[0].plot(data_sizes, recall_violation, marker='o', label='Rule Violation')
axs[0].plot(data_sizes, recall_mixed, marker='o', label='Mixed Error')

axs[0].set_xlabel('Data Size (k)')
axs[0].set_ylabel('F1指标')
axs[0].set_title('(a) 在不同清洗任务下的F1指标',y=-0.15)
axs[0].legend()
axs[0].grid(True)

# 绘制第二张图
axs[1].plot(data_sizes_2, time_abnormal, marker='o', label='Abnormal Value')
axs[1].plot(data_sizes_2, time_missing, marker='o', label='Missing Value')
axs[1].plot(data_sizes_2, time_violation, marker='o', label='Rule Violation')
axs[1].plot(data_sizes_2, time_mixed, marker='o', label='Mixed Error')

axs[1].set_xlabel('Data Size (k)')
axs[1].set_ylabel('时间(min)')
axs[1].set_title('(b) 在不同清洗任务下的运行时间',y=-0.15)
axs[1].legend()
axs[1].grid(True)

# 绘制第三张图
x = np.arange(len(error_types))
width = 0.35

axs[2].bar(x - width / 2, recall_this_system, width, label='Our System')
axs[2].bar(x + width / 2, recall_holoclean, width, label='Holoclean System')

axs[2].set_xlabel('清洗任务')
axs[2].set_ylabel('F1指标')
axs[2].set_title('(c) 与Holoclean的性能对比',y=-0.15)
axs[2].set_xticks(x)
axs[2].set_xticklabels(error_types)
axs[2].legend()
axs[2].grid(True)

# # 绘制第四张图
# x = np.arange(len(error_types_2))
# width = 0.35
#
# axs[1, 1].bar(x - width / 2, time_this_system, width, label='This System')
# axs[1, 1].bar(x + width / 2, time_holoclean, width, label='Holoclean System')
#
# axs[1, 1].set_xlabel('Error Type')
# axs[1, 1].set_ylabel('Time (s)')
# axs[1, 1].set_title('Performance of Data Cleaning Systems (Time)')
# axs[1, 1].set_xticks(x)
# axs[1, 1].set_xticklabels(error_types_2)
# axs[1, 1].legend()
# axs[1, 1].grid(True)

# 调整子图之间的间距
plt.tight_layout()
# plt.figure(figsize=(20, 20), dpi=600)
# 显示图形
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.savefig('output1.svg', format='svg',dpi=600)
plt.show()