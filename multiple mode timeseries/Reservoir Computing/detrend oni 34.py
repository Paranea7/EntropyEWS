import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 使用相对路径，确保路径正确
file_path = '../data/detrend.nino34.ascii.txt'  # 请替换为实际数据路径

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

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['ANOM'], linestyle='-', color='r')  # 以红色线条绘制

# 设置标题和标签
plt.title('Monthly Anomaly Over Time')
plt.xlabel('Year')
plt.ylabel('Anomaly (ANOM)')

# 设置 x 轴的时间格式，以每五年一个标记
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))  # 每五年一个标记

# 旋转 x 轴标签以提高可读性
plt.xticks(rotation=45)

plt.grid()
plt.tight_layout()
plt.show()