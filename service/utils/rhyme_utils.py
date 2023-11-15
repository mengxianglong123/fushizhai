from env import CUR_PATH
import config.rhythm_config as config


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