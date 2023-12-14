from env import CUR_PATH
import func.img_caption.img_caption as caption
import func.rhythm.scheduler as scheduler
from func.rhythm.checker import Checker
from func.rhythm.generator import Generator
import config.rhythm_config as config
import config.common_config as common
from pojo.result import Result
import re
from utils.rhyme_utils import obj_list_to_dict



class Creation:
    """
    创作模块
    """

    @staticmethod
    def create_poem(img_path: str, add_words: str, rhyme_type: int, rhyme_name: str, book_name: str, rhyme: str):
        """
        根据图片创作指定格律的诗词
        :param img_path: 图片路径
        :param add_words: 用户补充词汇(使用分隔符分开)
        :param rhyme_type: 格律类型(律诗，词牌)
        :param rhyme_name: 规则名称
        :param book_name: 韵书名称
        :param rhyme: 需要压的韵
        :return: 最终的格律诗词
        """
        # 1. 根据图片获取描述信息
        words = caption.ImageCaption().get_key_words(CUR_PATH + img_path)
        # todo 此处添加万物雅称转换
        # 2. 合并用户提示词
        if add_words is not None:
            words = [*words, *Creation.split_words(add_words)]
        # 3. 将词汇进行扩展
        select_words = []
        for word in words:
            select_words = [*select_words, *common.vector.get_relative_words(word, 5)]
        select_words = [*words, *select_words]
        # 4. 生成指定格式的诗词
        res = (scheduler.Scheduler(Checker(), Generator(Checker()))
               .generate_rhyme_poem(select_words,
                                    config.rhymebooks[book_name],
                                    rhyme_name, rhyme_type, rhyme))
        return Result(200, "创作完成", res)

    @staticmethod
    def check_rhyme(poem: str, rule_name: str, rule_type: int, book_name: str):
        """
        进行格律校验
        :param poem: 需要检验的诗词原文
        :param rule_name: 格律名称
        :param rule_type: 格律类型(律诗、宋词)
        :param book_name: 韵书名称
        :return: 校验结果
        """
        # 1. 对整首诗词的韵律进行推断
        rhyme = Checker().getPoemRhyme(poem, rule_name, rule_type, config.rhymebooks[book_name])
        # 2. 获取校验结果与修改建议
        err_list = scheduler.Scheduler(Checker(), Generator(Checker())).check_rhyme(poem, rule_name, rule_type, config.rhymebooks[book_name], rhyme)

        return Result(200, "校验完成", obj_list_to_dict(err_list))



    @staticmethod
    def split_words(inputs: str):
        """
        分割用户输入的词汇
        :param inputs:
        :return:
        """
        words = inputs.strip()  # 去除多余空格
        words: list = re.split(r"[" + common.split_chr + "]", words)
        if words[-1] == "":
            words = words[:-1]  # 移除最后一个元素
        return words



