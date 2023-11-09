raw_data_path = "D:\\Data\\Classical-Modern-main\\Classical-Modern-main"  # 原始数据路径地址
max_length = 200  # 文本最大长度(基于文本长度分布进行设置)
batch_size = 128  # 单批次数据大小
num_workers = 0  # 对于Windows用户，这里应设置为0，否则会出现多线程错误
use_cache = True  # 是否使用缓存
d_model = 128  # 词嵌入维度 todo 后期升级显卡后把数调大点
