import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
def plot_metrics_3x1(error_rates, data_sets, systems, metrics, performance_data):
    """
    在一张图中以 2×2 的方式排列四个指标的子图；
    每个指标的子图仍然是 2×3 布局，用来展示六个数据集在该指标下的性能。
    相较之前的版本，图表布局更紧凑以节省空间。

    :param error_rates: 错误注入率列表 (例如 [0.25, 0.5, 0.75, 1, ...])。
    :param data_sets: 数据集名称列表 (例如 ["Hospital", "Flights", ...])。
    :param systems: 系统名称列表 (例如 ["Uniclean", "Horizon", ...])。
    :param metrics: 指标名称列表 (例如 ["F1 Score", "EDR", "R-EDR", "CTR"])。
    :param performance_data: 字典形式的性能数据，键为指标名称，
                             值为 3D 列表，形状为 (len(data_sets), len(systems), len(error_rates))。
                             即 performance_data[metric][i][j] 给出第 i 个数据集、第 j 个系统
                             随错误率变化的性能曲线。
    """
    # 如果您希望输出的文件名和指标对应，可以自定义如下映射
    name_map = {
        "F1 Score": "f1_performance.eps",
        "EDR":      "edr_performance.eps",
        # "R-EDR":    "redr_performance.eps",
        "Hybrid Distance":      "hd_performance.eps"
    }

    # 设定针对各指标的显示上下限（如果有）
    limits = {
        "CTR":   {"upper": 40, "upperSYS": True},        # Time per 100 Records(s) 只限制上界
        "EDR":   {"lower": -1.5, "upper": 1, "upperSYS": False},
        "R-EDR": {"lower": -1.5, "upper": 1, "upperSYS": False}
    }

    # 适当扩展显示范围的比例
    expand_ratio = 0.1

    # 不同系统用不同的 marker 和颜色
    markers = ['o', 'X', 'D', '^', 'v', 'P', '*']
    colors = plt.cm.tab10(np.arange(len(systems)))

    # ======================
    #   创建外层 2×2 网格
    # ======================
    # figure 比较紧凑，适当减小
    fig = plt.figure(figsize=(30, 10))
    # 调整 wspace / hspace 尝试让外层间隔更小
    outer_grid = gridspec.GridSpec(
        1, 3,
        wspace=0.15,
        hspace=0.2
    )

    # 依次处理 4 个指标
    for metric_idx, metric in enumerate(metrics):
        # row = metric_idx // 2
        # col = metric_idx % 2
        row=0
        col=metric_idx
        # 在 2×2 网格中拿到当前指标所在的 subplotSpec
        inner_grid = gridspec.GridSpecFromSubplotSpec(
            2, 3,
            subplot_spec=outer_grid[row, col],
            wspace=0.15,  # 让子图之间横向间隔小一些
            hspace=0.25   # 让子图之间纵向间隔小一些
        )

        for i, data_set in enumerate(data_sets):
            # 将第 i 个数据集放到 2×3 子网格中
            ax = plt.subplot(inner_grid[i])

            for j, system in enumerate(systems):
                # 提取原始性能数据 (1D 列表: error_rates -> 性能值)
                original_data = performance_data[metric][i][j]

                # 根据限制条件调整数据
                if metric in limits:
                    lower_limit = limits[metric].get("lower", float("-inf"))
                    upper_limit = limits[metric].get("upper", float("inf"))
                    adjusted_data = [
                        max(min(value, upper_limit), lower_limit)
                        for value in original_data
                    ]
                else:
                    adjusted_data = original_data

                # 绘制曲线
                # 将线条宽度、marker 大小都适当减小
                ax.plot(
                    error_rates,
                    adjusted_data,
                    label=system,
                    marker=markers[j % len(markers)],
                    color=colors[j],
                    linestyle='-',
                    linewidth=5,   # 线条
                    markersize=16   # marker
                )

            # 设置子图标题为对应的数据集名称
            ax.set_title(data_set, fontsize=30)
            # ax.tick_params(axis='y', labelsize=30)
            # 只在最下面那行显示 X 轴标签
            # if i >= 3:
                # ax.set_xlabel("Error Rate (%)", fontsize=25)
            if i % 6 == 4:
                ax.set_xlabel("Error Rate (%) \n"+metric, fontsize=30,fontweight='bold')
                if metric=="CTR":
                    ax.set_xlabel("Error Rate (%) \n" + metric+"(s)", fontsize=30, fontweight='bold')
            # 只在第一列显示 Y 轴标签
            if i % 3 == 0:
                # ax.set_ylabel(metric, fontsize=30)
                ax.tick_params(axis='y', labelsize=20)  # 调整 Y 轴刻度字体大小
            # 只为最左侧的子图显示 Y 轴标签和刻度
            else:
                # 隐藏中间和右边子图的 Y 轴刻度和标签
                ax.tick_params(axis='y', which='both', left=False, labelleft=False)

            ax.grid(True, linestyle='--', alpha=0.6)

            # 处理 y 轴范围
            if metric in limits:
                lower_limit = limits[metric].get("lower", float("-inf"))
                upper_limit = limits[metric].get("upper", float("inf"))

                # 根据 expand_ratio 做适当扩展
                if lower_limit > float("-inf"):
                    expanded_lower = lower_limit - abs(lower_limit) * expand_ratio
                else:
                    expanded_lower = None

                if upper_limit < float("inf"):
                    expanded_upper = upper_limit + abs(upper_limit) * expand_ratio
                else:
                    expanded_upper = None

                ax.set_ylim(expanded_lower, expanded_upper)

                # 若需自定义刻度，可在这里进一步处理
                yticks = ax.get_yticks()
                custom_yticks = []
                for y in yticks:
                    # 如果有下界且当前刻度小于等于下界
                    if "lower" in limits[metric] and y <= lower_limit:
                        custom_yticks.append(f"<{lower_limit}")
                    # 如果有上界且需要显示为 >上界
                    elif ("upperSYS" in limits[metric] and limits[metric]["upperSYS"]
                          and "upper" in limits[metric] and y >= upper_limit):
                        custom_yticks.append(f">{upper_limit}")
                    else:
                        custom_yticks.append(round(y, 2))  # 保留两位小数
                ax.set_yticklabels(custom_yticks)

    # =================
    #   添加全局图例
    # =================
    # 为了让整个图更紧凑，可以把图例放在整张图的底部或顶部，
    # 这里演示放顶部，并调小间距
    handles = [
        plt.Line2D([0], [0],
                   marker=markers[k],
                   color=colors[k],
                   label=sys_name,
                   linestyle='None',
                   markersize=25)  # 图例也稍微紧凑
        for k, sys_name in enumerate(systems)
    ]
    fig.legend(
        handles=handles,
        loc='upper center',
        ncol=len(systems),
        fontsize=30,
        bbox_to_anchor=(0.5, 1.02)
    )
    # 也可以统一只输出一个大图文件：
    plt.savefig("all_metrics_1*3.eps", format="eps",bbox_inches='tight')
    plt.savefig("all_metrics_1*3.png", dpi=300, format="png",bbox_inches='tight')
    plt.show()
def plot_metrics_4x1(error_rates, data_sets, systems, metrics, performance_data):
    """
    在一张图中以 2×2 的方式排列四个指标的子图；
    每个指标的子图仍然是 2×3 布局，用来展示六个数据集在该指标下的性能。
    相较之前的版本，图表布局更紧凑以节省空间。

    :param error_rates: 错误注入率列表 (例如 [0.25, 0.5, 0.75, 1, ...])。
    :param data_sets: 数据集名称列表 (例如 ["Hospital", "Flights", ...])。
    :param systems: 系统名称列表 (例如 ["Uniclean", "Horizon", ...])。
    :param metrics: 指标名称列表 (例如 ["F1 Score", "EDR", "R-EDR", "CTR"])。
    :param performance_data: 字典形式的性能数据，键为指标名称，
                             值为 3D 列表，形状为 (len(data_sets), len(systems), len(error_rates))。
                             即 performance_data[metric][i][j] 给出第 i 个数据集、第 j 个系统
                             随错误率变化的性能曲线。
    """
    # 如果您希望输出的文件名和指标对应，可以自定义如下映射
    name_map = {
        "F1 Score": "f1_performance.eps",
        "EDR":      "edr_performance.eps",
        "R-EDR":    "redr_performance.eps",
        "CTR":      "time_performance.eps"
    }

    # 设定针对各指标的显示上下限（如果有）
    limits = {
        "CTR":   {"upper": 40, "upperSYS": True},        # Time per 100 Records(s) 只限制上界
        "EDR":   {"lower": -1.5, "upper": 1, "upperSYS": False},
        "R-EDR": {"lower": -1.5, "upper": 1, "upperSYS": False}
    }

    # 适当扩展显示范围的比例
    expand_ratio = 0.1

    # 不同系统用不同的 marker 和颜色
    markers = ['o', 'X', 'D', '^', 'v', 'P', '*']
    colors = plt.cm.tab10(np.arange(len(systems)))

    # ======================
    #   创建外层 2×2 网格
    # ======================
    # figure 比较紧凑，适当减小
    fig = plt.figure(figsize=(40, 10))
    # 调整 wspace / hspace 尝试让外层间隔更小
    outer_grid = gridspec.GridSpec(
        1, 4,
        wspace=0.15,
        hspace=0.2
    )

    # 依次处理 4 个指标
    for metric_idx, metric in enumerate(metrics):
        # row = metric_idx // 2
        # col = metric_idx % 2
        row=0
        col=metric_idx
        # 在 2×2 网格中拿到当前指标所在的 subplotSpec
        inner_grid = gridspec.GridSpecFromSubplotSpec(
            2, 3,
            subplot_spec=outer_grid[row, col],
            wspace=0.15,  # 让子图之间横向间隔小一些
            hspace=0.25   # 让子图之间纵向间隔小一些
        )

        for i, data_set in enumerate(data_sets):
            # 将第 i 个数据集放到 2×3 子网格中
            ax = plt.subplot(inner_grid[i])

            for j, system in enumerate(systems):
                # 提取原始性能数据 (1D 列表: error_rates -> 性能值)
                original_data = performance_data[metric][i][j]

                # 根据限制条件调整数据
                if metric in limits:
                    lower_limit = limits[metric].get("lower", float("-inf"))
                    upper_limit = limits[metric].get("upper", float("inf"))
                    adjusted_data = [
                        max(min(value, upper_limit), lower_limit)
                        for value in original_data
                    ]
                else:
                    adjusted_data = original_data

                # 绘制曲线
                # 将线条宽度、marker 大小都适当减小
                ax.plot(
                    error_rates,
                    adjusted_data,
                    label=system,
                    marker=markers[j % len(markers)],
                    color=colors[j],
                    linestyle='-',
                    linewidth=5,   # 线条
                    markersize=16   # marker
                )

            # 设置子图标题为对应的数据集名称
            ax.set_title(data_set, fontsize=30)
            # ax.tick_params(axis='y', labelsize=30)
            # 只在最下面那行显示 X 轴标签
            # if i >= 3:
                # ax.set_xlabel("Error Rate (%)", fontsize=25)
            if i % 6 == 4:
                ax.set_xlabel("Error Rate (%) \n"+metric, fontsize=30,fontweight='bold')
                if metric=="CTR":
                    ax.set_xlabel("Error Rate (%) \n" + metric+"(s)", fontsize=30, fontweight='bold')
            # 只在第一列显示 Y 轴标签
            if i % 3 == 0:
                # ax.set_ylabel(metric, fontsize=30)
                ax.tick_params(axis='y', labelsize=20)  # 调整 Y 轴刻度字体大小
            # 只为最左侧的子图显示 Y 轴标签和刻度
            else:
                # 隐藏中间和右边子图的 Y 轴刻度和标签
                ax.tick_params(axis='y', which='both', left=False, labelleft=False)

            ax.grid(True, linestyle='--', alpha=0.6)

            # 处理 y 轴范围
            if metric in limits:
                lower_limit = limits[metric].get("lower", float("-inf"))
                upper_limit = limits[metric].get("upper", float("inf"))

                # 根据 expand_ratio 做适当扩展
                if lower_limit > float("-inf"):
                    expanded_lower = lower_limit - abs(lower_limit) * expand_ratio
                else:
                    expanded_lower = None

                if upper_limit < float("inf"):
                    expanded_upper = upper_limit + abs(upper_limit) * expand_ratio
                else:
                    expanded_upper = None

                ax.set_ylim(expanded_lower, expanded_upper)

                # 若需自定义刻度，可在这里进一步处理
                yticks = ax.get_yticks()
                custom_yticks = []
                for y in yticks:
                    # 如果有下界且当前刻度小于等于下界
                    if "lower" in limits[metric] and y <= lower_limit:
                        custom_yticks.append(f"<{lower_limit}")
                    # 如果有上界且需要显示为 >上界
                    elif ("upperSYS" in limits[metric] and limits[metric]["upperSYS"]
                          and "upper" in limits[metric] and y >= upper_limit):
                        custom_yticks.append(f">{upper_limit}")
                    else:
                        custom_yticks.append(round(y, 2))  # 保留两位小数
                ax.set_yticklabels(custom_yticks)

    # =================
    #   添加全局图例
    # =================
    # 为了让整个图更紧凑，可以把图例放在整张图的底部或顶部，
    # 这里演示放顶部，并调小间距
    handles = [
        plt.Line2D([0], [0],
                   marker=markers[k],
                   color=colors[k],
                   label=sys_name,
                   linestyle='None',
                   markersize=25)  # 图例也稍微紧凑
        for k, sys_name in enumerate(systems)
    ]
    fig.legend(
        handles=handles,
        loc='upper center',
        ncol=len(systems),
        fontsize=30,
        bbox_to_anchor=(0.5, 1.02)
    )
    # 也可以统一只输出一个大图文件：
    plt.savefig("all_metrics_1*4.eps", format="eps",bbox_inches='tight')
    plt.savefig("all_metrics_1*4.png", dpi=300, format="png",bbox_inches='tight')
    plt.show()
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
        "CTR": "time_performance.eps"
    }
    # 指标的限制条件
    limits = {
        "CTR": {"upper": 70,"upperSYS":True},      # Time per 100 Records(s)只限制上界
        "EDR": {"lower": -1.5, "upper": 1, "upperSYS":False},  # EDR限制下界为-1.5，上界为1.0
        "R-EDR": {"lower": -1.5,"upper": 1,"upperSYS":False}  # REDR限制下界为-1.5，上界为1.0
    }
    expand_ratio = 0.1  # 用于扩展显示范围的比例

    markers = ['o', 's', 'D', '^', 'v', 'P', '*']  # 用于区分系统的点形状
    colors = plt.cm.tab10(np.arange(len(systems)))  # 为不同系统分配颜色

    for metric in metrics:  # 遍历每个指标
        # 创建一个2x3的子图布局
        fig, axes = plt.subplots(2, 3, figsize=(2, 10), sharex=True, sharey=True)
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
    # metrics = ["F1 Score", "EDR", "R-EDR", "CTR"]
    metrics = ["F1 Score", "EDR", "Hybrid Distance"]

    def convert_to_performance_data(csv_path):
        # 读取 CSV 文件
        df = pd.read_csv(csv_path, header=None)

        # 初始化存储数据
        performance_data = defaultdict(list)
        current_dataset = None
        current_system = None
        metric_map = {"F1 Score": 0, "EDR": 1, "Hybrid Distance": 2, "R-EDR": 3, "CTR": 4}
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
    plot_metrics_3x1(error_rates, data_sets, systems, metrics, performance_data)
