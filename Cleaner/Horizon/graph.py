class Vertex:
    def __init__(self, key, key1, type):
        """
        初始化顶点对象

        :param key: 顶点的ID
        :param key1: 顶点的属性
        :param type: 顶点的类型
        """
        self.id = key
        self.attr = key1
        self.type = type
        self.connectedTo = {}
        self.connectedQLT = {}

    def addNeighbor(self, nbr):
        """
        添加邻居顶点

        :param nbr: 邻居顶点对象
        """
        if nbr in self.connectedTo:
            self.connectedTo[nbr] += 1
        else:
            self.connectedTo[nbr] = 1
        self.connectedQLT[nbr] = 0

    def __str__(self):
        """
        返回顶点的字符串表示
        """
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        """
        获取所有邻居顶点

        :return: 邻居顶点列表
        """
        return list(self.connectedTo.keys())

    def getId(self):
        """
        获取顶点ID

        :return: 顶点ID
        """
        return self.id

    def getAttr(self):
        """
        获取顶点属性

        :return: 顶点属性
        """
        return self.attr

    def getType(self):
        """
        获取顶点类型

        :return: 顶点类型
        """
        return self.type

    def getWeight(self, nbr):
        """
        获取与邻居顶点的连接权重

        :param nbr: 邻居顶点对象
        :return: 权重值
        """
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        """
        初始化图对象
        """
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key, key1, type):
        """
        添加顶点

        :param key: 顶点ID
        :param key1: 顶点属性
        :param type: 顶点类型
        :return: 新添加的顶点对象
        """
        if key not in self.vertList:
            self.numVertices += 1
            newVertex = Vertex(key, key1, type)
            self.vertList[key] = newVertex
            return newVertex

    def getVertex(self, n):
        """
        获取顶点对象

        :param n: 顶点ID
        :return: 顶点对象或None
        """
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        """
        判断顶点是否在图中

        :param n: 顶点ID
        :return: True或False
        """
        return n in self.vertList

    def addEdge(self, f, t, const=0):
        """
        添加边

        :param f: 起始顶点ID
        :param t: 目标顶点ID
        :param const: 可选参数，默认为0
        """
        self.vertList[f].addNeighbor(self.vertList[t])

    def getVertices(self):
        """
        获取图中所有顶点ID

        :return: 顶点ID列表
        """
        return self.vertList.keys()

    def __iter__(self):
        """
        返回图对象的迭代器
        """
        return iter(self.vertList.values())
def tr(G):
    """
    计算图的转置图

    :param G: 图的邻接表表示
    :return: 转置图的邻接表表示
    """
    GT = dict()
    for u in G.keys():
        GT[u] = GT.get(u, set())
    for u in G.keys():
        for v in G[u]:
            GT[v].add(u)
    return GT


def topoSort(G):
    """
    拓扑排序

    :param G: 图的邻接表表示
    :return: 拓扑排序结果列表
    """
    res = []
    S = set()

    def dfs(G, u):
        if u in S:
            return
        S.add(u)
        for v in G[u]:
            if v in S:
                continue
            dfs(G, v)
        res.append(u)

    for u in G.keys():
        dfs(G, u)
    res.reverse()
    return res


def walk(G, s, S=None):
    """
    遍历图，返回从顶点s开始的路径

    :param G: 图的邻接表表示
    :param s: 起始顶点
    :param S: 可选参数，指定不遍历的顶点集合
    :return: 从顶点s开始的路径字典
    """
    if S is None:
        S = set()
    Q = []
    P = dict()
    Q.append(s)
    P[s] = None
    while Q:
        u = Q.pop()
        for v in G[u]:
            if v in P.keys() or v in S:
                continue
            Q.append(v)
            P[v] = u
    return P
