# 用到的文件
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
import os
import sys
import gc
import numpy as np

# 该函数的作用就是读取csv文件
def readData(file_path):
	try:
		file_data = np.loadtxt(file_path, delimiter=',')
		return file_data
	except Exception as e:
		print(f"Error loading data: {e}")
		return None

# 该函数的作用就是保存一条线上的数据
def getLine(code_root, p1, p2, line_resolution=1000):
	
	# 读取模拟数据
	case_name = os.path.basename(code_root) # 'testcase'
	foam_name = f"{os.path.basename(code_root)}.foam" # 'testcase.foam'

	data = OpenFOAMReader(FileName=foam_name, CaseType=1) # 0表示并行之后未整合的数据，1表示整合过之后的数据

	if data:
	    print(f"\t读取{p1}成功.")
	else:
	    print(f"\t读取{p1}失败")

	# 获取时间序列
	time_arr = data.TimestepValues

	# 更新时间线
	UpdatePipeline(time=time_arr[-1])

	line = PlotOverLine(Input=data)
	line.Resolution = line_resolution
	line.Point1 = [p1[0], p1[1], p1[2]]
	line.Point2 = [p2[0], p2[1], p2[2]]

	# 更新数据管道
	line.UpdatePipeline()

	# 创建读取结果保存文件夹
	line_folder_name = 'postdata/line'
	line_folder_path = os.path.join(code_root, line_folder_name)
	if not os.path.exists(line_folder_path):
	    os.makedirs(line_folder_path) # 注意区分和"os.mkdir()"的区别
	    print(f"\t创建{line_folder_path}成功")

	file_name = f"{case_name}_line_{p1[0]}_{p1[1]}_{p1[2]}.csv"
	file_dir = os.path.join(line_folder_path, file_name)

	# 保存结果
	SaveData(file_dir, line)
	print(f"\t保存{p1}成功")

	gc.collect() # 非常重要

if __name__ == "__main__":

	code_root = os.getcwd() # 获取代码所在文件夹的路径
	file_path = sys.argv[1] # 获取存储位置信息的csv文件路径

	file_data = readData(file_path) # 读取csv文件
	rows = file_data.shape[0] # csv文件行数

	if file_data.ndim == 1:
		p1 = file_data[:3]
		p2 = file_data[3:]
		getLine(code_root, p1, p2)
	else:
		for i in range(rows):
			p1 = file_data[i,:3]
			p2 = file_data[i,3:]
			getLine(code_root, p1, p2)