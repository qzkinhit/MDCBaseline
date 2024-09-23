#!/usr/bin/python
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import unicodedata
import numpy as np
# there is no cross_validation module in sklearn0.24, use model_selection instead
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import hstack, vstack
import random
import pickle


# test data只包括clean的
def activeclean(dirty_data, clean_data, test_data, full_data, indextuple, batchsize=50, total=10000):
	#makes sure the initialization uses the training data
    # 训练集中dirty的部分
	X = dirty_data[0][translate_indices(indextuple[0],indextuple[1]),:]
	y = dirty_data[1][translate_indices(indextuple[0],indextuple[1])]

	X_clean = clean_data[0]
	y_clean = clean_data[1]

	X_test = test_data[0]
	y_test = test_data[1]

	print("[ActiveClean Real] Initialization")
	txt = "[ActiveClean Real] Initialization"

	# 干净的index
	lset = set(indextuple[2])
	dirtyex = [i for i in indextuple[0]]
	cleanex = []

	total_labels = []



	##Not in the paper but this initialization seems to work better, do a smarter initialization than
	##just random sampling (use random initialization)
	# 在训练集中随机抽取batchsize个
	topbatch = np.random.choice(range(0,len(dirtyex)), batchsize)
	# real中存储的是索引，是训练集中抽取的数据在整个数据集(full_data)的索引
	examples_real = [dirtyex[j] for j in topbatch]
	# map中存储的是索引，与real相同，real中数据中干净的部分
	examples_map = translate_indices(examples_real, indextuple[2])

	# 这里有一个问题：cleanex中添加的是干净的部分，而dirtyex把所有抽样数据都删除了
	# 所以cleanex与dirtyex取并集不等于train
	#Apply Cleaning to the Initial Batch
	cleanex.extend(examples_map)
	for j in examples_real:
		dirtyex.remove(j)


	clf = SGDClassifier(loss="hinge", alpha=0.000001, max_iter=200, fit_intercept=True, warm_start=True)
	# 利用抽样的干净的训练集cleanex训练分类器
	clf.fit(X_clean[cleanex,:],y_clean[cleanex])

	for i in range(50, total, batchsize):
		# 用当前的下游模型训练测试集
		# 这里不涉及信息泄露，因为只作为效果的参考，没有用于模型训练过程
		print("[ActiveClean Real] Number Cleaned So Far ", len(cleanex))
		ypred = clf.predict(X_test)
		print("[ActiveClean Real] Prediction Freqs", np.sum(ypred), np.shape(ypred))
		print(classification_report(y_test, ypred))
		txt += "\n[ActiveClean Real] Number Cleaned So Far : " + str(len(cleanex))
		txt += "\n[ActiveClean Real] Prediction Freqs : " + str(np.sum(ypred))
		txt += "\n" + classification_report(y_test, ypred)

		#Sample a new batch of data
		examples_real = np.random.choice(dirtyex, batchsize)
		examples_map = translate_indices(examples_real, indextuple[2])

		# 判断抽样的数据是否是干净的，并把这些数据以及对应的label（是否干净）存在total_label中
		total_labels.extend([(r, (r in lset)) for r in examples_real])

		#on prev. cleaned data train error classifier
		ec = error_classifier(total_labels, full_data)

		# 把本次抽样的从dirtyex中移除
		for j in examples_real:
			try:
				dirtyex.remove(j)
			except ValueError:
				pass

		# 剔除准确率高的部分
		dirtyex = ec_filter(dirtyex, full_data, ec)

		# Add Clean Data to The Dataset
		# 在cleanex加入的是map不是real
		# 注意：这里只认可真正干净的数据，不认可分类器认为干净的数据
		cleanex.extend(examples_map)
		# uses partial fit (not in the paper--not exactly SGD)
		clf.partial_fit(X_clean[cleanex,:],y_clean[cleanex])


		print("[ActiveClean Real] Accuracy ", i ,accuracy_score(y_test, ypred))
		txt += "[ActiveClean Real] Accuracy " + str(i) + " : " + str(accuracy_score(y_test, ypred))

		if len(dirtyex) < 50:
			print("[ActiveClean Real] No More Dirty Data Detected")
			txt += "\n[ActiveClean Real] No More Dirty Data Detected"
			break;
	return txt

# 返回globali在imap中的元素及其索引
def translate_indices(globali, imap):
	lset = set(globali)
	return [s for s,t in enumerate(imap) if t in lset]


# 利用抽样的数据的label训练一个错误检测的分类器
def error_classifier(total_labels, full_data):
	indices = [i[0] for i in total_labels]
	labels = [int(i[1]) for i in total_labels]
	# 判断是否所有的label都是clean
	if np.sum(labels) < len(labels):
		clf = SGDClassifier(loss="log_loss", alpha=1e-6, max_iter=200, fit_intercept=True)
		clf.fit(full_data[indices,:],labels)
		#print labels
	#print clf.score(full_data[indices,:],labels)
		return clf
	else:
		return None


# sec5.3 in paper
def ec_filter(dirtyex, full_data, clf, t=0.90):
	if clf != None:
		pred = clf.predict_proba(full_data[dirtyex,:])
		#print pred
		#print len([j for i,j in enumerate(dirtyex) if pred[i][0] < t]), len(dirtyex)
		return [j for i,j in enumerate(dirtyex) if pred[i][0] < t]

	print("CLF none")

	return dirtyex


def run(filepath):
	# data是字典的形式，一共有8个元素，即下面访问的8个"../../Data/IMDB/"+filepat
	data = pickle.load(open("../../Data/"+filepath,'rb'), encoding='latin1')
	# X是以稀疏矩阵的形式存储，每个元素标记了坐标和取值
	# y为array，标签为0 1
	# indice表示clean和dirty在full中的下标
	# size是int，表示full的大小
	X_clean = data['X_clean']
	y_clean = data['y_clean']
	X_dirty = data['X_dirty']
	y_dirty = data['y_dirty']
	X_full = data['X_full']
	indices_dirty = data['indices_dirty']
	indices_clean = data['indices_clean']
	size = data['shape']
	examples = np.arange(0,size,1)
	# 抽取训练集和测试集的下标；找到测试集索引中clean的索引和索引的索引（这里实现的好乱）
	# 注意是找到了测试集中干净的
	train_indices, test_indices = train_test_split(examples, test_size=0.20)
	clean_test_indices = translate_indices(test_indices,indices_clean)
	txt = activeclean((X_dirty, y_dirty),(X_clean, y_clean),(X_clean[clean_test_indices,:], y_clean[clean_test_indices]),X_full,(train_indices,indices_dirty,indices_clean))
	return txt