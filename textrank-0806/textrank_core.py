import sys
import os
import numpy as np
import networkx as nx
import math
from pagerank_myself import calculate_pagerank

from collections import Counter

try:
    sys.setdefaultencoding('utf-8')
except:
    pass

# 定义句子的标点符号列表
sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
# 定义各种词性的列表，在做词性标注工作时需要用到
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']


def as_text(v):
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors = 'ignore')
    elif isinstance(v, str):
        return v
    elif isinstance(v, list):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))

def is_text(v):
    return isinstance(v, str)

class AttrDict(dict):
    # 一个可以通过点来获得属性的词典
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def combine(word_list, window = 2):
    '''
    构造在window下的单词组合，并用它们来构造单词的边
    word_list: 全部由单词所组成的列表
    window: 窗口大小
    '''

    # 窗口长度最小应该为2
    if window < 2:
        window = 2
    for x in range(1, window):
        # 当循环变量x的长度已经大于传入的列表长度时，循环已无意义，因此在这种情况下结束循环
        if x > len(word_list):
            break
        # word_list:  单词列表总共的长度
        # word_list2: 单词列表在某个跨度下需要循环的次数（只内层循环，会逐一递减）
        # (word_list2表示了在某一个不变的跨度下需要打印多少条边)
        word_list2 = word_list[x:]
        # res的数据类型为zip
        res = zip(word_list, word_list2)
        # 打印在同一个跨度下统计出的各条边（这个循环里的跨度不变）
        for r in res:
            # 打印每一条边（每次执行到yield语句后都返回一个迭代值）
            yield r


def sort_words(vertex_source, edge_source, special_words_dict,
                window = 2, pagerank_config = {'alpha' : 0.85}):
    '''
    将单词按照重要程度由大到小进行排序（权重降序排序）

    :param vertex_source:  二维的列表，子列表代表句子，子列表里的元素是单词，通过这些单词构造pagerank的节点
    :param edge_source:    二维的列表，子列表代表句子，子列表里的元素是单词，根据单词的位置关系构造textrank的边
    :param special_words_dict:   存储特殊语气词的列表
    :param window:         一个句子中相邻的window个单词，两两之间认为存在边
    :param pagerank_config:  pagerank的设置
    :return:               排序后的词语以及它们各自所对应的权值
    '''

    # sorted_words为list数据类型
    sorted_words = []
    # word_index:字是key，编号是value（存的是list1里的字）
    # index_word:编号是key，字是value（存的是list1里的字）
    # word_index和index_word都是字典类型
    word_index = {}
    index_word = {}
    _vertex_source = vertex_source  # list1
    _edge_source = edge_source      # list2
    _special_words_dict = special_words_dict
    words_number = 0
    j = 0
    # word_list记录每次传进来的词语（以词语为单位，不是以字为单位）（记录的是list1里的每个词汇，不是list2里的）
    # _vertex_source的类型是list，它存储了list1里的所有词语，它的长度为词语的个数（不是字的个数）
    # _edge_source的类型也是list，它存储了list2里的所有词语，它的长度为词语的个数（不是字的个数）
    for word_list in _vertex_source:
        for word in word_list:
            if not word in word_index:
                # 互相往两个字典里添加新的元素
                word_index[word] = words_number
                index_word[words_number] = word
                words_number += 1

    # words_number记录list1的词语中字的总个数（重复的词只算一次）（计算的是字的个数，不是词语的个数）
    # 定义graph矩阵，其空间大小为words_number * words_number
    graph = np.zeros((words_number, words_number))

    # 此处word_list里存储的是list2里的词（以词为单位，每循环一次记录一个词语）
    for word_list in _edge_source:
        for w1, w2 in combine(word_list, window):
            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]
                # print('special_words_dict[w2]:')
                # print(_special_words_dict[j])

                if special_words_dict[j] is True:
                    graph[index1][index2] = 5.0
                    graph[index2][index1] = 5.0
                else:
                    graph[index1][index2] = 1.0
                    graph[index2][index1] = 1.0
        j = j + 1
    # 创建新的列表，存储每个节点的出度
    out_list = []
    # 遍历无向图中所有的节点
    for i in range(0, len(word_index)):
        # print('\n')
        # 声明临时变量out_degree
        out_degree = 0
        # 计算每个节点的出度
        for j in range(0, len(word_index)):
            # 如果矩阵该坐标值不为零，则节点的出度值+1（说明节点在这个位置有出度）
            if graph[i][j] != 0:
                out_degree += 1
        # print('节点出度：' + str(out_degree))
        # 依次将每个节点的出度信息添加到列表out_list中
        out_list.append(out_degree)

    # graph[][]本质上是一个二维列表
    # 将graph二维数组解释转换为图的邻接矩阵，并将转换后的邻接矩阵赋值给nx_graph
    nx_graph = nx.from_numpy_matrix(graph)
    # 调用公式，迭代计算无向图中各个节点的权重
    # scores为字典类型（dict），key是字的index值，value是这个字的权重
    # scores = nx.pagerank(nx_graph, **pagerank_config)
    scores = calculate_pagerank(nx_graph,out_list = out_list, **pagerank_config)
    # scores.items(): 可迭代对象（为dict_items类型）
    # key: 用于进行比较的元素，只有一个参数，具体的参数取自于可迭代对象中
    # sorted_scores: list类型
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse = True)

    # sorted_scores的长度和words_number的长度相同
    # 循环次数和list1的长度相同
    for index, score in sorted_scores:
        # item的数据类型： <class '__main__.AttrDict'>
        item = AttrDict(word = index_word[index], weight = score)
        sorted_words.append(item)
    # 返回排序后的词语以及它们各自所对应的权值
    return sorted_words

# 不考虑特殊语气词时的情况
def sort_words_02(vertex_source, edge_source,window = 2,
                  pagerank_config = {'alpha' : 0.85}):
    sorted_words = []
    # word_index:字是key，编号是value（存的是list1里的字）
    # index_word:编号是key，字是value（存的是list1里的字）
    # word_index和index_word都是字典类型
    word_index = {}
    index_word = {}
    _vertex_source = vertex_source  # list1
    _edge_source = edge_source  # list2
    words_number = 0
    j = 0
    # word_list记录每次传进来的词语（以词语为单位，不是以字为单位）（记录的是list1里的每个词汇，不是list2里的）
    # _vertex_source的类型是list，它存储了list1里的所有词语，它的长度为词语的个数（不是字的个数）
    # _edge_source的类型也是list，它存储了list2里的所有词语，它的长度为词语的个数（不是字的个数）
    for word_list in _vertex_source:
        for word in word_list:
            if not word in word_index:
                # 互相往两个字典里添加新的元素
                word_index[word] = words_number
                index_word[words_number] = word
                words_number += 1

    # words_number记录list1的词语中字的总个数（重复的词只算一次）（计算的是字的个数，不是词语的个数）
    # 定义graph矩阵，其空间大小为words_number * words_number
    graph = np.zeros((words_number, words_number))

    # 此处word_list里存储的是list2里的词（以词为单位，每循环一次记录一个词语）
    for word_list in _edge_source:

        for w1, w2 in combine(word_list, window):

            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]

                graph[index1][index2] = 1.0
                graph[index2][index1] = 1.0

        j = j + 1
    # 创建新的列表，存储每个节点的出度
    out_list = []
    # 遍历无向图中所有的节点
    for i in range(0, len(word_index)):
        # print('\n')
        # 声明临时变量out_degree
        out_degree = 0
        # 计算每个节点的出度
        for j in range(0, len(word_index)):
            # 如果矩阵该坐标值不为零，则节点的出度值+1（说明节点在这个位置有出度）
            if graph[i][j] != 0:
                out_degree += 1
        # print('节点出度：' + str(out_degree))
        # 依次将每个节点的出度信息添加到列表out_list中
        out_list.append(out_degree)

    # graph[][]本质上是一个二维数组
    # 将graph二维数组解释转换为图的邻接矩阵，并将转换后的邻接矩阵赋值给nx_graph
    nx_graph = nx.from_numpy_matrix(graph)
    # 调用公式，迭代计算无向图中各个节点的权重
    # scores为字典类型（dict），key是字的index值，value是这个字的权重
    # scores = nx.pagerank(nx_graph, **pagerank_config)
    scores = calculate_pagerank(nx_graph, out_list=out_list, **pagerank_config)
    # scores.items(): 可迭代对象（为dict_items类型）
    # key: 用于进行比较的元素，只有一个参数，具体的参数取自于可迭代对象中
    # sorted_scores: list类型
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    # sorted_scores的长度和words_number的长度相同
    # 循环次数和list1的长度相同
    for index, score in sorted_scores:
        # item的数据类型： <class '__main__.AttrDict'>
        item = AttrDict(word=index_word[index], weight=score)
        sorted_words.append(item)

    # 返回排序后的词语以及它们各自所对应的权值
    return sorted_words


# 计算两个句子的相似度（句子划分的list中每个元素是一个“字”）
def get_sentence_similarity(word_list1, word_list2):
    '''
    本函数主要用于计算两个句子的相似度
    相似度的比较结果与被传入的两个句子传入的顺序无关，即无论谁在前其计算结果都是一致的

    :param word_list1: 代表被比较相似度的第一个句子，它是由单词所组成的列表
    :param word_list2: 代表被比较相似度的第二个句子，他也是由单词所组成的列表
    :return: 变量similarity，它时float类型的变量，存储了两个句子相似度的小数值
    '''

    # words以列表的形式存储了两个句子中的字，每个字是一个元素，两个句子都出现的字只算一次，一个句子的重字也只算一次
    words = list(set(word_list1 + word_list2))
    # 这几个vector（向量）均为list类型
    vector1 = [float(word_list1.count(word)) for word in words]
    vector2 = [float(word_list2.count(word)) for word in words]

    # 对于vector3而言，只有两个句子都有同样的字才会计算在内，任何一个句子中不包含这个字时都不进行计算
    # vector3中每个元素的值为vector1和vector2中相同位置的元素值相乘所获得
    vector3 = [vector1[i] * vector2[i] for i in range(len(vector1))]
    num1 = 0
    num2 = 0
    num3 = 0

    for i in vector3:
        num3 += i

    for i in vector1:
        num1 += i * i

    for i in vector2:
        num2 += i * i

    # 对num1和num2的计算结果开根号
    result1 = math.sqrt(num1)
    result2 = math.sqrt(num2)

    # numerator中记录的是分子的值
    numerator = num3
    # denominator中记录的是分母的值
    denominator = result1 * result2

    if denominator == 0:
        denominator = 0.000001

    # similarity中记录的是相似度
    similarity = numerator / denominator
    return similarity


def sort_sentences(sentences, words,
                   sim_func = get_sentence_similarity,
                   pagerank_config = {'alpha' : 0.85}):
    '''
    把句子的关键程度按照由大到小的顺序排列，排名靠前的句子重要程度更高

    :param sentences:    数据类型为列表（list），该列表中的每一个元素代表了一个句子
    :param words:   二维的列表，其子列表与sentence列表中的句子元素对应，该子列表由词组成，每一个元素为一个词
    :param sim_func:     计算出两个词的相似性，其参数是由两个词所组成的列表
    :param pagerank_config:   设置pagerank计算公式里alpha的值，一般这个值取0.85
    :return:  返回列表类型的sorted_sentences，这里面存储的是排好顺序的句子
    '''

    sorted_sentences = []
    _source = words
    sentences_num = len(_source)
    graph = np.zeros((sentences_num, sentences_num))

    for i in range(sentences_num):
        for j in range(i,sentences_num):
            similarity = sim_func(_source[i], _source[j])
            # 构建两个节点之间的连接边，其权值为返回的相似度(用相似度的值充当无向图边的权值)
            # (不同于找关键词，找关键句时不同节点连接边的权重会引相似度的不同而不同)
            graph[i][j] = similarity
            graph[j][i] = similarity


    nx_graph = nx.from_numpy_matrix(graph)
    # scores为字典类型（dict），key是字的index值，value是这个字的权重
    # 通过计算公式，迭代传播各节点的权重，计算出每个句子的得分
    # scores = nx.pagerank(nx_graph, **pagerank_config)
    scores = calculate_pagerank(nx_graph, **pagerank_config)

    # 对每个句子的得分进行排序，统计出重要程度较高的句子
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse = True)

    for index, score in sorted_scores:
        item = AttrDict(index = index, sentences = sentences[index], weight = score)
        sorted_sentences.append(item)

    # 返回按照排序之后的关键句统计结果
    return sorted_sentences

if __name__ == '__main__':
    pass
