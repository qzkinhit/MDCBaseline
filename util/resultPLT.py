import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calculate_accuracy_and_recall(clean, dirty, cleaned, attributes):
    """
    计算指定属性集合下的修复准确率和召回率

    :param clean: 干净数据 DataFrame
    :param dirty: 脏数据 DataFrame
    :param cleaned: 清洗后数据 DataFrame
    :param attributes: 指定属性集合
    :return: 修复准确率和召回率
    """
    total_true_positives = 0
    total_false_positives = 0
    total_true_negatives = 0

    for attribute in attributes:
        clean_values = clean[attribute]
        dirty_values = dirty[attribute]
        cleaned_values = cleaned[attribute]

        # 对齐索引
        common_indices = clean_values.index.intersection(cleaned_values.index).intersection(dirty_values.index)
        clean_values = clean_values.loc[common_indices]
        dirty_values = dirty_values.loc[common_indices]
        cleaned_values = cleaned_values.loc[common_indices]

        # 正确修复的数据
        true_positives = ((cleaned_values == clean_values) & (dirty_values != cleaned_values)).sum()
        # 修错的数据
        false_positives = ((cleaned_values != clean_values) & (dirty_values != cleaned_values)).sum()
        # 应该需要修复的数据
        true_negatives = (dirty_values != clean_values).sum()

        total_true_positives += true_positives
        total_false_positives += false_positives
        total_true_negatives += true_negatives

    # 总体修复的准确率
    accuracy = total_true_positives / (total_true_positives + total_false_positives)
    # 总体修复的召回率
    recall = total_true_positives / total_true_negatives

    return accuracy, recall


def plot_metrics(names, clean_dfs, dirty_dfs, cleaned_dfs, attributes_list):
    """
    绘制数据集清洗的准确率、召回率和F1值图, 既能表示多个清洗系统对于一个数据集的效果，也能表示一个清洗系统在多个数据集上的效果。

    :param names: 名称列表，可以是清洗系统名或数据集名
    :param clean_dfs: 干净数据 DataFrame 列表
    :param dirty_dfs: 脏数据 DataFrame 列表
    :param cleaned_dfs: 清洗后数据 DataFrame 列表
    :param attributes_list: 每个数据集的指定属性集合列表
    """
    accuracies = []
    recalls = []
    f1_scores = []
    labels = []

    for name, clean, dirty, cleaned_list, attributes in zip(names, clean_dfs, dirty_dfs, cleaned_dfs, attributes_list):
        for i, cleaned in enumerate(cleaned_list):
            accuracy, recall = calculate_accuracy_and_recall(clean, dirty, cleaned, attributes)
            accuracies.append(accuracy)
            recalls.append(recall)
            f1_scores.append(2 * (accuracy * recall) / (accuracy + recall))
            labels.append(f"{name} Cleaned {i + 1}")

    x = np.arange(len(labels))
    width = 0.35

    # 绘制准确率图
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x, accuracies, width, label='Accuracy')
    ax.set_xlabel('Cleaned Datasets')
    ax.set_ylabel('Accuracy')
    ax.set_title('Accuracy for Multiple Systems/Datasets')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()
    plt.savefig("accuracy_metrics.png")
    plt.show()

    # 绘制召回率图
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x, recalls, width, label='Recall')
    ax.set_xlabel('Cleaned Datasets')
    ax.set_ylabel('Recall')
    ax.set_title('Recall for Multiple Systems/Datasets')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()
    plt.savefig("recall_metrics.png")
    plt.show()

    # 绘制F1值图
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x, f1_scores, width, label='F1 Score')
    ax.set_xlabel('Cleaned Datasets')
    ax.set_ylabel('F1 Score')
    ax.set_title('F1 Score for Multiple Systems/Datasets')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()
    plt.savefig("f1_score_metrics.png")
    plt.show()


if __name__ == "__main__":
    # 示例数据加载
    names = ["System1", "System2"]
    clean_paths = ["data/clean1.csv", "data/clean2.csv"]
    dirty_paths = ["data/dirty1.csv", "data/dirty2.csv"]
    cleaned_paths = [["data/cleaned1_1.csv", "data/cleaned1_2.csv"], ["data/cleaned2_1.csv", "data/cleaned2_2.csv"]]

    clean_dfs = [pd.read_csv(path) for path in clean_paths]
    dirty_dfs = [pd.read_csv(path) for path in dirty_paths]
    cleaned_dfs = [[pd.read_csv(path) for path in paths] for paths in cleaned_paths]

    attributes_list = [["attr1", "attr2", "attr3"], ["attr1", "attr2"]]

    plot_metrics(names, clean_dfs, dirty_dfs, cleaned_dfs, attributes_list)
