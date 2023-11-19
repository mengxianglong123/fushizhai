from flask import Flask, Blueprint, request
from api import creation, file, simo
# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

# 添加蓝图
app.register_blueprint(creation.creation)  # 创作模块
app.register_blueprint(file.file)  # 文件服务
app.register_blueprint(simo.simo)

app.run(host="0.0.0.0")

