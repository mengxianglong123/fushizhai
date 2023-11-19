import func.simo.simo as simo_func
from flask import Blueprint, request
from pojo.result import Result

"""
思墨堂
"""
simo = Blueprint("simo", __name__, url_prefix="/simo")


@simo.route("/getWords/<int:num>/<string:word>")
def get_inspiration_words(num, word):
    """
    获取灵感词汇
    :param num: 数据条数
    :param word: 起始词汇
    :return:
    """
    words = simo_func.SiMo().get_inspiration_words(word)
    if num <= len(words):
        words = words[0:num]  # 截取数据
    return vars(Result(200, "查询成功", words))


@simo.route("/getSentences/<int:num>/<string:word>")
def get_inspiration_sentences(num, word):
    """
    获取灵感句子
    :param num: 数据条数
    :param word: 起始词汇
    :return:
    """
    sentences = simo_func.SiMo().get_inspiration_sentences(word)
    if num <= len(sentences):
        sentences = sentences[0:num]
    return vars(Result(200, "查询成功", sentences))


@simo.route("/getPoems/<int:num>/<string:word>")
def get_inspiration_poems(num, word):
    """
    获取灵感诗词
    :param num: 数据条数
    :param word: 起始词汇
    :return:
    """
    poems = simo_func.SiMo().get_inspiration_poems(word)
    if num <= len(poems):
        poems = poems[0:num]
    return vars(Result(200, "查询成功", poems))
