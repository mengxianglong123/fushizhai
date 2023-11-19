from transformers import (
    EncoderDecoderModel,
    AutoTokenizer
)
import torch
from env import CUR_PATH


# 基础路径
PRETRAINED = CUR_PATH + "/static/models/wenyan-translation"



class Translation:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(PRETRAINED)  # 编码器
        self.model = EncoderDecoderModel.from_pretrained(PRETRAINED)  # 模型

    def inference(self, text):
        """
        文言文翻译
        :param text:
        :return:
        """
        tk_kwargs = dict(
            truncation=True,
            max_length=128,
            padding="max_length",
            return_tensors='pt')

        inputs = self.tokenizer([text, ], **tk_kwargs)
        self.model.eval()
        with torch.no_grad():
            return self.tokenizer.batch_decode(
                self.model.generate(
                    inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    num_beams=3,
                    bos_token_id=101,
                    eos_token_id=self.tokenizer.sep_token_id,
                    pad_token_id=self.tokenizer.pad_token_id,
                    max_length=128
                ), skip_special_tokens=True)[0].replace(" ", "")  # 默认只翻译一句话，不进行批量翻译
