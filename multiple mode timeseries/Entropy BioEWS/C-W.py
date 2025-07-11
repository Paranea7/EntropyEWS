import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 读取第一个 CSV 文件
file_path1 = './data/rolling_average_values.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1, header=None)

# 读取第二个 CSV 文件
file_path2 = './data/tran5_rainfall2500_Oct30_2014.csv'
data2 = pd.read_csv(file_path2, header=None)

# 计算每一行的平均值并保存到 data2_1
data2_1 = data2.mean(axis=1)

# 将数据展平为一维
flattened_data1 = data1.values.flatten()
flattened_data2 = data2_1.values.flatten()

# 绘制主图
plt.figure(figsize=(10, 5))
plt.scatter(flattened_data2, flattened_data1, color='blue', label='Vegetation vs Waterfall', alpha=0.5)
plt.title('Vegetation vs Waterfall')
plt.xlabel('Waterfall')
plt.ylabel('Vegetation')
plt.legend()
plt.grid()

# 创建局部放大图的坐标位置，定义位置和大小
axins = inset_axes(plt.gca(), width="30%", height="30%", loc='upper right')

# 绘制局部放大图
axins.scatter(flattened_data2, flattened_data1, color='blue', alpha=0.5)
axins.set_xlim(710, 770)  # 设置局部放大图 x 轴范围


# 添加局部放大图的边框
axins.set_xticks([])  # 如果不需要显示局部放大图的 x 轴刻度，可以注释这一行
axins.set_yticks([])  # 如果不需要显示局部放大图的 y 轴刻度，可以注释这一行
# 画出主图与局部图之间的关系
plt.draw()
plt.show()