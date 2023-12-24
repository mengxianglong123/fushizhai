import func.word.word_vector
from func.word.word_vector import WordVector
import func.simo.get_menglang_data as menglang
import random
from utils.singletone import singleton


@singleton
class SiMo:
    """
    思墨堂 灵感模块
    """

    def __init__(self):
        self.word_vector: func.word.word_vector.WordVector = WordVector()

    def get_vector_words(self, word):
        """
        获取向量扩展词汇
        :param word: 起始词汇
        :return:
        """
        return self.word_vector.get_relative_words(word, 20)

    def get_inspiration_words(self, word):
        """
        获取灵感词汇
        :param word: 起始词汇
        :return:
        """
        # 1. 将起始词汇进行扩展
        words = self.get_vector_words(word)
        words = [word, *words]
        # todo 后期添加万物雅称
        # 2. 查询成语
        idioms = menglang.get_idioms(words)
        idioms = map(lambda x: x['content'], idioms)  # 过滤出详细内容
        # 3. 查询词语
        m_words = menglang.get_words(words)
        m_words = map(lambda x: x['content'], m_words)  # 过滤
        words = [*words, *idioms, *m_words]  # 合并数据
        random.shuffle(words)  # 随机打乱
        return words

    def get_inspiration_sentences(self, word):
        """
        获取灵感句子
        :return:
        """
        # 获取扩展词汇
        words = self.get_vector_words(word)
        words = [word, *words]
        # 查询句子,并打乱顺序
        sentences = menglang.get_sentences(words)
        random.shuffle(sentences)
        return sentences

    def get_inspiration_poems(self, word):
        """
        获取灵感诗词
        :param word:
        :return:
        """
        # 获取扩展词汇
        words = self.get_vector_words(word)
        words = [word, *words]
        # 查询诗词，并打乱顺序
        poems = menglang.get_poems(words)
        random.shuffle(poems)
        return poems
