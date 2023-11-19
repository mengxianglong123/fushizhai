from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
# Version less than 1.1 please use TokenClassificationPreprocessor
from modelscope.preprocessors import TokenClassificationTransformersPreprocessor
from utils.singletone import singleton
from env import CUR_PATH


@singleton
class SequenceLabel:
    def __init__(self):
        model_id = CUR_PATH + '/static/models/sequence_label'
        model = Model.from_pretrained(model_id)
        tokenizer = TokenClassificationTransformersPreprocessor(model.model_dir)
        self.pipeline_ins = pipeline(task=Tasks.token_classification, model=model, preprocessor=tokenizer)

    def get_tags(self, input):
        """
        获取词性标注列表
        :param input:
        :return:
        """
        result = self.pipeline_ins(input=input)
        return result['output']
