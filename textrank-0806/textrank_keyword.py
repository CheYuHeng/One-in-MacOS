import textrank_core
from textrank_Segmentation import Segmentation

class TextRankKeyword(object):
    def __init__(self, stop_words_file=None,
                 allow_speech_tags=textrank_core.allow_speech_tags,
                 delimiters=textrank_core.sentence_delimiters):

        # 以下为该类中的所有基本属性
        self.text = ''
        self.keywords = None

        # 创建Segmentation类型的对象seg
        self.seg = Segmentation(stop_words_file=stop_words_file,
                                allow_speech_tags=allow_speech_tags,
                                delimiters=delimiters)

        # 其中五个基本属性的声明，之后处理后的四种不同程度的过滤文本会分别传入到这四个属性里
        # special_words_dict属性
        self.sentences = None
        self.special_words_dict = None
        self.words_no_filter = None  # 二维列表
        self.words_no_stop_words = None
        self.words_all_filters = None

    # 分析文本的函数，在这个函数中体现算法的思想
    def analyze(self, text,
                window=2,
                lower=False,
                need_special_words=True,
                vertex_source='all_filters',
                edge_source='no_stop_words',
                pagerank_config={'alpha': 0.85, }):
        '''
        :param text:        文本的内容
        :param window:      窗口的大小，通过它来构造单词之间的边，其默认值为2
        :param lower:       判断是否需要将文本转换为小写，默认为False
        :param need_special_words:       判断是否需要考虑特殊的语气词，True代表需要考虑，默认为True
        :param vertex_source:  选择使用三种模式中的哪一种来构造pagerank对应图中的节点，
                                关键词均来自于vertex_source中
        :param edge_source:    选择使用三种模式中的哪一种来构造pagerank对应图中的节点之间的边，
                                边的构造需要结合window参数
        :param pagerank_config:   对pagerank算法配置参数，其阻尼系数设置为0.85
        '''
        '''
        sentences: 由句子所组成的列表
        words_no_filter: 对sentence中每个句子分词得到两级列表
        words_no_stop_words: 去掉words_no_filter中的停止词而得到的二维列表
        words_all_filters: 保留words_no_stop_words中指定词性的单词而得到的二维列表
        '''

        self.text = text
        self.word_index = {}
        self.index_word = {}
        # keywords: 关键词的列表
        self.keywords = []
        self.graph = None

        # result接收从segment函数中打包返回的四种不同程度的分词结果
        result = self.seg.segment(text=text, lower=lower)

        # 依次将四种不同程度的处理结果赋值给四个不同的列表
        self.sentences = result.sentences
        self.special_words_dict = result.special_words_dict
        self.words_no_filter = result.words_no_filter
        self.words_no_stop_words = result.words_no_stop_words
        self.words_all_filters = result.words_all_filters

        # 列举三种可供选择的模式
        options = ['no_filter', 'no_stop_words', 'all_filters']

        # 几种模式的选择
        if vertex_source in options:
            _vertex_source = result['words_' + vertex_source]
        else:
            _vertex_source = result['words_all_filters']
        if edge_source in options:
            _edge_source = result['words_' + edge_source]
        else:
            _edge_source = result['words_no_stop_words']

        _special_words_dict = result['special_words_dict']

        # 当考虑特殊语气词时调用第一种函数计算
        if need_special_words == True:
            self.keywords = textrank_core.sort_words(_vertex_source,
                                                     _edge_source,
                                                     _special_words_dict,
                                                     window=window,
                                                     pagerank_config=pagerank_config)

        # 不考虑特殊语气词时调用第二种函数计算
        else:
            self.keywords = textrank_core.sort_words_02(_vertex_source,
                                                     _edge_source,
                                                     window=window,
                                                     pagerank_config=pagerank_config)


    # 获取最重要的num个长度大于等于word_min_len的关键词
    def get_keywords(self, num=6, word_min_len=1):
        '''

        :param num:需要获取的关键词的数量
        :param word_min_len:关键词的最小长度值
        :return:所有关键词的列表
        '''
        result = []
        count = 0
        for item in self.keywords:
            # 循环过程中，逐渐增加count的大小，直到达到需获取的关键词数量后终止循环
            if count >= num:
                break
            if len(item.word) >= word_min_len:
                result.append(item)
                count += 1
        # 循环结束后result列表中已经存储了所有的关键词，将这个列表返回
        return result

    # 获取一定数量的关键短语
    def get_keyphrases(self, key_words_num=12, min_occur_time=2):
        '''

        :param key_words_num:  需要返回的关键短语的数量
        :param min_occur_time: 这个短语在原文本中最少出现的次数
        :return:  所有的关键短语列表
        '''

        # 关键词的集合
        keywords_set = set([item.word for item in self.get_keywords(num=key_words_num, word_min_len=1)])
        # 关键短语的集合
        key_phrases = set()
        for sentence in self.words_no_filter:
            one = []
            for word in sentence:
                # 某个词汇如果已经存储在关键词集合中，则直接将它添加到one列表中
                if word in keywords_set:
                    one.append(word)
                # 某个词汇如果尚未存储在关键词集合中，则分多钟情况处理
                else:
                    # 如果列表中已经存储了词汇
                    if len(one) > 1:
                        # 添加新的关键词，并让它与既有的关键词组成关键短语
                        key_phrases.add(''.join(one))
                    if len(one) == 0:
                        continue
                    else:
                        one = []
            if len(one) > 1:
                key_phrases.add(''.join(one))

        # 返回所有的关键短语，其中设定好了限定条件：关键短语的出现次数必须大于给定的变量值
        return [phrase for phrase in key_phrases if self.text.count(phrase) >= min_occur_time]

# 主模块，保持结构的完整性
if __name__ == '__main__':
    pass
