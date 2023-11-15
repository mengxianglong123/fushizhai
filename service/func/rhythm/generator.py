import config.common_config as common
from transformers import BertTokenizer, GPT2LMHeadModel
import config.rhythm_config as rhy_config
from config.rhythm_config import rhymebooks
from func.rhythm.checker import Checker
import torch
import random
from utils.singletone import singleton
from env import CUR_PATH


@singleton
class Generator:
    '''
    生成器
    '''

    def __init__(self, checker):
        '''
        初始化
        '''
        self.tokenizer = common.tokenizer  # 分词器
        self.model = GPT2LMHeadModel.from_pretrained(CUR_PATH + "/static/models/gpt2-chinese-poem")  # 模型 todo 后期可以尝试换魔搭的gpt3
        self.checker = checker  # 校验器

    def generate_poem_rhyme(self, select_words: list, book: list, rule: list, rhyme: str):  # todo 清平乐有多个韵脚(既有平又有仄)
        '''
        按照格律生成完整诗词
        :param select_words: 备选词
        :param book: 韵书
        :param rule: 韵律
        :param rhyme: 韵脚(需要押的韵)
        :return:
        '''
        res: str = ""
        past_key_values = None
        context = []
        # 遍历格律
        for index, line in enumerate(rule):
            sentence: str = ""  # 本行要生成的句子
            encodes: list = []  # 编码列表
            need_add_word = random.randint(0, 1)  # 生成随机数用于判断本句是否需要加词
            # 首句需要从备选词中选词
            if index == 0 or (need_add_word == 1 and len(select_words) != 0):  # 如果该句选中，也进入该流程
                rn = random.randint(0, len(select_words) - 1)  # 随机选择一个词作为起始
                sentence += select_words[rn]  # 拼接
                select_words.pop(rn)  # 拼接后需要删除
            # 本句起始编码
            if sentence != "":
                encodes = self.tokenizer.encode(sentence)[0:-1]
                context = torch.tensor([encodes])  # 上下文
            else:
                encodes = self.tokenizer.encode(",")[-2:-1]  # 如果新起一句，可以将逗号作为context
                context = torch.tensor([encodes])

            while len(sentence) < len(line):
                output = self.model(context, past_key_values=past_key_values)  # 放入模型
                past_key_values = output.past_key_values  # 历史信息
                token = self.filter(output.logits[0, -1, :],
                                    int(rule[index][len(sentence)]),  # 需要转为int类型
                                    rhyme,
                                    book)[0]  # 筛选出满足要求的字符的编码，返回列表，默认选第一个
                context = torch.tensor([[token.unsqueeze(0)]])  # 更新上文
                sentence += self.tokenizer.decode(token)  # 将当前筛选结果添加本句中
            if res == "":
                res =  sentence
            else:
                res = res + "，" + sentence
        return res

    def filter(self, logits, chr_rule: int, rhyme: str, book: list):
        '''
        过滤出满足要求的汉字
        :param logits: 模型输出的概率向量
        :param chr_rule: 需要筛选字的格律
        :param rhyme: 韵脚
        :param book: 韵书
        :return: 满足条件的结果列表
        '''
        # 选取topk列表
        datas, indexs = torch.topk(logits, common.top_k, largest=True)  # todo 如果生成效果差，可以考虑将索引shuffle
        tokens: list = []
        # 遍历索引列表
        for item in indexs:
            c: str = self.tokenizer.decode(item)  # 解码为中文
            if not self.is_cn_char(c):
                continue  # 非中文字符直接跳过
            if not self.checker.pingze_eq(chr_rule, self.checker.getTonePattern(c, book)):  # 校验平仄
                continue  # 不满足直接跳过
            if not self.checker.rhyme_eq(chr_rule, c, rhyme, book):  # 校验韵律
                continue  # 不满足直接跳过
            tokens.append(item)  # 加入到结果集合中
        if len(tokens) > 0:
            return torch.as_tensor(tokens)  # 返回列表
        # 没有找到满足的，执行兜底函数
        chs: list = self.get_chars_by_rule(chr_rule, rhyme, book)
        random.shuffle(chs)  # 随机打乱
        while self.tokenizer.tokenize(chs[0])[0] == "[UNK]":
            random.shuffle(chs)  # 首位是未知字符需要再次打乱
        return torch.as_tensor(self.tokenizer.convert_tokens_to_ids(chs))  # 返回编码列表

    def get_chars_by_rule(self, chr_rule: int, rhyme: str, book: list):
        '''
        根据规则获取字符列表
        :param chr_rule: 字符格律
        :param rhyme: 韵脚
        :param book: 韵书
        :return: 返回满足条件的字符列表
        '''
        res: list = []
        # 没有平仄和韵律要求
        if chr_rule == rhy_config.TONE_EITHER:
            # 将所有字符返回
            for i in range(len(book)):
                for j in range(len(book[i])):
                    for k in range(len(book[i][j])):
                        res.append(book[i][j][k])
        # 只有平仄要求
        if chr_rule == rhy_config.TONE_LEVEL or chr_rule == rhy_config.TONE_OBLIQUE:
            for i in range(len(book[chr_rule - 1])):
                for j in range(len(book[chr_rule - 1][i])):
                    res.append(book[chr_rule - 1][i][j])
        # 既有平仄要求，又有韵律要求
        if chr_rule == rhy_config.TONE_LEVEL_RHYME or chr_rule == rhy_config.TONE_OBLIQUE_RHYME:
            for i in range(len(book[chr_rule - 3])):
                if book[chr_rule - 3][i][0] != rhyme:
                    continue
                for j in range(len(book[chr_rule - 3][i])):
                    res.append(book[chr_rule - 3][i][j])
        return res


    def is_cn_char(self, item):
        '''
        判断是否是中文字符
        :param item: 字符
        :return:
        '''
        if len(item) > 1:
            return False  # 只能是一个字符
        if '\u4e00' <= item <= '\u9fff':
            return True  # 是否在中文范围内
        return False

    def get_next_word(self, poem: str, book: list, rule: list, rhyme: str):
        '''
        预测输入诗词的下一个字
        :param poem: 用户输入的诗词
        :param book: 韵书
        :param rule: 格律
        :param rhyme: 需要压的韵
        :return:
        '''
        # 将诗词分割为列表
        sentences = self.checker.split_poem(poem + "X")  # X代表需要被填充的字
        # 遍历诗词，获取预测字的位置及格律要求
        chr_rule: int = 0
        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                chr_rule = int(rule[i][j])  # 一定要转为int
        # 调用模型，获取logits
        encodes = self.tokenizer.encode(poem)[0:-1]  # 编码
        context = torch.tensor([encodes])
        output = self.model(context)
        tokens = self.filter(output.logits[0, -1, :], chr_rule, rhyme, book)  # 获取建议字符列表编码
        res = self.tokenizer.decode(tokens)  # 解码为汉字
        return res.split(" ")


if __name__ == '__main__':
    c = Checker()
    g = Generator(c)
    # res = g.get_next_word("横看成岭侧成峰，远近高低各不", rhymebooks["中华新韵"], c.getRule("七绝平起首句入韵", rhy_config.LV_RHY_TYPE), "庚")
    # print(res)
    # print(g.tokenizer.tokenize("垍")[0] == "[UNK]")
    # print(g.get_chars_by_rule(rhy_config.TONE_LEVEL_RHYME, "庚", rhymebooks["中华新韵"]))

    # print(g.is_cn_char("[SEP]"))

    res = g.generate_poem_rhyme(["疏影","芙蓉"], rhymebooks["中华新韵"], c.getRule("七绝平起首句入韵", rhy_config.LV_RHY_TYPE), "庚")
    print(res)
