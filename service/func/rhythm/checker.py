import re
import config.rhythm_config as rhy_config
from pojo.check_result import CheckResult

class Checker:
    '''
    校验器
    '''

    def __init__(self):
        pass

    def split_poem(self, poem: str):
        '''
        将用户输入的诗词分割为单句的列表
        :param poem: 用户输入的诗词
        :return: 单句列表
        '''
        poem = poem.strip()  # 去除多余空格
        sentences: list = re.split(r"[,，。？?！!]", poem)
        if sentences[-1] == "":
            sentences = sentences[:-1]  # 移除最后一个元素
        return sentences

    def getRule(self, rule_name: str, rhy_type):
        '''
        获取指定格律
        :param rule_name: 检验规则(规则名字)
        :param rhy_type: 校验形式(律诗、词牌、不校验)
        :return:
        '''
        rule: str = ""
        if rhy_type == rhy_config.NO_RHY_TYPE:
            return rule  # 不需要检验
        elif rhy_type == rhy_config.LV_RHY_TYPE:
            rule = rhy_config.meters[rule_name]  # 律诗
        elif rhy_type == rhy_config.CI_RHY_TYPE:
            rule = rhy_config.ci_meters[rule_name]  # 词牌
        else:
            return rule  # 其他情况不合规矩 todo 在此处抛异常
        rule: list = rule.split(",")  # 分割为列表
        return rule

    def check(self, poem: str, rule_name: str, rhy_type: int, book: list, rhyme: str):
        '''
        校验函数
        :param poem: 用户输入的句子
        :param rule_name: 检验规则(规则名字)
        :param rhy_type: 校验形式(律诗、词牌、不校验)
        :param book: 韵书
        :param rhyme: 韵脚
        :return:
        '''
        res: list = []  # 最终校验结果列表
        # 1. 分割诗词
        sentences: list = self.split_poem(poem)
        # 2. 获取格律
        rule: list = self.getRule(rule_name, rhy_type)
        if rule == "" : return res # 无需校验

        # 3. 校验平仄
        res = self.checkPingZe(sentences, rule, res, book)

        # 4. 韵律校验
        res = self.checkRhyme(sentences, rule, rhyme, book, res)
        return res

    def checkPingZe(self, sentences: list, rule: list, res: list, book: list):
        '''
        校验平仄
        :param sentences: 分割后用户的句子
        :param rule: 格律(分割后的列表)
        :param res: 校验结果
        :param book: 韵书
        :return:
        '''
        # 遍历句子
        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                tone = self.getTonePattern(sentences[i][j], book)  # 获取单个字的韵律
                standard = int(rule[i][j])  # 获取格律中的标准平仄
                if not self.pingze_eq(standard, tone):
                    res.append(CheckResult(i, j, True, False, []))  # 不满足平仄要求
        return res

    def pingze_eq(self, standard: int, tone: int):
        '''
        判断平仄是否相等
        :param standard: 需要满足的格律
        :param tone: 当前字符格律
        :return:
        '''
        # 如果单个字同时发平仄音，则一定能满足平仄要求，只有以下两种情况不满足平仄要求，其他的都满足
        if tone == rhy_config.TONE_LEVEL and (
                standard == rhy_config.TONE_OBLIQUE or standard == rhy_config.TONE_OBLIQUE_RHYME):
            return False  # 本字为平，要求为仄
        if tone == rhy_config.TONE_OBLIQUE and (
                standard == rhy_config.TONE_LEVEL or standard == rhy_config.TONE_LEVEL_RHYME):
            return False  # 本字位仄，要求为平
        return True  # 其他均满足平仄要求

    def checkRhyme(self, sentences: list, rule: list, rhyme: str, book: list, res: list):
        '''
        检查是否押韵
        备注：所有的韵脚统一采用同韵字组的第一个字作为唯一标识
        :param sentences: 用户分割后的原句
        :param rule: 格律
        :param rhyme: 韵脚
        :param book: 韵书
        :param res: 最终的校验结果
        :return:
        '''
        # 遍历句子
        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                if not self.rhyme_eq(int(rule[i][j]), sentences[i][j], rhyme, book):
                    res.append(CheckResult(i, j, False, True, []))  # 不满足押韵条件
        return res

    def rhyme_eq(self, rule_chr: int, c: str, rhyme: str, book: list):
        '''
        判断单个字符是否满足押韵要求
        :param rule_chr: 当前位置的格律要求
        :param c: 当前字符
        :param rhyme: 需要压的韵
        :param book: 韵书
        :return:
        '''
        if not (rule_chr == rhy_config.TONE_LEVEL_RHYME or rule_chr == rhy_config.TONE_OBLIQUE_RHYME):
            return True  # 不需要押韵，满足要求
        if rhyme == "" or rhyme is None:
            return True  # 不需要押韵
        cur_rhy = self.getRhymeGroup(c, book)  # 当前字的韵律(列表)
        if rhyme not in cur_rhy:
            return False  # 不满足押韵条件
        return True

    def getTonePattern(self, c: str, book: list):
        '''
        获取单个字符的平仄
        备注：某多音字可能同时发平仄音，如果同时发平仄，则直接返回TOKEN_EITHER
        :param c: 需要被检测的字符
        :param book: 指定的韵书(二维数组)
        :return:
        '''
        ret: list = []  # 存储匹配到的平仄音
        for i in range(len(book)):
            for j in range(len(book[i])):
                if c in book[i][j]:
                    ret.append(i)  # 将行索引添加到列表中, 0 - 平， 1 - 仄
        # 进行聚合汇总,将列表所有元素求和
        sum: int = 0
        for item in ret:
            sum = sum + item
        # 如果和为0，代表所有的都是平音
        if sum == 0:
            return rhy_config.TONE_LEVEL
        # 如果和为列表的长度，说明所有的都是仄音
        if sum == len(ret):
            return rhy_config.TONE_OBLIQUE
        # 其他情况说明平仄音都发
        return rhy_config.TONE_EITHER

    def getRhymeGroup(self, c: str, book: list):
        '''
        根据某个字获取其所在的韵组(可能有多个)
        :param c: 要查询的汉字
        :param book: 指定的韵书
        :return:
        '''
        # 最终返回结果
        res: list = []
        # 遍历韵书
        for i in range(len(book)):
            for j in range(len(book[i])):
                if c in book[i][j]:
                    res.append(book[i][j][0])  # 将同组第一个作为唯一标识
        return res

    def getPoemRhyme(self, poem: str, rule_name: str, rhy_type: int, book: list):
        '''
        推断整首诗的韵脚
        规则：所有韵脚中出现次数最多的韵即为最终结果
        :param poem: 输入诗词
        :param rule_name: 指定的韵书
        :param rhy_type: 校验形式(律诗、词牌、无需校验)
        :param book: 韵书
        :return:
        '''
        # 分割诗词
        sentences = self.split_poem(poem)
        # 获取格律
        rule = self.getRule(rule_name,rhy_type)
        # 获取所有需要押韵位置的字
        need_rhyme_list: list = []
        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                if int(rule[i][j]) == rhy_config.TONE_OBLIQUE_RHYME or int(rule[i][j]) == rhy_config.TONE_LEVEL_RHYME:
                    need_rhyme_list.append(sentences[i][j])
        # 统计出现的韵脚次数
        score: dict = {}
        for item in need_rhyme_list:
            rhs = self.getRhymeGroup(item, book)  # 获取该字的韵律
            for r in rhs:
                if r in score.keys():
                    score[r] += 1
                else:
                    score[r] = 1
        # 挑选出次数最多的那一个
        max_num: int = 0
        final_rhy: str = ""
        for key in score.keys():
            if max_num < score.get(key):
                max_num = score.get(key)
                final_rhy = key
        return final_rhy

if __name__ == '__main__':
    checker = Checker()
    # print(checker.split_poem("   横看成岭侧成非，远近高低各不同。不识庐山真面飞，只缘身在此山唯。   "))
    # checker.getPoemRhyme('横看成岭侧成非，远近高低各不同。不识庐山真面飞，只缘身在此山唯。', "七绝平起首句入韵",
    #                      rhy_config.LV_RHY_TYPE,
    #                      rhy_config.rhymebooks["中华新韵"])

    #print(checker.getTonePattern("去", rhy_config.rhymebooks["中华新韵"]))
    # checker.getRhymeGroup("云", rhy_config.rhymebooks["中华新韵"])
    s = '横看成岭侧成峰，远近高低各不韵。不识庐山真面目，只缘身在此山中。'
    res = checker.check(s,
                  "七绝平起首句入韵",
                  rhy_config.LV_RHY_TYPE,
                  rhy_config.rhymebooks["中华新韵"],
                  "庚")
    sentences = checker.split_poem(s)
    for item in res:
        item: CheckResult
        print(sentences[item.row][item.column])
