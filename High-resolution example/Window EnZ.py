import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取存储的熵值数据
file_path1 = '../data/High-resolution data/entropyzhang.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1, header=None)
data1 = data1.iloc[1:, :]
# 设置滑动窗口的大小和步长
window_size = 251  # 每个窗口251个数据点
step_size = 80     # 每次移动80个数据点

# 初始化一个列表来存储每个窗口的结果
results = []

# 对数据进行滑动窗口处理
for start in range(0, data1.shape[0] - window_size + 1, step_size):
    end = start + window_size
    window = data1.iloc[start:end, 0]  # 选择当前窗口的数据
    window_mean = window.mean()  # 计算窗口的平均值
    results.append(window_mean)  # 将结果添加到列表中

# 将结果转换为 DataFrame
results_df = pd.DataFrame(results, columns=['Mean_Entropy'])

# 保存处理后的结果到 CSV 文件
results_df.to_csv('./data/processed_entropy_means.csv', index=False)

# 可选：绘图展示滑动窗口结果
plt.figure(figsize=(10, 5))
plt.plot(results_df['Mean_Entropy'], marker='o')
plt.title('Sliding Window Mean Entropy')
# 定义要显示的特定距离
ticks = [0, 20, 40, 60, 80, 100, 120]

# 计算对应的索引
tick_indices = [int(tick / 2.49) for tick in ticks if tick / 2.49 < len(results)]

# 确保 tick_indices 的长度与 ticks 一致
if len(tick_indices) != len(ticks):
    print(f"Warning: Number of ticks ({len(ticks)}) does not match number of calculated tick indices ({len(tick_indices)})")

# 设置 x 轴为距离并应用自定义的刻度和标签，确保长度匹配
plt.xticks(ticks=tick_indices, labels=np.array(ticks)[:len(tick_indices)])  # 仅为已有的 tick_indices 设置标签
plt.xlabel('Distance (km)')  # 更新 x 轴标签
plt.ylabel('Mean Entropy Value')
plt.grid()
plt.show()