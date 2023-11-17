import func.word.word_vector
from func.word.word_vector import WordVector


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
        # todo 后期添加万物雅称
        # 2. 查询成语
        
        # 3. 查询词语

