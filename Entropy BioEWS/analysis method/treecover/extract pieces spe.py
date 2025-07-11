import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset

# 指定要遍历的目录
directory_path = '../../data/Africa'  # 替换为你的目录路径
slices_directory = os.path.join(directory_path, 'slices')  # 目标切片文件夹路径

# 如果切片目录不存在，则创建该目录
if not os.path.exists(slices_directory):
    os.makedirs(slices_directory)

# 遍历目录中的所有 HDF 文件
for filename in os.listdir(directory_path):
    if filename.endswith('.hdf'):
        file_path = os.path.join(directory_path, filename)  # 完整路径
        print(f"Processing file: {file_path}")

        # 使用 netCDF4 打开 HDF 文件
        with Dataset(file_path, mode='r') as nc_file:
            # 检查并提取数据集
            if 'Percent_Tree_Cover' in nc_file.variables:
                percent_tree_cover = nc_file.variables['Percent_Tree_Cover'][:]  # 提取完整数组
                print(percent_tree_cover)
                print(f"Extracted data shape: {percent_tree_cover.shape}")

                # 提取中心200行数据
                if percent_tree_cover.ndim == 2:
                    middle_index = percent_tree_cover.shape[0] // 2
                    start_index = max(middle_index - 100, 0)
                    end_index = min(middle_index + 100, percent_tree_cover.shape[0])
                    data_center = percent_tree_cover[start_index:end_index, :]  # 提取中心行
                else:
                    print(f"Unexpected data dimensions: {percent_tree_cover.ndim}")
                    continue

                # 检查提取的数据是否包含 null 值
                if np.any(np.isnan(data_center)):
                    print("Warning: Extracted data contains null values.")

                # 提取数据为 DataFrame
                data_center_df = pd.DataFrame(data_center)



                # 创建 CSV 文件名
                csv_filename = f"{os.path.splitext(filename)[0]}_center_200.csv"
                csv_file_path = os.path.join(slices_directory, csv_filename)

                # 保存数据为 CSV 文件，并检查写入是否成功
                data_center_df.to_csv(csv_file_path, index=False,encoding='utf-8')
                print(f"Saved center 200 rows to {csv_file_path}")

print("所有切片数据已保存到切片文件夹中。")