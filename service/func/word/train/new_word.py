"""
新词发现
"""

import jiagu

jiagu.findword('poem_content.txt', 'poem_dict.txt') # 根据文本，利用信息熵做新词发现。
