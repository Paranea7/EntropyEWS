import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 使用相对路径，确保路径正确
file_path = '../data/nino34.long.data.txt'  # 请替换为实际数据路径

# 读取数据
data = pd.read_csv(file_path, sep=r'\s+', skiprows=1, header=None,
                   names=['YR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'])

# 将最后一行的倒数6个元素替换为NaN
data.iloc[-1, -7:] = np.nan

# 计算1980-2010年每个月的平均气温
monthly_1980_2010 = data.iloc[110:140, 1:]  # 取第110到139行（对应1980-2010年）
monthly_means = monthly_1980_2010.mean()  # 计算每个月的均值，结果是一个 Series

# 创建一个新的数据集，减去每个月的基准值
new_data = data.copy()

# 对每个月的值减去基准值
for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
    new_data[month] -= monthly_means[month]  # monthly_means现在是一个Series，可以按月份索引

# 一维化 new_data 从第二列到最后一列的数据
flattened_data = new_data.iloc[:, 1:].values.flatten()

# 设置x轴的时间序列
# 假设数据是从1870年开始的，以每1/12年为单位
years = np.arange(1870, 2025, 1/12)

# 筛选1950年之后的数据
start_index = np.where(years >= 1950)[0][0]  # 找到1950年对应的索引

# 绘图
plt.figure(figsize=(12, 6))
plt.plot(years[start_index:start_index + len(flattened_data)], flattened_data[961::], color='blue', linewidth=1)

# 设置标签
plt.xlabel('Year')
plt.ylabel('SST')
plt.title('nino34')

# 设置x轴的刻度和标签
ticks = np.arange(1950, 2026, 5)  # 每5年一个刻度
plt.xticks(ticks, [f'{year}' for year in ticks])

# 网格
plt.grid(True)

# 显示图形
plt.show()