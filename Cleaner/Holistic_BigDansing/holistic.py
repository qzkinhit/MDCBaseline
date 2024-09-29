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

    def iterate(self, blocked_list):
        pair = [[]]
        for i in range(len(blocked_list)):
            for j in range(len(blocked_list[i])):
                for k in range(j + 1, len(blocked_list[i])):
                    pair[i].append([blocked_list[i][j], blocked_list[i][k]])
            pair.append([])
        return pair

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
            out_path = os.path.join(self.output_path, "Exp_result", "holistic", self.task_name[:-1], "onlyED_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
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

            out_path = os.path.join(self.output_path, "Exp_result", "holistic", self.task_name[:-1], "oriED+EC_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            res_path = os.path.join(self.output_path, "Repaired_res", "holistic", self.task_name[:-1], "repaired_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".csv")
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
            out_path = os.path.join(self.output_path, "Exp_result", "holistic", self.task_name[:-1], "all_computed_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
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
            out_path = os.path.join(self.output_path, "Exp_result", "holistic", self.task_name[:-1], "perfectED+EC_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".txt")
            res_path = os.path.join(self.output_path, "Repaired_res", "holistic", self.task_name[:-1], "perfect_repaired_" + self.task_name + check_string(self.dirty_path.split("/")[-1]) + ".csv")
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
