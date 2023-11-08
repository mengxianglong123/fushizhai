import torch
from torch.utils.data import DataLoader, Dataset
import torch.utils.data as Data
import config.translate_config as config
from config.common_config import tokenizer
from config.common_config import device
import os


def load_data():
    """
    加载翻译数据集
    :return: 两个列表
    """
    # 定义缓存文件存储路径
    cache_file_source = "work_dir/source.pt"
    cache_file_target = "work_dir/target.pt"
    # 如果使用缓存，且缓存文件存在，则直接加载
    if config.use_cache and os.path.exists(cache_file_source) and os.path.exists(cache_file_target):
        print("正在加载缓存文件, 请稍后...")
        return torch.load(cache_file_source, map_location="cpu"), torch.load(cache_file_target, map_location="cpu")

    # 原文数据
    with open("../../../static/data/translate_source.txt", mode="r", encoding="utf-8") as source:
        source_lines = source.readlines()
    # 翻译数据
    with open("../../../static/data/translate_target.txt", mode="r", encoding="utf-8") as target:
        target_lines = target.readlines()
    # 对数据进行编码
    source_codes = []
    target_codes = []
    for i in range(0, len(source_lines)):
        # 编码原句
        source_code = tokenizer.encode(text=source_lines[i],
                                       # 设置最大长度
                                       max_length=config.max_length,
                                       # 一律补零到max_length长度
                                       padding='max_length',
                                       # 当句子长度大于max_length时,截断
                                       truncation=True
                                       )
        # 编码译文
        target_code = tokenizer.encode(text=target_lines[i],
                                       max_length=config.max_length,
                                       padding='max_length',
                                       truncation=True
                                       )
        # 添加到对应列表中
        source_codes.append(source_code)
        target_codes.append(target_code)
    source_codes = torch.tensor(source_codes)
    target_codes = torch.tensor(target_codes)
    # 保存缓存
    if config.use_cache:
        torch.save(source_codes, cache_file_source)
        torch.save(target_codes, cache_file_target)
    # 返回列表
    return source_codes, target_codes


class TranslationDataSet(Dataset):
    """
    翻译数据的DataSet
    """

    def __init__(self):
        """
        初始化DataSet
        """
        sources, targets = load_data()
        self.sources = sources
        self.targets = targets

    def __len__(self):
        """
        返回数据总长度
        :return:
        """
        return len(self.sources)

    def __getitem__(self, idx):
        """
        按照下标返回单对数据
        :param idx: 下标
        :return:
        """
        source = self.sources[idx]
        target = self.targets[idx]
        return source, target


def split_data(dataset):
    """
    分割数据集
    :param dataset:
    :return:
    """
    # 数据总数
    total_length = len(dataset)
    # 80%作为训练集，剩下20%作为测试集
    train_length = int(total_length * 0.8)
    validation_length = total_length - train_length
    # 利用torch.utils.data.random_split()直接切分数据集, 按照80%, 20%的比例进行切分
    train_dataset, validation_dataset = Data.random_split(dataset=dataset, lengths=[train_length, validation_length])
    return train_dataset, validation_dataset


def collate_fn(batch):
    """
    将dataset的数据进一步处理，并组成一个batch。
    :param batch: 一个batch的数据，例如：
                  [([6, 8, 93, 12, ..], [62, 891, ...]),
                  ....
                  ...]
    :return: 包括src, tgt, tgt_y, n_tokens
             其中src为原句子，即要被翻译的句子
             tgt为目标句子：翻译后的句子，但不包含最后一个token
             tgt_y为label：翻译后的句子，但不包含第一个token，即<bos>
             n_tokens：tgt_y中的token数，<pad>不计算在内。
    """
    sources = []
    targets = []
    for source, target in batch:
        sources.append(source)
        targets.append(target)
    # 堆叠,将其转换为tensor
    src = torch.stack(sources)
    tgt = torch.stack(targets)

    # tgt_y是目标句子去掉第一个token，即去掉<cls>
    tgt_y = tgt[:, 1:]
    # tgt是目标句子去掉最后一个token
    tgt = tgt[:, :-1]

    # 计算本次batch要预测的token数
    n_tokens = (tgt_y != 102).sum()  # 102代表pad填充(根据tokenizer确实能)

    # 返回batch后的结果
    return src, tgt, tgt_y, n_tokens


def get_data_loader():
    """
    获取data_loader
    :return: 返回训练数据集加载器和验证数据集加载器
    """
    # 1. 分割数据集
    train_dataset, validation_dataset = split_data(TranslationDataSet())
    # 2. 训练数据集加载器
    train_loader = DataLoader(train_dataset,
                              batch_size=config.batch_size,
                              shuffle=True,
                              collate_fn=collate_fn,
                              num_workers=config.num_workers)
    # 3. 验证集数据加载器
    val_loader = DataLoader(validation_dataset,
                            batch_size=config.batch_size,
                            shuffle=False,
                            collate_fn=collate_fn,
                            num_workers=config.num_workers)

    return train_loader, val_loader


if __name__ == '__main__':
    train_loader, val_loader = get_data_loader()
    for src, tgt, tgt_y, n_tokens in train_loader:
        print(src.size())
        print(tgt.size())
        print(tgt_y.size())
        print(n_tokens)
