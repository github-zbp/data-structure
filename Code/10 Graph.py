# coding = utf-8

# 顶点类
class Vertex:
    def __init__(self,key):
        self.key = key
        self.connect = {}   # 存储该节点所连接的节点，下标是Vertex节点对象，值是边的权重

    # 连接一个顶点
    def connectTo(self,nbr,weight=0):   # key是所连接的顶点的key
        self.connect[nbr] = weight

    def __str__(self):
        return str(self.key) + ' connect to ' + str([x.key for x in self.connect])

    # 获取所有本顶点连接的顶点（对象）
    def getConnections(self):
        return self.connect.keys()

    # 获取本顶点的key
    def getKey(self):
        return self.key

    # 获取本顶点和某一顶点所连接的边的权重
    def getWeight(self,nbr):
        return self.connect[nbr]


# 图
class Graph:
    def __init__(self,vertexClass=Vertex):  # 默认使用Vertex这个顶点类来实例化图的顶点
        self.vertList = {}      # 用于存放本图中所有的顶点,vertList的key是vertex顶点类的key，value是vertex顶点对象本身，一个顶点对象代表一个顶点
        self.vertNum = 0        # 本图中顶点个数
        self.vertexClass = vertexClass

    # 向图中添加一个顶点
    def addVertex(self,key):
        self.vertNum += 1
        newVertex = self.vertexClass(key)
        self.vertList[key] = newVertex
        return newVertex

    # 从图中获取某一个顶点
    def getVertex(self,key):
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def __contains__(self, key):
        return key in self.vertList

    # 为图中某两个顶点之间添加一条边，边是有方向的，是从from到to的
    def addEdge(self,f,t,cost=0,bothDirect=False): # cost就是边的权重,f和t是顶点的key,bothDirect是否双向添加边
        if f not in self.vertList:
            nv = self.addVertex(f)

        if t not in self.vertList:
            nv = self.addVertex(t)

        self.vertList[f].connectTo(self.vertList[t],cost)

        if bothDirect:
            self.vertList[t].connectTo(self.vertList[f],cost)

    # 获取图中所有顶点的key
    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def __str__(self):
        strVertList = {i:str(v) for i,v in self.vertList.items()}
        return str(strVertList)

# 词梯问题

# 为了适应词梯问题，需要对Vertex类进行扩展
class wordVertex(Vertex):
    def __init__(self,key):
        super(wordVertex,self).__init__(key)
        self.distance = 0   # 单词所在树的层数默认为0
        self.color = "w"    # 单词顶点的颜色默认是白色
        self.prefix = None  # 单词顶点的前驱顶点默认是None


# 构建一个单词关系图
def buildWordGraph(wordList):   # 传入一个单词列表
    d = {}      # dict
    g = Graph(wordVertex)

    # 字典d中的每一个元素都是一个set集合，每一个集合内的单词都是只差1个字母的单词
    for word in wordList:
        for i in range(len(word)):
            key = word[:i]+"_"+word[i+1:]
            if key not in d:
                d[key] = set()

            d[key].add(word)

    # 建立两个只差1个字母的单词的边。例如 fool 和 cool 之间会建立两条边，一条fool指向cool的边，一条cool指向fool的边。
    # 由于Graph这个类中的边是单向的，所以要对两个顶点建立两条边才能表示双向。
    for bucket in d:
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1,word2)

    return g

# 使用bfs算法构建树
def bfs(start):   # g是单词图，start是开始的单词的顶点对象
    vertQueue = []      # 探索队列
    vertQueue.insert(0,start)

    while len(vertQueue) > 0:
        currentVert = vertQueue.pop()  # 当前探索的顶点
        for nbr in currentVert.getConnections():
            if nbr.color == "w":   # 如果该相邻节点没有探索过才将他放入探索队列中
                nbr.distance = currentVert.distance + 1    # 设置该相邻节点在树中的层数
                nbr.prefix = currentVert    # 设置该相邻节点在树中的父节点
                currentVert.color = "g"  # 设置为正在探索的状态
                vertQueue.insert(0,nbr)    # 进入探索队列
            currentVert.color = "b"     # 设置为已探索状态

# 通过回溯的方式打印出最短路径
def getPath(destination):     # destination是结束的单词的顶点对象
    # 从树的叶节点往上层找,直到找到根节点
    print(destination.key)
    while destination.prefix != None:
        print(destination.prefix.key)
        destination = destination.prefix

# 骑士周游问题
# 构建棋盘图
def buildChaseGraph(bsize=5):     # bsize是棋盘大小，默认是5
    g = Graph(wordVertex)   # 由于棋盘问题的每个格子需要设置颜色以标明状态，所以这里使用wordVertex这个节点
    ways = [(-1,-2),(-2,-1),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]     # 方位有8个

    for y in range(bsize):
        for x in range(bsize):    # 一个格子一个格子的遍历
            id = getPos(x,y,bsize)  # 获取当前格子的序号
            for way in ways:
                if not outOfChase(x+way[0],y+way[1],bsize):  #  判断相邻格子是否超出边界，只留下没有超出边界的格子可以作为当前格子的相邻顶点
                    nbrId = getPos(x+way[0],y+way[1],bsize)   # 获取相邻格子的序号
                    g.addEdge(id,nbrId)

    return g

# 根据横纵坐标获取格子的序号,例如5*5的棋盘中，x=1,y=2的格子序号是11
# 其中第一个格子（左下角的格子）其坐标是 (0,0)
def getPos(x,y,bsize):
    return x+y*bsize

# 判断坐标是否超过棋盘范围
def outOfChase(x,y,bsize):
    if x < 0 or x>=bsize or y<0 or y>=bsize:
        return True
    else:
        return False

# 获取一个周游路径
def getPath(current,bsize,stack=[]):   # g是建立好的图，start是开始的格子的顶点,stack是用于记录路径的栈（用列表模拟栈）
    stack.append(current.key)
    current.color = "g"   # 标记该格子已探索

    if len(stack) == bsize*bsize:
        done = True
    else:
        done = False
        # nbrs = list(current.getConnections())   # 未改进的做法（不对current的相邻点排序）
        nbrs = orderByAvail(current)                # 改进的做法（对current的相邻点排序）

        i=0
        while i < len(nbrs) and not done:
            if nbrs[i].color == "w":
                done = getPath(nbrs[i],bsize,stack)
            i += 1

        if not done:
            current.color = "w"
            stack.pop()

    return done

# 对顶点 vert 的相邻顶点排序
def orderByAvail(vert):
    orderList = []
    for nbr1 in vert.getConnections():
        if nbr1.color == "w":
            c = 0   # 记录vert的每个相邻顶点的相邻顶点的个数
            for nbr2 in nbr1.getConnections():
                if nbr2.color == "w":
                    c += 1
            orderList.append((c,nbr1))

    # 对vert的相邻顶点排序
    orderList.sort(key=lambda x:x[0])

    return [y[1] for y in orderList]


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


# 最短路径算法
class shortVert(Vertex):
    def __init__(self,key,dist=0):
        super(shortVert,self).__init__(key)
        self.dist = dist   # 记录该节点和某一个节点间的距离
        self.pred = None    # 记录该节点的前驱（该前驱只针对以某一个作为起点的最短路径的前驱，也就是说，换一个起点这个前驱就会变）

# 这里我们使用一个有序队列实现优先队列
class PriorityQueue:
    def __init__(self,queue=[]):
        self.queue = queue     # 列表中的元素顶点对象
        self.buildQueue()

    # 添加一个元素，自动给改元素排序
    def push(self,item):
        self.queue.append(item)
        self.sortLastItem()

    # 弹出最小元素
    def pop(self):
        return self.queue.pop()

    def sortLastItem(self):
        itemPos = len(self.queue) - 1  # i是新添加的元素的位置
        finished = False
        while itemPos > 0 and not finished:
            if self.queue[itemPos].dist > self.queue[itemPos - 1].dist:
                self.queue[itemPos], self.queue[itemPos - 1] = self.queue[itemPos - 1], self.queue[itemPos]
                itemPos -= 1  # 更新新添加元素的位置
            else:
                finished = True

    # 给一个元素重新排序，del的复杂度是O(n)，所以不推荐使用
    # def resetPos(self,item):
    #     itemPos = 0
    #
    #     while itemPos < len(self.queue):
    #         if self.queue[itemPos] == item:
    #             break
    #         else:
    #             itemPos += 1
    #
    #     itemReset = self.queue[itemPos]
    #     del(self.queue[itemPos])
    #     self.push(itemReset)

    def resetPos(self,item,val):
        itemPos = 0

        # 根据元素值查找下标，其实可以用 self.queue.index(item)代替
        while itemPos < len(self.queue):
            if self.queue[itemPos] == item:
                break
            else:
                itemPos += 1

        # 修改节点的dist值
        item.dist = val

        finished = False
        while itemPos < len(self.queue)-1 and not finished:
            if self.queue[itemPos].dist < self.queue[itemPos+1].dist:
                self.queue[itemPos],self.queue[itemPos+1] = self.queue[itemPos+1],self.queue[itemPos]
                itemPos += 1
            else:
                finished = True
        
        finished = False
        while itemPos > 0 and not finished:
            if self.queue[itemPos].dist > self.queue[itemPos-1].dist:
                self.queue[itemPos],self.queue[itemPos-1] = self.queue[itemPos-1],self.queue[itemPos]
                itemPos -= 1
            else:
                finished = True

    # 构建一个优先队列(其实就是排序)
    def buildQueue(self):
        self.queue = self.__class__.quickSort(self.queue)

    # 使用快排法排序(这里排出来的是个倒序的)
    @classmethod
    def quickSort(cls,aList):
        if len(aList) <= 1:
            return aList
        # print(aList)
        mid = aList[0]
        left = []
        right = []

        for index in range(1,len(aList)):
            if aList[index].dist < mid.dist:
                right.append(aList[index])
            else:
                left.append(aList[index])
                
        left = cls.quickSort(left)
        right = cls.quickSort(right)

        return left + [mid] + right

    def __str__(self):
        return str([{vert.key:vert.dist} for vert in self.queue])

# 设置图中针对某一节点为起点的最短路径
import sys
def setShort(g,start):  # g是图，start是起点顶点
    # dist距离指某节点相对起点的真实距离。
    # 初始将图中起点的dist设为0，其他所有节点的dist设置为sys.maxsize
    # 将所有节点放入优先队列
    pq = PriorityQueue()
    for vert in g.vertList.values():
        vert.pred = None
        if start == vert:
            vert.dist = 0
        else:
            vert.dist = sys.maxsize

        pq.push(vert)

    # 当优先队列的元素为空则起点到其他所有顶点的最短路径就已经设置好了
    # 下面这段代码的作用是对所有非start的节点设置前驱
    # 之后查找start到顶点A的最短距离则是通过回溯A的前驱来完成的
    while len(pq.queue) > 0:
        nowVert = pq.pop()  # 弹出距离最短的节点；第一个弹出的节点肯定是start；优先队列中元素位置会随着距离的更新而改变

        # 设置当前节点的相邻节点的dist
        for nbr in nowVert.getConnections():
            newDist = nowVert.dist + nowVert.getWeight(nbr)     #  nbr的新距离等于nowVert到起点的距离+nbr到nowVert的距离

            # 如果nbr的新距离比nbr的旧距离短则更新nbr的距离
            if newDist < nbr.dist:
                pq.resetPos(nbr,newDist)   # 更新nbr的距离，同时改变nbr在优先队列中的位置
                nbr.pred = nowVert          # 设置nbr的前驱

# 获取最短路径
def getShort(start,destination):      # 传入起点和终点2个顶点
    path = []
    curVert = destination
    while curVert.pred:
        path.append(curVert.key)
        curVert = curVert.pred

    path.append(start.key)
    path.reverse()

    return path

# 最小生成树
# 该算法的实现和最短距离几乎一模一样，但是最小生成树算法中的dist不是某节点X到起点的距离，而是X的上游相邻节点们到X的距离的最小的那个距离
def prim(g,start):
    pq = PriorityQueue()
    for vert in g.vertList.values():
        vert.pred = None
        if vert == start:
            vert.dist = 0
        else:
            vert.dist = sys.maxsize
    

    while len(pq.queue) > 0:
        nowVert = pq.pop()      

        for nbr in nowVert.getConnections():
            newDist = nowVert.getWeight(nbr)    # *diff
            if nbr in pq.queue and newDist < nbr.dist:  # *diff
                pq.resetPos(nbr,newDist)   # 更新nbr的距离，同时改变nbr在优先队列中的位置
                nbr.pred = nowVert


if __name__ == "__main__":
    # 构建一个有距离的图
    g = Graph(shortVert)
    g.addEdge("u","v",2,True)
    g.addEdge("u","w",5,True)
    g.addEdge("u","x",1,True)
    g.addEdge("v","w",3,True)
    g.addEdge("v","x",2,True)
    g.addEdge("x","w",3,True)
    g.addEdge("x","y",1,True)
    g.addEdge("w","y",1,True)
    g.addEdge("w","z",5,True)
    g.addEdge("y","z",1,True)

    start = g.getVertex("u")
    end = g.getVertex("z")
    setShort(g,start)
    path = getShort(start,end)
    print(path)

