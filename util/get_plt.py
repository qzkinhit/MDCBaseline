import random

import numpy as np
from matplotlib import pyplot as plt


def single_system_performance_with_bar(data_sets, metrics, performance_data):
    """
    为单一系统在多个数据集上的不同指标绘制条形图，其中 "S" 表示清洗速度，单位为秒。

    :param data_sets: 数据集名称列表
    :param metrics: 指标名称列表
    :param performance_data: 指标数据的字典，每个键是指标名称，每个值是数据集的性能列表
    """
    num_datasets = len(data_sets)
    num_metrics = len(metrics)
    x = np.arange(num_datasets)  # 数据集位置
    colors = plt.cm.viridis(np.linspace(0, 1, num_datasets))  # 各数据集的颜色
    fig, axes = plt.subplots(1, num_metrics, figsize=(20, 5))

    for i, metric in enumerate(metrics):
        ax = axes[i]
        metric_data = performance_data[metric]

        # 绘制单系统的性能条形图
        ax.bar(x, metric_data, color=colors[i], width=0.5, label=metric)

        # 设置子图标题和标签
        ax.set_title(metric)
        ax.set_xticks(x)
        ax.set_xticklabels(data_sets, rotation=45)
        # 设置纵轴范围以符合每个指标的值范围
        if metric in ["F1", "EDR", "REDR"]:
            ax.set_ylim(0, 1)  # 假设这些指标范围在 0 到 1 之间
        elif metric == "S":  # 清洗速度指标
            ax.set_ylabel("Speed (seconds per 100 records)")
            ax.set_ylim(0, max(metric_data) * 1.1)  # 清洗速度范围动态调整
        elif metric == "Hybrid Distance":
            ax.set_ylim(0, max(metric_data) * 1.1)  # 为 Hybrid Distance 设置自适应范围

        ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.suptitle("Single System Performance Across Datasets for Various Metrics (Including Cleaning Speed)")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()



def performance_difference_with_bar(data_sets, metrics, baseline_performance, alternative_performance):
    """
    绘制系统性能差异图，显示不同数据集上贪心选择与基准系统之间的性能差异百分比，每个数据集的条形颜色不同。
    纵轴限制在50-150%区间，便于突出差异细节。

    :param data_sets: 数据集名称列表
    :param metrics: 指标名称列表
    :param baseline_performance: 基准系统的性能数据，每个键是指标名称，每个值是基准性能列表
    :param alternative_performance: 贪心选择系统的性能数据，每个键是指标名称，每个值是贪心选择的性能列表
    """
    num_datasets = len(data_sets)
    num_metrics = len(metrics)
    x = np.arange(num_datasets)  # 数据集位置
    colors = plt.cm.viridis(np.linspace(0, 1, num_datasets))  # 各数据集的颜色

    fig, axes = plt.subplots(1, num_metrics, figsize=(20, 5), sharey=True)

    for i, metric in enumerate(metrics):
        ax = axes[i]
        baseline = baseline_performance[metric]
        alternative = alternative_performance[metric]

        # 计算性能差异百分比
        percentage_difference = [(alt / base) * 100 for alt, base in zip(alternative, baseline)]

        # 绘制性能差异条形图
        for j in range(num_datasets):
            ax.bar(x[j], percentage_difference[j], color=colors[j], width=0.5, label=data_sets[j] if i == 0 else "")

        # 设置子图标题和标签
        ax.set_title(metric)
        ax.set_xticks(x)
        ax.set_xticklabels(data_sets, rotation=45)
        ax.set_ylim(50, 150)  # 将y轴限制在50-150%范围内
        ax.set_ylabel("Difference (%)")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 统一图例
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles[:num_datasets], labels[:num_datasets], loc="upper center", ncol=num_datasets,
               bbox_to_anchor=(0.5, 1.15))
    fig.suptitle("Performance Difference Across Datasets: Greedy vs. Baseline System")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def add_random_fluctuations(base_values, fluctuation_range=0.5):
    """
    为给定的基础值添加随机波动。

    :param base_values: 基础值列表
    :param fluctuation_range: 波动范围
    :return: 添加波动后的值列表
    """
    return [value + random.uniform(-fluctuation_range, fluctuation_range) * value for value in base_values]


def injected_error_rates(error_injection_rates, datasets, cell_error_rates, entry_error_rates):
    """
    绘制两张图：一张表示不同数据集在多种错误独立注入率下的单元格错误率，另一张表示数据条目错误率。

    :param error_injection_rates: 注入率列表（X轴）
    :param datasets: 数据集名称列表
    :param cell_error_rates: 各数据集在不同注入率下的单元格错误率（二维列表）
    :param entry_error_rates: 各数据集在不同注入率下的数据条目错误率（二维列表）
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    markers = ['o', 's', 'D', '^', 'v', 'P', '*']  # 点形状
    colors = plt.cm.viridis(np.linspace(0, 1, len(datasets)))  # 各数据集的颜色

    # 第一张图：单元格错误率
    ax1 = axes[0]
    for i, dataset in enumerate(datasets):
        ax1.plot(error_injection_rates, cell_error_rates[i], marker=markers[i % len(markers)],
                 color=colors[i], label=dataset, linestyle='-', markersize=6)
    ax1.set_title("Cell Error Rate by Injection Rate")
    ax1.set_xlabel("Error Injection Rate (%)")
    ax1.set_ylabel("Cell Error Rate (%)")
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 第二张图：条目错误率
    ax2 = axes[1]
    for i, dataset in enumerate(datasets):
        ax2.plot(error_injection_rates, entry_error_rates[i], marker=markers[i % len(markers)],
                 color=colors[i], label=dataset, linestyle='-', markersize=6)
    ax2.set_title("Entry Error Rate by Injection Rate")
    ax2.set_xlabel("Error Injection Rate (%)")
    ax2.set_ylabel("Entry Error Rate (%)")
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加统一图例
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=len(datasets), bbox_to_anchor=(0.5, 1.15))
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def baseline_performance_difference_with_line(data_sets, system_names, performance_metrics, baseline_index=0):
    """
    在同一图表中展示五个指标下的系统性能折线图，并在顶部统一显示图例。

    :param data_sets: 数据集名称列表
    :param system_names: 系统名称列表
    :param performance_metrics: 包含五个指标的性能数据字典，每个键对应一个指标的二维列表
    :param baseline_index: 基准系统的索引，默认为第一个系统
    """
    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    axes = axes.flatten()  # 将轴展平便于索引
    markers = ['o', 's', 'D', '^', 'v', 'P', '*']  # 用于区分不同系统的点形状

    for i, (metric_name, performance_data) in enumerate(performance_metrics.items()):
        ax = axes[i]

        # 计算相对性能百分比
        baseline_performance = performance_data[baseline_index]
        relative_performance = [
            [perf / base * 100 for perf, base in zip(system_perf, baseline_performance)]
            for system_perf in performance_data
        ]

        # 绘制每个系统的性能折线图
        for j, (system_name, rel_perf) in enumerate(zip(system_names, relative_performance)):
            ax.plot(np.arange(len(data_sets)), rel_perf, marker=markers[j % len(markers)], label=system_name,
                    linestyle='-', markersize=6)

        # 设置子图标题和标签
        ax.set_title(metric_name)
        ax.set_xticks(np.arange(len(data_sets)))
        ax.set_xticklabels(data_sets, rotation=45)
        ax.set_ylim(70, 105)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 在主图下方添加统一图例
    legend_elements = [
        plt.Line2D([0], [0], marker=markers[i], color='black', label=system_name, markersize=8, linestyle='None')
        for i, system_name in enumerate(system_names)]
    fig.legend(handles=legend_elements, loc="upper center", ncol=len(system_names))

    # 把标题放在最底下
    fig.text(0.5, -0.1, "Performance Comparison Across Systems for Different Metrics (Relative to Baseline)",
             ha='center', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 调整布局以适应标题和图例
    plt.show()



if __name__ == "__main__":
    # 重新定义示例数据
    data_sets_example = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer", "Commercial"]
    metrics_example = ["F1", "S", "EDR", "REDR", "Hybrid Distance"]
    performance_data_example = {
        "F1": [0.86, 0.91, 0.89, 0.88, 0.90, 0.86, 0.87],
        "S": [1.5, 1.8, 2.0, 1.7, 1.9, 1.6, 1.4],  # 清洗速度指标，单位为每百条数据的秒数
        "EDR": [0.88, 0.93, 0.91, 0.90, 0.92, 0.88, 0.89],
        "REDR": [0.89, 0.94, 0.92, 0.91, 0.93, 0.89, 0.90],
        "Hybrid Distance": [0.15, 0.13, 0.17, 0.14, 0.16, 0.15, 0.14]
    }

    # 调用函数生成条形图，每个数据集使用不同颜色
    single_system_performance_with_bar(data_sets_example, metrics_example, performance_data_example)
    # 示例数据
    data_sets_example = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer"]
    metrics_example = ["F1/F0", "S/S0", "EDR/EDR0", "REDR/REDR0", "HD/HD0"]
    baseline_performance_example = {
        "F1/F0": [0.90, 0.92, 0.91, 0.93, 0.89, 0.91],
        "S/S0": [1.2, 1.4, 1.5, 1.3, 1.2, 1.4],
        "EDR/EDR0": [0.88, 0.90, 0.89, 0.91, 0.87, 0.89],
        "REDR/REDR0": [0.87, 0.89, 0.88, 0.90, 0.86, 0.88],
        "HD/HD0": [0.15, 0.14, 0.16, 0.15, 0.13, 0.14]
    }
    alternative_performance_example = {
        "F1/F0": [0.85, 0.88, 0.86, 0.89, 0.84, 0.87],
        "S/S0": [1.3, 1.6, 1.7, 1.4, 1.3, 1.5],
        "EDR/EDR0": [0.82, 0.85, 0.84, 0.87, 0.81, 0.83],
        "REDR/REDR0": [0.80, 0.83, 0.82, 0.85, 0.79, 0.81],
        "HD/HD0": [0.18, 0.16, 0.19, 0.17, 0.15, 0.16]
    }

    # 调用函数绘制带有不同颜色条形的图表
    performance_difference_with_bar(data_sets_example, metrics_example, baseline_performance_example,
                                        alternative_performance_example)
    # 示例数据
    error_injection_rates_example = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    datasets_example = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer"]

    # 基础单元格错误率和条目错误率
    base_cell_error_rates = [
        [2, 4, 6, 8, 10, 12, 14, 16],
        [1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12],
        [2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [2.2, 4.4, 6.6, 8.8, 11, 13.2, 15.4, 17.6],
        [1.8, 3.6, 5.4, 7.2, 9, 10.8, 12.6, 14.4]
    ]
    base_entry_error_rates = [
        [5, 10, 15, 20, 25, 30, 35, 40],
        [4, 8, 12, 16, 20, 24, 28, 32],
        [6, 12, 18, 24, 30, 36, 42, 48],
        [3, 6, 9, 12, 15, 18, 21, 24],
        [5.5, 11, 16.5, 22, 27.5, 33, 38.5, 44],
        [4.5, 9, 13.5, 18, 22.5, 27, 31.5, 36]
    ]

    # 为每个数据集的基础错误率添加波动
    cell_error_rates_example = [add_random_fluctuations(base) for base in base_cell_error_rates]
    entry_error_rates_example = [add_random_fluctuations(base) for base in base_entry_error_rates]

    # 绘制图表
    injected_error_rates(error_injection_rates_example, datasets_example, cell_error_rates_example,
                              entry_error_rates_example)
    # 模拟输入数据
    data_sets_example = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer", "Commercial"]
    system_names_example = ["My System", "Baran", "Holistic", "bigDansing", "Horizon", "Holoclean"]
    performance_metrics_example = {
        "F1 Score": [
            [0.95, 0.97, 0.93, 0.92, 0.96, 0.94, 0.95],
            [0.76, 0.83, 0.84, 0.81, 0.80, 0.78, 0.80],
            [0.72, 0.76, 0.78, 0.74, 0.73, 0.71, 0.72],
            [0.82, 0.86, 0.89, 0.90, 0.84, 0.85, 0.86],
            [0.89, 0.92, 0.91, 0.93, 0.90, 0.91, 0.92],
            [0.74, 0.79, 0.81, 0.78, 0.76, 0.79, 0.77]
        ],
        "T": [
            [0.93, 0.94, 0.91, 0.89, 0.92, 0.90, 0.93],
            [0.73, 0.81, 0.82, 0.78, 0.76, 0.74, 0.77],
            [0.71, 0.74, 0.75, 0.72, 0.70, 0.69, 0.71],
            [0.83, 0.85, 0.88, 0.87, 0.82, 0.83, 0.84],
            [0.87, 0.90, 0.89, 0.91, 0.88, 0.89, 0.90],
            [0.70, 0.78, 0.80, 0.76, 0.75, 0.76, 0.75]
        ],
        "EDR": [
            [0.92, 0.93, 0.90, 0.88, 0.91, 0.89, 0.92],
            [0.75, 0.82, 0.83, 0.79, 0.78, 0.76, 0.78],
            [0.72, 0.75, 0.76, 0.73, 0.71, 0.70, 0.72],
            [0.84, 0.87, 0.88, 0.86, 0.83, 0.84, 0.85],
            [0.88, 0.90, 0.90, 0.92, 0.89, 0.90, 0.91],
            [0.72, 0.79, 0.80, 0.77, 0.75, 0.77, 0.76]
        ],
        "REDR": [
            [0.94, 0.95, 0.91, 0.90, 0.93, 0.92, 0.94],
            [0.74, 0.82, 0.83, 0.80, 0.78, 0.77, 0.79],
            [0.73, 0.76, 0.78, 0.74, 0.72, 0.71, 0.73],
            [0.85, 0.88, 0.89, 0.88, 0.85, 0.86, 0.87],
            [0.89, 0.92, 0.90, 0.94, 0.90, 0.91, 0.92],
            [0.75, 0.80, 0.82, 0.79, 0.76, 0.78, 0.77]
        ],
        "Hybrid Distance": [
            [0.91, 0.92, 0.89, 0.87, 0.90, 0.88, 0.91],
            [0.72, 0.80, 0.82, 0.78, 0.77, 0.75, 0.76],
            [0.71, 0.74, 0.75, 0.71, 0.70, 0.69, 0.71],
            [0.83, 0.86, 0.87, 0.85, 0.82, 0.83, 0.84],
            [0.86, 0.91, 0.89, 0.90, 0.87, 0.88, 0.89],
            [0.70, 0.78, 0.79, 0.76, 0.74, 0.75, 0.74]
        ]
    }
    # 调用 plot_baseline_performance_combined 生成组合图
    baseline_performance_difference_with_line(data_sets_example, system_names_example, performance_metrics_example)