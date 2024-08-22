#导入库
import matplotlib.pyplot as plt
def getplt():
    plt.rcParams['font.sans-serif'] = ['STSong']
    plt.rcParams['axes.unicode_minus'] = False

    #设定画布。dpi越大图越清晰，绘图时间越久
    # p=[0.6521739130434783, 0.7, 0.6021505376344086, 0.5431818181818182, 0.42986247544204322]
    # t=[36.8729031085968, 76.4940276145935, 151.04747772216797, 352.74730134010315, 707.4098641872406]
    p=[0.447937131631, 0.488821218075, 0.5114341846758, 0.485265225933]
    t=[725.629695892334, 1021.0421087741852, 1215.7561395168304, 1493.8742818832397]
    #导入数据
    x=list([5,7,9,11])
    #绘图命令
    plt.plot(x, p, lw=4, ls='-', c='b', alpha=0.1)
    plt.plot()
    plt.xlabel("n", fontdict={'size': 16})
    plt.ylabel("p", fontdict={'size': 16})
    plt.title("搜索深度和准确率关系图", fontdict={'size': 15})
    #show出图形
    plt.show()
    #保存图片

    plt.plot(x, t, lw=4, ls='-', c='b', alpha=0.1)
    plt.plot()
    plt.xlabel("n", fontdict={'size': 16})
    plt.ylabel("t(s)", fontdict={'size': 16})
    plt.title("搜索深度和时间关系图", fontdict={'size': 15})
    #show出图形
    plt.show()
    #保存图片