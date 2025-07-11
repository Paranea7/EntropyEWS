import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import os

def calculate_metrics(data):
    """计算方差、自相关、偏度和峰度"""
    var = data.var()  # 方差
    acf = pd.Series(data).autocorr()  # 自相关
    skw = skew(data)  # 偏度
    kurt = kurtosis(data)  # 峰度
    return var, acf, skw, kurt

def process_csv_files(directory):
    """处理指定目录中的所有CSV文件"""
    metrics = []  # 用于存储所有文件的统计量

    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")

            # 读取数据
            data = pd.read_csv(file_path, header=None)
            # 排除第一个元素（Entropy），只取后面的数据
            values = data.values.flatten()[1:]  # 从第二个元素开始
            values = values.astype(float)
            # 计算指标
            variance, autocorr, skewness, kurt = calculate_metrics(values)

            # 将计算结果存储到列表
            metrics.append({
                'Filename': filename,
                'Variance': variance,
                'Autocorrelation': autocorr,
                'Skewness': skewness,
                'Kurtosis': kurt
            })

    # 将列表转换为DataFrame
    metrics_df = pd.DataFrame(metrics)

    # 绘制统计量的时间序列图
    plt.figure(figsize=(20, 40))

    # 绘制方差
    plt.subplot(4, 1, 1)
    plt.plot(metrics_df['Filename'], metrics_df['Variance'], marker='o', label='Variance')
    plt.title('Variance over Files')
    plt.xlabel('Filename')
    plt.xticks(rotation=45)
    plt.ylabel('Variance')
    plt.grid()
    plt.legend()

    # 绘制自相关
    plt.subplot(4, 1, 2)
    plt.plot(metrics_df['Filename'], metrics_df['Autocorrelation'], marker='o', label='Autocorrelation', color='orange')
    plt.title('Autocorrelation over Files')
    plt.xlabel('Filename')
    plt.xticks(rotation=45)
    plt.ylabel('Autocorrelation')
    plt.grid()
    plt.legend()

    # 绘制偏度
    plt.subplot(4, 1, 3)
    plt.plot(metrics_df['Filename'], metrics_df['Skewness'], marker='o', label='Skewness', color='green')
    plt.title('Skewness over Files')
    plt.xlabel('Filename')
    plt.xticks(rotation=45)
    plt.ylabel('Skewness')
    plt.grid()
    plt.legend()

    # 绘制峰度
    plt.subplot(4, 1, 4)
    plt.plot(metrics_df['Filename'], metrics_df['Kurtosis'], marker='o', label='Kurtosis', color='red')
    plt.title('Kurtosis over Files')
    plt.xlabel('Filename')
    plt.xticks(rotation=45)
    plt.ylabel('Kurtosis')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'time_series_metrics.png'))
    plt.close()  # 关闭图形以释放内存
    print(f"All metrics time series plot saved as: time_series_metrics.png")

# 设置CSV文件所在目录
data_directory = './data/Africa/h19v08/delta/Enz'  # 替换为您的CSV文件目录
process_csv_files(data_directory)