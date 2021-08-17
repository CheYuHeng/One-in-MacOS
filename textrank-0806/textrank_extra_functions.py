import math
import networkx as nx
import numpy as np
from textrank_keyword import TextRankKeyword

# 计算两个句子的相似度（句子划分的list中每个元素是一个“词”）
def get_sentence_similarity_2(word_list1, word_list2):
    '''

    :param word_list1:
    :param word_list2:
    :return:
    '''

    tr4w1 = TextRankKeyword()
    tr4w2 = TextRankKeyword()

    tr4w1.analyze(text=word_list1, lower=True, window=2)
    tr4w2.analyze(text=word_list2, lower=True, window=2)

    # 设置临时的list类型变量words,里面存储的内容是句子分词后的结果
    words = []

    # 将输入的句子1中的文本做分词操作，结果存入words中
    for i in tr4w1.words_no_filter:
        words.append(i)

    # words_element为过过渡用的list类型变量，里面临时存储了words[0]中的信息，它的每个元素是一个词
    words_element = words[0]
    # print(words_element)

    # 将输入的句子2中的文本做分词操作，结果仍存入words中
    for i in tr4w2.words_no_filter:
        words.append(i)

    # 把第二个列表中的第二个list里的所有元素依次添加到临时变两种
    for i in words[1]:
        words_element.append(i)

    # words_set为集合类型的临时变量，其目的是去除words_element中的重复元素词汇
    words_set = set(words_element)
    # 去重后将其再转换为list类型并赋值给新的list类型变量words_list中
    # 这时候words_list中存储的每一个元素都是两个传入的句子中划分好的词汇，且不含重复元素
    words_list = list(set(words_set))

    # vector: 向量
    # 这几个vector均为list类型
    vector1 = [float(word_list1.count(word)) for word in words_list]
    vector2 = [float(word_list2.count(word)) for word in words_list]

    # 对于vector3而言，只有两个句子都有同样的字才会计算在内，任何一个句子中不包含这个字时都不进行计算
    # vector3中每个元素的值为vector1和vector2中相同位置的元素值相乘所获得
    vector3 = [vector1[i] * vector2[i] for i in range(len(vector1))]


    # 主体计算部分，设置了多个计算过程的临时变量，计算思路参考了向量夹角余弦值的数学计算公式
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

    # 判断特殊情况，分母不能为0，如果为0则临时替换一个接近于0的较小值
    if denominator == 0:
        denominator = 0.000001

    # similarity中存储的是相似度的计算结果，它由分子除以分母得到，其值应小于等于1
    similarity = numerator / denominator
    return similarity

