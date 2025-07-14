import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = '../data/High-resolution data/V_spacedata.csv'  # 替换为您的CSV文件路径
data = pd.read_csv(file_path, header=None)  # 无列名

# 选择从第三行到最后一行的数据
data = data.iloc[2:, :]  # 选择第三行及其之后的所有行

# 定义一个计算熵的函数
def calculate_entropy(column):
    # 计算每个值的频率
    value_counts = column.value_counts(normalize=True)
    # 使用熵的公式计算熵值
    entropy = -np.sum(value_counts * np.log2(value_counts))
    return entropy

# 计算在每一列的熵值
entropy_values = data.apply(calculate_entropy)

# 将熵值转换为一维数组
entropy_series = entropy_values.values.flatten()
# 打印出每一列的熵值
print("每一列的熵值: ", entropy_series)

# 保存熵值到 CSV 文件
entropy_df = pd.DataFrame(entropy_values)
entropy_df.to_csv('../data/High-resolution data/entropyzhang.csv', index=False)

# 可选：绘图展示熵值
plt.figure(figsize=(10, 5))
plt.plot(entropy_series, marker='o')
plt.title('Entropy of Each Column')
plt.xlabel('Column Index')
plt.ylabel('Entropy Value')
plt.grid()
plt.show()