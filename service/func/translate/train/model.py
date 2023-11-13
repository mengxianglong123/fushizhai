import torch
from torch import nn
from config.common_config import device
import config.translate_config as config
import math
from func.translate.train.data_loader import get_data_loader
from config.common_config import vocab


class PositionalEncoding(nn.Module):
    """
    位置编码器(nn.Transformer没有实现，需要手动实现)
    """
    def __init__(self, d_model, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        # 初始化Shape为(max_len, d_model)的PE (positional encoding)
        pe = torch.zeros(max_len, d_model).to(device)
        # 初始化一个tensor [[0, 1, 2, 3, ...]]
        position = torch.arange(0, max_len).unsqueeze(1)
        # 这里就是sin和cos括号中的内容，通过e和ln进行了变换
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
        )
        # 计算PE(pos, 2i)
        pe[:, 0::2] = torch.sin(position * div_term)
        # 计算PE(pos, 2i+1)
        pe[:, 1::2] = torch.cos(position * div_term)
        # 为了方便计算，在最外面在unsqueeze出一个batch
        pe = pe.unsqueeze(0)
        # 如果一个参数不参与梯度下降，但又希望保存model的时候将其保存下来
        # 这个时候就可以用register_buffer
        self.register_buffer("pe", pe)

    def forward(self, x):
        """
        x 为embedding后的inputs，例如(1,7, 128)，batch size为1,7个单词，单词维度为128
        """
        # 将x和positional encoding相加。
        x = x + self.pe[:, : x.size(1)].requires_grad_(False)
        return self.dropout(x)


class TranslationModel(nn.Module):
    """
    翻译模型
    """
    def __init__(self, d_model, src_vocab, tgt_vocab, dropout=0.1):
        """
        初始化模型
        :param d_model: 词维度大小
        :param src_vocab: 源文本词库
        :param tgt_vocab: 目标文本词库
        :param dropout: 随机失活
        """
        super(TranslationModel, self).__init__()

        # 定义原句的embedding
        self.src_embedding = nn.Embedding(len(src_vocab), d_model, padding_idx=0)  # padding_idx 取决于tokenizer
        # 定义目标句子的embedding
        self.tgt_embedding = nn.Embedding(len(tgt_vocab), d_model, padding_idx=0)
        # 定义位置编码器
        self.positional_encoding = PositionalEncoding(d_model, dropout, max_len=config.max_length)
        # 定义transformer
        self.transformer = nn.Transformer(d_model, dropout=dropout, batch_first=True, num_decoder_layers=4, num_encoder_layers=5)
        # 定义最后的预测层，这里并没有定义Softmax，而是把他放在了模型外。
        self.predictor = nn.Linear(d_model, len(tgt_vocab))

    def forward(self, src, tgt):
        """
        进行前向传递，输出为Decoder的输出。注意，这里并没有使用self.predictor进行预测，
        因为训练和推理行为不太一样，所以放在了模型外面。
        :param src: 原batch后的句子，例如[[0, 12, 34, .., 1, 2, 2, ...], ...]
        :param tgt: 目标batch后的句子，例如[[0, 74, 56, .., 1, 2, 2, ...], ...]
        :return: Transformer的输出，或者说是TransformerDecoder的输出。
        """

        """
        生成tgt_mask，即阶梯型的mask，例如：
        [[0., -inf, -inf, -inf, -inf],
        [0., 0., -inf, -inf, -inf],
        [0., 0., 0., -inf, -inf],
        [0., 0., 0., 0., -inf],
        [0., 0., 0., 0., 0.]]
        tgt.size()[-1]为目标句子的长度。
        """
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(tgt.size()[-1]).to(device)
        # 掩盖住原句中的<pad>部分，例如[[False,False,False,..., True,True,...], ...]
        src_key_padding_mask = TranslationModel.get_key_padding_mask(src)
        # 掩盖住目标句子中的<pad>部分
        tgt_key_padding_mask = TranslationModel.get_key_padding_mask(tgt)

        # 对src和tgt进行编码
        src = self.src_embedding(src)
        tgt = self.tgt_embedding(tgt)
        # 给src和tgt的token添加位置信息
        src = self.positional_encoding(src)
        tgt = self.positional_encoding(tgt)

        # 将准备好的数据库传入transformer
        out = self.transformer(src, tgt,
                               tgt_mask=tgt_mask,
                               src_key_padding_mask=src_key_padding_mask,
                               tgt_key_padding_mask=tgt_key_padding_mask)

        """
        这里直接返回transformer的结果。因为训练和推理时的行为不一样，
        所以在该模型外再进行线性层的预测。
        """
        return out


    @staticmethod
    def get_key_padding_mask(tokens):
        """
        用于key_padding_mask
        """
        return tokens == 0  # <pad>编码取决于tokenizer

def get_model():
    """
    获取模型
    :return:
    """
    # 检查是否使用检查点
    if config.model_checkpoint is not None:
        print("加载缓存模型")
        return torch.load("./runs/models/" + config.model_checkpoint).to(device)
    return TranslationModel(config.d_model, vocab, vocab).to(device)

if __name__ == '__main__':
    train_loader, val_loader = get_data_loader()
    src, tgt, tgt_y, n_tokens = next(iter(train_loader))
    src, tgt, tgt_y = src.to(device), tgt.to(device), tgt_y.to(device)
    print(src.size())
    # model = get_model()
    # model = model.to(device)
    # print(model(src, tgt).size())