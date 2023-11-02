"""
预处理数据
"""
import os
def merge(output):
    """
    合并文件为一个文件
    :param output:
    :return:
    """
    base_dir: str = "D:\\Data\\Poetry-master"
    with open(output, 'w', encoding='utf-8') as o:
        for file in os.listdir(base_dir):
            if file.endswith('.csv'):
                with open(base_dir + "\\" +file, encoding='utf-8') as i:
                    i.readline()    # the first row is the header, skipping
                    for line in i:
                        o.write(line)

def extract_content():
    """
    提取所有诗词正文并保存
    :return:
    """
    with open("poem_content.txt", mode="w", encoding="utf-8") as o:
        with open("./poem.csv", mode= "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                o.write(line.split(",")[-1])

