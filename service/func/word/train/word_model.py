import fasttext
import jieba
import re


def remove_non_chinese(text):
    """
    去除非中文字符
    :param text:
    :return:
    """

    # 使用正则表达式匹配出所有非中文字符
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    return re.sub(pattern, '', text)

def process_data():
    """
    将数据分词后按照空格隔开,并保存
    :return:
    """
    # 加载自定义词库
    jieba.load_userdict("poem_dict.txt")
    # 读取源文件
    with open("./poem_content.txt", mode="r", encoding="utf-8") as f:
        with open("./poem_content_cut.txt", mode="w", encoding="utf-8") as o:
            # 读取所有行，并对每一行进行分词处理
            lines = f.readlines()
            for line in lines:
                cut_word = jieba.cut(remove_non_chinese(line))  # 去除多余符号，进行分词处理
                seg = ' '.join(cut_word)  # 按照空格分开
                o.write(seg + '\n')  # 写出到文件中

def train_model():
    """
    训练词向量模型
    :return:
    """
    model = fasttext.train_unsupervised("poem_content_cut.txt", "cbow", dim=300, epoch=10, lr=0.05, thread=16)
    model.save_model("poem_word_vec_cbow.model.bin")


def test_model():
    model = fasttext.load_model('poem_word_vec_cbow.model.bin')
    print(model.get_nearest_neighbors('沙漠', k=30))

if __name__ == '__main__':
    # train_model()
    test_model()
