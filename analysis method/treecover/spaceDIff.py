import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset

# 指定要遍历的目录
directory_path = '../../data/Africa/h20v08'  # 替换为你的目录路径
slices_directory = os.path.join(directory_path, 'space_delta')  # 目标文件夹路径

# 创建目标文件夹（如果不存在）
os.makedirs(slices_directory, exist_ok=True)

# 使用字典存储各个年份的树冠覆盖率
tree_cover_data = {}

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

                # 从第二列开始进行后减前计算
                if percent_tree_cover.ndim > 1 and percent_tree_cover.shape[1] > 1:
                    # 初始化用来存储差异结果的数组
                    differences = np.zeros((percent_tree_cover.shape[0], percent_tree_cover.shape[1] - 1))

                    # 计算每一列与前一列的差
                    for col in range(1, percent_tree_cover.shape[1]):
                        differences[:, col - 1] = percent_tree_cover[:, col] - percent_tree_cover[:, col - 1]

                    # 根据差异结果赋值
                    result_array = np.zeros_like(differences)  # 初始化结果数组
                    result_array[differences > 0] = 1
                    result_array[differences < 0] = -1
                    result_array[differences == 0] = 0

                    # 将结果数组转换为 DataFrame
                    result_df = pd.DataFrame(result_array)

                    # 获取年份信息（假设是文件名的第8到第12个字符）
                    year = filename[8:12]

                    # 生成输出文件名
                    output_filename = f"{year}.csv"
                    csv_file_path = os.path.join(slices_directory, output_filename)

                    # 保存结果到 CSV 文件
                    result_df.to_csv(csv_file_path, index=False, header=False)

                    print(f"结果已保存到 CSV 文件: {csv_file_path}")
                else:
                    print(f"文件 {filename} 的数据维度不符合要求，跳过。")