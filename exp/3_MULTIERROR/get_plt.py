import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from collections import defaultdict

def plot_metrics_with_limits(error_rates, data_sets, systems, metrics, performance_data):
    """
    为每个指标绘制一张2x3的图表，表示六个数据集在该指标下的性能，并根据指标限制值优化显示。

    :param error_rates: 错误注入率列表 (例如 [0.25, 0.5, 0.75, 1, ...])。
    :param data_sets: 数据集名称列表 (例如 ["Hospital", "Flights", ...])。
    :param systems: 系统名称列表 (例如 ["Uniclean", "Horizon", ...])。
    :param metrics: 指标名称列表 (例如 ["F1 Score", "EDR", "REDR", "Time per 100 Records(s)"])。
    :param performance_data: 字典形式的性能数据，键为指标名称，
                             值为3D列表，形状为 (len(metrics), len(data_sets), len(systems), len(error_rates))。
    """
    name = {
        "F1 Score": "f1_performance.eps",
        "EDR": "edr_performance.eps",
        "R-EDR": "redr_performance.eps",
        "Time per 100 Records(s)": "time_performance.eps"
    }
    # 指标的限制条件
    limits = {
        "Time per 100 Records(s)": {"upper": 70,"upperSYS":True},      # Time per 100 Records(s)只限制上界
        "EDR": {"lower": -1.5, "upper": 1, "upperSYS":False},  # EDR限制下界为-1.5，上界为1.0
        "R-EDR": {"lower": -1.5,"upper": 1,"upperSYS":False}  # REDR限制下界为-1.5，上界为1.0
    }
    expand_ratio = 0.1  # 用于扩展显示范围的比例

    markers = ['o', 's', 'D', '^', 'v', 'P', '*']  # 用于区分系统的点形状
    colors = plt.cm.tab10(np.arange(len(systems)))  # 为不同系统分配颜色

    for metric in metrics:  # 遍历每个指标
        # 创建一个2x3的子图布局
        fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True, sharey=True)
        axes = axes.flatten()

        for i, data_set in enumerate(data_sets):  # 遍历每个数据集
            ax = axes[i]
            for j, system in enumerate(systems):  # 遍历每个系统
                # 提取原始性能数据
                original_data = performance_data[metric][i][j]

                # 根据限制条件调整数据
                if metric in limits:
                    lower_limit = limits[metric].get("lower", float("-inf"))  # 默认无下界
                    upper_limit = limits[metric].get("upper", float("inf"))  # 默认无上界
                    adjusted_data = [
                        max(min(value, upper_limit), lower_limit) for value in original_data
                    ]
                else:
                    adjusted_data = original_data

                # 绘制曲线
                ax.plot(
                    error_rates,
                    adjusted_data,
                    label=system,
                    marker=markers[j % len(markers)],
                    color=colors[j],
                    linestyle='-',
                    linewidth=3,
                    markersize=12
                )

            # 设置子图标题为对应的数据集名称
            ax.set_title(data_set, fontsize=14)
            # 设置X轴标签
            if i >= 3:  # 最后一行显示X轴标签
                ax.set_xlabel("Error Rate (%)", fontsize=12)
            # 设置Y轴标签
            if i % 3 == 0:  # 第一列显示Y轴标签
                ax.set_ylabel(metric, fontsize=12)
            # 添加网格线
            ax.grid(True, linestyle='--', alpha=0.6)

            # 设置y轴范围和自定义刻度标签
            if metric in limits:
                lower_limit = limits[metric].get("lower", float("-inf"))
                upper_limit = limits[metric].get("upper", float("inf"))
                expanded_lower_limit = lower_limit - abs(upper_limit * expand_ratio)if lower_limit > float("-inf") else None
                expanded_upper_limit = upper_limit + abs(upper_limit * expand_ratio) if upper_limit < float("inf") else None
                ax.set_ylim(expanded_lower_limit, expanded_upper_limit)

                yticks = ax.get_yticks()
                # custom_yticks = [
                #     f">{upper_limit}" if y >= upper_limit else y for y in yticks
                # ] if "upper" in limits[metric] and "lower" not in limits[metric] else yticks
                custom_yticks = [
                    f"<{lower_limit}" if "lower" in limits[metric] and y <= lower_limit else
                    (f">{upper_limit}" if "upperSYS" in limits[metric] and limits[metric][
                        "upperSYS"] and y >= upper_limit else upper_limit)
                    if "upper" in limits[metric] and y >= upper_limit else
                    y for y in yticks
                ]

                ax.set_yticklabels(custom_yticks)

        # 隐藏多余的子图框
        for ax in axes[len(data_sets):]:
            ax.axis('off')

        fig.legend(
            handles=[
                plt.Line2D([0], [0], marker=markers[k], color=colors[k], label=system, linestyle='None', markersize=12)
                for k, system in enumerate(systems)
            ],
            loc='upper center',
            ncol=len(systems),
            fontsize=20,  # 控制标签文字大小
        )

        # 调整布局，避免重叠
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 调整底部边距
        fig.text(
            0.5,
            0.02,
            "* Systems except "
            + r"$\bf{UniClean}$ and $\bf{Horizon}$ unable to handle full 200k $\bf{Tax}$ and $\bf{Soccer}$ dataset in 24 hour. "
              "\n For those baseline systems e evaluated using segmented lower than 10k batch inputs.",
            ha="center",
            fontsize=15
        )
        plt.savefig(metric+'.png', format="png")
        # plt.show()
        plt.savefig(name[metric], format="eps")

# 测试用例
if __name__ == "__main__":
    # 数据集名称
    data_sets = ["Hospital", "Flights", "Beers", "Rayyan", "Tax", "Soccer"]
    # 系统名称
    systems = ["Uniclean", "Horizon", "Raha-Baran", "HoloClean", "BigDansing", "Holistic"]
    # 错误注入率
    error_rates = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
    # 指标名称
    metrics = ["F1 Score", "EDR", "R-EDR", "Time per 100 Records(s)"]


    def convert_to_performance_data(csv_path):
        # 读取 CSV 文件
        df = pd.read_csv(csv_path, header=None)

        # 初始化存储数据
        performance_data = defaultdict(list)
        current_dataset = None
        current_system = None
        metric_map = {"F1 Score": 0, "EDR": 1, "Hybrid Distance": 2, "R-EDR": 3, "Time per 100 Records(s)": 4}
        datasets_order = []
        system_order = []

        # 遍历行
        for index, row in df.iterrows():
            if not pd.isna(row[0]) and pd.isna(row[1]):  # 数据集名称
                current_dataset = row[0].strip()
                datasets_order.append(current_dataset)
                performance_data[current_dataset] = [[] for _ in metric_map]
                system_order = []
            elif not pd.isna(row[0]) and not pd.isna(row[1]):  # 系统名称和指标
                current_system = row[0].strip()
                metric = row[1].strip()
                values = [float(v) for v in row[2:].dropna().tolist()]

                if metric in metric_map:
                    if current_system not in system_order:
                        for i in range(len(performance_data[current_dataset])):
                            performance_data[current_dataset][i].append([])
                        system_order.append(current_system)
                    # 将指标数据添加到对应的位置
                    performance_data[current_dataset][metric_map[metric]][-1] = values

        # 转换为字典格式
        final_data = {metric: [] for metric in metric_map}
        for dataset in datasets_order:
            for metric, index in metric_map.items():
                final_data[metric].append(performance_data[dataset][index])

        return final_data


    # 将 CSV 路径替换为你的实际路径
    csv_path = 'error_total.csv'
    performance_data = convert_to_performance_data(csv_path)

    # 输出结构化数据
    print(performance_data)
    # 调用绘图函数
    plot_metrics_with_limits(error_rates, data_sets, systems, metrics, performance_data)
