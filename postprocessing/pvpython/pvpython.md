### 1. Motivation

1. 模拟案例过多，需要**批量处理**；
2. 其他作图软件，如ParaView**作图不美观**，批量作图**格式**、**角度**不一致；
3. 本方法**不是最优解**，如果有处理高效、作图美观的方法，希望和大家交流。



### 2. Tools

#### 2.1 pvpython

1. `pvpython`无需额外安装，只需在`~/.bashrc`中添加一行命令即可

   ```bash
   export PATH=/path_to_your_paraview/ParaView-5.10.0-MPI-Linux-Python3.9-x86_64/bin:$PATH
   ```

#### 2.2 python

1. 建议使用`miniconda`进行`python`包管理。



### 3. Line

#### 3.1 Over s single line

```python
# 用到的文件
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
import os

# 读取模拟数据
foam_name = f"{os.path.basename(os.getcwd())}.foam"

data = OpenFOAMReader(FileName=foam_name, CaseType=1) # 0表示并行之后未整合的数据，1表示整合过之后的数据

if data:
    print("\t数据读取成功.")
else:
    print("\t数据读取失败")

# 获取时间序列
time_arr = data.TimestepValues

# 更新时间线
UpdatePipeline(time=time_arr[-1])

line = PlotOverLine(Input=data)
p1_x, p1_y, p1_z = 0, 0.05, 0.005
p2_x, p2_y, p2_z = 0.1, 0.05, 0.005
line.Point1 = [p1_x, p1_y, p1_z]
line.Point2 = [p2_x, p2_y, p2_z]

# 更新数据管道
line.UpdatePipeline()

# 创建读取结果保存文件夹
root = os.getcwd()
line_folder_name = 'postdata/line'
line_folder_dir = os.path.join(root, line_folder_name)
print(line_folder_dir)
if not os.path.exists(line_folder_dir):
    os.makedirs(line_folder_dir) # 注意区分和"os.mkdir()"的区别
    print(f"\t创建{line_folder_dir}成功")
else:
    print(f"\t创建{line_folder_dir}失败")

file_name = f"line_{p1_x}_{p1_y}_{p1_z}.csv"
file_dir = os.path.join(line_folder_dir, file_name)

# 保存结果
SaveData(file_dir, line)
```

#### 3.2 Over multi lines

