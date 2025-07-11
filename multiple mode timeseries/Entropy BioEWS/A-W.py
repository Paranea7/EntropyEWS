import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 读取第一个 CSV 文件
file_path1 = './data/A_Window.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1, header=None)
# 选择从第三行到最后一行的数据
data1 = data1.iloc[1:, :]  # 这将选择第三行及其之后的所有行
print(data1)
# 读取第二个 CSV 文件
file_path2 = './data/tran5_rainfall2500_Oct30_2014.csv'
data2 = pd.read_csv(file_path2, header=None)
# 计算每一行的平均值并保存到 data2_1
data2_1 = data2.mean(axis=1)
data2_2 = data2_1.iloc[1:]
flattened_data1 = data1.values.flatten()
flattened_data2 = data2_2.values.flatten()

# 绘制图像
plt.figure(figsize=(10, 5))
plt.scatter(flattened_data2, flattened_data1, color='blue', label='Aspacedata-Waterfall', alpha=0.5)
plt.title('Aspacedata-Waterfall')
plt.xlabel('Waterfall')
plt.ylabel('Aspacedata')
plt.legend()
plt.grid()
plt.show()