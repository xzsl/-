from scipy.io import loadmat
import scipy.io as io
import matplotlib.pyplot as plt
import scipy.io as sio
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import copy
#用来对3D点云作图的
def sampleShow(XYZ,i=1):
    x = XYZ[:, 0]
    y = XYZ[:, 1]
    z = XYZ[:, 2]
    # 抽样显示
    x11 = x[::i]
    x22 = y[::i]
    x33 = z[::i]
    ax = plt.subplot(111, projection='3d')
    ax.scatter(x11, x22, x33, c='r')
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()
#获取只包含铁轨数据的3D点云块
def getUpData(XYZ):
    # 输出只包含铁轨数据的范围
    tmp = []
    for point in XYZ:
        if point[2] > -50:
            tmp.append(point)
    tmp=np.array(tmp)
    return tmp #获得顶部数据
#获得缺陷的3D点云数据
def getDefect(XYZ,thre):
    # 输出只包含缺陷的数据
    tmp = []
    for point in XYZ:
        if point[2] > thre:
            tmp.append(point)
    tmp=np.array(tmp)
    return tmp #获得顶部数据
#获得缺陷的一个最小包含方形区域
def getDefectArea(XYZ,defect):
    tmp=[]
    xleft,xright=min(defect[:,0]),max(defect[:,0])
    yleft,yright=min(defect[:,1]),max(defect[:,1])
    for point in XYZ:
        if (point[0]>xleft and point[0]<xright and point[1]>yleft and point[1]<yright):
            tmp.append(point)
    tmp=np.array(tmp)  
    return tmp
#在正常钢轨上加上缺陷数据，在加之前，需要把对应位置的3D点云数据给挖掉
def replaceDefect(XYZ,defect):
    #挖掉
    tmp = []
    xleft,xright=min(defect[:,0]),max(defect[:,0])
    yleft,yright=min(defect[:,1]),max(defect[:,1])
    for point in XYZ:
        if not(point[0]>xleft and point[0]<xright and point[1]>yleft and point[1]<yright):
            tmp.append(point)
     #添加缺陷
    for point in defect:
        tmp.append(point)
    tmp=np.array(tmp)  
    return tmp
#保存为matlab的mat文件
def saveMat(XYZ,name):
    x = XYZ[:, 0]
    y = XYZ[:, 1]
    z = XYZ[:, 2]
    f = []
    for i in range(len(x)):
        f.append([x[i], y[i], z[i]])
    io.savemat(
        './GenerateHumpOut/'+str(name)+'.mat', {'XYZ': f})  # 绝对路径
#对缺陷位置进行偏移，让缺陷出现在钢轨的偏移后位置上
def OffsetDefect(defect,offX,offY):
    tmp=[]
    defe=copy.deepcopy(defect)
    for point in defe:
        point[0]=point[0]+offX
        point[1]=point[1]+offY
        tmp.append(point)
    tmp=np.array(tmp)  
    return tmp
#对缺陷位置进行偏移，并且生成对应的凹陷
def OffsetDefectIn(defect,offX,offY,zNormal):
    tmp=[]
    defe=copy.deepcopy(defect)
    for point in defe:
        point[0]=point[0]+offX
        point[1]=point[1]+offY
        point[2]=zNormal-point[2]
        tmp.append(point)
    tmp=np.array(tmp)  
    return tmp
#将3D点云保存为stl文件
import numpy as np
from mayavi import mlab
import vtk
from scipy.spatial import Delaunay

def stlcreator(pm,i):
    """根据点云数据生成stl文件"""
    # pm为三维点云数组
    x = pm[:, 0]
    y = pm[:, 1]
    z = pm[:, 2]
    xy = np.column_stack((x, y));
    tri = Delaunay(xy);    # 划分平面三角网格
    element = tri.simplices;    # 每一个三角网格所包含点的索引号
    surface = mlab.pipeline.triangular_mesh_source(x, y, z, element);    # 建立三角曲面
    surface_vtk = surface.outputs[0]._vtk_obj;    # 生成vtk文件
    stlWriter = vtk.vtkSTLWriter();    # stl生成器
    filepath="/Users/wenkaicui/Desktop/科研/虚实结合STL生成/"+i+".stl";
    stlWriter.SetFileName(filepath)    # 设置文件路径
    stlWriter.SetInputConnection(surface_vtk.GetOutputPort());    # 设置stlWriter的vtk接口
    stlWriter.Write();    # 保存曲面为stl
def scaleDefect(defect,i):
    tmp=[]
    defe=copy.deepcopy(defect)
    for point in defe:
        point[0]=point[0]*0.6*i
        point[1]=point[1]*0.6*i
        point[2]=point[2]*0.6*i
        tmp.append(point)
    tmp=np.array(tmp)
    return tmp

