import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 读取第一个 CSV 文件
file_path1 = './data/processed_entropy_means.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1, header=None)
# 选择从第三行到最后一行的数据
data1 = data1.iloc[1:]  # 这将选择第三行及其之后的所有行
print("data1:\n", data1)

# 读取第二个 CSV 文件
file_path2 = './data/tran5_rainfall2500_Oct30_2014.csv'
data2 = pd.read_csv(file_path2, header=None)

# 计算每一行的平均值并保存到 data2_1
data2_1 = data2.mean(axis=1)
data2_2 = data2_1.iloc[1:]

# 检查数据类型并转换为数值
data1 = pd.to_numeric(data1.values.flatten(), errors='coerce')
data2_2 = pd.to_numeric(data2_2.values, errors='coerce')

# 绘制主图
plt.figure(figsize=(12, 6))
plt.scatter(data2_2, data1, color='blue', label='H-Waterfall', alpha=0.5)
plt.title('H-Waterfall')
plt.xlabel('Waterfall')
plt.ylabel('H')
plt.axhline(0, color='black', lw=0.8, ls='--')  # 添加水平线
plt.axvline(0, color='red', lw=0.8, ls='--')  # 添加垂直线
plt.xlim(min(data2_2) - 0.1, max(data2_2) + 0.1)  # 设置 X 轴范围
plt.ylim(min(data1) - 0.1, max(data1) + 0.1)  # 设置 Y 轴范围
plt.legend()
plt.grid()

# 添加局部放大图
# 创建局部放大图的坐标位置，定义位置和大小
axins = inset_axes(plt.gca(), width="30%", height="30%", loc='lower right')

# 在局部放大图中绘制散点
axins.scatter(data2_2, data1, color='blue', alpha=0.5)
axins.set_xlim(720, 760)  # 设置局部放大的 X 轴范围
axins.set_ylim(0.4, 0.6)  # 设置局部放大图的 Y 轴范围
axins.axhline(0, color='black', lw=0.8, ls='--')  # 添加水平线
axins.axvline(0, color='red', lw=0.8, ls='--')  # 添加垂直线
axins.grid()

plt.show()