# Pose2Carton: SJTU AI2612 Project 3 项目分支

## Pose2Carton
A educational project (e.g., using 3D pose to control 3D carton) for learning 3D vision (application of human mesh recovery) or imitation learning

## 项目分支简介
本项目全程在`Windows10(21H1)`下进行，使用`Maya 2020`.
其余环境同下文中`Requirements`，使用`open3d==0.11.1`进行无材质的匹配可视化，使用`open3d==0.10.0`进行有材质的匹配可视化。
没有对原分支的代码进行任何功能上的改动，只做了一些方便任务进行的调整。

## 个人的安装过程:
由于在`Windows10(21H1)`下进行，使用`Maya 2020`，所以直接按照官网的安装过程。
- 安装pip:下载get-pip.py 存至本地，同时将maya的下的bin路径添加至环境变量
- 之后执行mayapy get-pip.py
- 如果需要使用numpy,scipy等科学计算库，由于mayapy的python并不属于常规cpython，需要自行从源码打包。或者：
- https://pypi.anaconda.org/carlkl/simple/
- 也就是 执行`mayapy -m pip install -i https://pypi.anaconda.org/carlkl/simple numpy`


## Requirements
* code only tested on linux system (ubuntu 16.04)
* open3d==0.11.0(**if you want to try online models, use open3d 0.10.0 along with your own video recording tool to save 
visualization**)
* 在`open3d==0.11.0`以上版本，`vis.py`不会显示材质。在`open3d==0.10.0`以上版本则可以，所以推荐使用包管理工具来管理版本。
* tqdm
* opencv-python
* 对于这个分支,代码能够在`Windows10(21H1)`和`Maya 2020`条件下正常运行。

`pip install -r requirements.txt` (anaconda recommended, python3)


## Tutorials
* For maya download & install:
  - [Tutorial1](https://blog.csdn.net/otter1010/article/details/111396928)
  - [Tutorial2](https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/simplecontent/content/installing-maya-2020-ubuntu.html) (Autodesk官方安装方式)
  - [Tutorial3](https://blog.csdn.net/White_Idiot/article/details/78253004)
* For SMPL, refer to [webpage](https://smpl.is.tue.mpg.de/) or popular implementation [Minimal-IK](https://github.com/CalciferZh/Minimal-IK)
* For online model matching, refer to [OnlineMatchTutorial](doc/fbx_from_the_internet.md)


## Code structure
* [`transfer.py`](transfer.py): the main mapping file
* [`vis.py`](vis.py): visualize the mapping sequence of the corresponding mesh
* [`pose_samples`](pose_samples/): some samples of SMPL model for one frame
* [`obj_seq_id`](obj_seq_id/): some samples of SMPL model for temporal sequence
* 对于这个分支，还有`fbx`和`result`，可以用来测试带有材质的模型匹配。



# Pose2Carton 

SJTU EE228 课程大作业/AI2612 课程作业：利用3D骨架控制3D卡通人物。

# Maya 环境配置
- 本项目在`Windows10(21H1)`下进行，使用`Maya 2020`.
对于Maya 2020的环境配置，考虑到本项目不涉及到在mayapy中使用额外的科学计算库(scipy,numpy)，那么个人过程如下：
(1)在官网下载maya2020.
(2)将maya的\bin路径加入PATH环境变量中.

- 如果你使用`Ubuntu`等Unix类系统，安装`Maya 2020`,那么我在这里提供Autodesk官方的一个方案：
(https://knowledge.autodesk.com/zh-hans/support/maya/learn-explore/caas/simplecontent/content/installing-maya-2020-ubuntu.html) (Autodesk官方安装方式)

- 如果你需要在`Maya 2020`的`mayapy`中使用包管理器(pip)以及科学计算库(numpy,scipy),那么可以参照下面的做法:`Windows10(21H1)`
(1) 下载`get-pip.py`
(2) 将maya的\bin路径加入PATH环境变量中,在`get-pip.py`的目录下执行`mayapy.exe ./get-pip.py`.
(3) `mayapy -m pip install -i https://pypi.anaconda.org/carlkl/simple numpy`
注意,这里提供的包是专门为mayapy重新包装的,和其他渠道的包不同,那些渠道的包由于mayapy的一些自行修改,不能在其中加载.

# 匹配流程
以下流程可能会在各个步骤出现一些报错，但是需要的文件正确生成即可。
- 对于不自带材质信息的.fbx文件,采用如下的流程：
  * 使用`open3d==0.11.1`.
- 对于自带材质信息的.fbx文件,采用如下的流程：
  * 使用`open3d==0.10.0`.
  * 运行`mayapy fbx_parser.py model.fbx`. model.fbx由使用者自己提供.
 
# 项目结果

这里放置来自你最终匹配结果的截图， 如

![image](img/pose2carton.png)
![image](img/vis.png)


# 协议 
本项目在 Apache-2.0 协议下开源.

所涉及代码及数据的最终解释权归倪冰冰老师课题组所有.

**Group 3**
