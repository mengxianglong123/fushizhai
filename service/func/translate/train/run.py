import torch
from torch import nn
from model import get_model
from config.common_config import device
import config.translate_config as config
from torch.nn.functional import pad, log_softmax
from tqdm import tqdm
from data_loader import get_data_loader
from torch.utils.tensorboard import SummaryWriter

torch.cuda.empty_cache()  # 清理缓存
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


def train():
    """
    训练函数
    :return:
    """
    # 训练步数
    step = 0
    # 每多少步保存一次模型
    save_after_step = 3000  # todo 根据实际情况进行调整
    # 调整为训练状态
    model.train()

    for epoch in range(config.epochs):
        loop = tqdm(enumerate(train_loader), total=len(train_loader))
        for src, tgt, tgt_y, n_tokens in train_loader:
            # 获取数据
            src, tgt, tgt_y = src.to(device), tgt.to(device), tgt_y.to(device)

            # 清空梯度
            optimizer.zero_grad()
            # 进行transformer计算
            out = model(src, tgt)
            # 将结果送给最后的线性层进行预测
            out = model.predictor(out)
            """
            计算损失。由于训练时我们的是对所有的输出都进行预测，所以需要对out进行reshape一下。
                    我们的out的Shape为(batch_size, 词数, 词典大小)，view之后变为：
                    (batch_size*词数, 词典大小)。
                    而在这些预测结果中，我们只需要对非<pad>部分进行，所以需要进行正则化。也就是
                    除以n_tokens。
            """
            loss = criteria(out.contiguous().view(-1, out.size(-1)), tgt_y.contiguous().view(-1)) / n_tokens
            # 计算梯度
            loss.backward()
            # 更新参数
            optimizer.step()

            # 记录日志
            writer.add_scalar(tag="train_loss",
                              scalar_value=loss.item(),
                              global_step=step)

            # 更新tqdm的值
            loop.set_description("Epoch {}/{}".format(epoch, config.epochs))
            loop.set_postfix(loss=loss.item())
            loop.update(1)

            step += 1

            del src
            del tgt
            del tgt_y

            if step != 0 and step % save_after_step == 0:
                torch.save(model, "./runs/models/" + "model_{}.pt".format(step))

        # 每训练完一个轮次，进行一次验证
        val(epoch)

    # 保存最终的模型
    torch.save(model, "./runs/models/" + f"model_final.pt")


def val(epoch):
    """
    模型验证函数
    :param epoch:
    :return:
    """
    print("======第{}轮次开始进行验证======".format(epoch))
    # 调整为验证状态
    model.eval()
    # 记录本次epoch的损失
    epoch_loss = 0.0
    with torch.no_grad():
        for src, tgt, tgt_y, n_tokens in tqdm(val_loader):
            # 获取数据
            src, tgt, tgt_y = src.to(device), tgt.to(device), tgt_y.to(device)
            # 进行transformer计算
            out = model(src, tgt)
            # 将结果送给最后的线性层进行预测
            out = model.predictor(out)
            # 损失计算
            loss = criteria(out.contiguous().view(-1, out.szie(-1)), tgt_y.contigous().view(-1))
            epoch_loss += loss.item()
            del src
            del tgt
            del tgt_y

    # 记录日志
    writer.add_scalar(tag="val_loss",
                      scalar_value=epoch_loss / len(val_loader.dataset),
                      global_step=epoch)




if __name__ == '__main__':
    train()
