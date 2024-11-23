import matplotlib.pyplot as plt
import numpy as np


def plot_radial_chart(datasets, metrics, scales, data_with_preparation, data_without_preparation, title):
    """
    绘制扩展雷达图，每个数据集独占一定角度，避免指标重叠。
    分别设置颜色图例和线型图例。

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
            normalized[key] = [(v - s[0]) / (s[1] - s[0]) for v, s in zip(values, scales)]
        return normalized

    data_with_norm = normalize_data(data_with_preparation, scales)
    data_without_norm = normalize_data(data_without_preparation, scales)

    # 计算总点数和角度
    total_points = len(datasets) * len(metrics)
    angles = np.linspace(0, 2 * np.pi, total_points, endpoint=False).tolist()
    angles += angles[:1]  # 闭合曲线

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
    colors = ['blue', 'green', 'red', 'purple']  # 每个数据集的颜色

    # 绘制每个数据集的指标
    for i, dataset in enumerate(datasets):
        # 取对应数据集的角度
        dataset_angles = angles[i * len(metrics):(i + 1) * len(metrics)] + [angles[i * len(metrics)]]

        # 有清洗准备策略
        values_with = data_with_norm[dataset] + [data_with_norm[dataset][0]]
        ax.plot(dataset_angles, values_with, label=dataset, color=colors[i], linewidth=2, linestyle='solid')
        ax.fill(dataset_angles, values_with, color=colors[i], alpha=0.2)

        # 无清洗准备策略
        values_without = data_without_norm[dataset] + [data_without_norm[dataset][0]]
        ax.plot(dataset_angles, values_without, color=colors[i], linewidth=2, linestyle='dashed')

    # 设置每个点的标签
    labels = [f"{dataset} {metric}" for dataset in datasets for metric in metrics]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=15)

    # 颜色图例（表示数据集）
    color_handles = [plt.Line2D([0], [0], color=color, lw=2, label=dataset) for color, dataset in zip(colors, datasets)]
    legend1 = fig.legend(handles=color_handles, loc='upper left', bbox_to_anchor=(0.05, 0.98), title="Dataset",fontsize=15)

    # 线型图例（表示是否使用清洗准备策略）
    line_handles = [
        plt.Line2D([0], [0], color='black', lw=2, linestyle='solid', label='With Preparation'),
        plt.Line2D([0], [0], color='black', lw=2, linestyle='dashed', label='Without Preparation'),
    ]
    legend2 = fig.legend(handles=line_handles, loc='upper right', bbox_to_anchor=(1, 0.98), fontsize=15)

    # 将图例附加到绘图对象中，防止覆盖
    ax.add_artist(legend1)
    ax.add_artist(legend2)

    # # 添加标题
    # ax.set_title(title, fontsize=16, pad=20)

    # 显示图形
    plt.show()


# 数据和配置
datasets = ['Hospital', 'Flights', 'Beers', 'Rayyan']
metrics = ['S', 'F1', 'EDR', 'REDR']
scales = [
    (0, 1),  # S
    (0, 1),  # F1
    (-0.1, 1),  # EDR
    (-0.1, 1),  # REDR
]

# 原始数据倒数处理
data_with_preparation = {
    'Hospital': [1 / 10.8115, 0.8847, 0.7839, 0.7543],
    'Flights': [1 / 3.5603, 0.6537, 0.5175, 0.1129],
    'Beers': [1 / 1.2966, 0.8373, 0.8329, 0.7730],
    'Rayyan': [1 / 5.2378, 0.9213, 0.9005, 0.8827],
}

data_without_preparation = {
    'Hospital': [1 / 13.2115, 0.7932, 0.6235, 0.5521],
    'Flights': [1 / 4.2316, 0.5724, 0.3987, 0.0562],
    'Beers': [1 / 1.5213, 0.7526, 0.6852, 0.6215],
    'Rayyan': [1 / 6.0123, 0.8431, 0.7512, 0.6834],
}

# 绘制图形
plot_radial_chart(datasets, metrics, scales, data_with_preparation, data_without_preparation,
                  title="Performance Comparison Across Datasets")
