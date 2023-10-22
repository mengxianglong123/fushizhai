'''
韵律相关配置
'''
import json
import os

# 律书
import sys

rhymebooks = None
# 律诗格律
meters = None
# 读取词牌韵律
ci_meters = None

# 常量配置
TONE_EITHER = 0
TONE_LEVEL = 1
TONE_OBLIQUE = 2
TONE_LEVEL_RHYME = 3
TONE_OBLIQUE_RHYME = 4
LV_RHY_TYPE = 0
CI_RHY_TYPE = 1
NO_RHY_TYPE = -1
# 常量解释
CONST2STR = {}
CONST2STR[TONE_EITHER]="中"
CONST2STR[TONE_LEVEL]="平"
CONST2STR[TONE_OBLIQUE]="仄"
CONST2STR[TONE_LEVEL_RHYME]="平韵"
CONST2STR[TONE_OBLIQUE_RHYME]="仄韵"
CONST2STR[LV_RHY_TYPE] = "律诗"
CONST2STR[CI_RHY_TYPE] = "词牌"
CONST2STR[NO_RHY_TYPE] = "无格律要求"

# todo 下面的代码后期移动到整个项目启动的初始化函数中
# 读取韵律
with open("../../static/rhythm/rhymebooks.json",'r',encoding='UTF-8') as f:
    rhymebooks = json.load(f)
    f.close()

# 读取律诗格律
with open("../../static/rhythm/meters.json",'r',encoding='UTF-8') as f:
    meters = json.load(f)
    f.close()

# 读取词牌格律
with open("../../static/rhythm/ci-meters.json",'r',encoding='UTF-8') as f:
    ci_meters = json.load(f)
    f.close()