from env import CUR_PATH
import config.rhythm_config as config
from func.rhythm.checker import Checker


def get_rhyme_rules(rhyme_type: int):
    """
    获取某类型下的所有韵律名称
    :param rhyme_type: 韵律类型(宋词、律诗)
    :return: 韵律名称列表
    """
    if rhyme_type == config.LV_RHY_TYPE:
        return list(config.meters.keys())
    elif rhyme_type == config.CI_RHY_TYPE:
        return list(config.ci_meters.keys())
    else:
        return None


def get_rhymebooks_name():
    """
    获取所有的韵书名称
    :return:
    """
    return list(config.rhymebooks.keys())


def obj_list_to_dict(obj_list):
    """
    将对象列表转为字典列表
    :param obj_list:
    :return:
    """
    dict_list = []
    for obj in obj_list:
        dict_list.append(vars(obj))
    return dict_list


def get_poem_can_rhyme(rhy_type: int, rhy_name: str, book_name: str):
    """
    获取某首诗可以压的韵
    :param rhy_type: 规则类型
    :param rhy_name: 规则名称
    :param book_name: 韵书名称
    :return:
    """
    # 获取规则
    rules = Checker().getRule(rhy_name, rhy_type)
    # 遍历规则，推断平仄
    level_num = 0  # 平韵数量
    oblique_num = 0  # 仄韵数量
    for rule in rules:
        if str(config.TONE_LEVEL_RHYME) in rule:
            level_num += 1
        if str(config.TONE_OBLIQUE_RHYME) in rule:
            oblique_num += 1
    # 根据结果推断平仄
    rhyme: int
    if level_num > 0 and oblique_num == 0:
        rhyme = 0
    elif level_num == 0 and oblique_num > 0:
        rhyme = 1
    else:
        return None

    # 获取对应平仄后的韵组的首个字
    book: list = config.rhymebooks[book_name][rhyme]
    chs = []
    for item in book:
        chs.append(item[0])
    return chs

