import pandas as pd
import matplotlib.pyplot as plt

# 读取第一个 CSV 文件
file_path1 = '../data/High-resolution data/V_Window.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1, header=None)
# 选择从第三行到最后一行的数据
data1 = data1.iloc[1:]  # 这将选择第三行及其之后的所有行

# 读取第二个 CSV 文件
file_path2 = '../data/High-resolution data/tran5_rainfall2500_Oct30_2014.csv'
data2 = pd.read_csv(file_path2, header=None)

# 计算每一行的平均值并保存到 data2_1
data2_1 = data2.mean(axis=1)
# 选择从第二行到最后一行的平均值
data2_2 = data2_1.iloc[1:]

# 检查数据类型并转换为数值
data1 = pd.to_numeric(data1.values.flatten(), errors='coerce')
data2_2 = pd.to_numeric(data2_2.values, errors='coerce')

plt.figure(figsize=(10, 5))
plt.scatter(data2_2, data1, color='blue', label='Vspacedata-Waterfall', alpha=0.5)
plt.title('Vspacedata-Waterfall')
plt.xlabel('Waterfall')
plt.ylabel('Vspacedata')
plt.axhline(0, color='black', lw=0.8, ls='--')  # 添加水平线
plt.axvline(0, color='red', lw=0.8, ls='--')  # 添加垂直线
plt.xlim(min(data2_2) - 0.0001, max(data2_2) + 0.0001)  # 设置 X 轴范围
plt.ylim(min(data1) - 0.0001, max(data1) + 0.0001)  # 设置 Y 轴范围
plt.legend()
plt.grid()
plt.show()