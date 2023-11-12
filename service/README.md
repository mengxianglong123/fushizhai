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

> 最后将当前项目的根目录的绝对路径存储为变量，读取文件时按照绝对路径去读，不要使用相对路径，因为当存在引用关系时，被引用的代码文件中的代码，会在引用文件中执行，如果两者不在同一目录，还使用相对路径，可能会导致路径不一致问题。



### 2. Pytroch加载模型时报错 ModuleNotFoundError: No module named ‘models‘ 

https://blog.csdn.net/wq_0708/article/details/119614489

> 就是将直接保存模型，改为保存状态

详细的使用方式：

https://blog.csdn.net/W1995S/article/details/113099647

