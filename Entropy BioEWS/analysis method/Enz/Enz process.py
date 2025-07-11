import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 定义计算熵的函数
def calculate_entropy(column):
    """计算给定列的熵值"""
    value_counts = column.value_counts(normalize=True)
    entropy = -np.sum(value_counts * np.log2(value_counts)) if not value_counts.empty else 0
    return entropy


def save_entropy_values(entropy_values, filename, output_directory):
    """保存熵值到CSV文件"""
    entropy_df = pd.DataFrame(entropy_values, columns=['Entropy'])
    output_file_path = os.path.join(output_directory, f'entropy_values_{filename}.csv')
    entropy_df.to_csv(output_file_path, index=False)
    print(f"Entropy values saved to: {output_file_path}")


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
    plt.close()  # 关闭当前图形以节省内存
    print(f"Plot saved to: {image_path}")


def process_csv_files(directory, output_directory):
    """处理指定目录中的所有CSV文件"""
    os.makedirs(output_directory, exist_ok=True)

    for filename in [f for f in os.listdir(directory) if f.endswith('.csv')]:
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")

        # 创建子文件夹
        file_output_directory = os.path.join(output_directory, os.path.splitext(filename)[0])
        os.makedirs(file_output_directory, exist_ok=True)

        # 读取CSV文件
        data = pd.read_csv(file_path, header=None)  # 无列名
        # 选择从第三行到最后一行的数据
        data = data.iloc[2:, :]  # 选择第三行及其之后的所有行

        # 计算每一列的熵值
        entropy_values = data.apply(calculate_entropy).values.flatten()  # 计算每列的熵值
        print("每一列的熵值: ", entropy_values)

        save_entropy_values(entropy_values, filename, file_output_directory)  # 保存熵值
        plot_entropy(entropy_values, filename, file_output_directory)  # 绘制和保存图像

        # 滑动窗口处理
        results = []
        window_size = 200  # 每个窗口251个数据点
        step_size = 50  # 每次移动80个数据点

        for start in range(0, len(entropy_values) - window_size + 1, step_size):
            end = start + window_size
            window = entropy_values[start:end]  # 选择当前窗口的数据
            window_mean = np.mean(window)  # 计算窗口的平均值
            results.append(window_mean)  # 将结果添加到列表中

        # 将结果转换为 DataFrame
        results_df = pd.DataFrame(results, columns=['Mean_Entropy'])

        # 保存处理后的结果到 CSV 文件
        results_df.to_csv(os.path.join(file_output_directory, f'processed_means_{filename}'), index=False)
        print(f"Sliding window mean entropy values saved to: processed_means_{filename}")

        # 保存滑动窗口结果图像
        plt.figure(figsize=(10, 5))
        plt.plot(results_df['Mean_Entropy'], marker='o', label='Sliding Window Mean Entropy')
        plt.title(f'Sliding Window Mean Entropy - {filename}')
        plt.xlabel('Window Index')
        plt.ylabel('Mean Entropy Value')
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(file_output_directory, f'sliding_window_mean_entropy_{filename}.png'))  # 保存图像
        plt.close()  # 关闭图形以释放内存
        print(f"Sliding window plot saved to: sliding_window_mean_entropy_{filename}.png")


# 设置CSV文件所在目录
data_directory = './data/Africa/h20v08/space_delta'  # 替换为您的CSV文件目录
output_directory = os.path.join(data_directory, "Enz")  # 创建名为Enz的子文件夹
process_csv_files(data_directory, output_directory)