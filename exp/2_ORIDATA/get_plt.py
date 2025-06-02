import random

import numpy as np
from matplotlib import pyplot as plt



def actual_performance_comparison_with_bars(data_sets, system_names, performance_metrics):
    """
    使用条形图展示系统在各个数据集上的性能对比，每个数据集下用不同纹理的条形表示不同系统。

    每个指标根据其数据范围调整 y 轴，超过范围的值使用 < 和 > 符号表示。

    :param data_sets: 数据集名称列表
    :param system_names: 系统名称列表
    :param performance_metrics: 包含多个指标的性能数据字典，每个键对应一个指标的二维列表
    """
    num_metrics = len(performance_metrics)
    fig, axes = plt.subplots(1, min(num_metrics, 6), figsize=(15, 5), sharex=True)

    # 如果指标超过四个，则需要额外的行
    # if num_metrics > 4:
    #     fig, axes = plt.subplots((num_metrics + 3) // 4, 4, figsize=(20, 5 * ((num_metrics + 3) // 4)), sharex=True)

    axes = axes.flatten()  # 将轴展平便于索引
    hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']  # 系统的填充图案
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']  # 获取默认颜色

    # 定义每个指标的 y 轴范围
    limits = {
        "Clean Time per 100 Records(s)": (None, 50),  # 超过70的值用 >70 表示
        "EDR": (-0.6, None),  # 仅限制下界，小于-0.5的值用 <-0.5 表示
        "REDR": (-0.6, None)  # 仅限制下界，小于-0.5的值用 <-0.5 表示
    }
    expand_ratio = 0  # 用于扩展显示的比例

    for i, (metric_name, performance_data) in enumerate(performance_metrics.items()):
        ax = axes[i]

        # 转置数据，以便每列对应一个系统
        transposed_data = list(zip(*performance_data))
        num_datasets = len(data_sets)
        num_systems = len(system_names)

        bar_width = 0.15  # 每个条形的宽度
        x = np.arange(num_datasets)  # 数据集的 x 位置

        # 根据界限条件裁剪数据
        adjusted_performance = []
        for perf_data in transposed_data:
            if metric_name in limits:
                lower_limit, upper_limit = limits[metric_name]
                adjusted_perf_data = [
                    max(value, lower_limit) if lower_limit is not None else value for value in perf_data
                ]
                adjusted_perf_data = [
                    min(value, upper_limit) if upper_limit is not None else value for value in adjusted_perf_data
                ]
            else:
                adjusted_perf_data = perf_data
            adjusted_performance.append(adjusted_perf_data)

        # 绘制每个系统的条形图
        for j, (system_name, system_data) in enumerate(zip(system_names, adjusted_performance)):
            ax.bar(x + j * bar_width, system_data, width=bar_width, label=system_name,
                   color=colors[j % len(colors)], hatch=hatch_patterns[j % len(hatch_patterns)])

        # 设置子图标题和标签
        ax.set_title(metric_name)
        ax.set_xticks(x + bar_width * (num_systems - 1) / 2)
        ax.set_xticklabels(data_sets, rotation=45)

        if metric_name in limits:
            lower_limit, upper_limit = limits[metric_name]
            # 微调下界和上界，确保条形图紧贴底部
            adjusted_lower_limit = lower_limit if lower_limit is not None and lower_limit < 0 else lower_limit
            # expanded_upper_limit = upper_limit + 0.05 if upper_limit<0 is not None else None
            ax.set_ylim(adjusted_lower_limit, upper_limit)
            yticks = ax.get_yticks()
            # adjusted_lower_limit = lower_limit + 0.01 if lower_limit is not None and lower_limit < 0 else lower_limit
            # ax.set_ylim(adjusted_lower_limit, upper_limit)
            # 使用集合去重，保持顺序不变，并确保 custom_yticks 长度与 yticks 一致
            seen = set()
            custom_yticks = []
            for y in yticks:
                label = (
                    f"<{lower_limit}" if lower_limit is not None and y <= lower_limit else
                    f">{upper_limit}" if upper_limit is not None and y >= upper_limit else
                    (f"{int(y)}" if metric_name == "Clean Time per 100 Records(s)"  else f"{y:.2f}")
                )
                if label not in seen:
                    custom_yticks.append(label)
                    seen.add(label)
                else:
                    # 保持长度一致，填充空字符串以替代重复标签
                    custom_yticks.append("")
                if metric_name == "EDR":
                    print(1111)

            ax.set_yticks(yticks)
            ax.set_yticklabels(custom_yticks)
        # 设置网格线
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 隐藏多余的子图
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # 在图的顶部添加图例
    fig.legend(system_names, loc="upper center", ncol=len(system_names), fontsize=19)
    fig.text(0.5, 0.11,"Datasets", ha='center', fontsize=12)
    fig.text(0.5, 0.08, "* All baseline systems except UniClean unable to handle full 50k Tax dataset in 24 hour."
                        "we evaluated using segmented 10k batch inputs.", ha='center', fontsize=12)

    plt.tight_layout(rect=[0, 0.1, 1, 0.85])  # 调整底部边距
    # fig.text(
    #     0.5,
    #     0.02,
    #     "* Systems except "
    #     + r"$\bf{UniClean}$ and $\bf{Horizon}$ unable to handle full 200k $\bf{Tax}$ and $\bf{Soccer}$ dataset in 24 hour. "
    #       "\n For those baseline systems e evaluated using segmented lower than 10k batch inputs.",
    #     ha="center",
    #     fontsize=15
    # )

    return plt

if __name__ == "__main__":
    data_sets = ["Hospitals", "Flights", "Beers", "Rayyan", "Tax", "Soccer"]
    system_names = ["Uniclean", "Horizon", "Raha-Baran", "HoloClean", "Holistic", "bigDansing"]
    performance_metrics = {
        "F1 Score": [
            [0.8847, 0.5841, 0.5753, 0.6262, 0.6080, 0.6050],  # Hospital
            [0.6537, 0.4049, 0.6278, 0.4763, 0.4067, 0.3870],  # Flights
            [0.8373, 0.1051, 0.7976, 0.0535, 0.0939, 0.0940],  # Beers
            [0.9213, 0.0091, 0.2983, 0.0088, 0.0006, 0.0000],  # Rayyan
            [0.5944, 0.0073, 0.0288, 0.0000, 0.0876, 0.0855],  # Tax
            [0.5341, 0.0728, 0.3276, 0.0000, 0.3772, 0.4122]  # Soccer
        ],
        "Clean Time per 100 Records(s)": [
            [10.8115, 0.3245, 43.1077, 15.0942, 105.3257, 23.2969],  # Hospital
            [3.5603, 1.4109, 19.3508, 1.9327, 231.8536, 2694.6635],  # Flights
            [1.2966, 1.4270, 24.7956, 9.6334, 65.4283, 1.2669],  # Beers
            [5.2378, 2.3133, 27.3773, 10.8541, 2017.268, 83.3452],  # Rayyan
            [0.2525, 11.1435, 38.0591, 12.4377, 574.0920, 103.8026],  # Tax
            [0.343, 0.7025, 23.7848, 2.8439, 100.1337, 505.6491]  # Soccer
        ],
        "EDR": [
            [0.7839, 0.0570, 0.4165, 0.4558, -0.0236, -0.0766],  # Hospital
            [0.5175, 0.1148, 0.4478, 0.3508, -0.1191, -0.1382],  # Flights
            [0.8329, 0.0027, 0.7868, -0.1704, -0.0113, -0.0104],  # Beers
            [0.9005, -0.5196, 0.1757, -1.9204, -2.0654, -1.3667],  # Rayyan
            [0.1005, -87.5904, 0.0181, -0.6687, -1.2640, -1.2427],  # Tax
            [0.3301, -7.0760, 0.2338, 0.0000, -0.1366, -0.0858]  # Soccer
        ],
        "REDR": [
            [0.7543, 0.0270, 0.3612, 0.4324, 0.0442, 0.0221],  # Hospital
            [0.1129, -0.1534, 0.0326, 0.0604, -0.0636, -0.0693],  # Flights
            [0.7730, 0.0000, 0.7224, 0.0000, 0.0000, 0.0000],  # Beers
            [0.8827, -0.1862, 0.1686, -0.2258, -0.1956, -0.1699],  # Rayyan
            [0.5524, -57.1333, 0.0182, -0.6545, -0.0353, -0.0272],  # Tax
            [0.3442, -4.3710, 0.2338, 0.0000, -0.0369, -0.0134]  # Soccer
        ],
        # "Hybrid Distance": [
        #     [0.0521, 0.0974, 0.1304, 0.1523, 0.1157, 0.1239],  # Hospital
        #     [0.0953, 0.1782, 0.1231, 0.2018, 0.1944, 0.1999],  # Flights
        #     [0.0306, 0.0794, 0.0538, 0.0942, 0.0823, 0.0822],  # Beers
        #     [0.0078, 0.0600, 0.0458, 0.1070, 0.0807, 0.0688],  # Rayyan
        #     [0.0031, 0.0943, 0.0012, 0.0057, 0.0120, 0.0145],  # Tax
        #     [0.0354, 0.1295, 0.0071, 0.0135, 0.0504, 0.0509]  # Soccer
        # ]
    }

    plt = actual_performance_comparison_with_bars(data_sets, system_names, performance_metrics)
    # 使用 savefig() 将图表保存为 SVG 格式
    plt.savefig("demoplt.png", format="png",bbox_inches="tight")
    plt.savefig("baseline_comparison.eps", format="eps",bbox_inches="tight")