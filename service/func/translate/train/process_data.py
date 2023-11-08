import os
import config.translate_config as config
import statistics
import numpy
from matplotlib import pyplot as plt


def merge_data(path, file_name):
    """
    合并所有的数据为一个文件
    source: 原文
    target: 译文
    :param path: 输入路径
    :param file_name: 输出文件名称
    :return:
    """
    # 获取目录下所有文件
    files = os.listdir(path)
    print(files)
    max_len = 0  # 最大长度
    word_lens = []
    # 遍历读取所有文件，并将其合并
    with open("../../../static/data/" + file_name, mode="w", encoding="utf-8") as out:
        line_num = 0  # 句子个数
        word_num = 0  # 单词个数
        for f in files:
            with open(path + "/" + f, mode="r", encoding="utf-8") as cur:
                lines = cur.readlines()
                for line in lines:
                    line_num += 1
                    word_num += len(line)
                    word_lens.append(len(line))
                    max_len = len(line) if max_len < len(line) else max_len  # 记录所有句子最大长度
                    out.write(line)  # 写入文件
    mean_len = word_num / line_num
    print(mean_len)  # 平均数
    print(statistics.median(word_lens))  # 中位数
    print(max_len)  # 最大长度
    plt.hist(numpy.array(word_lens), bins=200, range=(1, 300))
    plt.show()


if __name__ == '__main__':
    # merge_data(config.raw_data_path + "/" "source", "translate_source.txt")  # 原文
    merge_data(config.raw_data_path + "/" "target", "translate_target.txt")  # 译文
