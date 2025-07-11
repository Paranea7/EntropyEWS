import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
file_path = '../data/High-resolution data/V_spacedata.csv'
data = pd.read_csv(file_path, header=None)
data = data.iloc[2:, :]  # 选择从第三行到最后一行的数据

# 定义滑动窗口的大小和步长
window_size = 251
step_size = 80
means = []

# 计算滑动窗口的平均值
for start_col in range(0, data.shape[1] - window_size + 1, step_size):
    window = data.iloc[:, start_col:start_col + window_size]
    window_mean = window.mean().mean()
    means.append(window_mean)

if data.shape[1] % step_size > 0:
    start_col = data.shape[1] - window_size
    if start_col >= 0:
        last_window = data.iloc[:, start_col:]
        last_window_mean = last_window.mean().mean()
        means.append(last_window_mean)

mean_df = pd.DataFrame(means, columns=['Average'])

# 读取第二个CSV文件
file_path_veg = '../data/High-resolution data/tran5_veg_30m.csv'
data_veg = pd.read_csv(file_path_veg, header=None)
data_veg.replace(-9999, np.nan, inplace=True)
data_veg.replace({1: 0, 0: 1}, inplace=True)
reversed_transposed_data = data_veg.iloc[::1, ::-1]
new_data = data_veg.iloc[:, 1:].copy()
diff_data = pd.DataFrame(index=new_data.index, columns=new_data.columns, dtype=np.float64)

# 计算每列减去前一列的值
for i in range(1, new_data.shape[1]):
    current_col = new_data.iloc[:, i].astype(np.float64)
    previous_col = new_data.iloc[:, i - 1].astype(np.float64)
    diff_data.iloc[:, i] = current_col - previous_col

# 创建新图形并绘制三个子图
fig, axs = plt.subplots(3, 1, figsize=(12, 18), gridspec_kw={'hspace': 0.4})  # 创建3行1列子图并设置间距

# 第一个子图：滑动窗口平均值折线图
axs[0].plot(mean_df['Average'], marker='o', linewidth=1)
axs[0].set_title('Rolling Average Values from Sliding Window')
axs[0].set_xlabel('Window Number')
axs[0].set_ylabel('Average Value')

# 第二个子图：热图，不显示 colorbar
cmap = sns.color_palette(["blue", "white", "red"])
sns.heatmap(diff_data.T, ax=axs[1], cbar=False, center=0, cmap=cmap, vmin=-1, vmax=1, annot=False)
axs[1].set_title('Heatmap of Differences Between Columns')
axs[1].set_xlabel('Columns')
axs[1].set_ylabel('Index')
# 关闭 y 轴索引
axs[1].tick_params(axis='y', which='both', left=False)

# 第三个子图：自定义热图，不显示 colorbar
heatmap_data = data_veg.values[::1, ::-1]
cmap_custom = sns.color_palette(["lightgreen", "green"])
sns.heatmap(heatmap_data.T, ax=axs[2], cbar=False, square=True, yticklabels=False, cmap=cmap_custom)
axs[2].set_title('Heatmap from CSV Data')
axs[2].set_xlabel('Column Index')
axs[2].set_ylabel('Row Index')
# 关闭 y 轴索引
axs[2].tick_params(axis='y', which='both', left=False)


plt.show()