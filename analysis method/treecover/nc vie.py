import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os

# 指定数据文件夹路径
folder_path = '../../data/brazil'  # 替换为你的文件夹路径

# 遍历文件夹中的每个文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.nc'):  # 只处理以 .nc4 结尾的文件
        file_path = os.path.join(folder_path, file_name)
        print(f'Processing file: {file_path}')

        # 1. 打开 nc4 文件
        dataset = nc.Dataset(file_path)

        # 2. 查看文件中的变量，找到降雨量数据的名称
        print(dataset.variables.keys())  # 查看所有可用的变量

        # 3. 假设降雨量数据存储在 'precipitation' 变量中
        #precipitation_data = dataset.variables['precipitation'][:]

        # 4. 关闭数据集
        dataset.close()

        # 5. 可视化
        #plt.figure(figsize=(10, 6))
        #plt.imshow(precipitation_data.T, cmap='Blues')  # 使用蓝色调色板
        #plt.colorbar(label='Precipitation (mm)')
        #plt.title(f'Precipitation Data Visualization - {file_name}')
        #plt.xlabel('Longitude')
        #plt.ylabel('Latitude')

        # 保存图片，您可以根据需要更改文件名
        #output_image_path = os.path.join(folder_path, f'{file_name}_visualization.png')
        #plt.savefig(output_image_path)
        #plt.close()  # 关闭图片，释放内存