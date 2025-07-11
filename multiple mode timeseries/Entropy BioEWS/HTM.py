import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# 读取CSV文件
file_path = './data/tran5_veg_30m.csv'
data = pd.read_csv(file_path)
# 将-9999替换为NaN，以便后续处理
data.replace(-9999, np.nan, inplace=True)
# 翻转1和0
data.replace({1: 0, 0: 1}, inplace=True)  # 将1替换为0，将0替换为1
# 查看数据的前几行以理解数据结构
print(data.head())

# 如果数据是数值类型且没有行列索引, 则可以直接绘制热力图
# 如果需要转置或获取特定的数据列，请进行相应的调整
# 假设 CSV 文件中没有特定的索引列或列名称
# 直接转换为数组
heatmap_data = data.values[::1, ::-1]  # 反转行和列

# 创建一个白色到绿色的调色盘
cmap = LinearSegmentedColormap.from_list("custom_green", ["lightgreen", "green"])

# 绘制热力图
plt.figure(figsize=(12, 10))  # 设置图形的大小
sns.heatmap(heatmap_data.T, cmap=cmap, cbar=True, square=True,yticklabels=False)  # 使用自定义调色盘
plt.title('Heatmap from CSV Data')
plt.xlabel('Column Index')  # 根据实际需要修改标签
plt.ylabel('Row Index')     # 根据实际需要修改标签
plt.show()