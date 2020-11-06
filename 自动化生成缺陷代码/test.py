import scipy.io as sio  
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

a = [1,2,3,4,5]
b = [1,2,3,4,5]
c = [1,2,3,4,5]

ax=plt.subplot(111,projection='3d')
ax.scatter(a,b,c,c='r')
ax.set_zlabel('Z') 
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()