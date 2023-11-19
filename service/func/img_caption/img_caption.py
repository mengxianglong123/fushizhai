from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from func.img_caption.sequence_label import SequenceLabel
from utils.singletone import singleton
from env import CUR_PATH


@singleton
class ImageCaption:
    """
    图像描述
    """
    def __init__(self):
        model_id = CUR_PATH + '/static/models/img_caption'  # todo 后期这里换成本地模型加载
        self.pipeline_caption = pipeline(Tasks.image_captioning, model=model_id)
        self.seq_label = SequenceLabel()


    def get_caption(self, path):
        """
        获取对图像的描述
        :param path: 图片路径(上传的图片可以暂存到某个路径下，并将文件路径传递过来，最后再删除)
        :return:
        """
        return self.pipeline_caption(path)['caption'].replace(" ", "")

    def get_key_words(self, path):
        """
        获取图像中的关键词
        :param path: 图片路径
        :return:
        """
        labels = self.seq_label.get_tags(self.get_caption(path))  # 获取标注结果
        filter_labels = filter(lambda x: x['type'] == 'NN' or x['type'] == 'NR', labels)  # 过滤出名词
        words = map(lambda x: x['span'], list(filter_labels))  # 只提取词语
        return list(words)


if __name__ == '__main__':
    mc = ImageCaption()
    res = mc.get_key_words("D:\\Download\\rain.jpeg")
    print(res)