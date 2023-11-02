import fasttext


class WordVector:
    def __init__(self):
        self.model = fasttext.load_model("../../static/poem_word_vec_cbow.model.bin")

    def get_relative_words(self, word, k=20):
        """
        获取词语相关词
        :param word: 起始词
        :param k: 返回的数量
        :return:
        """
        words: list = self.model.get_nearest_neighbors(word, k=k)
        return list(map(lambda x: x[1], words))

if __name__ == '__main__':
    vec = WordVector()
    print(vec.get_relative_words("端午"))
