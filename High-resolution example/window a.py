import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = '../data/High-resolution data/A_spacedata.csv'  # 替换为您的CSV文件路径
data = pd.read_csv(file_path, header=None)  # 无列名

# 选择从第三行到最后一行的数据
data = data.iloc[2:, :]  # 这将选择第三行及其之后的所有行

# 定义滑动窗口的大小和步长
window_size =251  # 每个窗口251列
step_size = 80     # 每次移动80列

# 计算滑动窗口的平均值（忽略NaN）
means = []

# 计算可以应用窗口的起始位置
for start_col in range(0, data.shape[1] - window_size + 1, step_size):
    window = data.iloc[:, start_col:start_col + window_size]  # 提取当前窗口的所有行和指定列
    # 计算每个窗口的平均值，忽略NaN
    window_mean = window.mean().mean()  # 对窗口内的每列计算平均值，然后再计算这些平均值的平均数
    means.append(window_mean)  # 添加到列表

# 将结果转换为DataFrame
mean_df = pd.DataFrame(means, columns=['Average'])  # 创建DataFrame并指定列名
mean_df.to_csv('./data/A_Window.csv', index=False, header=True)

# 绘制折线图
plt.figure(figsize=(12, 6))
plt.plot(mean_df['Average'], marker='o', linewidth=1)  # 绘制每个窗口的平均值

# 添加图表的细节
plt.title('Rolling Average Values from Sliding Window Ignoring -9999')
# 定义要显示的特定距离
ticks = [0, 20, 40, 60, 80, 100, 120]

# 计算对应的索引
tick_indices = [int(tick / 2.49) for tick in ticks if tick / 2.49 < len(means)]

# 确保 tick_indices 的长度与 ticks 一致
if len(tick_indices) != len(ticks):
    print(f"Warning: Number of ticks ({len(ticks)}) does not match number of calculated tick indices ({len(tick_indices)})")

# 设置 x 轴为距离并应用自定义的刻度和标签，确保长度匹配
plt.xticks(ticks=tick_indices, labels=np.array(ticks)[:len(tick_indices)])  # 仅为已有的 tick_indices 设置标签
plt.xlabel('Distance (km)')  # 更新 x 轴标签
plt.ylabel('Average Value')
plt.grid()
plt.show()