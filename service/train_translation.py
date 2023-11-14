from func.translate.train.run import train
from func.translate.translation import Translation
import torch
from config.common_config import device
from func.translate.train.data_loader import get_data_loader


import sys
sys.path.append("D:\\Code\\Python\\fushizhai\\service\\func\\translate\\train")
m = torch.load("model_final.pt").to(device)
Translation.translate(m, "谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。无丝竹之乱耳，无案牍之劳形。")
