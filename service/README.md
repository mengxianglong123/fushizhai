# 赋诗斋-服务层

## 问题记录

### 1. Python项目的路径问题

Python在命令行启动时如果报错`module not found error`

https://blog.csdn.net/qq_37701443/article/details/84751005

核心要点，将当前的项目目录添加到sys中

```python
import sys
import os
sys.path.append(rootPath)  # 将当前项目路径添加到其中即可
```

> 最好将当前项目的根目录的绝对路径存储为变量，读取文件时按照绝对路径去读，不要使用相对路径，因为当存在引用关系时，被引用的代码文件中的代码，会在引用文件中执行，如果两者不在同一目录，还使用相对路径，可能会导致路径不一致问题。



### 2. Pytroch加载模型时报错 ModuleNotFoundError: No module named ‘models‘ 

https://blog.csdn.net/wq_0708/article/details/119614489

> 就是将直接保存模型，改为保存状态

详细的使用方式：

https://blog.csdn.net/W1995S/article/details/113099647



在官网教程[[译\]保存和加载模型](https://zj-image-processing.readthedocs.io/zh-cn/latest/pytorch/model/[译]保存和加载模型/)中给出了多种模型使用方式，其中最常用的有

1. 保存/加载`static_dict`
2. 保存/加载完整模型

对于第一种方式，只保存训练好的模型的学习参数，但是加载时需要额外提供定义的模型结构；对于第二种方式，直接使用`PyTorch`的保存和加载函数即可，不过教程中也提到了第二种方式的缺陷，就是需要在调用时**维护模型类文件的路径**，否则会出错

之前一直使用第一种方式进行模型的读写，直到遇到了下面这个问题，才真正理解了第二种方式的缺陷

`ModuleNotFoundError: No module named 'models'`

使用[ultralytics/yolov5](https://github.com/ultralytics/yolov5)的时候出现了如上错误。在网上查找了资料后发现这就是保存/加载完整模型带来的问题。参考

- [torch.load() requires model module in the same folder #3678](https://github.com/pytorch/pytorch/issues/3678)
- [ModuleNotFoundError: No module named 'models' #18325](https://github.com/pytorch/pytorch/issues/18325)
- [Pytorch.load() error:No module named ‘model’](https://discuss.pytorch.org/t/pytorch-load-error-no-module-named-model/25821)

> `PyTorch`集成了`Pickle`工具进行模型的保存和加载。如果直接保存完整模型，那么附带的需要在调用时维持和模型定义文件的相对位置，否则会出现错误
