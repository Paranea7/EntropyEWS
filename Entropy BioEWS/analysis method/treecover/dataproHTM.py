import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 指定切片文件夹路径
slices_directory = './data/Amazon1/slices'  # 替换为切片文件所在的路径

# 遍历切片文件夹中的所有 CSV 文件
for filename in os.listdir(slices_directory):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(slices_directory, filename)  # 完整路径
        print(f"Processing file: {csv_file_path}")

        # 加载 CSV 数据
        data = pd.read_csv(csv_file_path)

        # 提取数据到 NumPy 数组
        # 假设数据列的名称为 0, 1, 2,... 如果列有具体名称请根据名称提取。
        heatmap_data = data.iloc[:, 1:].values  # 提取除第一列外的所有数据

        # 创建热图
        plt.figure(figsize=(10, 8))  # 根据需要调整图形大小
        sns.heatmap(heatmap_data, cmap='Greens', center=0, cbar_kws={'label': 'Value'})

        # 设置标题和标签
        plt.title(f'Heatmap of {filename}')
        plt.xlabel('Columns')
        plt.ylabel('Rows')

        # 保存热图为文件
        heatmap_filename = f"{os.path.splitext(filename)[0]}_heatmap.png"
        plt.savefig(os.path.join(slices_directory, heatmap_filename))
        plt.close()  # 关闭图形，以释放内存
        print(f"Saved heatmap to {os.path.join(slices_directory, heatmap_filename)}")

print("所有热图已生成。")