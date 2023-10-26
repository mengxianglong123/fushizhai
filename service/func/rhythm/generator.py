import config.common_config as common
from transformers import BertTokenizer, GPT2LMHeadModel
import config.rhythm_config as rhy_config
from config.rhythm_config import rhymebooks
from checker import Checker
import torch
import random


class Generator:
    '''
    生成器
    '''

    def __init__(self, checker):
        '''
        初始化
        '''
        self.tokenizer = BertTokenizer.from_pretrained("uer/gpt2-chinese-poem")  # 分词器
        self.model = GPT2LMHeadModel.from_pretrained("uer/gpt2-chinese-poem")  # 模型 todo 后期可以尝试换魔搭的gpt3
        self.checker = checker  # 校验器

    def generate_poem_rhyme(self, select_words: list, book: list, rule: list, rhyme: str):
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
            # 本行要生成的句子
            sentence: str = ""
            encodes: list = []
            # 首句需要从备选词中选词
            if index == 0:  # todo 如果该句选中，也进入该流程
                rn = random.randint(0, len(select_words) - 1)  # 随机选择一个词作为起始 todo 选中后需要删除
                sentence += select_words[rn]
            # 本句起始编码
            if sentence != "":
                encodes = self.tokenizer.encode(sentence)[0:-1]
                context = torch.tensor([encodes])  # 上下文
            # else:
            #     encodes = self.tokenizer.encode(res)[-2:-1]  # todo 如果新起一句，可以将逗号作为context

            while len(sentence) < len(line):
                output = self.model(context, past_key_values=past_key_values)  # 放入模型
                past_key_values = output.past_key_values  # 历史信息
                token = self.filter(output.logits[0, -1, :],
                                    int(rule[index][len(sentence)]),  # 需要转为int类型
                                    rhyme,
                                    book)  # 筛选出满足要求的字符的编码
                context = torch.tensor([[token.unsqueeze(0)]])  # 更新上文
                sentence += self.tokenizer.decode(token)  # 将当前筛选结果添加本句中
            res = res + sentence  # 将本句拼接到全文
            sentence = ""
            # print(res)

    def filter(self, logits, chr_rule: int, rhyme: str, book: list):
        '''
        过滤出满足要求的汉字
        :param logits: 模型输出的概率向量
        :param chr_rule: 需要筛选字的格律
        :param rhyme: 韵脚
        :param book: 韵书
        :return:
        '''
        # 选取topk列表
        datas, indexs = torch.topk(logits, common.top_k, largest=True)
        # 最终返回字符编码
        token: int = -1
        # 遍历索引列表
        for item in indexs:
            item = self.tokenizer.decode(item)  # 解码为中文
            pingze_ok = False  # 是否满足平仄
            rhy_ok = False  # 是否满足韵脚
            if self.is_cn_char(item):
                continue  # 非中文字符直接跳过
            if not self.checker.pingze_eq(chr_rule, self.checker.getTonePattern(item, book)):  # 校验平仄
                continue  # 不满足直接跳过
            # 
        return torch.argmax(logits)


    def is_cn_char(self, item):
        '''
        判断是否是中文字符
        :param item:
        :return:
        '''
        if len(item) > 1:
            return False  # 只能是一个字符
        if '\u4e00' <= item <= '\u9fff':
            return True  # 是否在中文范围内
        return False


if __name__ == '__main__':
    c = Checker()
    g = Generator(c)
    print(g.is_cn_char("[SEP]"))

    # g.generate_poem_rhyme(["此处","明月"], rhymebooks["中华新韵"], c.getRule("七绝平起首句入韵", rhy_config.LV_RHY_TYPE), "云")
