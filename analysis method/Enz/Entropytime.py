import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from collections import Counter

# 指定要遍历的目录
directory_path = '../../data/Africa/h20v08'  # 替换为你的目录路径
slices_directory = os.path.join(directory_path, '2D-OP')  # 目标文件夹路径

# 创建目标文件夹（如果不存在）
os.makedirs(slices_directory, exist_ok=True)

# 函数：计算排列熵
def permutation_entropy(vector):
    """计算给定向量的排列熵"""
    permutation = np.argsort(vector)
    return -sum((count/len(permutation)) * np.log(count/len(permutation))
                 for count in Counter(tuple(permutation)).values())

def unique_sort_pattern(array):
    """生成唯一的排序模式，过滤掉掩盖的元素"""
    # 使用 compressed() 方法来移除掩盖的元素
    masked_array = np.ma.masked_array(array)
    filtered_array = masked_array.compressed()  # 仅保留未掩盖的元素

    if len(filtered_array) == 0:
        return np.array([])  # 如果没有有效的元素，返回空数组

    indexed_array = np.array(list(enumerate(filtered_array)))
    sorted_indices = indexed_array[np.argsort(indexed_array[:, 1])]
    return sorted_indices[:, 0]  # 返回排序后的索引

# 遍历目录中的所有 HDF 文件
for filename in os.listdir(directory_path):
    if filename.endswith('.hdf'):  # 仅处理 .hdf 结尾的文件
        file_path = os.path.join(directory_path, filename)  # 获取文件的完整路径
        print(f"Processing file: {file_path}")

        # 使用 netCDF4 打开 HDF 文件
        with Dataset(file_path, mode='r') as nc_file:
            # 检查并提取数据集
            if 'Percent_Tree_Cover_SD' in nc_file.variables:
                percent_tree_cover = nc_file.variables['Percent_Tree_Cover_SD'][:]  # 提取完整数组
                rows, cols = percent_tree_cover.shape
                entropy_matrix = np.zeros((rows, cols))  # 存储排列熵的矩阵

                # 遍历数据矩阵，提取2x2小方格
                for i in range(rows - 1):
                    for j in range(cols - 1):
                        # 提取2x2小方格，最大允许一个点重合
                        small_square = percent_tree_cover[i:i+2, j:j+2].flatten()

                        # 生成唯一的排列模式
                        permutation_vector = unique_sort_pattern(small_square)

                        # 计算排列熵
                        entropy = permutation_entropy(permutation_vector)
                        entropy_matrix[i, j] = entropy

                # 将排列熵矩阵保存为文件
                entropy_df = pd.DataFrame(entropy_matrix)
                entropy_file_path = os.path.join(slices_directory, f"entropy_{filename}.csv")
                entropy_df.to_csv(entropy_file_path, index=False)
                print(f"Saved entropy matrix to: {entropy_file_path}")