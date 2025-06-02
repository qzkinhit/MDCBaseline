import matplotlib.pyplot as plt
import numpy as np


def plot_radial_chart(datasets, metrics, scales, data_with_preparation, data_without_preparation, title):
    """
    绘制扩展雷达图，每个数据集独占一定角度，避免指标重叠。
    分别设置颜色图例和线型图例。
    如果比值归一化后大于1，则在坐标中显示为">1.0"。

    Parameters:
    - datasets: list[str] 数据集名称
    - metrics: list[str] 性能指标名称
    - scales: list[tuple] 每个指标的比例范围 [(min, max), ...]
    - data_with_preparation: dict 数据集在有清洗准备策略下的性能
    - data_without_preparation: dict 数据集在无清洗准备策略下的性能
    - title: str 图表标题
    """

    # 数据归一化
    def normalize_data(data, scales):
        normalized = {}
        for key, values in data.items():
            normalized[key] = [
                (v - s[0]) / (s[1] - s[0]) for v, s in zip(values, scales)
            ]
        return normalized

    # 归一化数据
    data_with_norm = normalize_data(data_with_preparation, scales)
    data_without_norm = normalize_data(data_without_preparation, scales)

    # 调整归一化数据
    def adjust_values(data_norm):
        adjusted_data = {}
        for dataset, values in data_norm.items():
            adjusted_values = [min(v, 1.0) for v in values]  # 将归一化值限制为最大1
            adjusted_data[dataset] = adjusted_values
        return adjusted_data

    data_with_adjusted = adjust_values(data_with_norm)
    data_without_adjusted = adjust_values(data_without_norm)

    # 计算总点数和角度
    total_points = len(datasets) * len(metrics)
    angles = np.linspace(0, 2 * np.pi, total_points, endpoint=False).tolist()
    angles += angles[:1]  # 闭合曲线

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta']  # 每个数据集的颜色

    # 绘制每个数据集的指标
    for i, dataset in enumerate(datasets):
        # 取对应数据集的角度
        dataset_angles = angles[i * len(metrics):(i + 1) * len(metrics)] + [angles[i * len(metrics)]]

        # 有清洗准备策略
        values_with = data_with_adjusted[dataset] + [data_with_adjusted[dataset][0]]
        ax.plot(dataset_angles, values_with, label=dataset, color=colors[i], linewidth=2, linestyle='solid')
        ax.fill(dataset_angles, values_with, color=colors[i], alpha=0.2)

        # 无清洗准备策略
        values_without = data_without_adjusted[dataset] + [data_without_adjusted[dataset][0]]
        ax.plot(dataset_angles, values_without, color=colors[i], linewidth=2, linestyle='dashed')

    # 设置每个点的标签
    labels = []
    for dataset, values in data_with_norm.items():
        for metric in metrics:
            labels.append(f"{metric}")
    ax.set_theta_offset(-np.pi / 2)  # 从 6 点钟方向开始
    ax.set_theta_direction(-1)  # 顺时针方向绘制
    ax.set_thetagrids(
        np.degrees(angles[:-1]),
        labels,
        fontsize=25,
        weight='bold',
        position=(-0.01,-0.03)
    )

    # 自定义径向坐标轴的标签（移动到左侧以避免重叠）
    ax.set_rgrids(
        [0.2, 0.4, 0.6, 0.8, 0.98],
        labels=['20%', '40%', '60%', '80%', '>100%'],
        angle=180,  # 将径向标签固定在左侧
        fontsize=18,
        weight='bold',
        ha='center'  # 居中对齐
    )

    # 颜色图例（表示数据集）
    color_handles = [plt.Line2D([0], [0], color=color, lw=2, label=dataset) for color, dataset in zip(colors, datasets)]
    legend1 = fig.legend(handles=color_handles, loc='upper left', bbox_to_anchor=(-0.01, 1), title="",
                         fontsize=25, frameon=True,)

    # # 线型图例（表示是否使用清洗准备策略）
    # line_handles = [
    #     plt.Line2D([0], [0], color='black', lw=2, linestyle='solid', label='With Preparation'),
    #     plt.Line2D([0], [0], color='black', lw=2, linestyle='dashed', label='Without Preparation'),
    # ]
    # legend2 = fig.legend(handles=line_handles, loc='upper right', fontsize=15,bbox_to_anchor=(1, 0.98))

    # 将图例附加到绘图对象中，防止覆盖
    ax.add_artist(legend1)
    # ax.add_artist(legend2)

    # 添加标题
    # ax.set_title(title, fontsize=16, pad=20)

    # 显示图形
    plt.savefig("dataset_scenario.eps", format="eps")
    plt.savefig("dataset_scenario.pdf", format="pdf",bbox_inches="tight")  # 使用PDF格式
    plt.show()
datasets = ['Hospital', 'Flights', 'Beers', 'Rayyan','Soccer','Commercial','Tax']
# datasets = ['Hospital', 'Beers', 'Rayyan', 'Tax','Commercial','Flights','Soccer']
metrics = ['S', 'F1', 'REDR', 'EDR']

scales = [
    (0, 1),  # S
    (0, 1),  # F1
    (-0.1, 1),  # REDR
    (-0.1, 1),  # EDR
]
# metrics = ['S', 'F1', 'REDR', 'EDR']
data_with_preparation = {
    'Hospital': [1 / 10.8115, 0.8847, 0.7543, 0.7839],
    'Flights': [1 / 3.5603, 0.6537, 0.6129, 0.5175],
    'Beers': [1 / 1.2966, 0.8373, 0.7730, 0.8329],
    'Rayyan': [1 / 5.2378, 0.9213, 0.8827, 0.9005],
    'Tax': [1 / 0.2525, 0.5944, 0.5524, 0.1005],
    'Commercial': [1 / 0.03055, 0.8400, 0.7700, 0.7500],
    'Soccer': [1 / 0.0343, 0.5341, 0.3442, 0.3301],
}
# metrics = ['S', 'F1', 'REDR', 'EDR']
data_without_preparation = {
    'Hospital': [1 / 15.8115, 0.6000, 0.4543, 0.4839],
    'Flights': [1 / 4.5603, 0.5400, 0.3175, 0.0000],
    'Beers': [1 / 2.2966, 0.6400, 0.6773, 0.7329],
    'Rayyan': [1 / 4.2378, 0.8200, 0.7827, 0.6005],
    'Tax': [1 / 40.25, 0.3200, 0.0000, 0.1005],
    'Commercial': [1 / 22.935, 0.2300, 0.0000, 0.0000],
    'Soccer': [1 / 0.0643, 0.4100, 0.3342, 0.3201],
}


# 绘制图形
plot_radial_chart(datasets, metrics, scales, data_with_preparation, data_without_preparation,
                  title="Metrics Comparison(%)")
