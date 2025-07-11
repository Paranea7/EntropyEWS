import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import seaborn as sns

# 指定要遍历的目录
directory_path = ('./data/Amazon/h11v08')  # 替换为你的目录路径
slices_directory = os.path.join(directory_path, 'global_SD')  # 目标文件夹路径
csv_directory = os.path.join(slices_directory, 'sd')  # CSV文件夹路径

# 创建目标文件夹（如果不存在）
os.makedirs(slices_directory, exist_ok=True)
os.makedirs(csv_directory, exist_ok=True)  # 创建CSV子文件夹（如果不存在）

# 遍历目录中的所有 HDF 文件
for filename in os.listdir(directory_path):
    if filename.endswith('.hdf'):
        file_path = os.path.join(directory_path, filename)  # 完整路径
        print(f"Processing file: {file_path}")

        # 使用 netCDF4 打开 HDF 文件
        with Dataset(file_path, mode='r') as nc_file:
            # 检查并提取数据集
            if 'Percent_Tree_Cover_SD' in nc_file.variables:
                percent_tree_cover = nc_file.variables['Percent_Tree_Cover_SD'][:]  # 提取完整数组

                # 检查数据维度
                if percent_tree_cover.ndim == 2:
                    # 保存为 CSV 格式
                    csv_filename = f"percent_tree_cover_{os.path.splitext(filename)[0]}.csv"
                    csv_path = os.path.join(csv_directory, csv_filename)
                    np.savetxt(csv_path, percent_tree_cover, delimiter=",")  # 使用 NumPy 保存为 CSV
                    print(f"CSV saved: {csv_path}")

                    # 创建热图
                    plt.figure(figsize=(10, 8))
                    sns.heatmap(percent_tree_cover, cmap='Greens', cbar=True)
                    plt.title('Tree Cover Percentage Heatmap')
                    plt.xlabel('Longitude')
                    plt.ylabel('Latitude')

                    # 保存热图到目标文件夹
                    heatmap_filename = f"heatmap_{os.path.splitext(filename)[0]}.png"
                    heatmap_path = os.path.join(slices_directory, heatmap_filename)
                    plt.savefig(heatmap_path)
                    plt.close()  # 关闭当前图形以避免内存问题
                    print(f"Heatmap saved: {heatmap_path}")
                else:
                    print(f"Data dimension for {filename} is not 2D, skipping...")