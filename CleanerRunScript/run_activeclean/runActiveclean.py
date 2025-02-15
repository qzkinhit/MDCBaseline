import sys
import os

# 动态添加 Cleaner 模块所在的路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import argparse
from Cleaner.Activeclean.activeclean import run
from util.readData import load_data_csv
from util.saveData import save_data_csv


#IMDB数据集运行脚本
# def Activeclean(data):
#     pre_txt = run(data)
#     return pre_txt


# if __name__ == "__main__":
#     # Set up argument parser
#     parser = argparse.ArgumentParser(description='Run Activeclean data cleaning script.')
#     parser.add_argument('--input', default='IMDB/imdb_features.p', type=str, help='Path to the input CSV file.')
#     parser.add_argument('--output', default='output.csv', type=str, help='Path to the output CSV file.')

#     # Parse arguments
#     args = parser.parse_args()

#     # Run the main function
#     # Load the data
#     print(f"Loading data from {args.input}")

#     # Perform data cleaning
#     print("Cleaning data")
#     pre_txt = Activeclean(args.input)

#     # Write results
#     with open('../../results/activeclean/'+args.output, 'w', encoding='utf-8') as f:
#         f.write(pre_txt)
#         f.close()


def Activeclean(correct_data_path, injected_data_path, type):
    """
    Activeclean 的主入口，调用 run 函数进行数据清洗
    Args:
        correct_data_path (str): 完全正确的数据集路径
        injected_data_path (str): 注入错误的数据集路径
    Returns:
        处理后的文本结果
    """
    # 调用 run 函数，传入正确数据集和注入错误的数据集路径
    pre_txt = run(correct_data_path, injected_data_path, type)
    return pre_txt


if __name__ == "__main__":
    # 设置参数解析器
    parser = argparse.ArgumentParser(description='Run Activeclean data cleaning script.')
    parser.add_argument('--correct_data', default='D:\PyCharm\PycharmProjects\MDCBaseline\Data\\nasa\\nasa_data_vectorized.csv', type=str, help='Path to the correct data file (fully clean).')
    parser.add_argument('--injected_data', default='D:\PyCharm\PycharmProjects\MDCBaseline\Data\\nasa\\nasa_systematic_5.csv', type=str, help='Path to the injected data file (with errors).')
    parser.add_argument('--output', default='D:\PyCharm\PycharmProjects\MDCBaseline\Data\\nasa\\nasa_systematic_5_output.txt', type=str, help='Path to save the cleaned output data file.')
    parser.add_argument('--ml_type', default='r', type=str, help='ML task: c or r.')

    # 解析命令行参数
    args = parser.parse_args()

    # 加载数据并进行清理
    print(f"Loading correct data from {args.correct_data}")
    print(f"Loading injected data from {args.injected_data}")
    print("Cleaning data using Activeclean...")

    # 调用 Activeclean 函数来运行数据清理
    pre_txt = Activeclean(args.correct_data, args.injected_data, args.ml_type)

    # 保存结果
    # 构建完整的输出路径
    output_path = os.path.join(os.path.dirname(__file__), '../../results/activeclean/', args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pre_txt)

    print(f"Results saved to {output_path}")
