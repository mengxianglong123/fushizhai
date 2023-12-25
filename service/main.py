from flask import Flask, Blueprint, request
from api import creation, file, simo, translation
from flask_cors import CORS

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)
CORS(app)

# 添加蓝图
app.register_blueprint(creation.creation)  # 创作模块
app.register_blueprint(file.file)  # 文件服务
app.register_blueprint(simo.simo)
app.register_blueprint(translation.translation)
# todo 添加初始化，将所有模型加载进内存
app.run(host="0.0.0.0")