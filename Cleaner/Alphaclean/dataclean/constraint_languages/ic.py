import numpy as np
from dataclean.constraints import *
from collections import Counter

"""Module: ic

This module describes classes that represent various types of integrity constraints.
"""


class FunctionalDependency(Constraint):
    """FunctionalDependency represents a functional dependency between two sets of attributes. A functional dependency (A -> B) implies that 
    for every value B there exists a single value A.
    """

    def __init__(self, source, target):
        """FunctionalDependency constructor

        Positional arguments:
        source -- a list of attribute names
        target -- a list of attribute names
        """

        self.source = source
        self.target = target

        self.hint = set(source + target)
        self.hintParams = {}

    def __str__(self):
        return '(source: %s,target: %s)' % (self.source, self.target)

    def __add__(self, other):
        """__mul__ bitwise and relationship two quality functions """
        if isinstance(self, FunctionalDependency):
            self.msg = '(source: %s,target: %s union source: %s,target: %s)' % (self.source, self.target, other.source,
                                                                                other.target)
        return super(FunctionalDependency, self).__add__(other);

    def __mul__(self, other):
        """__mul__ bitwise and relationship two quality functions """
        if isinstance(self, FunctionalDependency):
            self.msg = '(source: %s,target: %s union source: %s,target: %s)' % (self.source, self.target, other.source,
                                                                                other.target)
        return super(FunctionalDependency, self).__mul__(other);

    def _qfn(self, df):

        N = df.shape[0]
        kv = {}
        normalization = 0

        for i in range(N):
            s = tuple(df[self.source].iloc[i, :])
            t = tuple(df[self.target].iloc[i, :])
            if s in kv:
                kv[s].add(t)
            else:
                kv[s] = set([t])

            normalization = max(len(kv[s]), normalization)# source对应最多的target个数
        qfn_a = np.zeros((N,))
        for i in range(N):
            s = tuple(df[self.source].iloc[i, :])
            qfn_a[i] = float(len(kv[s]) - 1) / normalization# 聚合查询

        return qfn_a


class new_FunctionalDependency(Constraint):
    """FunctionalDependency represents a functional dependency between two sets of attributes. A functional dependency (A -> B) implies that
    for every value B there exists a single value A.
    """

    def __init__(self, source, target):
        """FunctionalDependency constructor

        Positional arguments:
        source -- a list of attribute names
        target -- a list of attribute names
        """

        self.source = source
        self.target = target

        self.hint = set(source + target)
        self.hintParams = {}

    def __str__(self):
        return '(source: %s,target: %s)' % (self.source, self.target)

    def __add__(self, other):
        """__mul__ bitwise and relationship two quality functions """
        if isinstance(self, FunctionalDependency):
            self.msg = '(source: %s,target: %s union source: %s,target: %s)' % (self.source, self.target, other.source,
                                                                                other.target)
        return super(new_FunctionalDependency, self).__add__(other);

    def __mul__(self, other):
        """__mul__ bitwise and relationship two quality functions """
        if isinstance(self, new_FunctionalDependency):
            self.msg = '(source: %s,target: %s union source: %s,target: %s)' % (self.source, self.target, other.source,
                                                                                other.target)
        return super(new_FunctionalDependency, self).__mul__(other);

    def _qfn(self, df):

        N = df.shape[0]
        kv = {}
        normalization = 0

        for i in range(N):
            s = tuple(df[self.source].iloc[i, :])
            t = tuple(df[self.target].iloc[i, :])
            if s in kv:
                kv[s].append(t)
            else:
                kv[s] = [t]

            #normalization = max(len(kv[s]), normalization)# source对应最多的target个数

        qfn_a = np.zeros((N,))
        for i in range(N):
            s = tuple(df[self.source].iloc[i, :])
            normalization = len(kv[s])
            count =  Counter(kv[s])
            dic = dict(count)
            if(len(dic.keys()) == 1) :
                qfn_a[i] = 0;
                continue;
            qfn_a[i] = 1 - float(dic[tuple(df[self.target].iloc[i, :])])/normalization


        return qfn_a




def OneToOne(source, target):
    """A OneToOne dependency is a common type of FD pair which we add some syntactic sugar for 
    """
    return  new_FunctionalDependency(source, target) + new_FunctionalDependency(target, source)  # 双向映射，同时乘法使得他们的类型变了


def OneDeterminedOne(source, target):
    """A OneDeterminedOne dependency is a common type of FD pair which we add some syntactic sugar for
    多对一
    """
    return FunctionalDependency(source, target)   # 单向映射


def OneDeterminedSeveral(source, target):
    """A OneDeterminedOne dependency is a common type of FD pair which we add some syntactic sugar for
    一对多
    """
    return FunctionalDependency(target, source)   # 单向映射


class DenialConstraint(Constraint):
    """A DenialConstraint is another way to represent a integrity constraints. A denial constraint
    is a set of predicates that cannot all be true.
    通过否定约束的方式实现复杂谓词检测
    """

    def __init__(self, predicateList):
        """DenialConstraint constructor

        Positional arguments:

        predicateList -- a List[DCPredicate]
        """

        self.predicateList = predicateList
        self.attrs = set([dcp.local_attr for dcp in predicateList])
        self.hint = self.attrs
        super(DenialConstraint, self).__init__(self.hint)

    def _qfn(self, df):

        N = df.shape[0]
        qfn_a = np.ones((N,))

        for i in range(N):

            for dcp in self.predicateList:
                val = dcp.get(df).iloc[i]

                if val == None:
                    qfn_a[i] = 0.0
                    break

                if not dcp.eval(val, df):
                    qfn_a[i] = 0.0
                    break

        return qfn_a


class DCPredicate(Constraint):
    """
    A DCPredicate is just a wrapper object for intepretability. The basic structure of a DCPredicate is
    as follows:
    * This predicate is applied to every row of the dataframe.
    * For each row, we can query an attribute called the "local attribute"
    * then, we can evaluate a boolean expression over this value and over the entire dataframe
    """

    def __init__(self, local_attr, expression):
        """ DCPredicate contructor

        Positional arguments:
        local_attr -- an attribute name
        expression -- a function mapping fn: domain(local_attr) x df -> {true, false}
        """
        self.local_attr = local_attr
        self.expression = expression

    def get(self, df):
        """Projects the provided dataframe onto the specified attribute

        Positional arguments:
        df -- a dataframe
        """
        return df[self.local_attr]

    def eval(self, value, df):
        """Evaluates the predicate

        Positional arguments:
        value -- a value from domain(local_attr)
        df -- a dataframe
        """
        return self.expression(value, df)


class DictValue(Predicate):
    """
    A DictValue constraint enforces that domain of a speficied attribute conforms to a dictionary
    """

    def __init__(self, attr, codebook, threshold=0.1):
        """ DictValue constructor

        Positional arguments:
        attr -- an attribute name
        codebook -- a dictionary with the allowed domain
        """

        self.attr = attr

        self.threshold = threshold

        self.codebook = codebook

        super(DictValue, self).__init__(attr, lambda x, codebook=codebook: x in codebook)
