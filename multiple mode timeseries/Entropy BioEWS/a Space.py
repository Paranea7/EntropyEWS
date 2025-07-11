import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取刚生成的 V_spacedata CSV 文件
file_path = './data/V_spacedata.csv'  # 确保文件路径正确
data = pd.read_csv(file_path)  # 读取CSV文件


# 创建新的 DataFrame，并初始化为 float64 类型
new_data = data.copy()  # 直接复制 V_spacedata 数据
diff_data = pd.DataFrame(index=new_data.index, columns=new_data.columns, dtype=np.float64)  # 初始化为 float64

# 计算每列减去前一列的值，从第二列开始
for i in range(1, new_data.shape[1]):
    current_col = new_data.iloc[:, i].astype(np.float64)  # 将当前列转换为 float64
    previous_col = new_data.iloc[:, i - 1].astype(np.float64)  # 将前一列转换为 float64

    # 计算相减，并排除 NaN 的影响
    diff_data.iloc[:, i] = current_col.subtract(previous_col, fill_value=0)

# 保存 diff_data 至 CSV 文件
diff_data.to_csv('./data/A_spacedata.csv', index=False, header=True)  # 不保存索引，保存列名
# 自定义 color map
cmap = sns.color_palette(["blue", 'lightblue',"white","yellow", "red"])

# 绘制新的热图
plt.figure(figsize=(12, 4))  # 设置图形的宽和高
heatmap = sns.heatmap(diff_data, cbar=True, center=0, cmap=cmap,
                       vmin=-2, vmax=2, annot=False)  # 设置色带的最小值和最大值

plt.title('Heatmap of Differences Between Columns')  # 添加标题
plt.xlabel('Columns')  # 添加x轴标签
plt.ylabel('Index')  # 添加y轴标签

# 自定义 colorbar 的 ticks 和标签
cbar = heatmap.collections[0].colorbar  # 获取 colorbar 对象
cbar.set_ticks([-2, -1, 0, 1, 2])  # 设定 colorbar 刻度
cbar.set_ticklabels(['-2','-1', '0', '1','2'])  # 设定刻度标签

plt.show()  # 显示图形
