from flask import Blueprint, request
from func.creation.creation import Creation
import utils.rhyme_utils as rhyme_utils
from pojo.result import Result

"""
创作模块
"""
creation = Blueprint("creation", __name__, url_prefix="/creation")


@creation.route("/createRhymePoem", methods=['get', 'post'])
def create_rhyme_poem():
    """
    创作格律诗词
    :return:
    """
    # 获取请求参数
    img_path = request.form.get("imgPath")
    add_words = request.form.get("addWords")
    rhyme_type: int = int(request.form.get("rhymeType"))  # 转int
    rhyme_name = request.form.get("rhymeName")
    book_name = request.form.get("bookName")
    rhyme = request.form.get("rhyme")
    # 响应请求
    return vars(Creation.create_poem(img_path, add_words, rhyme_type, rhyme_name, book_name, rhyme))


@creation.route("/checkPoemRhyme", methods=['get', 'post'])
def check_poem_rhyme():
    """
    校验诗词格律，并返回校验结果和修改意见
    :return:
    """
    # 获取请求参数
    poem = request.form.get("poem")
    rule_name = request.form.get("ruleName")
    rule_type = int(request.form.get("ruleType"))  # 转int
    book_name = request.form.get("bookName")
    # 响应请求
    return vars(Creation.check_rhyme(poem, rule_name, rule_type, book_name))


@creation.route("/getRhymeBookNames")
def get_rhyme_book_names():
    """
    获取所有韵书名称
    :return:
    """
    return vars(Result(200, "查询成功", rhyme_utils.get_rhymebooks_name()))


@creation.route("/getRhymeRulesByType/<int:rhyme_type>")
def get_rhyme_rules(rhyme_type):
    """
    获取某类型下的所有韵律规则名称
    :return:
    """
    names = rhyme_utils.get_rhyme_rules(rhyme_type)
    return vars(Result(200, "查询完成", names))
