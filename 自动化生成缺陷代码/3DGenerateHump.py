# 代码逻辑：
# 1.首先需要有一个具有缺陷的铁轨和一个没有缺陷的铁轨。这两个铁轨除了缺陷的位置其余是完全一样的
# 2.将具有缺陷的铁轨中的缺陷按照最小包围方形框提取出来，范围为Area
# 3.调整Area的X和Y的范围，平移Area区域（平移的范围需要考虑缺陷的范围和平坦区域的范围）
# 3.将没有缺陷的铁轨去掉Area位置和大小的一片区域，然后将Area填充进来，可以实现在不同位置自动加入凸起的缺陷。

from scipy.io import loadmat
import scipy.io as io
import matplotlib.pyplot as plt
import scipy.io as sio
from mpl_toolkits.mplot3d import Axes3D
from utils.a import sampleShow,getUpData,getDefect,replaceDefect,getDefectArea,saveMat,OffsetDefect,stlcreator,OffsetDefectIn
import numpy as np
import copy

file = "./HaveDefect.mat"  # 有凸起缺陷缺陷的钢轨
file2="./NoDefect.mat"#正常钢轨


stlcreator(file2,"test1105")



data = loadmat(file, mat_dtype=True)
XYZ = data['XYZ']
# 输出点云形状
print(XYZ.shape)
x = XYZ[:, 0]
y = XYZ[:, 1]
z = XYZ[:, 2]
# 输出点云中z的最大值
print(max(z))
# 输出x和y的范围
print('X的范围为:', min(x), max(x))
print('Y的范围为:', min(y), max(y))
#获得不包括底部的点云数据
tmp=getUpData(XYZ)
print('顶部数据的数据量为：',tmp.shape)
# 输出x和y的范围
print('不包含底部的X的范围为:', min(tmp[:,0]), max(tmp[:,0]))
print('不包含底部的Y的范围为:', min(tmp[:,1]), max(tmp[:,1]))
#存储平坦位置的范围
flatX1,flatX2=min(tmp[:,0])+5, max(tmp[:,0])-5
flatY1,flatY2=min(tmp[:,1])+5, max(tmp[:,1])-5
flat=[flatX1,flatX2,flatY1,flatY2]
# 获取缺陷信息
dataNormal = loadmat(file2, mat_dtype=True)
XYZNormal = dataNormal['XYZ']
zNormal=max(XYZNormal[:,2])
defect=getDefect(tmp,zNormal)#根据正常钢轨的最高点找出缺陷位置
sampleShow(defect)
xleft,xright=min(defect[:,0]),max(defect[:,0])#这个就是缺陷位置的x范围
yleft,yright=min(defect[:,1]),max(defect[:,1])#这个就是缺陷位置的y范围
print('缺陷的X的范围为:', xleft, xright)
print('缺陷的Y的范围为:', yleft, yright)
#获取一片方形区域的defect
defect=getDefectArea(XYZ,defect)
sampleShow(defect)
#求出缺陷在平坦区域的可偏移范围
offsetX=[flatX1-xleft,flatX2-xright]
offsetY=[flatY1-yleft,flatY2-yright] 
print("缺陷在平坦区域的可偏移范围为：",offsetX,offsetY)
for i in range(2):

    #在范围内取随机数，得到想要偏移的值
    Xoff=np.random.uniform(offsetX[0],offsetX[1])
    Yoff=np.random.uniform(20,70)
    #根据偏移的值来偏移缺陷
    offDefect=OffsetDefect(defect,Xoff,Yoff)
    #在正常上挖去缺陷大小的一片区域,并把缺陷替换上去
    GenerateDefectRail=replaceDefect(XYZNormal,offDefect)
    sampleShow(GenerateDefectRail,20)
    # 自动生成缺陷
    def generate(x1, x2, x3):
        pass
    # 将其转化为mat文件保存
    #saveMat(GenerateDefectRail,i)
    #保存为stl文件
    #stlcreator(GenerateDefectRail,str(i))
#反向保存为凹陷
for i in range(2):
    
    #在范围内取随机数，得到想要偏移的值
    Xoff=np.random.uniform(offsetX[0],offsetX[1])
    Yoff=np.random.uniform(20,70)
    #根据偏移的值来偏移缺陷
    offDefect=OffsetDefectIn(defect,Xoff,Yoff,zNormal)
    #在正常上挖去缺陷大小的一片区域,并把缺陷替换上去
    GenerateDefectRail=replaceDefect(XYZNormal,offDefect)
    sampleShow(GenerateDefectRail,20)
    # 将其转化为mat文件保存
    #saveMat(GenerateDefectRail,i)
    #保存为stl文件
    #stlcreator(GenerateDefectRail,"In"+str(i))
#将原始的defect深拷贝到OriDefect中
#将缺陷改变大小再进行生成凸起
tmpdefect=scaleVariation
for i in range(2):
    #在范围内取随机数，得到想要偏移的值
    Xoff=np.random.uniform(offsetX[0],offsetX[1])
    Yoff=np.random.uniform(20,70)
    #根据偏移的值来偏移缺陷
    offDefect=OffsetDefect(defect,Xoff,Yoff)
    #在正常上挖去缺陷大小的一片区域,并把缺陷替换上去
    GenerateDefectRail=replaceDefect(XYZNormal,offDefect)
    #sampleShow(GenerateDefectRail,20)
    # 将其转化为mat文件保存
    #saveMat(GenerateDefectRail,i)
    #保存为stl文件
    stlcreator(GenerateDefectRail,"test"+str(i))
#将缺陷旋转后再进行生成



