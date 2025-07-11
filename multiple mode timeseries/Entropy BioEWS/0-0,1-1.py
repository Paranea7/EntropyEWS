import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件，没有列名
file_path = './data/tran5_veg_30m.csv'  # 确保文件路径正确
data = pd.read_csv(file_path, header=None)  # 读取CSV并指定header=None以生成默认列名

# 将 -9999 替换为 NaN，以处理缺失值
data.replace(-9999, np.nan, inplace=True)

# 翻转1和0
data.replace({1: 0, 0: 1}, inplace=True)  # 将1替换为0，将0替换为1

# 反转行和列
reversed_transposed_data = data.iloc[::1, ::-1]
# 创建新的 DataFrame，并初始化为 float64 类型
new_data = data.iloc[:, 1:].copy()  # 从第二列开始复制数据
diff_data = pd.DataFrame(index=new_data.index, columns=new_data.columns, dtype=np.float64)  # 初始化为 float64

# 计算每列减去前一列的值，从第二列开始
for i in range(1, new_data.shape[1]):
    current_col = new_data.iloc[:, i].astype(np.float64)  # 将当前列转换为 float64
    previous_col = new_data.iloc[:, i - 1].astype(np.float64)  # 将前一列转换为 float64

    difference = current_col - previous_col  # 先计算差值

    # 使用条件判断设置 diff_data 的值以及注释信息
    for j in range(len(difference)):
        if difference.iloc[j] == 0:
            if current_col.iloc[j] == 1 and previous_col.iloc[j] == 1:
                diff_data.iloc[j, i] = 2  # 0 由 1 - 1 得到
            elif current_col.iloc[j] == 0 and previous_col.iloc[j] == 0:
                diff_data.iloc[j, i] = 0  # 0 由 0 - 0 得到
        else:
            diff_data.iloc[j, i] = difference.iloc[j]  # 其他情况直接赋值
# 自定义 color map
cmap = sns.color_palette(["blue", "cyan", "red", "yellow"])

# 绘制新的热图
plt.figure(figsize=(12, 4))  # 设置图形的宽和高
heatmap = sns.heatmap(diff_data.T, cbar=True, cmap=cmap,
                      vmin=-1, vmax=2, annot=False)  # 设置色带的最小值和最大值

plt.title('Heatmap of Differences Between Columns')  # 添加标题
plt.xlabel('Columns')  # 添加x轴标签
plt.ylabel('Index')  # 添加y轴标签

# 自定义 colorbar 的 ticks 和标签
cbar = heatmap.collections[0].colorbar  # 获取 colorbar 对象
cbar.set_ticks([-1, 0, 1, 2])  # 设定 colorbar 刻度
cbar.set_ticklabels(['-1', '0(0-0)', '1', '0(1-1)'])  # 设定刻度标签

plt.show()  # 显示图形