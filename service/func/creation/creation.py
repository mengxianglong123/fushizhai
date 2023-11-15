from env import CUR_PATH
import func.img_caption.img_caption as caption
import func.rhythm.scheduler as scheduler
from func.rhythm.checker import Checker
from func.rhythm.generator import Generator
import config.rhythm_config as config
import config.common_config as common
import re

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
        return res



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



