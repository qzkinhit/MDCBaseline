# -*- coding: utf-8 -*-
import queue
import csv
import pandas as pd
import time


from Cleaner.Horizon.graph import Graph, topoSort, walk, tr


def BuildFDPatternGraph(D_path, constrains_path):
    """
    根据数据文件和功能依赖约束文件，构建功能依赖模式图。

    :param D_path: 数据文件路径，CSV格式，包含多个属性的记录
    :param constrains_path: 功能依赖约束文件路径，格式为"属性A ⇒ 属性B"
    :return: 构建的图对象
    """
    g = Graph()  # 创建图对象
    my_dict = {}
    data = pd.read_csv(D_path)  # 读取数据文件
    data = data.fillna("empty")  # 填充缺失值
    data = data.astype(str)  # 将数据转换为字符串类型，方便处理
    tot = len(data)  # 记录总数据条数

    # 处理约束文件，构建属性映射字典，标记属性是否为左手边(LHS)或右手边(RHS)
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")  # 分割功能依赖 A ⇒ B
            if lr[0].strip() in my_dict and my_dict[lr[0].strip()] == 1:
                my_dict[lr[1].strip()] = 1
                continue
            my_dict[lr[0].strip()] = 0  # 左边属性标记为0（LHS）
            my_dict[lr[1].strip()] = 1  # 右边属性标记为1（RHS）

    # 根据约束文件和数据文件为图添加顶点和边
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            left_data = data[lr[0].strip()].tolist()  # 获取左边属性的所有数据
            right_data = data[lr[1].strip()].tolist()  # 获取右边属性的所有数据
            uni_left_data = list(set(left_data))  # 去重后的左边数据
            uni_right_data = list(set(right_data))  # 去重后的右边数据

            # 为左边属性添加顶点
            for item in uni_left_data:
                g.addVertex(str(item), lr[0].strip(), my_dict[lr[0].strip()])

            # 为右边属性添加顶点
            for item in uni_right_data:
                g.addVertex(str(item), lr[1].strip(), my_dict[lr[1].strip()])

            # 添加边，表示功能依赖
            for l_item, r_item in zip(left_data, right_data):
                g.addEdge(str(l_item), str(r_item))

    # 计算连接权重（每个顶点的连接次数除以总数据量）
    for v in g:
        for w in v.getConnections():
            v.connectedTo[w] = v.connectedTo[w] / tot

    # 输出图中每条边及其权重
    cnt = 0
    for v in g:
        for w in v.getConnections():
            # print("( %s , %s ), %f" % (v.getId(), w.getId(), v.connectedTo[w]))
            cnt += 1

    return g  # 返回构建的图对象


def dfs(g, root, vis):
    """
    深度优先搜索，计算从root顶点出发的支持度和数量。

    :param g: 图对象
    :param root: 当前顶点
    :param vis: 访问标记字典，记录哪些顶点已访问
    :return: 当前顶点及其连接的总支持度和数量
    """
    if len(root.getConnections()) == 0:  # 如果当前顶点没有连接，返回0,0
        return 0, 0
    if vis[root.attr] == 1:  # 如果该顶点已被访问，跳过（避免重复访问或处理回边）
        return 0, 0
    sup = 0  # 累积支持度
    num = 0  # 累积数量
    vis[root.attr] = 1  # 标记当前顶点为已访问
    for v in root.getConnections():
        if vis[g.vertList[v.id].attr] == 0:  # 如果邻居未访问
            sup += root.connectedTo[v]  # 累加边的权重
            num += 1
            tmpa, tmpb = dfs(g, g.vertList[v.id], vis)  # 递归访问邻居节点
            sup += tmpa
            num += tmpb
            root.connectedQLT[v] = (tmpa + root.connectedTo[v]) / (tmpb + 1)  # 更新质量得分
    vis[root.attr] = 0  # 回溯时取消标记
    return sup, num  # 返回支持度和数量


# def dfs1(g, root, vis):
#     """
#     深度优先搜索，打印图中从root出发的路径和连接质量
#
#     :param g: 图对象
#     :param root: 当前顶点
#     :param vis: 访问标记字典
#     """
#     print(root.id)
#     if len(root.getConnections()) == 0:
#         return
#     if vis[root.attr] == 1:
#         return
#     vis[root.attr] = 1
#     for v in root.getConnections():
#         print(root.connectedQLT[v])
#         dfs1(g, g.vertList[v.id], vis)
#     vis[root.attr] = 0


def ComputePatternQulity(g):
    """
    计算图中每个模式的质量。

    :param g: 图对象
    """
    vis = {}  # 访问标记字典，用于跟踪顶点的访问状态
    for v in g:
        if v.getType() == 0:  # 只处理受限属性（LHS）的顶点
            for vv in g:  # 初始化访问标记
                vis[vv.attr] = 0
            dfs(g, v, vis)  # 对受限属性执行DFS，计算支持度和质量


def BuildSCCGraghAndSort(constrains_path):
    """
    构建功能依赖的强连通分量图并进行拓扑排序。

    :param constrains_path: 约束文件路径，文件格式为 "属性A ⇒ 属性B"，表示属性A功能依赖于属性B。
    :return:
        - order: 强连通分量图的拓扑排序结果。
        - tar: 顶点到强连通分量的映射字典。
        - scc: 强连通分量列表。
        - G: 原始图的邻接表表示。
    """
    sccg = Graph()  # 创建图对象
    G = {}  # 邻接表表示

    # 构建功能依赖图
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")  # 分割功能依赖 A ⇒ B
            sccg.addVertex(lr[0].strip(), "", 0)  # 添加左边属性顶点
            sccg.addVertex(lr[1].strip(), "", 0)  # 添加右边属性顶点
            sccg.addEdge(lr[0].strip(), lr[1].strip())  # 添加功能依赖边（A → B）

    # 将图转换为邻接表表示
    for v in sccg.vertList:
        tmp = set()
        for vv in sccg.vertList[v].getConnections():
            tmp.add(vv.id)  # 将顶点的连接添加到集合中
        G.update({v: tmp})  # 更新邻接表

    # 计算转置图
    GT = tr(G)

    # 计算拓扑排序和强连通分量
    seen = set()  # 已访问顶点集合
    scc = []  # 存储强连通分量
    for u in topoSort(G):  # 对图进行拓扑排序
        if u in seen:
            continue
        C = walk(GT, u, seen)  # 在转置图上进行遍历
        seen.update(C)  # 更新已访问的顶点
        scc.append(sorted(list(C.keys())))  # 将强连通分量加入结果

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
            left = tar[li]  # 左侧顶点的强连通分量编号
            right = tar[ui]  # 右侧顶点的强连通分量编号
            if left != right:
                ret[left].add(right)

    # 计算入度（用于拓扑排序）
    indegree = [0] * cnt
    for i in range(cnt):
        for j in ret[i]:
            indegree[j] += 1

    # 拓扑排序
    q = queue.Queue()
    for i in range(cnt):
        if indegree[i] == 0:  # 入度为0的顶点加入队列
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
    return order, tar, scc, G  # 返回拓扑排序结果、映射字典、强连通分量、原始图


class TmpOrder:
    def __init__(self):
        """
        初始化 TmpOrder 对象，表示一个功能依赖项及其在排序中的位置信息。

        属性:
        - left: 字符串，表示功能依赖的左侧属性（即前提属性 LHS）。
        - right: 字符串，表示功能依赖的右侧属性（即结果属性 RHS）。
        - lnum: 整数，表示左侧属性所属的强连通分量编号。
        - rnum: 整数，表示右侧属性所属的强连通分量编号。
        """
        self.left = ""  # 功能依赖的左侧属性
        self.right = ""  # 功能依赖的右侧属性
        self.lnum = 0  # 左侧属性所属的强连通分量编号
        self.rnum = 0  # 右侧属性所属的强连通分量编号


def OrderFDs(constrains_path, order, tar, scc, G):
    """
    根据强连通分量和拓扑排序，对功能依赖进行排序。

    :param constrains_path: 约束文件路径。
    :param order: 强连通分量图的拓扑排序结果。
    :param tar: 顶点到强连通分量的映射。
    :param scc: 强连通分量列表。
    :param G: 原始图的邻接表表示。
    :return: 排序后的功能依赖列表。
    """
    OrderedFDs = []

    # 读取约束文件并创建功能依赖对象列表
    with open(constrains_path, encoding='utf-8') as f:
        for line in f:
            lr = line.split("⇒")
            tmp = TmpOrder()
            tmp.lnum = tar[lr[0].strip()]  # 左侧属性的强连通分量编号
            tmp.rnum = tar[lr[1].strip()]  # 右侧属性的强连通分量编号
            tmp.left = lr[0].strip()  # 左侧属性
            tmp.right = lr[1].strip()  # 右侧属性
            OrderedFDs.append(tmp)

    # 根据强连通分量编号排序
    OrderedFDs.sort(key=lambda x: (x.lnum, x.rnum))

    # 输出排序结果
    for i in OrderedFDs:
        print(i.lnum, i.rnum)

    return OrderedFDs  # 返回排序后的功能依赖列表


# def export_res(pattern_expressions, dirty_path):
#     """
#     将修复后的结果导出为 CSV 文件。
#
#     :param pattern_expressions: 修复后的模式表达式（每个元组的修复结果）。
#     :param dirty_path: 脏数据文件路径。
#     """
#     res_df = pd.read_csv(dirty_path)  # 读取脏数据文件
#
#     # 更新修复结果
#     for i in range(len(res_df)):
#         for v in pattern_expressions[i]:  # 遍历模式表达式中的每个修复结果
#             res_df.iloc[i, list(res_df.columns).index(v)] = pattern_expressions[i][v]  # 更新相应的单元格
#
#     # 保存修复结果文件
#     res_path = "./Repaired_res/horizon/" + task_name[:-1] + "/repaired_" + task_name + dirty_path[-25:-4] + ".csv"
#     res_df.to_csv(res_path, index=False)  # 导出修复后的数据到 CSV 文件


def GeneratePatternPreservingRepairs(dirty_path, constraints_path, gt_wrong_cells, clean_df):
    """
    生成保持模式的修复，根据功能依赖图和排序修复脏数据。

    :param dirty_path: 脏数据文件路径，包含需要修复的数据。
    :param constraints_path: 约束文件路径，包含功能依赖的定义。
    :param gt_wrong_cells: 地面真值的错误单元格列表，用于对修复进行评估。
    :param clean_df: 干净数据的 DataFrame，用于参考真值。
    :return: 模式表达式列表，包含修复后的数据。
    """
    # 1. 构建功能依赖模式图并计算每个模式的质量
    g = BuildFDPatternGraph(dirty_path, constraints_path)
    ComputePatternQulity(g)

    # 2. 构建强连通分量图并进行拓扑排序
    order, tar, scc, G = BuildSCCGraghAndSort(constraints_path)

    # 3. 对功能依赖进行排序
    OrderedFDs = OrderFDs(constraints_path, order, tar, scc, G)

    pattern_expressions = []  # 保存修复后的模式表达式
    rtable_set = []  # 保存每个元组的修复结果

    # 4. 读取脏数据文件
    with open(dirty_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, restval='empty')
        data = pd.read_csv(dirty_path)
        data = data.fillna("empty")  # 用 'empty' 填充空缺值
        data = data.astype(str)  # 确保数据都是字符串格式

        for i in range(len(data)):
            Rtable = {}  # 保存当前元组的修复结果
            check = 0  # 用于标记修复状态

            # 初始化 Rtable，对于图中的受限属性，添加原始数据到 Rtable 中
            for v in g.vertList:
                if g.vertList[v].type == 0:  # 只处理受限属性（左侧属性）
                    content = data.loc[i, g.vertList[v].attr]  # 获取原始数据
                    Rtable.update({g.vertList[v].attr: content})  # 更新 Rtable

            # 5. 遍历排序后的功能依赖进行修复
            for j in range(len(OrderedFDs)):
                # 如果 Rtable 中没有该依赖的左边属性，添加它
                if OrderedFDs[j].left not in Rtable.keys():
                    Rtable.update({OrderedFDs[j].left: data.loc[i, OrderedFDs[j].left]})

                Lval = Rtable[OrderedFDs[j].left]  # 获取左侧属性的值
                # print('Lval', Lval)
                # 如果右侧属性已经在 Rtable 中，则跳过
                if OrderedFDs[j].right in Rtable:
                    continue

                if Lval == '':  # 如果左侧属性为空值，则设为 'empty'
                    Lval = 'empty'
                # if Lval == 'empty':  # 如果左侧属性为 'empty'，则跳过
                #     continue
                # 根据图中的连接质量选择最佳修复值
                maxedge = -1
                for v in g.vertList[Lval].getConnections():
                    # if v.id=='empty':
                    #     continue
                    # print(v.id + "," + str(g.vertList[Lval].connectedQLT[v]))
                    if v.attr == OrderedFDs[j].right and g.vertList[Lval].connectedQLT[v] > maxedge:
                        maxedge = g.vertList[Lval].connectedQLT[v]
                        maxp = v.id  # 记录修复值
                        # print('maxp', maxp)

                # 如果找到合适的修复，更新右侧属性
                if maxedge != -1 and maxp != 'empty':
                    Rtable.update({OrderedFDs[j].right: maxp})

                # 如果模式完美匹配地面真值，处理修复
                if PERFECTED:
                    if (i, list(clean_df.columns).index(OrderedFDs[j].right)) not in gt_wrong_cells:
                        Rtable.update({OrderedFDs[j].right: data.loc[i, OrderedFDs[j].right]})
                    if (i, list(clean_df.columns).index(OrderedFDs[j].left)) not in gt_wrong_cells:
                        Rtable.update({OrderedFDs[j].left: data.loc[i, OrderedFDs[j].left]})

            # 将修复后的 Rtable 加入结果
            pattern_expressions.append(Rtable)
            rtable_set.append(Rtable)

        # print(rtable_set)

    return pattern_expressions  # 返回模式表达式（修复后的数据）


def dirty_cells(dirty_file, clean_file):
    """
    识别脏数据文件与干净数据文件中的脏单元格。

    :param dirty_file: 脏数据的 DataFrame。
    :param clean_file: 干净数据的 DataFrame（真值）。
    :return: 脏单元格的列表，列表中的每个元素是一个 (i, j) 元组，表示第 i 行第 j 列的单元格有错误。
    """
    dirty_c = []  # 用于保存脏单元格的列表
    for i in range(len(clean_file)):  # 遍历每一行
        for j in range(len(clean_file.columns)):  # 遍历每一列
            if dirty_file.iloc[i, j] != clean_file.iloc[i, j]:  # 如果脏数据与真值不同
                dirty_c.append((i, j))  # 将脏单元格的索引 (i, j) 加入列表
    return dirty_c  # 返回脏单元格列表

PERFECTED = 0


def Horizon(dirty_path, rule_path, clean_path):
    """
    主函数，用于执行数据清洗过程，仅处理数据，返回修复后的模式表达式。

    :param dirty_path: 脏数据文件路径，CSV 文件，包含待修复的数据。
    :param rule_path: 约束规则文件路径，包含功能依赖的规则。
    :param clean_path: 干净数据文件路径，CSV 文件，作为地面真值数据（ground truth）。
    :return: 修复后的模式表达式
    """
    start_time = time.time()  # 记录开始时间

    # 读取脏数据和干净数据
    dirty_df = pd.read_csv(dirty_path).astype(str)  # 读取脏数据，并将所有数据转为字符串
    clean_df = pd.read_csv(clean_path).astype(str)  # 读取干净数据，并将所有数据转为字符串
    dirty_df = dirty_df.fillna("empty")  # 将脏数据中的缺失值填充为 "empty"
    clean_df = clean_df.fillna("empty")  # 将干净数据中的缺失值填充为 "empty"

    # 识别脏单元格
    dirty_c = dirty_cells(dirty_df, clean_df)  # 调用 dirty_cells 函数，识别哪些单元格是脏的
    gt_wrong_cells = [(i, j) for i in range(len(clean_df)) for j in range(len(clean_df.columns))
                      if clean_df.iloc[i, j] != dirty_df.iloc[i, j]]  # 生成地面真值的脏单元格列表

    # 生成保持模式的修复
    pattern_expressions = GeneratePatternPreservingRepairs(dirty_path, rule_path, gt_wrong_cells, clean_df)
    end_time = time.time()  # 记录结束时间

    return pattern_expressions, dirty_c, end_time - start_time


