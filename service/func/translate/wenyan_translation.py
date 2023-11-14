from transformers import (
    EncoderDecoderModel,
    AutoTokenizer
)
import torch
from env import CUR_PATH


# 基础环境
PRETRAINED = CUR_PATH + "/static/models/wenyan-translation"
tokenizer = AutoTokenizer.from_pretrained(PRETRAINED)
model = EncoderDecoderModel.from_pretrained(PRETRAINED)


def inference(text):
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

    inputs = tokenizer([text, ], **tk_kwargs)
    model.eval()
    with torch.no_grad():
        return tokenizer.batch_decode(
            model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                num_beams=3,
                bos_token_id=101,
                eos_token_id=tokenizer.sep_token_id,
                pad_token_id=tokenizer.pad_token_id,
                max_length=128
            ), skip_special_tokens=True)[0].replace(" ","")
