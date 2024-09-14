class Vertex:
    def __init__(self, key, key1, type):
        """
        初始化顶点对象，表示功能依赖模式图中的一个顶点（通常是一个属性值或属性-值对）。

        :param key: 顶点的ID，通常是某个属性或元组的标识符。
        :param key1: 顶点的属性（attribute），表示该顶点代表的数据属性值或属性的名称。
        :param type: 顶点的类型，可能用于区分不同的功能依赖模式图中的顶点类型（例如，受限属性或自由属性）。
        """
        self.id = key  # 顶点的唯一标识符
        self.attr = key1  # 顶点的属性或属性值
        self.type = type  # 顶点的类型，0 表示受限属性，1 表示自由属性
        self.connectedTo = {}  # 存储与其他顶点的连接及其权重，表示邻接关系
        self.connectedQLT = {}  # 存储与其他顶点连接的质量，用于模式修复中的边权重

    def addNeighbor(self, nbr):
        """
        添加与邻居顶点的连接，表示功能依赖关系（从一个属性到另一个属性）。
        如果邻居已经存在，则累加连接次数。

        :param nbr: 邻居顶点对象，表示与当前顶点相连的功能依赖模式中的另一个顶点。
        """
        if nbr in self.connectedTo:
            self.connectedTo[nbr] += 1  # 如果邻居顶点已经存在，增加权重
        else:
            self.connectedTo[nbr] = 1  # 新邻居顶点，初始化连接权重为 1
        self.connectedQLT[nbr] = 0  # 初始化连接的质量为 0（可以通过后续计算更新）

    def __str__(self):
        """
        返回顶点的字符串表示形式，显示顶点的ID及其连接的邻居顶点。

        :return: 顶点的字符串表示
        """
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        """
        获取所有与当前顶点连接的邻居顶点，通常这些邻居顶点代表功能依赖中的其他属性或属性值。

        :return: 与当前顶点相连的邻居顶点列表
        """
        return list(self.connectedTo.keys())

    def getId(self):
        """
        获取顶点的唯一标识符，用于识别当前顶点。

        :return: 顶点的ID
        """
        return self.id

    def getAttr(self):
        """
        获取顶点的属性或属性值，通常用于表示功能依赖模式中的具体属性或属性值。

        :return: 顶点的属性
        """
        return self.attr

    def getType(self):
        """
        获取顶点的类型，顶点类型可以用来区分不同的功能依赖（FD）模式中的顶点。
        例如，0 表示受限属性，1 表示自由属性。

        :return: 顶点类型
        """
        return self.type

    def getWeight(self, nbr):
        """
        获取与邻居顶点的连接权重，表示功能依赖关系的强度或影响力。
        在功能依赖模式修复中，这个权重可以反映一个模式被选择的频率或优先级。

        :param nbr: 邻居顶点对象，与当前顶点通过功能依赖连接的顶点。
        :return: 与邻居顶点的连接权重
        """
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        """
        初始化图对象。这个图对象用于表示功能依赖模式图，图中顶点代表数据的属性或属性值，
        顶点之间的边表示功能依赖关系。

        self.vertList: 字典，存储图中的顶点，键是顶点的ID，值是Vertex对象。
        self.numVertices: 整数，记录图中顶点的数量。
        """
        self.vertList = {}  # 存储顶点的字典，键为顶点ID，值为Vertex对象
        self.numVertices = 0  # 图中顶点的数量

    def addVertex(self, key, key1, type):
        """
        向图中添加一个新顶点。顶点通常代表数据中的一个属性或属性值。

        :param key: 顶点ID，表示该顶点的唯一标识符
        :param key1: 顶点的属性（attribute），表示该顶点代表的数据属性值
        :param type: 顶点的类型，区分受限属性（bound）和自由属性（free）
        :return: 新添加的顶点对象
        """
        if key not in self.vertList:  # 如果顶点ID不在图中，添加新顶点
            self.numVertices += 1  # 增加顶点数量
            newVertex = Vertex(key, key1, type)  # 创建新顶点
            self.vertList[key] = newVertex  # 将新顶点添加到图的顶点列表中
            return newVertex  # 返回新添加的顶点对象

    def getVertex(self, n):
        """
        获取图中指定ID的顶点对象。

        :param n: 顶点ID
        :return: 如果找到返回顶点对象，否则返回None
        """
        if n in self.vertList:  # 如果顶点ID在图中
            return self.vertList[n]  # 返回对应的顶点对象
        else:
            return None  # 如果顶点不存在，返回None

    def __contains__(self, n):
        """
        判断图中是否包含指定ID的顶点。

        :param n: 顶点ID
        :return: True 如果顶点存在，False 如果顶点不存在
        """
        return n in self.vertList  # 判断顶点是否在图的顶点列表中

    def addEdge(self, f, t, const=0):
        """
        在两个顶点之间添加一条边，表示两个属性之间的功能依赖关系。

        :param f: 起始顶点ID，表示功能依赖的前提属性（LHS）
        :param t: 目标顶点ID，表示功能依赖的后继属性（RHS）
        :param const: 可选参数，默认为0，表示边的默认权重，可以用于表示依赖关系的强度
        """
        if f in self.vertList and t in self.vertList:  # 确保两个顶点都在图中
            self.vertList[f].addNeighbor(self.vertList[t])  # 在起始顶点和目标顶点之间添加边

    def getVertices(self):
        """
        获取图中所有顶点的ID。

        :return: 顶点ID的列表
        """
        return self.vertList.keys()  # 返回顶点列表中的所有顶点ID

    def __iter__(self):
        """
        实现迭代器，允许遍历图中的所有顶点对象。

        :return: 图中顶点对象的迭代器
        """
        return iter(self.vertList.values())  # 返回图顶点对象的迭代器
def tr(G):
    """
    计算图的转置图（将每条边的方向反转）。

    :param G: 图的邻接表表示，G 是一个字典，键是顶点，值是该顶点指向的邻居顶点的集合。
    :return: 转置图的邻接表表示，GT 是一个字典，键是顶点，值是指向该顶点的邻居顶点的集合。
    """
    GT = dict()  # 创建一个新的字典，用来存储转置图
    for u in G.keys():
        GT[u] = GT.get(u, set())  # 初始化转置图中的每个顶点的邻接集合为空
    for u in G.keys():
        for v in G[u]:
            GT[v].add(u)  # 将原图中的每条边 (u -> v) 反向为 (v -> u)
    return GT  # 返回转置图

def topoSort(G):
    """
    对有向无环图（DAG）进行拓扑排序。

    :param G: 图的邻接表表示，G 是一个字典，键是顶点，值是该顶点指向的邻居顶点的集合。
    :return: 拓扑排序结果列表，列表中的顶点按拓扑排序顺序排列。
    """
    res = []  # 存储拓扑排序结果
    S = set()  # 存储已访问的顶点

    def dfs(G, u):
        """
        深度优先搜索辅助函数。

        :param G: 图的邻接表
        :param u: 当前顶点
        """
        if u in S:  # 如果顶点 u 已被访问，直接返回
            return
        S.add(u)  # 标记顶点 u 为已访问
        for v in G[u]:  # 遍历顶点 u 的邻居
            if v in S:
                continue
            dfs(G, v)  # 递归调用 DFS
        res.append(u)  # DFS 完成后将顶点加入结果列表

    for u in G.keys():
        dfs(G, u)  # 对每个顶点进行 DFS
    res.reverse()  # 将结果列表反转，得到拓扑排序
    return res  # 返回拓扑排序的结果


def walk(G, s, S=None):
    """
    从顶点 s 开始遍历图，返回路径。可以选择忽略部分顶点。

    :param G: 图的邻接表表示，G 是一个字典，键是顶点，值是该顶点指向的邻居顶点的集合。
    :param s: 起始顶点
    :param S: 可选参数，指定一个顶点集合，遍历时忽略这些顶点。默认值为 None。
    :return: P 字典，表示从起始顶点 s 开始的路径，其中键是顶点，值是该顶点的前驱节点。
    """
    if S is None:
        S = set()  # 如果没有指定顶点集合 S，则初始化为空集
    Q = []  # 使用列表模拟栈（或队列）
    P = dict()  # 存储路径的字典，键是顶点，值是前驱节点
    Q.append(s)  # 将起始顶点 s 加入队列
    P[s] = None  # 起始顶点的前驱节点设为 None（没有前驱节点）

    while Q:
        u = Q.pop()  # 取出队列中的最后一个顶点
        for v in G[u]:  # 遍历顶点 u 的所有邻居
            if v in P.keys() or v in S:  # 如果顶点 v 已经在路径中或被忽略，跳过
                continue
            Q.append(v)  # 将邻居顶点 v 加入队列
            P[v] = u  # 设置顶点 v 的前驱节点为 u
    return P  # 返回路径字典