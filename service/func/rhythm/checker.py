import re
import config.rhythm_config as rhy_config
import pojo.check_result as check_result

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
        sentences: list = re.split(r"[,，。？?！!]", poem)
        sentences = sentences[:-1]  # 移除最后一个元素
        return sentences

    def check(self, poem: str, rule_name: str, rhy_type: int, book: list):
        '''
        校验函数
        :param poem: 用户输入的句子
        :param rule_name: 检验规则(规则名字)
        :param rhy_type: 校验形式(律诗、词牌)
        :param book: 韵书
        :return:
        '''
        res: list = []  # 最终校验结果列表
        # 1. 分割诗词
        sentences: list = self.split_poem(poem)
        # 2. 获取格律
        rule: str = ""
        if rhy_type == rhy_config.NO_RHY_TYPE:
            return res  # 不需要检验
        elif rhy_type == rhy_config.LV_RHY_TYPE:
            rule = rhy_config.meters[rule_name]  # 律诗
        elif rhy_type == rhy_config.CI_RHY_TYPE:
            rule = rhy_config.ci_meters[rule_name]  # 词牌
        else:
            return res  # 其他情况不合规矩 todo 在此处抛异常
        rule: list = rule.split(",")  # 分割为列表

        # 3. 校验平仄
        res = self.checkPingZe(sentences, rule, res, book)

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
                # 如果单个字同时发平仄音，则一定能满足平仄要求，只有以下两种情况不满足平仄要求，其他的都满足
                if tone == rhy_config.TONE_LEVEL and (standard == rhy_config.TONE_OBLIQUE or standard == rhy_config.TONE_OBLIQUE_RHYME):
                    res.append(check_result.CheckResult(i, j, True, False, []))  # 本字为平，要求为仄
                if tone == rhy_config.TONE_OBLIQUE and (standard == rhy_config.TONE_LEVEL or standard == rhy_config.TONE_LEVEL_RHYME):
                    res.append(check_result.CheckResult(i, j, True, False, []))  # 本字位仄，要求为平
        return res

    

    def getTonePattern(self, chr: str, book: list):
        '''
        获取单个字符的平仄
        备注：某多音字可能同时发平仄音，如果同时发平仄，则直接返回TOKEN_EITHER
        :param chr: 需要被检测的字符
        :param book: 指定的韵书(二维数组)
        :return:
        '''
        ret: list = []  # 存储匹配到的平仄音
        for i in range(len(book)):
            for j in range(len(book[i])):
                if chr in book[i][j]:
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



if __name__ == '__main__':
    checker = Checker()
    #print(checker.getTonePattern("去", rhy_config.rhymebooks["中华新韵"]))
    checker.check('横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。', "七绝平起首句入韵", rhy_config.LV_RHY_TYPE, rhy_config.rhymebooks["中华新韵"])
