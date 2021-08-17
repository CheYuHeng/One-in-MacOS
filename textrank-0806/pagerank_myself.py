import networkx as nx

# 自行编写的图中各节点pr值的计算公式，功能较为简略
def calculate_pagerank(G, alpha = 0.85, max_iter = 100, tol=1.0e-6,
                       weight='weight', dangling = None, out_list = []):
    '''

    :param G:  G代表图，无向图或有向图
    :param alpha:  pagerank计算公式中常用的系数，多数情况下取值0.85
    :param max_iter: 设置循环迭代次数的上限，这里为100
    :param tol:  设置迭代收敛的范围
    :param weight: 代表各节点的权重
    :param dangling: 不与任何其它节点有边连接的节点
    :param out_list: 列表，存储了无向图中每个节点的出度
    :return: 返回字典类型的graph，里面存放了图中各节点的编号以及它们收敛后的权重
    '''

    # 判断图G是不是为空（没有任何节点），如果是，则直接返回空
    if len(G) == 0:
        return {}

    # 判断G是不是有向图，如果不是，就转换为有向图再赋给D，是则直接赋给D
    if not G.is_directed():
        D = G.to_directed()
    # G是有向图，则直接赋值给D，这样保证D一定是有向图
    else:
        D = G

    # W的类型为DiGraph，即W是一个有向图，它里面存储了图中每个节点的信息，包括出度入度等
    # 通过调用stochastic_graph函数来计算每个节点的出度，即每个节点所连的边数
    W = nx.stochastic_graph(D, weight=weight)

    # N为整型，它记录的是节点总共的数量
    N = W.number_of_nodes()

    # 先确定每个节点PR响亮的初始值，这里取1/N，例如5个节点的图中每个点pr值初始为0.2
    graph = dict.fromkeys(W, 1.0/N)
    p = dict.fromkeys(W, 1.0/N)

    # 如果所有的节点均有边与之相连，即每个点都有出入度，则直接将初始pr值赋值给这些节点
    if dangling is None:
        dangling_weights = p
    # 如果有的节点没有边连接，即它的出入度均为0,这种情况下其pr值计算公式如下
    else:
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v/s) for k, v in dangling.items())

    # 这个list里存储所有无边连接的节点的编号
    dangling_node_list = []
    # 循环节点出度列表，循环变量n获取每个节点的出度信息
    for n in range(0, len(out_list)):
        # 如果某个节点的出度为0，则将它添加到该列表中
        if out_list[n] == 0:
            dangling_node_list.append(n)

    # 用stop_range来表示迭代计算值的收敛范围
    stop_range = N * tol

    # 迭代计算各节点的权重，直至收敛
    for cycle in range(max_iter):
        # 将graph中存储的节点信息赋值给graph_pr
        # graph_pr中保留了各节点的权重信息
        graph_pr = graph
        # graph中的节点值先全清0，之后进行下一步的计算
        graph = dict.fromkeys(graph_pr.keys(), 0)
        dang = alpha * sum(graph_pr[n] for n in dangling_node_list)

        for i in graph:
            for j in W[i]:
                # 这部分相当于pr计算公式的后半部分，alpha值乘以每个节点的pr值和出度的倒数
                # 再求和到graph里
                graph[j] += alpha * graph_pr[i] * W[i][j][weight]
            # pr公式后半段这之前已经计算完毕，接下来该计算前半段了
            # 这里可以看做在计算(1 - alpja)/N于后半段的和
            # 每一次迭代最终的计算结果都存在字典类型的graph里
            graph[i] += dang * dangling_weights.get(i, 0) + (1.0 - alpha) * p.get(i, 0)

        # 每次内循环后都计算一下当前的收敛值
        result = sum([abs(graph[n] - graph_pr[n]) for n in graph])

        # 将当前的收敛值与stop_range进行比较
        # 当迭代已经收敛至合理范围时，即这个计算值小于stop_range时，返回图的计算结果，保留此时计算的各点权重
        if result < stop_range:
            return graph
