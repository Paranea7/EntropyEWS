import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_entropy(entropy_values, filename, output_directory):
    """绘制熵值并保存图像"""
    plt.figure(figsize=(10, 5))
    plt.plot(entropy_values, marker='o', label=f'Entropy of {filename}')
    plt.title(f'Entropy of Each Column for {filename}')
    plt.xlabel('Column Index')
    plt.ylabel('Entropy Value')
    plt.grid()
    plt.legend()

    image_path = os.path.join(output_directory, f'entropy_plot_{filename}.png')
    plt.savefig(image_path)
    plt.close()
    print(f"Plot saved to: {image_path}")


def process_csv_files(directory, output_directory):
    """处理指定目录中的所有CSV文件"""

    # 创建文件夹结构
    original_plots_directory = os.path.join(output_directory, "original_plots")
    processed_data_directory = os.path.join(output_directory, "processed_data")
    processed_plots_directory = os.path.join(output_directory, "processed_plots")

    os.makedirs(original_plots_directory, exist_ok=True)
    os.makedirs(processed_data_directory, exist_ok=True)
    os.makedirs(processed_plots_directory, exist_ok=True)

    # 查找所有 CSV 文件
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    print(f"Found CSV files: {csv_files}")

    for filename in csv_files:
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")

        # 读取CSV文件
        data = pd.read_csv(file_path, header=None)  # 无列名
        # 选择从第三行到最后一行的数据
        data = data.iloc[2:, :]  # 选择第三行及其之后的所有行
        print(f"Data shape after loading: {data.shape}")

        # 检查数据是否为空
        if data.empty:
            print(f"No data after filtering for file: {filename}")
            continue

        # 计算每一列的均值
        entropy_values = data.mean()
        print(f"Mean entropy values: {entropy_values}")

        # 绘制和保存原文件的熵图
        plot_entropy(entropy_values, filename, original_plots_directory)  # 绘制和保存图像

        # 滑动窗口处理
        results = []
        window_size = 200  # 每个窗口200个数据点
        step_size = 50  # 每次移动50个数据点

        for start in range(0, len(entropy_values) - window_size + 1, step_size):
            end = start + window_size
            window = entropy_values[start:end]  # 选择当前窗口的数据
            window_mean = np.mean(window)  # 计算窗口的平均值
            results.append(window_mean)  # 将结果添加到列表中

        # 将结果转换为 DataFrame
        results_df = pd.DataFrame(results, columns=['Mean_Entropy'])

        # 保存处理后的结果到 CSV 文件
        results_df.to_csv(os.path.join(processed_data_directory, f'processed_means_{filename}'), index=False)
        print(
            f"Sliding window mean entropy values saved to: {os.path.join(processed_data_directory, f'processed_means_{filename}')}")

        # 保存滑动窗口结果图像
        plt.figure(figsize=(10, 5))
        plt.plot(results_df['Mean_Entropy'], marker='o', label='Sliding Window Mean Entropy')
        plt.title(f'Sliding Window Mean Entropy - {filename}')
        plt.xlabel('Window Index')
        plt.ylabel('Mean Entropy Value')
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(processed_plots_directory, f'sliding_window_mean_entropy_{filename}.png'))  # 保存图像
        plt.close()
        print(
            f"Sliding window plot saved to: {os.path.join(processed_plots_directory, f'sliding_window_mean_entropy_{filename}.png')}")


# 设置CSV文件所在目录
data_directory = '../../data/data/Amazon/h10v08/2D-OP/2x2'  # 替换为您的CSV文件目录
output_directory = os.path.join(data_directory, "plote")  # 创建名为plote的子文件夹
process_csv_files(data_directory, output_directory)