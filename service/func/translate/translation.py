import torch
from config.common_config import device
from config.common_config import tokenizer
import config.translate_config as config


class Translation:

    @staticmethod
    def get_translation_codes(model: torch.nn.Module, src_codes):
        """
        获取翻译结果的编码
        :param model: 模型
        :param src_codes: 源文本(编码后)
        :return: 翻译后的结果(编码)
        """
        # 调整为验证状态
        model.eval()
        # tgt首次为[CLS]，具体编码取决于tokenizer
        tgt = torch.tensor([[101]]).to(device)
        # 将src转为tensor,并添加batch_size维度
        src = torch.tensor(src_codes).unsqueeze(0).to(device)
        print(src)
        # 一个词一个词的预测，直到预测到[SEP]，或者达到句子最大长度
        for i in range(config.max_length):
            # 进行transformer计算
            out = model(src, tgt)
            # 放入最后的线性层进行预测,因为只需要看最后一个词，所以取`out[:, -1]`
            predict = model.predictor(out[:, -1])
            # 找出最大值的index
            y = torch.argmax(predict, dim=1)
            # 和之前的预测结果拼接到一起
            tgt = torch.concat([tgt, y.unsqueeze(0)], dim=1)
            # 如果遇到[SEP]，预测结束
            if y == 102:
                break
        return tgt.squeeze(0)

    @staticmethod
    def translate(model: torch.nn.Module, src: str):
        """
        将古文翻译问现代文
        :param model: 模型
        :param src: 源文本
        :return: 目标文本
        """
        # 将模型移动到对应设备
        model.to(device)
        # 将输入数据进行编码
        src_codes = tokenizer.encode(src)
        # 获取模型翻译编码输出
        tgt = Translation.get_translation_codes(model, src_codes).to("cpu")
        # 解码
        tgt = tokenizer.decode(tgt)
        print(tgt)
        # 清洗
        tgt = tgt.replace(" ","").replace("[CLS]","").replace("[SEP]","")
        print(tgt)
        return tgt

if __name__ == '__main__':
    """
    解决模型load报错module not found，因为模型结构包含了路径信息，尽量直接保存状态
    """
    import sys
    sys.path.append("D:\\Code\\Python\\fushizhai\\service\\func\\translate\\train")
    m = torch.load("train/runs/models/model_144000.pt").to(device)
    Translation.translate(m, "彼尝以衣冠礼乐之国自居，理当如是乎？")
