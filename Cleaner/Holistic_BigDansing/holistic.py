import sys

import pandas as pd
import numpy as np
import copy
import re
from Cleaner.Holistic_BigDansing.mvc import read_graph, min_vertex_cover, read_graph_dc
from Cleaner.Holistic_BigDansing.tes import greedy_min_vertex_cover, greedy_min_vertex_cover_dc
from Cleaner.Holistic_BigDansing.DC_Rules import DCRule
from tqdm import tqdm

def check_string(string: str):
    if re.search(r"-inner_error-", string):
        return "-inner_error-" + string[-6:-4]
    elif re.search(r"-outer_error-", string):
        return "-outer_error-" + string[-6:-4]
    elif re.search(r"-inner_outer_error-", string):
        return "-inner_outer_error-" + string[-6:-4]
    elif re.search(r"-dirty-original_error-", string):
        return "-original_error-" + string[-9:-4]
    else:
        return ""

class Holistic:
    def __init__(self, task_name, PERFECTED, ONLYED, output_path):
        self.wrong = []
        self.rule = []
        self.blocked_list = [[]]
        self.data = []
        self.data_cl = []
        self.input_data = []
        self.dicc = {}
        self.visdic = {}
        self.edgedic = {}
        self.diccop = {}
        self.maypair = [[]]
        self.attr_index = {}
        self.dic = {}
        self.scodic = {}
        self.clean_right = 0
        self.all_clean = 0
        self.clean_right_pre = 0
        self.Rules = []
        self.exps = []
        self.mvc = []
        self.sorts = []
        self.vio = []
        self.cnt = 0
        self.constant_pre = []
        self.contantdic = {}
        self.wrong_cells = []
        self.repaired_cells = []
        self.clean_in_cands = []
        self.clean_in_cands_repair_right = []
        self.repair_right_cells = []
        self.repaired_cells_value = {}
        self.repair_wrong_cells = []
        self.task_name = task_name
        self.PERFECTED = PERFECTED
        self.ONLYED = ONLYED
        self.output_path = output_path
        self.schema = []
        self.start_time = None
        # 设置显示选项
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
    '''
        scope操作符：从数据集中删除不相关的数据单元
        Parameters
        ----------
        sco :
            要从数据集中取出的列名，是一个list
        Returns
        -------
        data :
            返回从数据集中取回的data
    '''
    def scope(self, sco):
        df = pd.read_csv(self.dirty_path, header=0).astype(str).fillna("nan")
        data = np.array(df[sco]).tolist()
        for i in data:
            for j in i:
                j = str(j)
        return data

    def scope1(self, sco):
        df = pd.read_csv(self.clean_path, header=0).astype(str).fillna("nan")
        data = np.array(df[sco]).tolist()
        return data

    '''
           block操作符：将共享了相同的blocking key的数据进行分组
           Parameters
           ----------
           data :
               数据集
           blo :
               blocking key,block操作符根据blo进行分组
           Returns
           -------
           blocked_list :
               返回根据blo分好块的data,为一个二层list，list[i]表示第i组blo一样的tuple
               example:
                   [[0, 1],[2, 3]]中表示有2组值，其中0，1的blo值相同且2，3的blo值相同
       '''

    def block(self, data, blo):
        blodic = {}
        blodiccnt = 0
        for i in range(len(data)):
            if (pd.isna(data[i][blo])):
                if ("nan" in blodic):
                    self.blocked_list[blodic["nan"]].append(i)
                else:
                    blodic["nan"] = blodiccnt
                    self.blocked_list.append([])
                    self.blocked_list[blodic["nan"]].append(i)
                    blodiccnt += 1
            elif (data[i][blo] in blodic):
                self.blocked_list[blodic[data[i][blo]]].append(i)
            else:
                blodic[data[i][blo]] = blodiccnt
                self.blocked_list.append([])
                self.blocked_list[blodic[data[i][blo]]].append(i)
                blodiccnt += 1
        return self.blocked_list

    def block_con(self, data, j, blo):
        blodic = {}
        blodiccnt = 0
        for i in range(len(data)):
            if (pd.isna(data[i][j])):
                continue
            elif (data[i][j] == blo):
                self.blocked_list[0].append(i)
        self.blocked_list.append([])
        return self.blocked_list

    '''
         iterate操作符：根据block操作中分完组的各个组生成其潜在可能违规的组,返回pair，生成候选冲突
         Parameters
         ----------
         data :
             数据集
         blocked_list :
             存放分好组的list列表
         Returns
         -------
         pair :
             返回根据blocked_list生成的候选冲突对,是一个三层的列表，pair[i]表示中blo中值相等，pair[i][j]表示潜在的违规对
             example :
                 [1, 2]表示1，2条数据为潜在的冲突对
     '''
    def iterate(self, blocked_list):
        pair = [[]]
        for i in range(len(blocked_list)):
            for j in range(len(blocked_list[i])):
                for k in range(j + 1, len(blocked_list[i])):
                    pair[i].append([blocked_list[i][j], blocked_list[i][k]])
            pair.append([])
        return pair
    '''
        generate：根据一个列表和一个字典生成一个表达式
        Parameters
        ----------
        newtemdic :
            列表，表示这条中规则要用到的列
        temdic :
            字典，指向每个列名对应违反的操作符
        Returns
        -------
        bds :
            返回生成的判断表达式
            example :
                ['str(li[l][attr_index["ounces"]])!=str(li[r][attr_index["ounces"]]) and int(li[l][attr_index["brewery_id"]])>int(li[r][attr_index["brewery_id"]])'
    '''

    def generate(self, index):
        biaodashi = []
        bds = ""
        for predicate in self.Rules[index].predicates:
            if (predicate.property[0] == "constant" or predicate.property[1] == "constant"):
                if (predicate.opt == '!='):
                    biaodashi.append("str(data[l][self.attr_index[\"" + str(predicate.components[0]) + "\"]])" + "!=" + "str(\"" + str(predicate.components[1]) + "\")")
                elif(predicate.opt == '='):
                    biaodashi.append("str(data[l][self.attr_index[\"" + str(predicate.components[0]) + "\"]])" + "==" + "str(\"" + str(predicate.components[1]) + "\")")
                else:
                    biaodashi.append("float(data[l][self.attr_index[\"" + str(predicate.components[0]) + "\"]])" + predicate.opt + "float(" + str(predicate.components[1]) + ")")
            else:
                if (predicate.opt == '!='):
                    biaodashi.append("str(data[l][self.attr_index[\"" + str(predicate.components[0]) + "\"]])" + "!=" + "str(data[r][self.attr_index[\"" + str(predicate.components[1]) + "\"]])")
                elif(predicate.opt == '='):
                    biaodashi.append("str(data[l][self.attr_index[\"" + str(
                        predicate.components[0]) + "\"]])" + "==" + "str(data[r][self.attr_index[\"" + str(
                        predicate.components[1]) + "\"]])")
                else:
                    biaodashi.append("float(data[l][self.attr_index[\"" + str(predicate.components[0]) + "\"]])" + predicate.opt + "float(data[r][self.attr_index[\"" + str(predicate.components[1]) + "\"]])")

        for i in range(len(biaodashi)):
            if (i == 0):
                bds = biaodashi[i]
            else:
                bds = bds + " and " + biaodashi[i]
        return bds
    '''
            detect：根据maypair和生成的表达式从潜在的违规maypair中生成真正的违规list：vio
            Parameters
            ----------
            maypair :
                iterate中生成的潜在违规对
            data :
                数据集
            Returns
            -------
            vio :
                返回生成的违规超边
                example :
                    <class 'list'>: [0, 1, (0, 1), (50, 1)]
                        其中vio[i]即为第i条超边
                        其中第1个数字，0表示违反了第0条规则，之后1个数字和2个元组指示了一组违规
                        3个数字中的第一个表示他们的操作符，如1表示"!=",后两个元组，表示违规的2个cell
                        如(0, 1)表示第0行第1列的cell
        '''
    def detect(self, maypair, data):
        print("Detecting Errors")
        for i in tqdm(range(len(maypair)-1), ncols=90):
            anotemdic = {"=": 0, "!=": 1, "<": 2, ">": 3, "<=": 4, ">=": 5}
            biaodashi = self.generate(i)
            for j in range(len(maypair[i])):
                for k in maypair[i][j]:
                    l = k[0]
                    r = k[1]
                    try:
                        eval(biaodashi)
                    except:
                        for predicate in self.Rules[i].predicates:
                            if (predicate.property[0] == "constant" or predicate.property[1] == "constant"):
                                pass
                            else:
                                if (predicate.opt != '=' and predicate.opt != '!='):
                                    try:
                                        float(data[l][self.attr_index[predicate.components[0]]])
                                    except:
                                        data[l][self.attr_index[predicate.components[0]]] = 0
                                    try:
                                        float(data[r][self.attr_index[predicate.components[1]]])
                                    except:
                                        data[r][self.attr_index[predicate.components[1]]] = 0

                    if (eval(biaodashi)):
                        self.vio.append([i])
                        for predicate in self.Rules[i].predicates:
                            if (predicate.property[0] == "constant" or predicate.property[1] == "constant"):
                                self.vio[self.cnt].append(anotemdic[predicate.opt])
                                self.vio[self.cnt].append((l, self.attr_index[predicate.components[0]]))
                                self.vio[self.cnt].append(predicate.components[1])
                            else:
                                self.vio[self.cnt].append(anotemdic[predicate.opt])
                                self.vio[self.cnt].append((l, self.attr_index[predicate.components[0]]))
                                self.vio[self.cnt].append((r, self.attr_index[predicate.components[1]]))
                        self.cnt += 1
        return self.vio

    # 参数为cell：违规的单元，edge：关联的边，oper：cell和edge违反的操作符，rc即repaircontext，存放表达式
    # diccop是一个字典字典中例如157：[1,2,3,4,5]表示第15行第7列的cell存在于第1，2，3，4，5条超边中，
    # mvcdic即为mvc得出的list，vio即为超边与上述的vio相同
    # 返回的是rc，rc中存放了所有的潜在的修复表达式
    '''
        lookup ：找到违规单元cell所有相关联的边，生成表达式
        Parameters ：
        ----------
        cell :
            违规的单元
        edge ;
            关联的边
        oper ;
            cell和edge违反的操作符
        rc :
            repaircontext,修复上下文，存放了表达式
        diccop :
            是一个字典，存放了整个超图
            example:
                {(1, 1): [2, 3, 4]}表示第1行第1列的cell存在于2，3，4三条超边中
        mvcdic :
            判断该值是否存在于mvc中
        vio :
            detect中生成的违规对的集合
        Returns
        -------
        rc :
            生成的修复上下文，里面存放了表达式
    '''

    def lookup(self, cell, edge, oper, diccop, mvcdic, vio, firstcell):
        if (firstcell != cell):
            return []
        self.exps.extend([[cell, edge, oper]])
        front = []
        try:
            front.extend(diccop[cell])
        except:
            pass
        for i in front:
            index1 = vio[i].index(cell)
            if (index1 % 3 == 2):
                index2 = index1 + 1
                index0 = index1 - 1
            if (index1 % 3 == 0):
                index2 = index1 - 1
                index0 = index1 - 2
            if (mvcdic.__contains__(vio[i][index2]) and vio[i][index2] != cell):
                continue
            if (vio[i][index2] in self.visdic):
                continue
            self.visdic[vio[i][index2]] = 1
            try:
                edges = diccop[vio[i][index2]]
            except:
                edges = []
                continue
            for j in edges:
                index11 = vio[j].index(vio[i][index2])
                if (index11 % 3 == 2):
                    index22 = index11 + 1
                    index00 = index11 - 1
                if (index11 % 3 == 0):
                    index22 = index11 - 1
                    index00 = index11 - 2
                if (mvcdic.__contains__(vio[j][index22])):
                    continue
                if (vio[j][index22] in self.visdic):
                    continue
                self.visdic[vio[j][index22]] = 1
                self.exps.extend(self.lookup(vio[i][index2], vio[j][index22], vio[j][index00], diccop, mvcdic, vio, cell))
        return self.exps

    # determination
    # 对rc中的表达式寻找最合适的修复，返回值为对于cell最终的修复
    '''
        determination ：对rc中的表达式寻找最合适的修复，返回值为对于cell最终的修复
        Parameters
        ----------
        cell :
            违规的单元
        exps :
            修复表达式
        data :
            数据集
        Returns
        -------
        finalthing or ll[0] :
            均为对于cell最终的修复
    '''

    def determination(self, exps, data):
        opt_dict = ["==", "!=", "<", ">", "<=", ">="]
        rep_dict = {}
        rep_dict.clear()
        max_v = -np.inf
        min_v = np.inf
        finalthing = -2
        for i in exps:
            temp1 = i[1][0]
            temp2 = i[1][1]
            if (opt_dict[i[2]] == "=="):
                continue
            if (opt_dict[i[2]] == "!="):
                if (data[temp1][temp2] in rep_dict):
                    rep_dict[data[temp1][temp2]] = rep_dict[data[temp1][temp2]] + 1
                else:
                    rep_dict[data[temp1][temp2]] = 1
            else:
                if (opt_dict[i[2]] == "<" or opt_dict[i[2]] == "<="):
                    if (max_v < float(data[temp1][temp2])):
                        max_v = float(data[temp1][temp2])
                    finalthing = max_v + 1
                else:
                    if (min_v > float(data[temp1][temp2]) and data[temp1][temp2] != 0):
                        min_v = float(data[temp1][temp2])
                    finalthing = min_v - 1

        if (finalthing != -2):
            return [finalthing]
        sorted_rep = sorted(rep_dict.items(), key=lambda x: x[1], reverse=True)
        rep_final = [item[0] for item in sorted_rep]
        try:
            return rep_final
        except:
            return [0]
    '''
        repair：跟据data和detect中生成的vio进行修复，是holistic算法中的algorithm1
                生成超图，对超图进行mvc算法，mvc得出错误cell，之后用lookup进行frontier的寻找，并得出表达式
                最后用determination得出最终修复，无法修复的根据postprocess进行修复
        Parameters
        ----------
        vio :
            detect中生成的违规对的集合
        data :
            数据集
        Returns
        -------
        data :
            完成修复的数据
        all_clean :
            进行的全部修复的总次数
        clean_right :
            进行的修复中的修复正确的次数
        clean_right_pre :
            进行的修复中的修复正确的次数,用来计算prec
    '''

    def repair(self, data, vio):
        sizebefore = 0
        sizeafter = 0
        processedcell = []
        input_data = read_graph_dc(vio)
        dicc = input_data.copy()
        for i in dicc:
            dicc[i] = list(set(dicc[i]))
        for i in dicc.items():
            processedcell.append(i[0])
        sizebefore = len(processedcell)
        self.repaired_cells = []
        self.clean_in_cands = []
        self.clean_in_cands_repair_right = []
        self.repair_right_cells = []
        self.repaired_cells_value = {}
        while (sizebefore > sizeafter):
            sizebefore = len(processedcell)
            input_data = read_graph_dc(vio)
            dicc = input_data.copy()

            for i in dicc:
                dicc[i] = list(set(dicc[i]))

            diccop = copy.deepcopy(dicc)
            self.mvc = greedy_min_vertex_cover_dc(dicc, vio)
            mvcdic = copy.deepcopy(self.mvc)
            while self.mvc:
                cell = self.mvc.pop()
                if self.PERFECTED and not self.ONLYED:
                    if (cell[0], self.schema.index(list(self.attr_index.keys())[cell[1]])) not in self.wrong_cells:
                        continue
                edges = dicc[cell]
                while edges:
                    edge = edges.pop()
                    index1 = vio[edge].index(cell)
                    '''
                        examples: 
                        对于[0, 1, (0, 1), (50, 1)]这个超边来说，如果你现在的cell是（0，1），
                        则其属于index1 % 3 == 2，index2表示他的另一个对应的cell，这里为（50，1），index为 index2 = 2 + 1
                        index0为其对应的操作符，index0 = 2 - 1。
                        假如对应的是（50，1）则index1 % 3 ==0 
                    '''
                    if (index1 % 3 == 2):
                        index2 = index1 + 1
                        index0 = index1 - 1
                    if (index1 % 3 == 0):
                        index2 = index1 - 1
                        index0 = index1 - 2
                    if (index1 % 3 == 1):
                        continue
                    self.visdic.clear()
                    self.edgedic.clear()
                    exps = []
                    exps = self.lookup(cell, vio[edge][index2], vio[edge][index0], diccop, mvcdic, vio, cell)
                l = cell[0]
                rr = cell[1]
                repair_cands = self.determination(exps, data)
                try:
                    truerepair = repair_cands[0]
                    if str(self.data_cl[l][rr]) in repair_cands:
                        self.clean_in_cands.append((l, self.schema.index(list(self.attr_index.keys())[rr])))
                        if ((str(truerepair) == str(self.data_cl[l][rr]))):
                            self.clean_in_cands_repair_right.append((l, self.schema.index(list(self.attr_index.keys())[rr])))
                except:
                    truerepair = 0
                self.exps.clear()
                self.all_clean = self.all_clean + 1
                self.repaired_cells.append((l, self.schema.index(list(self.attr_index.keys())[rr])))
                self.repaired_cells_value[(l, self.schema.index(list(self.attr_index.keys())[rr]))] = truerepair
                if ((str(truerepair) == str(self.data_cl[l][rr]))):
                    self.clean_right_pre = self.clean_right_pre + 1
                    self.repair_right_cells.append((l, self.schema.index(list(self.attr_index.keys())[rr])))
                if ((str(truerepair) == str(self.data_cl[l][rr])) and (data[l][rr] != self.data_cl[l][rr])):
                    self.clean_right = self.clean_right + 1
                data[l][rr] = truerepair
            print("Finish Repairing")
            vio = self.detect(self.maypair, data)
            input_data = read_graph_dc(vio)
            dicc = input_data.copy()
            if (len(list(dicc)) == 0):
                return data, self.all_clean, self.clean_right, self.clean_right_pre
            for i in dicc.items():
                processedcell.append(i[0])
            sizeafter = len(processedcell)
        self.all_clean, self.clean_right, self.clean_right_pre = self.postprocess(self.mvc, dicc, self.all_clean, self.clean_right, self.clean_right_pre)
        return data, self.all_clean, self.clean_right, self.clean_right_pre
    '''
        postprocess：跟对repair的内循环无法修复的mvc中的单元进行粗修复
        Parameters
        ----------
        mvc :
            mvc算法得出的cell
        dicc :
            是一个字典，存放了整个超图
            example:
                {(1, 1): [2, 3, 4]}表示第1行第1列的cell存在于2，3，4三条超边中
        data :
            数据集
        all_clean :
            进行的全部修复的总次数
        clean_righ :
            进行的修复中的修复正确的次数
        Returns
        -------
        all_clean :
            进行的全部修复的总次数
        clean_righ :
            进行的修复中的修复正确的次数
    '''
    def postprocess(self, mvc, dicc, all_clean, clean_right, clean_right_pre):
        while mvc:
            cell = mvc.pop()
            edges = dicc[cell]
            edge = edges.pop()
            index1 = self.vio[edge].index(cell)
            if (index1 % 3 == 2):
                index2 = index1 + 1
                index0 = index1 - 1
            if (index1 % 3 == 0):
                index2 = index1 - 1
                index0 = index1 - 2
            if (index1 % 3 == 1):
                continue
            l1 = cell[0]
            r1 = cell[1]
            l2 = self.vio[edge][index2][0]
            r2 = self.vio[edge][index2][1]
            if (self.vio[edge][index0] == 1):
                truerepair = self.data[l2][r2]
            if (self.vio[edge][index0] == 2):
                truerepair = self.data[l2][r2] - 1
            if (self.vio[edge][index0] == 3):
                truerepair = self.data[l2][r2] + 1
            if (self.vio[edge][index0] == 4):
                truerepair = self.data[l2][r2]
            if (self.vio[edge][index0] == 5):
                truerepair = self.data[l2][r2]
            all_clean += 1
            self.repaired_cells.append((l1, self.schema.index(list(self.attr_index.keys())[r1])))
            self.repaired_cells_value[(l1, self.schema.index(list(self.attr_index.keys())[r1]))] = truerepair
            if (str(truerepair) == str(self.data_cl[l1][r1])):
                clean_right_pre = clean_right_pre + 1
                self.repair_right_cells.append((l1, self.schema.index(list(self.attr_index.keys())[r1])))
            if ((str(truerepair) == str(self.data_cl[l1][r1])) and (self.data[l1][r1] != self.data_cl[l1][r1])):
                clean_right = clean_right + 1
            self.data[l1][r1] = truerepair
        return all_clean, clean_right, clean_right_pre

    def run(self, file_path, dirty_path, clean_path):
        import time
        self.start_time = time.time()
        self.dirty_path = dirty_path
        self.clean_path = clean_path
        # 获取列名
        dirty_df = pd.read_csv(dirty_path).astype(str).fillna("nan")
        self.schema = list(dirty_df.columns)
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            file = f.read()
        rules = file.split('\n')
        # 要进行scope的
        sco = []
        diccnt = 0
        flag = 0
        # 记录等号数量和非等号规则的数量，如果规则只含有等号，则不做任何处理
        equal_num = 0
        other_num = 0

        for rule in rules:
            equal_num = 0
            other_num = 0
            DR = DCRule(rule, self.schema)
            for predicate in DR.predicates:
                if (predicate.property[0] == "attribute"):
                    sco.append(predicate.components[0])
                if (predicate.property[1] == "attribute"):
                    sco.append(predicate.components[1])
                if (predicate.opt == '='):
                    equal_num += 1
                else:
                    other_num += 1
            DR_copy = copy.deepcopy(DR)
            DR_copy.att_copy(DR)
            self.Rules.append(DR_copy)
        attr_indexcnt = 0
        for i in range(len(sco)):
            sco[i] = sco[i].strip()
        sco = list(set(sco))
        sco = list(dirty_df.columns)
        for i in sco:
            self.sorts.append([])
            self.attr_index.setdefault(i, attr_indexcnt)
            attr_indexcnt += 1
        data = self.scope(sco)
        # all_wrong的计算
        all_wrong = 0
        self.data_cl = self.scope1(sco)
        df = pd.read_csv(dirty_path, header=0).astype(str).fillna("nan")
        data_wrong = np.array(df).tolist()
        df = pd.read_csv(clean_path, header=0).astype(str).fillna("nan")
        data_clean = np.array(df).tolist()
        self.wrong_cells = []
        for i in range(len(data_wrong)):
            for j in range(len(data_wrong[i])):
                try:
                    float(data_wrong[i][j])
                    float(data_clean[i][j])
                    if (float(data_wrong[i][j]) != float(data_clean[i][j])):
                        all_wrong += 1
                        self.wrong_cells.append((i, j))
                except:
                    if (str(data_wrong[i][j]) != str(data_clean[i][j])):
                        all_wrong += 1
                        self.wrong_cells.append((i, j))

        self.maypair = []
        for r in tqdm(range(len(self.Rules))):
            self.maypair.append([])
            self.maypair[r].append([])
            for i in range(len(dirty_df)):
                for j in range(i+1, len(dirty_df)):
                    self.maypair[r][0].append([i, j])

        viocntnt = 0
        print("Finish Blocking and Iterating")
        self.vio = self.detect(self.maypair, data)
        print("Finish Detectings")
        liclean, all_clean, clean_right, clean_right_pre = self.repair(data, self.vio)
        print("Finish Repairing")

        self.repaired_cells = list(set(self.repaired_cells))
        self.wrong_cells = list(set(self.wrong_cells))
        end_time = time.time()

        import os
        if not self.PERFECTED:
            det_right = 0
            out_path = os.path.join(self.output_path, "Exp_result", "rayyan", self.task_name[:-1], "onlyED_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            f = open(out_path, 'w')
            sys.stdout = f
            for cell in self.repaired_cells:
                if cell in self.wrong_cells:
                    det_right = det_right + 1
            pre = det_right / (len(self.repaired_cells)+1e-10)
            rec = det_right / (len(self.wrong_cells)+1e-10)
            f1 = 2*pre*rec/(pre+rec+1e-10)
            print("{pre}\n{rec}\n{f1}\n{time}".format(pre=pre, rec=rec, f1=f1, time=(end_time-self.start_time)))
            f.close()

            out_path = os.path.join(self.output_path, "Exp_result", "rayyan", self.task_name[:-1], "oriED+EC_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            res_path = os.path.join(self.output_path, "Repaired_res", "rayyan", self.task_name[:-1], "repaired_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".csv")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            os.makedirs(os.path.dirname(res_path), exist_ok=True)
            dirty_df = pd.read_csv(dirty_path)
            for cell, value in self.repaired_cells_value.items():
                dirty_df.iloc[cell[0], cell[1]] = value
            dirty_df.to_csv(res_path, index=False)
            f = open(out_path, 'w')
            sys.stdout = f
            rep_right = 0
            rep_total = len(self.repaired_cells)
            wrong_cells = len(self.wrong_cells)
            rec_right = 0
            for cell in self.repair_right_cells:
                rep_right += 1
            for cell in self.wrong_cells:
                if cell in self.repair_right_cells:
                    rec_right += 1
            pre = rep_right / (rep_total+1e-10)
            rec = rec_right / (wrong_cells+1e-10)
            f1 = 2*pre*rec / (rec+pre+1e-10)
            print("{pre}\n{rec}\n{f1}\n{time}".format(pre=pre, rec=rec, f1=f1, time=(end_time-self.start_time)))
            f.close()

            sys.stdout = sys.__stdout__
            out_path = os.path.join(self.output_path, "Exp_result", "rayyan", self.task_name[:-1], "all_computed_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            f = open(out_path, 'w')
            sys.stdout = f
            right2wrong = 0
            right2right = 0
            wrong2right = 0
            wrong2wrong = 0

            rep_total = len(self.repaired_cells)
            wrong_cells = len(self.wrong_cells)
            for cell in self.repair_right_cells:
                if cell in self.wrong_cells:
                    wrong2right += 1
                else:
                    right2right += 1
            print("rep_right:"+str(rep_right))
            print("rec_right:"+str(rec_right))
            print("wrong_cells:"+str(wrong_cells))
            print("prec:"+str(pre))
            print("rec:"+str(rec))
            print("wrong2right:"+str(wrong2right))
            print("right2right:"+str(right2right))
            self.repair_wrong_cells = [i for i in self.repaired_cells if i not in self.repair_right_cells]
            for cell in self.repair_wrong_cells:
                if cell in self.wrong_cells:
                    wrong2wrong += 1
                else:
                    right2wrong += 1
            print("wrong2wrong:"+str(wrong2wrong))
            print("right2wrong:"+str(right2wrong))
            print("proportion of clean value in candidates:"+str(len(self.clean_in_cands)/rep_total))
            if len(self.clean_in_cands) > 0:
                print("proportion of clean value in candidates and selected correctly:"+str(len(self.clean_in_cands_repair_right)/len(self.clean_in_cands)))
            else:
                print("proportion of clean value in candidates and selected correctly:0")
            f.close()
        else:
            end_time = time.time()
            rep_right = 0
            rep_total = len(self.repaired_cells)
            wrong_cells = len(self.wrong_cells)
            rec_right = 0
            rep_t = 0
            for cell in self.wrong_cells:
                if cell in self.repaired_cells:
                    rep_t += 1
                    if cell in self.repair_right_cells:
                        rec_right += 1
            pre = rec_right / (rep_t+1e-10)
            rec = rec_right / (wrong_cells+1e-10)
            f1 = 2*pre*rec / (rec+pre+1e-10)
            out_path = os.path.join(self.output_path, "Exp_result", "rayyan", self.task_name[:-1], "perfectED+EC_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            res_path = os.path.join(self.output_path, "Repaired_res", "rayyan", self.task_name[:-1], "perfect_repaired_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".csv")
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            os.makedirs(os.path.dirname(res_path), exist_ok=True)
            dirty_df = pd.read_csv(dirty_path)
            for cell, value in self.repaired_cells_value.items():
                dirty_df.iloc[cell[0], cell[1]] = value
            dirty_df.to_csv(res_path, index=False)
            f = open(out_path, 'w')
            sys.stdout = f
            print("{pre}\n{rec}\n{f1}\n{time}".format(pre=pre, rec=rec, f1=f1, time=(end_time-self.start_time)))
            f.close()
