import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = './data/tran5_rainfall2500_Oct30_2014.csv'
data = pd.read_csv(file_path, header=None)
# 计算每一行的平均值并保存到 data2_1
data2_1 = data.mean(axis=1)
# 将数据展平为一维
flattened_data = data2_1.values.flatten()


# 生成x轴的索引
x = range(1, len(flattened_data) + 1)

# 绘制折线图
plt.figure(figsize=(12, 6))
plt.plot(x, flattened_data, marker='o', linestyle='-')

# 添加图形的细节
plt.title('Line Plot of Flattened CSV Data')
# 定义要显示的特定距离
ticks = [0, 20, 40, 60, 80, 100, 120]

# 计算对应的索引
tick_indices = [int(tick / 2.49) for tick in ticks if tick / 2.49 < len(flattened_data)]

# 确保 tick_indices 的长度与 ticks 一致
if len(tick_indices) != len(ticks):
    print(f"Warning: Number of ticks ({len(ticks)}) does not match number of calculated tick indices ({len(tick_indices)})")

# 设置 x 轴为距离并应用自定义的刻度和标签，确保长度匹配
plt.xticks(ticks=tick_indices, labels=np.array(ticks)[:len(tick_indices)])  # 仅为已有的 tick_indices 设置标签
plt.xlabel('Distance (km)')  # 更新 x 轴标签
plt.ylabel('Values')
plt.grid()
plt.show()