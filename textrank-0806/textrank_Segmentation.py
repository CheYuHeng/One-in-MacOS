# from . import textrank_core
import textrank_core
import jieba.posseg as pseg
import os
import codecs


# 读取停用词文件中停用词的函数
def get_default_words_file():
    # os.path.dirname(path): 返回文件路径
    # os.path.realpath(__file__):  获得该方法所在的脚本的路径
    d = os.path.dirname(os.path.realpath(__file__))

    # 所有的停用词都存储在了stopwords.txt文件中(包含了中英文的停用词)
    return os.path.join(d, 'stopwords.txt')


# 读取特殊语气词文件中所有的特殊语气词的函数
def get_special_words_file():
    doc = os.path.dirname(os.path.realpath(__file__))
    # 所有的特殊语气词都存储在了special_words.txt文件中
    return os.path.join(doc, 'special_words.txt')


# 文本分词
class WordSegmentation(object):

    def __init__(self, stop_words_file=None, special_words_file=None,
                 allow_speech_tags=textrank_core.allow_speech_tags):
        '''
        初始化函数，获取此行的列表以及停用词表

        :param stop_words_file: 保存停用词表的文件路径，用utf-8的编码方式，每行放一个停用词
        :param allow_speech_tags:   默认的词性列表，用于过滤某些词性的词
        '''

        # allow_speech_tags为词性的列表，主要用于进行词性的过滤
        allow_speech_tags = [textrank_core.as_text(item) for item in allow_speech_tags]
        # 将词性列表设置成默认的词性列表
        self.default_speech_tag_filter = allow_speech_tags
        # stop_words的数据类型为set
        # 使用set方法创建空集合
        self.stop_words = set()
        # 获取停用词文件的路径
        self.stop_words_file = get_default_words_file()
        # 如果停用词文件的路径不是str类型，则使用默认的停用词
        if type(stop_words_file) is str:
            self.stop_words_file = stop_words_file
        # 打开并读取停用词文件，将其中的停用词加入到停用词集合里
        for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
            # 将词汇添加到停用词表中（去除空格）
            self.stop_words.add(word.strip())

        # special_words变量为list类型，它存储读取到的特殊语气词
        self.special_words = []
        # 获取特殊语气词文件的路径
        self.special_words_file = get_special_words_file()

        if type(special_words_file) is str:
            self.special_words_file = special_words_file
        # 打开并读取特殊语气词文件，并将其中的特殊语气词加入到特殊语气词列表中
        for word in codecs.open(self.special_words_file, 'r', 'utf-8', 'ignore'):
            # 将词汇添加到特殊语气词表中
            self.special_words.append(word.strip())

    # 对文本进行分词，返回的分词结果用列表的方式进行存储
    def segment(self, text, lower=True, use_stop_words=True, use_speech_tags_filter=False):
        '''

        :param text:    需要进行分词处理的文本
        :param lower:     （对于英文）单词是否要小写
        :param use_stop_words:  设置为True，则过滤掉停用词，设置为False，不进行过滤
        :param use_speech_tags_filter:  是否基于词性来过滤，若为True，则过使用默认的词性列表进行过滤
        :return:   词性过滤之后的词列表
        '''

        # text变量存储需要被分词的文本整体
        text = textrank_core.as_text(text)

        # jieba_result为generator数据类型
        # 词性标注结果列表
        # jieba_result中存储的是传入文本中每个词汇及其对应的词性
        jieba_result_1 = pseg.cut(text)

        # 进行了词性过滤之后的词性标注结果
        if use_speech_tags_filter == True:
            # jieba_result = [w for w in jieba_result_1 if w.flag in self.default_speech_tag_filter]
            jieba_result = []
            for w in jieba_result_1:
                # 只有属于指定词性的词才能够添加到jieba_result[]中，指定词性的词是指位于allow_speech_tags表中的词
                if w.flag in self.default_speech_tag_filter:
                    jieba_result.append(w)
        # 不进行词性过滤时的词性标注结果
        else:
            # jieba_result = [w for w in jieba_result_1]
            jieba_result = []
            # 不进行词性过滤时，任何词性的词都能够添加到jieba_result[]中
            for w in jieba_result_1:
                jieba_result.append(w)

        # jieba_result为list数据类型
        # jieba_result_1为generator数据类型

        # word_list为list类型，里面存放的每个元素都是分隔后的词汇
        # 去掉特殊的符号以及词两端之间的空格（x在这里面是特殊符号）
        # word_list_1 = [w.word.strip() for w in jieba_result if w.flag != 'x']
        word_list = []
        for w in jieba_result:
            # 如果w不是非语素词，即w不用来表示未知数或特殊符号，则将w去除掉空格后的结果添加到word_list列表中
            if w.flag != 'x':
                word_list.append(w.word.strip())

        # 去除掉空字符
        # word_list = [word for word in word_list if len(word) > 0]
        word_list2 = []
        for word in word_list:
            if len(word) > 0:
                word_list2.append(word)

        # 判断是否需要将英文单词置为小写
        word_list3 = []
        if lower:
            # word_list = []
            for word in word_list2:
                word_list3.append(word.lower())

        # 判断是否需要使用停用词集合来进行过滤
        word_list4 = []
        # 如果不使用停用词集合进行过滤，则列表中的元素不会有变化
        if use_stop_words == False:
            word_list4 = word_list3

        # 使用停用词集合进行过滤时的情形
        if use_stop_words:
            for word in word_list3:
                # 只有非停用词才能添加到word_list4[]中，这实现了对停用词的过滤
                if word.strip() not in self.stop_words:
                    word_list4.append(word.strip())

        return word_list4

    # 将列表sentences中每个元素/句子转换为由单词所组成的列表
    def segment_sentences(self, sentences, lower=True,
                          use_stop_words=True, use_speech_tags_filter=False):
        '''

        :param sentences:       句子的列表
        :param lower:           对于英文单词，是否要将它转换为小写
        :param use_stop_words:  是否要过滤停用词
        :param use_speech_tags_filter:   是否要使用默认的词性列表来进行过滤
        :return:    以词性过滤后的词列表为元素的列表
        '''

        res = []
        for sentence in sentences:
            # 调用segment方法，将词性过滤后的词列表加入到列表当中
            res.append(self.segment(text=sentence,
                                    lower=lower,
                                    use_stop_words=use_stop_words,
                                    use_speech_tags_filter=use_speech_tags_filter))

        # 返回以词性过滤后的词列表为元素的列表
        return res

    # 将列表sentences中每个元素/句子转换为由单词所组成的列表
    def judge_special_words(self, sentences):
        '''

        :param sentences:       句子的列表
        :return:    是否有语气词的判断结果
        '''

        if_special_words = False
        special_result = []

        print('看看句子的输出效果：')
        sentence_count = 0
        for i in sentences:
            sentence_count += 1
            # print(i)
        print('句子的数量：' + str(sentence_count))
        print('句子的长度：' + str(len(sentences)))

        # i代表的是一个单独的完整句子
        for i in sentences:
            for j in self.special_words:
                if i.find(j) != -1:
                    if_special_words = True
                    break
                else:
                    if_special_words = False
            special_result.append(if_special_words)
            self.special_words_dict = if_special_words

        # 返回以词性过滤后的词列表为元素的列表
        print('查看特殊词词库：')
        print(self.special_words)
        return special_result


class SentenceSegmentation(object):

    # 初始化函数，获取用于分句的分隔符集合
    def __init__(self, delimiters=textrank_core.sentence_delimiters):
        '''

        :param delimiters:
        '''
        self.delimiters = set([textrank_core.as_text(item) for item in delimiters])

    # 将文本划分为句子，返回句子列表
    def segment(self, text):
        # 获取文本
        res = [textrank_core.as_text(text)]
        # 使用两层的循环进行分句
        # 遍历分隔符对象
        for sep in self.delimiters:
            # res表示分句的结果
            text, res = res, []
            # 遍历文本对象
            for seq in text:
                res += seq.split(sep)
        # 去除句子两端之间的空格，并过滤掉空的句子
        res = [s.strip() for s in res if len(s.strip()) > 0]
        # 返回句子的列表
        return res


class Segmentation(object):
    # 初始化函数
    def __init__(self, stop_words_file=None,
                 allow_speech_tags=textrank_core.allow_speech_tags,
                 delimiters=textrank_core.sentence_delimiters):
        '''

        :param stop_words_file:     停止词文件，里面存储了停用词文件的路径
        :param allow_speech_tags:
        :param delimiters:          用于拆分句子的符号集合
        '''

        # 创建分词类的实例
        self.ws = WordSegmentation(stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags)
        # self.ws = WordSegmentation(allow_speech_tags=allow_speech_tags)
        # 创建分句类的实例
        self.ss = SentenceSegmentation(delimiters=delimiters)

    def segment(self, text, lower=False):
        # 获取文本
        text = textrank_core.as_text(text)
        # 拆分文本，得到句子列表
        sentences = self.ss.segment(text)
        # 没有进行词性过滤后的词列表
        words_no_filter = self.ws.segment_sentences(sentences=sentences,
                                                    lower=lower,
                                                    use_stop_words=False,
                                                    use_speech_tags_filter=False)

        special_words_dict = self.ws.judge_special_words(sentences=sentences)

        # 去掉停用词后的词列表
        words_no_stop_words = self.ws.segment_sentences(sentences=sentences,
                                                        lower=lower,
                                                        use_stop_words=True,
                                                        use_speech_tags_filter=False)

        # 进行词性过滤并去掉停用词后的词列表
        words_all_filters = self.ws.segment_sentences(sentences=sentences,
                                                      lower=lower,
                                                      use_stop_words=True,
                                                      use_speech_tags_filter=True)

        # 返回以上的处理结果（四种不同程度的加工方式打包返回）
        return textrank_core.AttrDict(
            sentences=sentences,
            special_words_dict=special_words_dict,
            words_no_filter=words_no_filter,
            words_no_stop_words=words_no_stop_words,
            words_all_filters=words_all_filters
        )


if __name__ == '__main__':
    # 这里是空语句，它保证了程序结构的完整性
    pass



