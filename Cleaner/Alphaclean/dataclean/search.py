"""
Module: search

A best-first search expands the most promising nodes chosen  according  to  a  specified  cost  function.
We  consider  a greedy  version  of  this  algorithm,  which  removes  nodes  on the frontier that are more than
\gamma times worse than the current  best  solution.   Making \gamma larger  makes  the  algorithm asympotically  
consistent,  whereas \gamma=  1  is  a  pure  greedy search.
"""

import numpy as np
import datetime

from .generators import *
from heapq import *

from dataclean.learning import *

# special case optimizations require references to the pattern objects
from dataclean.constraint_languages.pattern import *

# Configuration schema
DEFAULT_SOLVER_CONFIG = {}

DEFAULT_SOLVER_CONFIG['pattern'] = {    # 模式
    'depth': 10,  ##搜索深度
    'gamma': 5,  ##贪心值
    'edit': 1,
    'operations': [Delete],  # 算子选择
    'similarity': {},
    'w2v': '../resources/GoogleNews-vectors-negative300.bin'
}

DEFAULT_SOLVER_CONFIG['dependency'] = { ##依赖
    'depth': 10,
    'gamma': 5,
    'edit': 3,
    'operations': [Swap],  # 算子选择
    'similarity': {},
    'w2v': '../resources/GoogleNews-vectors-negative300.bin'
}


def solve(df, patterns=[], dependencies=[], partitionOn=None, config=DEFAULT_SOLVER_CONFIG):
    """The solve function takes as input a specification in terms of a list of patterns and 
    a list of depdencies and returns a cleaned instance and a data cleaning program.
    solve函数以模式列表和依赖列表的形式作为输入，并返回一个经过清理的实例和一个数据清理程序。
    Release notes: patterns have precedence over dependenceis should do this properly in the future

    Positional arguments:
    df -- Pandas DataFrame
    patterns -- a list of single attribute pattern constraints//单属性的模式
    dependencies -- a list of single or multiple attribute constraints that are run after the pattern constraints//多属性之间的依赖
    patitionOn -- a blocking rule to partition the dataset//利用规则来划分数据集
    config -- a config object
    """

    op = NOOP()

    logging.debug('Starting the search algorithm with the following config: ' + str(df.shape) + " " + str(config))

    if needWord2Vec(config):  ##是否需要w2v
        w2vp = loadWord2Vec(config['pattern']['w2v'])
        w2vd = loadWord2Vec(config['dependency']['w2v'])  ##repair

        logging.debug('Using word2vec for semantic similarity')

    else:
        w2vp = None
        w2vd = None

    config['pattern']['model'] = w2vp
    config['dependency']['model'] = w2vd

    training_set = (set(), set())
    pruningModel = None
    edit_score = 0
    if partitionOn != None:

        logging.warning("You didn't specify any blocking rules, this might be slow")

        blocks = set(df[partitionOn].dropna().values)

        # df = df.set_index(partitionOn)

        for i, b in enumerate(blocks):
            logging.info("Computing Block=" + str(b) + ' ' + str(i + 1) + " out of " + str(len(blocks)))

            print("Computing Block=" + str(b) + ' ' + str(i + 1) + " out of " + str(len(blocks)))

            dfc = df.loc[df[partitionOn] == b].copy()

            logging.debug("Block=" + str(b) + ' size=' + str(dfc.shape[0]))

            op1, dfc, edit = patternConstraints(dfc, patterns, config['pattern'])
            edit_score = edit_score + edit
            op2, output_block, edit, training = dependencyConstraints(dfc, dependencies, config['dependency'], pruningModel)
            edit_score = edit_score + edit
            # update output block
            now = datetime.datetime.now()
            df.loc[df[partitionOn] == b] = output_block
            print((datetime.datetime.now() - now).total_seconds())
            if training != None :
                training_set = (training_set[0].union(training[0]), training_set[1].union(training[1]))
            # learning method
                pruningModel = getFeatures(training_set[0], training_set[1], df)

            if len(training_set[0]) > 10000:
                exit()

            op = op * (op1 * op2)

    else:

        op1, df , edit = patternConstraints(df, patterns, config['pattern'])
        edit_score = edit_score + edit
        op2, df, edit, _ = dependencyConstraints(df, dependencies, config['dependency'])
        edit_score = edit_score + edit
        op = op * (op1 * op2)

    return op, df, edit_score


def loadWord2Vec(filename):
    """导入word2vec模型"""
    from gensim.models.keyedvectors import KeyedVectors
    return KeyedVectors.load_word2vec_format(filename, binary=True)


def needWord2Vec(config):
    """判断是否需要word2vec"""
    semantic_in_pattern = 'semantic' in [config['pattern']['similarity'][k] for k in config['pattern']['similarity']]
    semantic_in_dependency = 'semantic' in [config['dependency']['similarity'][k] for k in
                                            config['dependency']['similarity']]
    return semantic_in_pattern or semantic_in_dependency


def patternConstraints(df, costFnList, config):
    """Enforces pattern constrains"""

    op = NOOP()
    edit = 0
    for c in costFnList:

        logging.debug('Enforcing pattern constraint=' + str(c))
        # print('Enforcing pattern constraint=' + str(c))
        if isinstance(c, Date):
            d = DatetimeCast(c.attr, c.pattern)
            df = d.run(df)
            op = op * d

        elif isinstance(c, Pattern):
            d = PatternCast(c.attr, c.pattern)
            df = d.run(df)
            op = op * d

        elif isinstance(c, Float):
            d = FloatCast(c.attr, c.range)
            df = d.run(df)
            op = op * d

        transform, df, edit_score, _ = treeSearch(df, c, config['operations'], evaluations=config['depth'],
                                      inflation=config['gamma'], editCost=config['edit'],
                                      similarity=config['similarity'], word2vec=config['model'])

        op = op * transform
        edit = edit + edit_score
    return op, df, edit


def dependencyConstraints(df, costFnList, config, pruningModel=None):
    """enforces dependency constraints"""

    op = NOOP()
    edit = 0
    training = None
    for c in costFnList:
        logging.debug('Enforcing dependency constraint=' + str(c))
        # print('Enforcing dependency constraint=' + str(c))
        # print(config)
        transform, df, edit_score, training = treeSearch(df, c, config['operations'], evaluations=config['depth'], \
                                             inflation=config['gamma'], editCost=config['edit'],
                                             similarity=config['similarity'], \
                                             word2vec=config['model'],
                                             pruningModel=pruningModel)
        op = op * transform
        edit = edit + edit_score
    return op, df, edit, training


def treeSearch(df, costFn, operations, evaluations, inflation, editCost,
               similarity, word2vec, pruningModel=None):
    """This is the function that actually runs the treesearch

    Positional arguments:
    df -- Pandas DataFrame
    costFn -- a cost function
    operations -- a list of operations//算子库，swap或delete，或其他组合
    evaluation -- a total number of evaluations
    inflation -- gamma
    editCost -- scaling on the edit cost
    similarity -- a dictionary the specified similarity metrics to use
    word2vec -- a word2vec model (avoid reloading things)
    """

    editCostObj = CellEdit(df.copy(), similarity, word2vec)
    efn = editCostObj.qfn

    best = (2.0, NOOP(), df)
    edit_score = 0
    branch_hash = set()
    branch_value = hash(str(df.values))
    branch_hash.add(branch_value)

    bad_op_cache = set()

    search_start_time = datetime.datetime.now()

    all_operations = set()
    for i in range(evaluations):

        level_start_time = datetime.datetime.now()

        logging.debug('Search Depth=' + str(i))

        value, op, frame = best


        # prune
        if (value - op.depth) > best[0] * inflation:
            continue

        bfs_source = frame.copy()

        p = ParameterSampler(bfs_source, costFn, operations, editCostObj)

        costEval = costFn.qfn(bfs_source)

        for l, opbranch in enumerate(p.getAllOperations()):

            logging.debug('Search Branch=' + str(l) + ' ' + opbranch.name)

            if not isinstance(opbranch, NOOP):
                all_operations.add(opbranch)

            # prune bad ops
            if opbranch.name in bad_op_cache:
                continue
            # learning method
            if pruningModel != None and not predict(pruningModel, opbranch, df):
                print("Pruned: ", opbranch)
                continue

            nextop = op * opbranch

            # disallow trasforms that cause an error
            try:
                output = opbranch.run(frame)
            except:
                logging.warn('Error in Search Branch=' + str(l) + ' ' + opbranch.name)
                bad_op_cache.add(opbranch.name)
                continue

            editfn = np.sum(efn(output))
            # evaluate pruning
            if pruningRules(output):
                logging.debug('Pruned Search Branch=' + str(l) + ' ' + opbranch.name)
                continue

            costEval = costFn.qfn(output)

            n = (np.sum(costEval) + editCost * editfn) / output.shape[0]

            if n < best[0]:
                logging.debug('Promoted Search Branch=' + str(l) + ' ' + opbranch.name)
                edit_score = editfn
               # print(n,editfn)
                best = (n, nextop, output)

        logging.debug(
            'Search Depth=' + str(i) + " took " + str((datetime.datetime.now() - level_start_time).total_seconds()))

    logging.debug('Search  took ' + str((datetime.datetime.now() - search_start_time).total_seconds()))

    return best[1], best[2], edit_score, (all_operations.difference(set(best[1].provenance)), set(best[1].provenance))


def pruningRules(output):
    if output.shape[1] == 0:
        return True

    elif output.shape[0] == 0:
        return True

    return False
