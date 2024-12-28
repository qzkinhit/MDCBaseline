import random

import numpy as np
from matplotlib import pyplot as plt

from matplotlib.ticker import FuncFormatter, MaxNLocator
def injected_error_rates(error_injection_rates, datasets, cell_error_rates, entry_error_rates):
    """
    绘制一张图：不同数据集在多种错误独立注入率下的单元格错误率和条目错误率。
    单元格错误率使用虚线，条目错误率使用实线，图例仅区分不同数据集，并显示在图的右边。

    :param error_injection_rates: 注入率列表（X轴）
    :param datasets: 数据集名称列表
    :param cell_error_rates: 各数据集在不同注入率下的单元格错误率（二维列表）
    :param entry_error_rates: 各数据集在不同注入率下的数据条目错误率（二维列表）
    """
    fig, ax1 = plt.subplots(figsize=(18, 10))
    markers = ['o', 's', 'D', '^', 'v', 'P', '*']  # 点形状
    colors = plt.cm.viridis(np.linspace(0, 1, len(datasets)))  # 各数据集的颜色

    # 设置通用字体大小和线宽
    marker_size = 25
    line_width = 5
    label_fontsize = 20
    legend_fontsize = 20

    # 绘制单元格错误率（虚线）
    for i, dataset in enumerate(datasets):
        ax1.plot(error_injection_rates, cell_error_rates[i],
                 marker=markers[i % len(markers)],
                 color=colors[i],
                 linestyle='--',
                 linewidth=line_width,
                 markersize=marker_size,
                 label=dataset)

    # 绘制条目错误率（实线）
    for i, dataset in enumerate(datasets):
        ax1.plot(error_injection_rates, entry_error_rates[i],
                 marker=markers[i % len(markers)],
                 color=colors[i],
                 linestyle='-',
                 linewidth=line_width,
                 markersize=marker_size)

    # 设置轴标签、标题等
    ax1.set_xlabel("Error Injection Rate (%)", fontsize=label_fontsize)
    ax1.set_ylabel("Error Rate (%)", fontsize=label_fontsize)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.tick_params(axis='x', labelsize=16)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 统一比例尺
    max_rate = max(max(max(cell_error_rates)), max(max(entry_error_rates)))
    ax1.set_ylim(0, max_rate * 1.1)
    line_cell = plt.Line2D([0], [0], color='black', linestyle='--', linewidth=3, label='Cell Error Rate (Dashed)')
    line_entry = plt.Line2D([0], [0], color='black', linestyle='-', linewidth=3, label='Entry Error Rate (Solid)')
    handles, labels = ax1.get_legend_handles_labels()
    handles.extend([line_cell, line_entry])
    ax1.legend(handles, datasets + ['Cell Error%', 'Entry Error%'],
               loc="center left", bbox_to_anchor=(1, 0.5), fontsize=legend_fontsize, frameon=True)

    # # 简化图例，只显示不同数据集，并放置在图的右边
    # handles, labels = ax1.get_legend_handles_labels()
    #
    # ax1.legend(handles, datasets, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=legend_fontsize, frameon=True)

    # plt.title("Cell and Entry Error Rates by Injection Rate", fontsize=label_fontsize)
    plt.tight_layout()
    plt.savefig("injected_error_rates.eps", format='eps', bbox_inches='tight')
    plt.show()


# 调用函数生成图表

if __name__ == "__main__":
    # 示例数据
    error_injection_rates_example = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    datasets_example = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer"]

    # 基础单元格错误率和条目错误率（根据表格更新）
    base_cell_error_rates = [
        [0.4368, 0.9263, 1.2737, 1.9158, 2.2211, 2.8000, 3.2000, 3.6526],  # Hospital
        [0.5191, 0.9259, 1.4240, 1.8869, 2.4130, 3.0373, 3.5073, 3.9141],  # Flights
        [0.6805, 0.8672, 1.1079, 1.3485, 1.5062, 1.7676, 1.9502, 2.1743],  # Beers
        [0.4545, 0.6273, 0.7364, 0.9182, 1.0000, 1.1636, 1.8818, 2.0455], # Rayyan
        [0.3160, 0.6304, 0.9395, 1.2520, 1.5679, 1.8634, 2.1738, 2.4672],  # Tax
        [0.4461, 0.8945, 1.3332, 1.7798, 2.2180, 2.6627, 3.0964, 3.5315]   # Soccer
    ]
    base_entry_error_rates = [
        [8.3, 16.2, 22.2, 30.8, 34.1, 41.2, 44.3, 50.9],  # Hospital
        [3.0303, 4.9242, 7.6599, 9.9747, 11.8687, 15.6145, 16.7929, 19.2340],  # Flights
        [6.1826, 7.8838, 9.9585, 12.5311, 13.1120, 15.9751, 16.4315, 17.9253],  # Beers
        [4.9, 6.7, 7.6, 9.1, 10.8, 11.4, 13.9, 14.1],  # Rayyan
        [4.535, 9.1145, 13.2775, 17.095, 20.758, 24.2355, 27.4745, 31.0185],  # Tax
        [4.067, 7.9765, 11.6945, 15.359, 18.737, 22.3265, 25.5915, 28.6235]   # Soccer
    ]

    # Function to process or analyze these rates can go here
    print("Updated error rates:")
    print("Base Cell Error Rates:", base_cell_error_rates)
    print("Base Entry Error Rates:", base_entry_error_rates)
    injected_error_rates(error_injection_rates_example, datasets_example, base_cell_error_rates,
                              base_entry_error_rates)