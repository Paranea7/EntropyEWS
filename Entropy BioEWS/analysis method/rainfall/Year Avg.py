import os
import xarray as xr

# 文件夹路径
data_dir = '../../data/trmm1'  # 替换为你的数据目录路径

# 遍历每个年份文件夹
for year in range(2000, 2020):
    year_str = str(year)
    year_path = os.path.join(data_dir, year_str)

    # 获取该年所有月数据的文件名
    monthly_files = [os.path.join(year_path, f) for f in os.listdir(year_path) if f.endswith('.nc4')]

    # 读取第一个文件以初始化合并数据
    ds_list = []
    for file in monthly_files:
        ds_month = xr.open_dataset(file)
        ds_list.append(ds_month)

    # 合并所有月数据
    ds_all_months = xr.concat(ds_list, dim='time')  # 这里假设每个文件都有一个'time'维度

    # 计算年平均
    ds_year_avg = ds_all_months.mean(dim='time')

    # 保存年平均结果
    output_filename = os.path.join(data_dir, f'{year_str}_year_avg.nc4')
    ds_year_avg.to_netcdf(output_filename)

    print(f'Year: {year_str}, Average Saved to: {output_filename}')