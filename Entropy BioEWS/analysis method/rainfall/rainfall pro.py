import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata

# 指定数据文件夹路径
folder_path = '../../data/trmmaf'  # 替换为你的文件夹路径

# 遍历文件夹中的每个文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.nc4'):  # 只处理以 .nc4 结尾的文件
        file_path = os.path.join(folder_path, file_name)
        print(f'Processing file: {file_path}')

        # 1. 打开 nc4 文件
        dataset = nc.Dataset(file_path)

        # 2. 查看文件中的变量，找到降雨量数据的名称
        print(dataset.variables.keys())  # 查看所有可用的变量

        # 3. 假设降雨量数据存储在 'precipitation' 变量中
        precipitation_data = dataset.variables['precipitation'][:]

        # 4. 关闭数据集
        dataset.close()

        # 5. 进行插值
        # 使用转置的降雨量数据
        precipitation_data_T = precipitation_data.T
        original_height, original_width = precipitation_data_T.shape

        # 创建目标网格
        target_y = np.linspace(0, original_height - 1, 200)  # 200 个点
        target_x = np.linspace(0, original_width - 1, 4800)  # 4800 个点
        target_xx, target_yy = np.meshgrid(target_x, target_y)

        # 创建原始网格
        original_x = np.arange(original_width)
        original_y = np.arange(original_height)
        original_xx, original_yy = np.meshgrid(original_x, original_y)

        # 使用线性插值法插值数据
        interpolated_precipitation = griddata((original_xx.flatten(), original_yy.flatten()),
                                              precipitation_data_T.flatten(),
                                              (target_xx, target_yy),
                                              method='linear')

        # 6. 保存原始数据的可视化
        plt.figure(figsize=(10, 6))
        plt.imshow(precipitation_data_T, cmap='Blues', aspect='auto')  # 原始数据可视化
        plt.colorbar(label='Precipitation (mm)')
        plt.title(f'Original Precipitation Data Visualization - {file_name}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        # 保存原始数据图像
        original_image_path = os.path.join(folder_path, f'{file_name}_original_visualization.png')
        plt.savefig(original_image_path)
        plt.close()  # 关闭图片，释放内存

        # 7. 保存插值后的数据的可视化
        plt.figure(figsize=(10, 6))
        plt.imshow(interpolated_precipitation, cmap='Blues', aspect='auto')  # 插值后的数据可视化
        plt.colorbar(label='Precipitation (mm)')
        plt.title(f'Interpolated Precipitation Data Visualization - {file_name}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        # 保存插值后数据图像
        interpolated_image_path = os.path.join(folder_path, f'{file_name}_interpolated_visualization.png')
        plt.savefig(interpolated_image_path)
        plt.close()  # 关闭图片，释放内存