from func.translate.wenyan_translation import Translation
from flask import Blueprint, request
from pojo.result import Result

""""
文言文翻译模块
"""
translation = Blueprint("translation", __name__, url_prefix="/translation")


@translation.route("/translate", methods=['get', 'post'])
def translate():
    """
    古文翻译
    :return:
    """
    # 获取请求参数
    text = request.form.get("text")
    # 进行翻译
    res = Translation().inference(text)
    # 返回数据
    return vars(Result(200, "翻译完成", res))
