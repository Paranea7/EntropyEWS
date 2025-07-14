import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def sliding_window_average(data, window_size, step_size):
    """计算滑动窗口的平均值"""
    n_rows, n_cols = data.shape
    window_height, window_width = window_size
    # 计算能得到多少个窗口
    num_windows = (n_cols - window_width) // step_size + 1
    averaged_data = np.zeros((n_rows, num_windows))

    # 滑动窗口计算
    for i in range(num_windows):
        start_col = i * step_size
        end_col = start_col + window_width
        averaged_data[:, i] = np.mean(data[:, start_col:end_col], axis=1)

    return averaged_data


def process_files_in_directory(directory, output_directory):
    """处理目录中的所有 CSV 文件"""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # 读取 CSV 数据，没有表头
            data = pd.read_csv(file_path, header=None)
            data_array = data.values  # 转换为 NumPy 数组

            # 设置窗口大小和步长
            window_size = (4800, 200)
            step_size = 50  # 横向推进1列
            averaged_data = sliding_window_average(data_array, window_size, step_size)

            # 保存结果到 CSV
            output_file_path = os.path.join(output_directory, f'averaged_{filename}')
            np.savetxt(output_file_path, averaged_data, delimiter=',')
            print(f"已保存滑动平均数据到 {output_file_path}")


# 主程序入口
if __name__ == "__main__":
    input_directory = './data/Amazon/h11v08/delta'  # 输入目录
    output_directory = os.path.join(input_directory, 'movewindow')  # 输出子目录
    process_files_in_directory(input_directory, output_directory)