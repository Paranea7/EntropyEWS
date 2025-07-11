import pandas as pd
import numpy as np
from scipy.stats import rankdata
from collections import Counter

# 读取CSV文件
file_path = './data/tran5_veg_30m.csv'
data = pd.read_csv(file_path)

# 将-9999替换为NaN，以便后续处理
data.replace(-9999, np.nan, inplace=True)

# 翻转1和0
data.replace({1: 0, 0: 1}, inplace=True)

# 确保数据是以numpy数组的形式处理，方便进行邻域提取
data_matrix = data.to_numpy()

# 定义提取邻域函数
def extract_neighborhoods(matrix):
    neighborhoods = []
    rows, cols = matrix.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            neighborhood = matrix[i:i+2, j:j+2]
            neighborhoods.append(neighborhood)
    return neighborhoods

# 定义生成秩序模式函数
def generate_ranks(neighborhood):
    ranks = rankdata(neighborhood.flatten())
    return tuple(ranks)

# 定义统计频率函数
def count_patterns(neighborhoods):
    patterns = [generate_ranks(neigh) for neigh in neighborhoods]
    frequency = Counter(patterns)
    return frequency

# 执行提取邻域
neighborhoods = extract_neighborhoods(data_matrix)

# 执行统计频率
frequency_count = count_patterns(neighborhoods)

# 打印频率统计
print("Frequency of each ordinal pattern:")
for pattern, count in frequency_count.items():
    print(f"Pattern: {pattern} - Frequency: {count}")