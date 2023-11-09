import torch
from torch import nn
from model import get_model
from config.common_config import device
from torch.nn.functional import pad, log_softmax
from tqdm import tqdm
from data_loader import get_data_loader
from torch.utils.tensorboard import SummaryWriter

# 获取模型
model = get_model()
# 定义优化器
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
# 训练记录
writer = SummaryWriter(log_dir='runs/transformer_loss')
# 数据加载器
train_loader, val_loader = get_data_loader()

class TranslationLoss(nn.Module):
    """
    损失计算
    """

    def __init__(self):
        super(TranslationLoss, self).__init__()
        # 使用KLDivLoss，不需要知道里面的具体细节。
        self.criterion = nn.KLDivLoss(reduction="sum")
        self.padding_idx = 0  # <pad>编码取决于tokenizer

    def forward(self, x, target):
        """
        损失函数的前向传递
        :param x: 将Decoder的输出再经过predictor线性层之后的输出。
                  也就是Linear后、Softmax前的状态
        :param target: tgt_y。也就是label，例如[[1, 34, 15, ...], ...]
        :return: loss
        """

        """
        由于KLDivLoss的input需要对softmax做log，所以使用log_softmax。
        等价于：log(softmax(x))
        """
        x = log_softmax(x, dim=-1)

        """
        构造Label的分布，也就是将[[1, 34, 15, ...]] 转化为:
        [[[0, 1, 0, ..., 0],
          [0, ..., 1, ..,0],
          ...]],
        ...]
        """
        # 首先按照x的Shape构造出一个全是0的Tensor
        true_dist = torch.zeros(x.size()).to(device)
        # 将对应index的部分填充为1
        true_dist.scatter_(1, target.data.unsqueeze(1), 1)
        # 找出<pad>部分，对于<pad>标签，全部填充为0，没有1，避免其参与损失计算。
        mask = torch.nonzero(target.data == self.padding_idx)
        if mask.dim() > 0:
            true_dist.index_fill_(0, mask.squeeze(), 0.0)

        # 计算损失
        return self.criterion(x, true_dist.clone().detach())


criteria = TranslationLoss()  # 损失计算
torch.cuda.empty_cache()  # 清理缓存

def train():
    """
    训练函数
    :return:
    """
    for src, tgt, tgt_y, n_tokens in tqdm(train_loader):
        continue

if __name__ == '__main__':
    train()