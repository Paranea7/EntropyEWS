import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 使用相对路径，确保路径正确
file_path = '../data/nina34.data.txt'  # 请替换为实际数据路径

# 读取数据
data = pd.read_csv(file_path, sep=r'\s+', skiprows=3, header=None,
                   names=['YR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'])

# 将最后一行的倒数6个元素替换为NaN
data.iloc[-1, -2:] = np.nan

# 计算1980-2010年每个月的平均气温
monthly_1980_2010 = data.iloc[34:64, 1:]  # 对应1980-2010年
monthly_means = monthly_1980_2010.mean()  # 计算每个月的均值，结果是一个 Series

# 创建一个新的数据集，减去每个月的基准值
new_data = data.copy()

# 对每个月的值减去基准值
for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
    new_data[month] -= monthly_means[month]  # monthly_means现在是一个Series，可以按月份索引

# 一维化 new_data 从第二列到最后一列的数据
flattened_data = new_data.iloc[:, 1:].values.flatten()

# 生成年份序列
num_months = flattened_data.size
# 假设数据从1950年开始以每月为增量
years = np.arange(1950, 1950 + num_months / 12, 1/12)

# 绘图
plt.figure(figsize=(12, 6))
plt.plot(years, flattened_data, color='blue', linewidth=1)

# 设置标签
plt.xlabel('Year')
plt.ylabel('SST')
plt.title('nina34')

# 每五年设置一个 x 轴刻度
plt.xticks(np.arange(1950, 2026, 5))  # 例如：1950, 1955, ..., 2020

# 网格
plt.grid(True)

# 显示图形
plt.show()