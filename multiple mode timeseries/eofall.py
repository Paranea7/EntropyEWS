import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.decomposition import PCA

# 使用相对路径，确保路径正确
file_path = './data/detrend.nino34.ascii.txt'  # 请替换为实际数据路径

# 读取数据，跳过前两行并指定列名
data = pd.read_csv(file_path, sep=r'\s+', skiprows=2, header=None,
                   names=['YR', 'MON', 'TOTAL', 'ClimAdjust', 'ANOM'])

# 确保 YR 和 MON 是整数类型，ANOM 转换为浮点数
data['YR'] = data['YR'].astype(int)
data['MON'] = data['MON'].astype(int)
data['ANOM'] = data['ANOM'].astype(float)

# 手动构造日期列
data['Date'] = pd.to_datetime(
    {'year': data['YR'], 'month': data['MON'], 'day': 1}
)

# 将数据转换为矩阵形式，行：时间，列：单一特征
X = data['ANOM'].values.reshape(-1, 1)

# 应用EOF（PCA）分解
pca = PCA()
pca.fit(X)

# 获取特征值和特征向量
eigenvalues = pca.explained_variance_
eigenvectors = pca.components_

# 输出特征值
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:", eigenvectors)

# 绘制主成分（第一主成分作为示例）
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], X @ eigenvectors[0].T, linestyle='-', color='b', label='1st EOF Mode')
plt.title('First EOF Mode Over Time')
plt.xlabel('Year')
plt.ylabel('EOF Mode')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()