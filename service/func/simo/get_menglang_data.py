import requests
import json

"""
从孟郎诗词网拉取数据
"""
BASE_URL = "http://49.232.2.177:8081/"  # 基准地址


def get_idioms(words: list):
    """
    获取成语
    :param words:
    :return:
    """
    idioms = []
    # 遍历词汇
    for word in words:
        param = {"content": word, "pageNum": 1, "pageSize": 15}
        res = requests.get(BASE_URL + "idiom/getTotal", params=param)  # 请求
        res = json.loads(res.text)
        idioms = [*idioms, *res['data']['list']]
    return idioms


def get_words(base_words):
    """
    获取孟郎诗词网词语数据
    :param base_words:
    :return:
    """
    words = []
    # 遍历
    for word in base_words:
        param = {"searchContent": word, "pageNum": 1, "pageSize": 15}
        res = requests.get(BASE_URL + "word/getWordByContent", params=param)
        res = json.loads(res.text)
        words = [*words, *res['data']['list']]
    print(words)
    return words


def get_sentences(words):
    """
    获取孟郎诗词网名句
    :param words: 起始词汇
    :return:
    """
    sentences = []
    # 遍历
    for word in words:
        param = {"content": word, "pageNum": 1, "pageSize": 15}
        res = requests.get(BASE_URL + "home/getSentenceByContent", params=param)
        res = json.loads(res.text)
        sentences = [*sentences, *res['data']['list']]
    return sentences


if __name__ == '__main__':
    get_sentences(["春", "夏"])
