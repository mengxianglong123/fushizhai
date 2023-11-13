from func.translate.train.run import train
from func.translate.translation import Translation
import torch
from config.common_config import device
from func.translate.train.data_loader import get_data_loader


t_loader, v_loader = get_data_loader()
for src, tgt, tgt_y, n_tokens in t_loader:
    print(tgt[0])
    print(tgt[0].size())
    print(tgt_y[0])
    print(tgt_y[0].size())
    break
