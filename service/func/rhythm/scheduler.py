from pojo.check_result import CheckResult
import config.common_config as common
from func.rhythm.checker import Checker
from func.rhythm.generator import Generator
import config.rhythm_config as rhy_config
from utils.singletone import singleton


@singleton
class Scheduler:
    '''
    调度器
    '''

    def __init__(self, checker: Checker, generator: Generator):
        self.checker = checker
        self.generator = generator

    def split_poem_err(self, poem: str, err: CheckResult):
        '''
        根据校验错误分割诗词，返回的结果不包含错误的字符
        :param poem: 诗词
        :param err:
        :return:
        '''
        row: int = 0
        column: int = 0
        # 遍历诗词，进行分割
        for i in range(len(poem)):
            if row == err.row and column == err.column:
                return poem[0: i]  # 找到指定坐标，进行切割(不包含错误字符)
            if poem[i] in common.split_chr:
                row += 1
                column = 0
            else:
                column += 1
        return None

    def check_rhyme(self, poem: str, rule_name: str, rhy_type: int, book: list, rhyme: str):
        '''
        对诗词格律进行校验，并获取修改建议
        :param poem: 输入诗词
        :param rule_name: 校验规则
        :param rhy_type: 校验形式(律诗、词牌、不校验)
        :param book: 韵书
        :param rhyme: 韵脚
        :return:
        '''
        # 获取检验结果
        err_list = self.checker.check(poem, rule_name, rhy_type, book, rhyme)
        # 遍历校验结果，依次获取修改建议
        for err in err_list:
            err: CheckResult
            # 获取错误位置前的截取结果
            s_split = self.split_poem_err(poem, err)
            # 获取修改建议，从将其加入到当前错误对象中
            err.suggests = self.generator.get_next_word(s_split, book, self.checker.getRule(rule_name, rhy_type), rhyme)
        return err_list

    def generate_rhyme_poem(self, select_words: list, book: list, rule_name: str, rule_type: int, rhyme: str):
        '''
        按照格律生成诗词
        :param select_words: 候选词
        :param book: 韵书
        :param rule_name: 格律名称
        :param rule_type: 校验形式(律诗、词牌、不校验)
        :param rhyme: 韵脚
        :return:
        '''
        return self.generator.generate_poem_rhyme(select_words, book, self.checker.getRule(rule_name, rule_type), rhyme)


if __name__ == '__main__':
    poem = "折戟沉沙铁未销，自将磨洗认前朝。东风不与周郎便，铜雀春深锁二韵。"
    c = Checker()
    g = Generator(c)
    s = Scheduler(c, g)
    err_list = s.check_rhyme(poem, "七绝仄起首句入韵",
                             rhy_config.LV_RHY_TYPE,
                             rhy_config.rhymebooks["平水韵"],
                             "萧")
    sentences = c.split_poem(poem)
    for err in err_list:
        err: CheckResult
        print(sentences[err.row][err.column] + str(err.is_pingze_err) + str(err.is_meter_err))
        print(err.suggests)
