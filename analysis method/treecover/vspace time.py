import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset

# 指定要遍历的目录
directory_path = '../../data/Amazon/h11v08'  # 替换为你的目录路径
slices_directory = os.path.join(directory_path, 'delta')  # 目标文件夹路径

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

                # 从文件名中提取年份（假设格式为 AYYYYDOY）
                year = filename[8:12]  # 从文件名的特定位置提取年份
                tree_cover_data[year] = percent_tree_cover  # 保存数据

# 确保有至少两个年份的数据进行比较
if len(tree_cover_data) < 2:
    print("需要至少两个年份的数据进行比较。")
else:
    # 获取所有年份并排序
    years = sorted(tree_cover_data.keys())

    # 遍历年份进行后减前的计算
    for i in range(1, len(years)):
        year_current = years[i]
        year_previous = years[i - 1]

        current_cover = tree_cover_data[year_current]
        previous_cover = tree_cover_data[year_previous]

        # 计算差异
        difference = current_cover - previous_cover

        # 根据差异创建新的数组
        result_array = np.zeros_like(difference)  # 初始化结果数组
        result_array[difference < 0] = -1
        result_array[difference > 0] = 1
        result_array[difference == 0] = 0

        # 将结果数组转换为 DataFrame
        result_df = pd.DataFrame(result_array)

        # 生成输出文件名
        output_filename = f"{year_current}-{year_previous}.csv"
        csv_file_path = os.path.join(slices_directory, output_filename)

        # 保存结果到 CSV 文件
        result_df.to_csv(csv_file_path, index=False, header=False)

        print(f"结果数组已保存到 CSV: {csv_file_path}")