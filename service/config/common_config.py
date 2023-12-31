from transformers import BertTokenizer
from func.word.word_vector import WordVector
import torch
# 生成诗词时，top_k数量
top_k = 100
# 分隔符
split_chr = ",，。？?！!"
# 中文通用tokenizer
tokenizer = BertTokenizer.from_pretrained("./static/models/gpt2-chinese-poem")
# 词典
vocab = tokenizer.get_vocab()
# 设备配置
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# 词向量工具
vector = WordVector()