import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset

# 定义经纬度范围
min_latitude = 3.515  # 所需最小纬度
max_latitude = 3.965  # 所需最大纬度
min_longitude = -75.195  # 所需最小经度
max_longitude = -64.323  # 所需最大经度

# 指定要遍历的目录
directory_path = './data/Amazon1'  # 替换为你的目录路径

# 用于存储所有提取的数据
all_extracted_data = []

# 遍历目录中的所有 HDF 文件
for filename in os.listdir(directory_path):
    if filename.endswith('.hdf'):
        file_path = os.path.join(directory_path, filename)  # 完整路径
        print(f"Processing file: {file_path}")

        # 使用 netCDF4 打开 HDF 文件
        with Dataset(file_path, mode='r') as nc_file:
            # 列出文件中的所有变量
            print("Datasets in the file:")
            print(nc_file.variables.keys())

            # 提取经纬度和数据
            latitudes = nc_file.variables['Latitude'][:].filled()  # 替换为实际经纬度数据集名称
            longitudes = nc_file.variables['Longitude'][:].filled()  # 替换为实际经纬度数据集名称
            data = nc_file.variables['Data_1'][:].filled()  # 替换为实际数据集名称

            # 找到经纬度范围内的索引
            lat_mask = (latitudes >= min_latitude) & (latitudes <= max_latitude)
            lon_mask = (longitudes >= min_longitude) & (longitudes <= max_longitude)

            # 提取范围内的数据
            for lat_index in np.where(lat_mask)[0]:
                for lon_index in np.where(lon_mask)[0]:
                    value = data[lat_index, lon_index]
                    all_extracted_data.append({
                        'Latitude': latitudes[lat_index],
                        'Longitude': longitudes[lon_index],
                        'Value': value,
                        'File': filename  # 记录文件名
                    })

# 转换为 DataFrame
output_df = pd.DataFrame(all_extracted_data)

# 保存结果到 CSV 文件
output_df.to_csv('extracted_data_range.csv', index=False)
print("提取的切片数据已保存到 'extracted_data_range.csv'")