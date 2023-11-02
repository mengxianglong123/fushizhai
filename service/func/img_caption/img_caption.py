from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


class ImageCaption:
    """
    图像描述
    """
    def __int__(self):
        model_id = 'damo/mplug_image-captioning_coco_base_zh'  # todo 后期这里换成本地模型加载
        self.pipeline_caption = pipeline(Tasks.image_captioning, model=model_id)

    def get_caption(self, path):
        """
        获取对图像的描述
        :param path: 图片路径(上传的图片可以暂存到某个路径下，并将文件路径传递过来，最后再删除)
        :return:
        """
        return self.pipeline_caption(path)
