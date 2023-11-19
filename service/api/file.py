from flask import Blueprint, request
from env import CUR_PATH
from pojo.result import Result
import time

"""
文件上传模块
"""
file = Blueprint("file", __name__, url_prefix="/file")
IMG_PATH = "/static/imgs/"


@file.route("/uploadImg", methods=["POST"])
def upload_img():
    """
    上传图片
    :return:
    """
    # 获取文件
    file = request.files['file']  # 字段名称必须叫file
    # 生成文件名字(时间戳+后缀)
    file_name = str(time.time()) + "." + file.filename.split(".")[-1]
    # 保存文件
    file.save(CUR_PATH + IMG_PATH + file_name)
    return vars(Result(200, "上传成功", {"path": IMG_PATH + file_name}))



