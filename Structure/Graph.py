# coding=utf-8

# 图

# 顶点类
class Vertex:
    def __init__(self, key):
        self.key = key      # 顶点的key
        self.connect = {}   # 顶点的边，下标是Vertex节点对象，值是边的权重

    # 连接一个顶点
    def connectTo(self, nbr, weight = 0):
        self.connect[nbr] = weight     # nbr 是节点对象

    # 获取本顶点指向的所有相邻顶点（不含其它顶点指向本顶点的相邻顶点）
    def getConnections(self):
        return self.connect.keys()

    # 获取本顶点的key
    def getKey(self):
        return self.key

    # 获取某个相邻顶点的权重
    def getWeight(self, nbr):
        return self.connect[nbr]

    def __str__(self):
        return str(self.key) + 'connect to' + str([vertex.key for vertex in self.connect])

# 图
class Graph:
    def __init__(self):
        self.vertList = {}   # 图中所有顶点集合
        self.vertNum = 0

    # 添加一个顶点
    def addVertex(self, key):
        self.vertNum += 1
        self.vertList[key] = Vertex(key)
        return self.vertList[key]

    # 从图中根据key获取某一个顶点
    def getVertex(self, key):
        return self.vertList[key] if key in self.vertList else None

    # 为两个节点添加有向边
    def addEdge(self, fromVertKey, toVertKey, weight):
        if fromVertKey not in self.vertList:
            self.addVertex(fromVertKey)

        if toVertKey not in self.vertList:
            self.addVertex(toVertKey)

        self.vertList[fromVertKey].connectTo(self.vertList[toVertKey], weight)

    # 获取图中所有顶点的key
    def getVertKeys(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

#####################################################

# 带有深度优先算法的图
class DFSVertex(Vertex):    # 为dfs算法而设的顶点
    def __init__(self,key):
        super(DFSVertex,self).__init__(key)
        self.st = 0   # 顶点开始被探索的时间点
        self.et = 0   # 顶点被探索完成的时间点
        self.color = "w"    # 节点状态，g是正在被探索，b是已被探索
        self.prefix = None  # 节点的前置节点，该属性可以让我们知道该节点在其所在的树中的父节点是谁

class DFSGraph(Graph):
    def __init__(self):
        super(DFSGraph, self).__init__()
        self.time = 0

    # 深度优先算法对图构建树或者森林
    def dfs(self):
        for aVertex in self.vertList:    # 将所有顶点的状态设为初始状态（未探索过，前置为空）
            aVertex.color = "w"
            aVertex.prefix = None

        # 开始探索所有的顶点
        for aVertex in self.vertList.values():
            if aVertex.color == "w":  # 只探索未探索过的节点
                self.explore(aVertex)

    # 探索节点（就是不停的往节点的下层找相邻节点）
    def explore(self,aVertex):      # 从dfs()内部调用explore()传进来的aVertex全都是起始顶点（也是树的根节点）
        aVertex.color = "g"     # 标记为正在探索
        self.time += 1
        aVertex.st = self.time  # 标记开始探索时间

        # 对该节点的相邻节点进行探索
        for nbr in aVertex.getConnections():
            if nbr.color == "w":
                nbr.prefix = aVertex    # 标记前置节点
                self.explore(nbr.color)

        # 探索完该节点和该节点的所有下层节点后
        aVertex.color = "b"     # 标记该节点为已探索
        self.time += 1
        aVertex.et = self.time  # 标记探索完的时间
