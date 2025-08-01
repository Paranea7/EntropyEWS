import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from concurrent.futures import ProcessPoolExecutor

# 指定要遍历的目录
directory_path = '../../data/Amazon/h11v08'  # 替换为您的目录路径
slices_directory = os.path.join(directory_path, 'OP')  # 目标文件夹路径

# 创建目标文件夹（如果不存在）
os.makedirs(slices_directory, exist_ok=True)
slices_directory_2_2 = os.path.join(slices_directory, '2x2')  # 2x2 模式文件夹
slices_directory_1_4 = os.path.join(slices_directory, '1x4')  # 1x4 模式文件夹
slices_directory_4_1 = os.path.join(slices_directory, '4x1')  # 4x1 模式文件夹
os.makedirs(slices_directory_2_2, exist_ok=True)
os.makedirs(slices_directory_1_4, exist_ok=True)
os.makedirs(slices_directory_4_1, exist_ok=True)

def unique_sort_pattern(array):
    """生成唯一的排序模式，过滤掉掩盖的元素"""
    masked_array = np.ma.masked_array(array)
    filtered_array = masked_array.compressed()  # 仅保留未掩盖的元素

    if len(filtered_array) == 0:
        return np.array([])  # 如果没有有效的元素，返回空数组

    indexed_array = np.array(list(enumerate(filtered_array)))
    sorted_indices = indexed_array[np.argsort(indexed_array[:, 1])]
    return sorted_indices[:, 0]  # 返回排序后的索引

def process_file(file_path):
    """处理每个 HDF 文件并计算模式和概率"""
    print(f"Processing file: {file_path}")

    # 使用 netCDF4 打开 HDF 文件
    with Dataset(file_path, mode='r') as nc_file:
        # 检查并提取数据集
        if 'Percent_Tree_Cover_SD' in nc_file.variables:
            percent_tree_cover = nc_file.variables['Percent_Tree_Cover_SD'][:]  # 提取完整数组
            rows, cols = percent_tree_cover.shape

            # 保存2x2模式的序数模式和概率
            patterns_probability_2x2 = []
            for i in range(rows - 1):
                for j in range(cols - 1):
                    small_square = percent_tree_cover[i:i + 2, j:j + 2].flatten()
                    permutation_vector = unique_sort_pattern(small_square)
                    unique, counts = np.unique(permutation_vector, return_counts=True)
                    probabilities = counts / len(permutation_vector)
                    patterns_probability_2x2.append((unique, probabilities))

            # 保存 2x2 序数模式和对应的概率
            patterns_df_2x2 = pd.DataFrame([(list(pattern), list(prob)) for (pattern, prob) in patterns_probability_2x2])
            patterns_file_path_2x2 = os.path.join(slices_directory_2_2, f"patterns_2x2_{os.path.basename(file_path)}.csv")
            patterns_df_2x2.to_csv(patterns_file_path_2x2, index=False, header=["Pattern", "Probability"])
            print(f"Saved 2x2 patterns and probabilities to: {patterns_file_path_2x2}")

            # 保存1x4模式的序数模式和概率
            patterns_probability_1x4 = []
            for i in range(rows):
                for j in range(cols - 3):
                    small_line = percent_tree_cover[i, j:j + 4].flatten()
                    permutation_vector = unique_sort_pattern(small_line)
                    unique, counts = np.unique(permutation_vector, return_counts=True)
                    probabilities = counts / len(permutation_vector)
                    patterns_probability_1x4.append((unique, probabilities))

            # 保存 1x4 序数模式和对应的概率
            patterns_df_1x4 = pd.DataFrame([(list(pattern), list(prob)) for (pattern, prob) in patterns_probability_1x4])
            patterns_file_path_1x4 = os.path.join(slices_directory_1_4, f"patterns_1x4_{os.path.basename(file_path)}.csv")
            patterns_df_1x4.to_csv(patterns_file_path_1x4, index=False, header=["Pattern", "Probability"])
            print(f"Saved 1x4 patterns and probabilities to: {patterns_file_path_1x4}")

            # 保存4x1模式的序数模式和概率
            patterns_probability_4x1 = []
            for i in range(rows - 3):
                for j in range(cols):
                    small_column = percent_tree_cover[i:i + 4, j].flatten()
                    permutation_vector = unique_sort_pattern(small_column)
                    unique, counts = np.unique(permutation_vector, return_counts=True)
                    probabilities = counts / len(permutation_vector)
                    patterns_probability_4x1.append((unique, probabilities))

            # 保存 4x1 序数模式和对应的概率
            patterns_df_4x1 = pd.DataFrame([(list(pattern), list(prob)) for (pattern, prob) in patterns_probability_4x1])
            patterns_file_path_4x1 = os.path.join(slices_directory_4_1, f"patterns_4x1_{os.path.basename(file_path)}.csv")
            patterns_df_4x1.to_csv(patterns_file_path_4x1, index=False, header=["Pattern", "Probability"])
            print(f"Saved 4x1 patterns and probabilities to: {patterns_file_path_4x1}")

# 主要处理逻辑
if __name__ == '__main__':
    # 获取所有HDF文件
    hdf_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.hdf')]

    # 使用 ProcessPoolExecutor 并行处理文件
    with ProcessPoolExecutor() as executor:
        executor.map(process_file, hdf_files)