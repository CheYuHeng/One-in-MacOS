import textrank_core
from textrank_Segmentation import Segmentation

class TextRankSentence(object):

    def __init__(self, stop_words_file = None,
                 allow_speech_tags = textrank_core.allow_speech_tags,
                 delimiters = textrank_core.sentence_delimiters):
        '''

        :param stop_words_file:  读取停用词文件（文本分句时不需要过滤停用词）
        :param allow_speech_tags:  读取指定词性的文件
        :param delimiters:      读取指定的标点符号，作为文本分句的依据
        '''

        self.seg = Segmentation(stop_words_file = stop_words_file,
                                allow_speech_tags = allow_speech_tags,
                                delimiters = delimiters)
        self.sentences = None
        self.words_no_filter = None
        self.words_no_stop_words = None
        self.words_all_filters = None

        self.key_sentences = None

    def analyze(self, text, lower = False,
                source = 'no_stop_words',
                sim_func = textrank_core.get_sentence_similarity,
                pagerank_config = {'alpha': 0.85, }):
        '''
        :param text:   传入的文本全部内容
        :param lower:   英文单词是否置小写
        :param source:  选择文本的过滤等级
        :param sim_func:    两个句子相似度比较结果
        :param pagerank_config: 计算节点TextRank得分时阻尼因子值的设置
        '''

        self.key_sentences = []
        result = self.seg.segment(text = text, lower = lower)
        self.sentences = result.sentences
        self.words_no_filter = result.words_no_filter
        self.words_no_stop_words = result.words_no_stop_words
        self.words_all_filters = result.words_all_filters

        options = ['no_filter','no_stop_words','all_filters']
        if source in options:
            _source = result['words_' + source]
        else:
            _source = result['words_no_stop_words']

        self.key_sentences = textrank_core.sort_sentences(sentences = self.sentences,
                                                          words = _source,
                                                          sim_func = sim_func,
                                                          pagerank_config = pagerank_config)

    def get_key_sentences(self, num = 6, sentence_min_len = 6):
        '''

        :param num:     需要获取的关键句的长度
        :param sentence_min_len:  关键句的最小出现次数
        :return:        提取的文本关键句结果
        '''

        result = []
        count = 0
        for item in self.key_sentences:
            if count >= num:
                break
            if len(item['sentences']) >= sentence_min_len:
                result.append(item)
                count += 1
        return result

if __name__ == '__main__':
    pass
