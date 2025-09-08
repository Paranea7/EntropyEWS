import pandas as pd
import matplotlib.pyplot as plt
import os


def process_csv_files(directory):
    """处理指定目录中的所有CSV文件，计算平均值并绘制序列图"""
    averages = []  # 用于存储每个文件的平均值
    years = list(range(2001, 2025))  # 创建从2001到2024的年份列表

    # 获取目录中所有CSV文件
    csv_files = sorted([f for f in os.listdir(directory) if f.endswith('.csv')])

    # 对每一个CSV文件进行处理
    for i, filename in enumerate(csv_files):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")

        # 读取数据
        data = pd.read_csv(file_path, header=None)

        # 计算平均值
        mean_value = data.mean().mean()  # 计算整个数据框的平均值
        averages.append(mean_value)

    # 确保处理的文件不超过年份数量
    num_files = len(averages)
    if num_files > len(years):
        # 截断年份以适应文件数量
        years = years[:num_files]

    # 绘制序列图
    plt.figure(figsize=(10, 6))
    plt.plot(years, averages, marker='o', label='Average Value')
    plt.title('Average Values from CSV Files (2001-2024)')
    plt.xlabel('Year')
    plt.ylabel('Average Value')
    plt.xticks(years, rotation=45)
    plt.grid()
    plt.legend()

    # 保存图像
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'average_values_plot.png'))
    plt.close()  # 关闭图形以释放内存
    print(f"Average values plot saved as: average_values_plot.png")


# 设置CSV文件所在目录
data_directory = '../../data/data/Amazon/h10v08/global_SD/sd'  # 替换为您的CSV文件目录
process_csv_files(data_directory)