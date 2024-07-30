# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import queue
import time
import argparse
import sys
import csv
import re
import pandas as pd
import time
import sys
import os


def check_string(string: str):
    if re.search(r"-inner_error-", string):
        return "-inner_error-" + string[-6:-4]
    elif re.search(r"-outer_error-", string):
        return "-outer_error-" + string[-6:-4]
    elif re.search(r"-inner_outer_error-", string):
        return "-inner_outer_error-" + string[-6:-4]
    elif re.search(r"-dirty-original_error-", string):
        return "-original_error-" + string[-9:-4]


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


def BuildFDPatternGraph(D_path, constrains_path):
    """
    构建功能依赖模式图

    :param D_path: 数据文件路径
    :param constrains_path: 约束文件路径
    :return: 构建的图对象
    """
    g = Graph()
    my_dict = {}
    data = pd.read_csv(D_path)
    data = data.fillna("nan")
    data = data.astype(str)
    tot = len(data)

    # 处理约束文件，构建属性映射字典
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            if lr[0].strip() in my_dict and my_dict[lr[0].strip()] == 1:
                my_dict[lr[1].strip()] = 1
                continue
            my_dict[lr[0].strip()] = 0
            my_dict[lr[1].strip()] = 1

    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            left_data = data[lr[0].strip()].tolist()
            right_data = data[lr[1].strip()].tolist()
            uni_left_data = list(set(left_data))
            uni_right_data = list(set(right_data))

            # 添加左边属性的顶点
            for item in uni_left_data:
                g.addVertex(str(item), lr[0].strip(), my_dict[lr[0].strip()])

            # 添加右边属性的顶点
            for item in uni_right_data:
                g.addVertex(str(item), lr[1].strip(), my_dict[lr[1].strip()])

            # 添加边
            for l_item, r_item in zip(left_data, right_data):
                g.addEdge(str(l_item), str(r_item))

    # 计算连接权重
    for v in g:
        for w in v.getConnections():
            v.connectedTo[w] = v.connectedTo[w] / tot

    # 输出结果
    cnt = 0
    for v in g:
        for w in v.getConnections():
            print("( %s , %s ), %f" % (v.getId(), w.getId(), v.connectedTo[w]))
            cnt += 1

    return g


def dfs(g, root, vis):
    """
    深度优先搜索，计算图中从root出发的支持度和数量

    :param g: 图对象
    :param root: 当前顶点
    :param vis: 访问标记字典
    :return: 支持度和数量
    """
    if len(root.getConnections()) == 0:
        return 0, 0
    if vis[root.attr] == 1:
        return 0, 0
    sup = 0
    num = 0
    vis[root.attr] = 1
    for v in root.getConnections():
        if vis[g.vertList[v.id].attr] == 0:
            sup += root.connectedTo[v]
            num += 1
            tmpa, tmpb = dfs(g, g.vertList[v.id], vis)
            sup += tmpa
            num += tmpb
            root.connectedQLT[v] = (tmpa + root.connectedTo[v]) / (tmpb + 1)
    vis[root.attr] = 0
    return sup, num


def dfs1(g, root, vis):
    """
    深度优先搜索，打印图中从root出发的路径和连接质量

    :param g: 图对象
    :param root: 当前顶点
    :param vis: 访问标记字典
    """
    print(root.id)
    if len(root.getConnections()) == 0:
        return
    if vis[root.attr] == 1:
        return
    vis[root.attr] = 1
    for v in root.getConnections():
        print(root.connectedQLT[v])
        dfs1(g, g.vertList[v.id], vis)
    vis[root.attr] = 0


def ComputePatternQulity(g):
    """
    计算图中每个模式的质量

    :param g: 图对象
    """
    vis = {}
    for v in g:
        if v.getType() == 0:
            for vv in g:
                vis[vv.attr] = 0
            dfs(g, v, vis)


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


def BuildSCCGraghAndSort(constrains_path):
    """
    构建强连通分量图并进行拓扑排序

    :param constrains_path: 约束文件路径
    :return: 拓扑排序结果、顶点映射、强连通分量列表、原始图
    """
    sccg = Graph()
    G = {}

    # 构建图
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            sccg.addVertex(lr[0].strip(), "", 0)
            sccg.addVertex(lr[1].strip(), "", 0)
            sccg.addEdge(lr[0].strip(), lr[1].strip())

    # 转换为邻接表表示
    for v in sccg.vertList:
        tmp = set()
        for vv in sccg.vertList[v].getConnections():
            tmp.add(vv.id)
        G.update({v: tmp})

    # 计算转置图
    GT = tr(G)

    # 计算拓扑排序和强连通分量
    seen = set()
    scc = []
    for u in topoSort(G):
        if u in seen:
            continue
        C = walk(GT, u, seen)
        seen.update(C)
        scc.append(sorted(list(C.keys())))

    # 构建顶点到强连通分量的映射
    tar = {}
    cnt = 0
    for li in scc:
        for ui in li:
            tar.update({ui: cnt})
        cnt += 1

    # 构建强连通分量图
    ret = {i: set() for i in range(cnt)}
    for li in G:
        for ui in G[li]:
            left = tar[li]
            right = tar[ui]
            if left != right:
                ret[left].add(right)

    # 计算入度
    indegree = [0] * cnt
    for i in range(cnt):
        for j in ret[i]:
            indegree[j] += 1

    # 拓扑排序
    q = queue.Queue()
    for i in range(cnt):
        if indegree[i] == 0:
            q.put(i)
    order = []
    while not q.empty():
        ele = q.get()
        order.append(ele)
        for i in ret[ele]:
            indegree[i] -= 1
            if indegree[i] == 0:
                q.put(i)

    print(scc)
    print(ret)
    print(order)
    print(tar)
    return order, tar, scc, G


class TmpOrder:
    def __init__(self):
        self.left = ""
        self.right = ""
        self.lnum = 0
        self.rnum = 0


def OrderFDs(constrains_path, order, tar, scc, G):
    """
    对功能依赖进行排序

    :param constrains_path: 约束文件路径
    :param order: 拓扑排序结果
    :param tar: 顶点到强连通分量的映射
    :param scc: 强连通分量列表
    :param G: 原始图的邻接表表示
    :return: 排序后的功能依赖列表
    """
    OrderedFDs = []

    # 读取约束文件并创建功能依赖对象列表
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            tmp = TmpOrder()
            tmp.lnum = tar[lr[0].strip()]
            tmp.rnum = tar[lr[1].strip()]
            tmp.left = lr[0].strip()
            tmp.right = lr[1].strip()
            OrderedFDs.append(tmp)

    # 根据左边和右边的强连通分量编号排序
    OrderedFDs.sort(key=lambda x: (x.lnum, x.rnum))

    # 输出排序结果
    for i in OrderedFDs:
        print(i.lnum, i.rnum)

    return OrderedFDs


def calDetPrecRec(pattern_expressions, dirty_path, clean_path,dirty_c):
    """
    计算检测的准确率和召回率

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    :param clean_path: 干净数据文件路径
    :return: 检测的准确率和召回率
    """
    attrList = []
    dirty_dict = []

    # 读取脏数据文件
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            dirty_dict.append(line)
            attrList = list(line.keys())

    # 读取干净数据文件
    clean_df = pd.read_csv(clean_path, header=0)
    clean_df.columns = attrList

    tot = 0
    correct_rec = 0

    # 计算正确检测的数量和总检测数量
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        cnt = 0
        for line in reader:
            for v in pattern_expressions[cnt]:
                if pattern_expressions[cnt][v] != dirty_dict[cnt][v]:
                    if (cnt, list(clean_df.columns).index(v)) in dirty_c:
                        correct_rec += 1
                tot += 1
            cnt += 1

    precision = correct_rec / tot
    recall = correct_rec / len(dirty_c)
    return precision, recall




def calRepPrec(pattern_expressions, dirty_path, clean_path):
    """
    计算修复的精度

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    :param clean_path: 干净数据文件路径
    :return: 修复的精度
    """
    attrList = []
    dirty_dict = []

    # 读取脏数据文件，存储为字典列表
    with open(dirty_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            dirty_dict.append(line)
            attrList = list(line.keys())

    # 读取干净数据文件
    df = pd.read_csv(clean_path, header=0)
    df.columns = attrList

    tot = 0
    correct = 0

    # 计算修复的正确数量和总数量
    with open(clean_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        cnt = 0
        for line in reader:
            for v in pattern_expressions[cnt]:
                if pattern_expressions[cnt][v] != dirty_dict[cnt][v]:
                    if pattern_expressions[cnt][v] == line[v]:
                        correct += 1
                    tot += 1
            cnt += 1
    return correct / tot


def calRepRec(pattern_expressions, dirty_path, clean_path):
    """
    计算修复的召回率

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    :param clean_path: 干净数据文件路径
    :return: 修复的召回率
    """
    attrList = []

    # 读取脏数据文件，获取属性列表
    with open(dirty_path, 'r') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            attrList = list(line.keys())
            break

    # 读取干净数据文件
    df = pd.read_csv(clean_path, header=0)
    df.columns = attrList

    dirty_dict = []
    tot = 0
    correct = 0

    # 读取脏数据文件，存储为字典列表
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        for line in reader:
            dirty_dict.append(line)

    # 计算修复的正确数量和总数量
    with open(clean_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        cnt = 0
        for line in reader:
            for v in dirty_dict[cnt]:
                if dirty_dict[cnt][v] != line[v]:
                    try:
                        if pattern_expressions[cnt][v] == line[v]:
                            correct += 1
                    except:
                        pass
                    tot += 1
            cnt += 1
    return correct / tot


def export_res(pattern_expressions, dirty_path):
    """
    导出修复结果

    :param pattern_expressions: 模式表达式
    :param dirty_path: 脏数据文件路径
    """
    res_df = pd.read_csv(dirty_path)

    # 更新修复结果
    for i in range(len(res_df)):
        for v in pattern_expressions[i]:
            res_df.iloc[i, list(res_df.columns).index(v)] = pattern_expressions[i][v]

    # 保存修复结果文件
    res_path = "./Repaired_res/horizon/" + task_name[:-1] + "/repaired_" + task_name + dirty_path[-25:-4] + ".csv"
    res_df.to_csv(res_path, index=False)


def calF1(precision, recall):
    """
    计算F1值

    :param precision: 精度
    :param recall: 召回率
    :return: F1值
    """
    return 2 * precision * recall / (precision + recall + 1e-10)




def GeneratePatternPreservingRepairs(dirty_path, constraints_path,gt_wrong_cells,clean_df):
    """
    生成保持模式的修复

    :param dirty_path: 脏数据文件路径
    :param constraints_path: 约束文件路径
    :return: 模式表达式列表
    """
    # 构建功能依赖模式图并计算模式质量
    g = BuildFDPatternGraph(dirty_path, constraints_path)
    ComputePatternQulity(g)

    # 构建强连通分量图并进行拓扑排序
    order, tar, scc, G = BuildSCCGraghAndSort(constraints_path)

    # 对功能依赖进行排序
    OrderedFDs = OrderFDs(constraints_path, order, tar, scc, G)

    pattern_expressions = []
    rtable_set = []

    # 读取脏数据文件
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='nan')
        data = pd.read_csv(dirty_path)
        data = data.fillna("nan")
        data = data.astype(str)

        for i in range(len(data)):
            Rtable = {}
            check = 0

            # 初始化Rtable
            for v in g.vertList:
                if g.vertList[v].type == 0:
                    content = data.loc[i, g.vertList[v].attr]
                    Rtable.update({g.vertList[v].attr: content})

            # 遍历排序后的功能依赖进行修复
            for j in range(len(OrderedFDs)):
                if OrderedFDs[j].left not in Rtable.keys():
                    Rtable.update({OrderedFDs[j].left: data.loc[i, OrderedFDs[j].left]})

                Lval = Rtable[OrderedFDs[j].left]

                if OrderedFDs[j].right in Rtable:
                    continue

                if Lval == '':
                    Lval = 'nan'

                maxedge = -1
                for v in g.vertList[Lval].getConnections():
                    print(v.id + "," + str(g.vertList[Lval].connectedQLT[v]))
                    if v.attr == OrderedFDs[j].right and g.vertList[Lval].connectedQLT[v] > maxedge:
                        maxedge = g.vertList[Lval].connectedQLT[v]
                        maxp = v.id

                if maxedge != -1:
                    Rtable.update({OrderedFDs[j].right: maxp})

                if PERFECTED:
                    if (i, list(clean_df.columns).index(OrderedFDs[j].right)) not in gt_wrong_cells:
                        Rtable.update({OrderedFDs[j].right: data.loc[i, OrderedFDs[j].right]})
                    if (i, list(clean_df.columns).index(OrderedFDs[j].left)) not in gt_wrong_cells:
                        Rtable.update({OrderedFDs[j].left: data.loc[i, OrderedFDs[j].left]})

            pattern_expressions.append(Rtable)
            rtable_set.append(Rtable)

        print(rtable_set)

    return pattern_expressions


def dirty_cells(dirty_file, clean_file):
    """
    识别脏数据和干净数据中的脏单元格

    :param dirty_file: 脏数据 DataFrame
    :param clean_file: 干净数据 DataFrame
    :return: 脏单元格列表
    """
    dirty_c = []
    for i in range(len(clean_file)):
        for j in range(len(clean_file.columns)):
            if dirty_file.iloc[i, j] != clean_file.iloc[i, j]:
                dirty_c.append((i, j))
    return dirty_c


ONLYED = 0
PERFECTED = 0


def main(dirty_path, rule_path, clean_path, task_name, ONLYED=0, PERFECTED=0):
    """
    主函数，用于执行数据清洗过程

    :param dirty_path: 脏数据文件路径
    :param rule_path: 约束规则文件路径
    :param clean_path: 干净数据文件路径
    :param task_name: 任务名称
    :param ONLYED: 控制变量，默认值为0
    :param PERFECTED: 控制变量，默认值为0
    """
    start_time = time.time()

    # 读取脏数据和干净数据
    dirty_df = pd.read_csv(dirty_path).astype(str)
    clean_df = pd.read_csv(clean_path).astype(str)
    dirty_df = dirty_df.fillna("nan")
    clean_df = clean_df.fillna("nan")

    # 识别脏单元格
    dirty_c = dirty_cells(dirty_df, clean_df)
    gt_wrong_cells = [(i, j) for i in range(len(clean_df)) for j in range(len(clean_df.columns)) if
                      clean_df.iloc[i, j] != dirty_df.iloc[i, j]]

    # 生成保持模式的修复
    pattern_expressions = GeneratePatternPreservingRepairs(dirty_path, rule_path,gt_wrong_cells,clean_df)
    end_time = time.time()

    # 计算检测的精度和召回率
    det_prec, det_rec = calDetPrecRec(pattern_expressions, dirty_path, clean_path,dirty_c)

    # 计算修复的精度、召回率和F1值
    rep_precision = calRepPrec(pattern_expressions, dirty_path, clean_path)
    rep_recall = calRepRec(pattern_expressions, dirty_path, clean_path)
    rep_f1 = calF1(rep_precision, rep_recall)

    # 打印和保存结果
    print(pattern_expressions)
    print(rep_precision)
    print(rep_recall)
    print(rep_f1)
    print("Elapsed time:", end_time - start_time)

    results_dir = "./results/" + task_name[:-1]
    os.makedirs(results_dir, exist_ok=True)

    if True:
        if PERFECTED:
            out_path = os.path.join(results_dir, f"perfectED+EC_{task_name}{check_string(dirty_path)}.txt")
            res_path = os.path.join(results_dir, f"perfect_repaired_{task_name}{check_string(dirty_path)}.csv")
        else:
            out_path = os.path.join(results_dir, "1.txt")
            res_path = os.path.join(results_dir, "repaired_1.csv")

        with open(out_path, 'w') as f:
            sys.stdout = f
            print(det_prec)
            print(det_rec)
            print(calF1(det_prec, det_rec))
            print("Elapsed time:", end_time - start_time)

            print(rep_precision)
            print(rep_recall)
            print(rep_f1)
            print("Elapsed time:", end_time - start_time)

        # 保存修复后的数据
        res_df = pd.read_csv(dirty_path)
        for i in range(len(res_df)):
            for v in pattern_expressions[i]:
                res_df.loc[i, v] = pattern_expressions[i][v]
        res_df.to_csv(res_path, index=False)


if __name__ == "__main__":
    dirty_path = "./data_with_rules/hospital/noise/hospital_test.csv"
    rule_path = "./data_with_rules/hospital/dc_rules_test.txt"
    clean_path = "./data_with_rules/hospital/test_clean.csv"
    task_name = "hospital1"

    main(dirty_path, rule_path, clean_path, task_name)
