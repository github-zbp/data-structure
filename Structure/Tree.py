# coding=utf-8

# 树（链表实现）

# 节点类
class Node:
    def __init__(self,value=''):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return str({'value':self.value, 'left':str(self.left), 'right':str(self.right)})


# 树
class BinaryTree(Node):
    def insertLeft(self, value):
        tree = BinaryTree(value)    # 创建一个左子树

        if self.left:
            tree.left = self.left

        self.left = tree

    def insertRight(self, value):
        tree = BinaryTree(value)    # 创建一个右子树

        if self.right:
            tree.right = self.right

        self.right = tree

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getRootValue(self):
        return self.value

    def setRootValue(self,value):
        self.value = value


###############################################

# 二叉堆实现优先队列
class BinaryHeap:
    def __init__(self):
        self.heapList = [0]     # 用一个不嵌套的列表表示二叉堆（优先队列）；将第一个元素设为0的目的是为了让根节点从下标1开始，这样就可以满足“某一个节点的下标为p，那么其左子节点的下标为2p,右子节点下标为2p+1，父节点下标为 p//2”这个条件；所以第一个元素0只是为了占位
        self.currentSize = 0    # 记录树节点个数,它既是节点个数，也是最后一个节点的下标

    # 往优先队列尾部插入
    def insert(self,item):
        self.heapList.append(item)
        self.currentSize += 1

        # 元素插入尾部后做数据上浮
        self.__percUp()

    # 从优先队列头部弹出元素
    def pop(self):
        minVal = self.heapList[1]   # 这里不要用pop(1)然后再用insert(1,self.heapList[-1])，因为这两个都是O(n)的复杂度
        self.heapList[1] = self.heapList[-1]
        self.heapList.pop()
        self.currentSize -= 1

        # 尾部元素补上根节点后做根节点下沉
        self.__percDown(1)  # 传入的1是根节点下标，表示要下沉根节点
        return minVal

    # 传入一个无序的列表，根据这个列表构建出一个二叉堆
    def buildHeap(self,alist):
        self.heapList = [0] + alist[:]
        self.currentSize = len(self.heapList)-1

        # 构建的思路就是对非叶子节点的节点从下到上逐一进行下沉操作
        i = self.currentSize // 2   # 这个i下标就是第一个进行下沉操作的下标，也是所有要下沉操作的节点中最后一个节点
        while i>0:
            self.__percDown(i)
            i-=1

    # 上浮最后一个尾部节点
    # 上浮的思路就是将最后一个节点和所有祖先节点的值进行比较，如果该节点比某一个祖先节点小则和它互换
    def __percUp(self):
        i = self.currentSize    # 最后一个元素的下标
        while i // 2 > 0:   # i//2是下标为i的节点的父节点的下标
            fatherIndex = i//2
            if self.heapList[fatherIndex] > self.heapList[i]:
                self.heapList[fatherIndex],self.heapList[i] = self.heapList[i],self.heapList[fatherIndex]
                i = fatherIndex
            else:
                break


    # 下沉节点，index是要下沉的节点的下标
    def __percDown(self,index):
        # 先比较index节点下左右子节点哪个大，然后再拿左右子节点中小的那个节点和index节点比
        # 如果index节点比它大，就和这个子节点交换
        # 例如 index节点的值是 100 它的左子节点是99，右子节点是98，那么index节点要和它的右子节点互换，这样父节点就变成了98，比左子节点99小，符合父节点比子节点小的这个规则
        stoped = False
        while index*2 <= self.currentSize and not stoped:  # index*2是左子节点的下标，index*2 <= self.currentSize表示存在index节点的左子节点。如果当前节点没有左子节点，那么右子节点肯定也没有，此时下沉停止
            # print(index)
            leftIndex = index*2
            rightIndex = index*2 + 1

            if rightIndex > self.currentSize: # 如果没有右子节点但是有左子节点，那么就拿左子节点和index节点比较
                comparedIndex = leftIndex
            else:
                comparedIndex = leftIndex if self.heapList[leftIndex]  <= self.heapList[rightIndex] else rightIndex

            if self.heapList[index] > self.heapList[comparedIndex]: # 如果index节点比要比较的节点的值大则互换，否则不互换
                self.heapList[index],self.heapList[comparedIndex] = self.heapList[comparedIndex],self.heapList[index]
                index = comparedIndex
            else:   # 如果index节点比要比较的子节点的值小，说明可以无需继续下沉了，停止循环
                stoped = True


##################################################

# 二叉树

# 二叉查找树的节点
class TreeNode:
    def __init__(self,key,value,left=None,right=None,parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    # 判断是否有左子节点
    def hasLeftChild(self):
        return self.left

    # 判断是否有左子节点
    def hasRightChild(self):
        return self.right

    # 判断是否是左子节点
    def isLeftChild(self):
        return self.parent and self.parent.left == self

    # 判断是否是右子节点
    def isRightChild(self):
        return self.parent and self.parent.right == self

    # 判断是否为根节点
    def isRoot(self):
        return not self.parent

    # 判断是否为叶子节点
    def isLeaf(self):
        return (not self.left) and (not self.right)

    # 判断是否有子节点
    def hasAnyChild(self):
        return self.left or self.right

    # 判断是否两个子节点都有
    def hasBothChild(self):
        return self.left and self.right

    # 替换节点(用于删除根节点时调用并用根节点的左子节点或者右子节点替换自己)
    def replaceNode(self,key,value,lc,rc):
        self.key = key
        self.value = value
        self.left = lc
        self.right = rc
        if self.hasLeftChild():
            self.left.parent = self

        if self.hasRightChild():
            self.right.parent = self

    def findSuccessor(self):
        node = self
        while node.hasLeftChild():
            node = node.left
        return node

    # 将后继节点从原位置挖出
    def spliceOut(self):
        if self.isRightChild():
            self.parent.right = None
        else:
            if self.hasRightChild():
                self.parent.left = self.right
                self.right.parent = self.parent
            elif self.isLeaf():
                self.parent.left = None

        # 后继节点不会有左节点 无需判断 if self.hasLeftChild()

    # 使用中序遍历作为迭代方法
    def __iter__(self):
        if self.hasLeftChild():
            for elem in self.left:  # 用for对self.left遍历的时候又会调用 self.left 的__iter__ 所以相当于是对__iter__()进行递归调用
                yield elem
        yield self.key
        if self.hasRightChild():
            for elem in self.right:
                yield elem


# 二叉查找树
class BST:  # BinarySearchTree
    def __init__(self):
        self.root = None    # root是BST的根节点
        self.size = 0

    # 往BST中添加节点,添加节点的规则要满足key如果大于父节点的key则作为其右子节点，如果小于父节点的key则作为其左子节点
    def put(self,key,value):
        if self.root:
            self.__put(self.root,key,value)
        else:
            self.root = TreeNode(key,value)
        self.size += 1

    def __put(self,currentNode,key,value):
        if key < currentNode.key:   # 如果要插入的key小于目前节点的key,则这个key就放在currentNode的左节点
            if currentNode.hasLeftChild():
                self.__put(currentNode.left,key,value)  # 如果这个节点已经有左节点，则递归
            else:   # 如果没有左子节点则创建左子节点，并且currentNode的left要指向这个节点，而新生成的这个节点的parent要指向currentNode
                currentNode.left = TreeNode(key,value,parent=currentNode)
        else:   # 如果要插入的key大于目前节点的key,则这个key就放在currentNode的右节点
            if currentNode.hasRightChild():
                self.__put(currentNode.right, key, value)
            else:
                currentNode.right = TreeNode(key,value,parent=currentNode)

    def get(self,key):
        if self.root:
            res = self.__get(self.root,key)     # 返回的res可能是none，也可能是一个节点
            return res and res.value
        else:
            return None

    def __get(self,currentNode,key):
        if currentNode == None:     # 说明找不到key
            return None

        if currentNode.key == key:
            return currentNode
        elif currentNode.key > key:
            return self.__get(currentNode.left,key)
        else:
            return self.__get(currentNode.right,key)

    # 根据key删除某个节点A
    # 分为三种情况：1. 节点A没有子节点； 2. 节点A只有1个子节点； 3. 节点A有两个子节点
    def remove(self,key):
        # 先获取key所在的节点
        node = self.__get(self.root,key)

        if node.isLeaf():       # 1. 节点A没有子节点
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None
            node.parent = None
        elif node.hasAnyChild() and not node.hasBothChild():    # 2. 节点A只有1个子节点
            sonNode = node.left if node.hasLeftChild() else node.right
            if node.isLeftChild():
                node.parent.left = sonNode
            elif node.isRightChild():
                node.parent.right = sonNode
            else:   # 要删除的节点是根节点
                self.root = sonNode
                sonNode.parent = None
        else:   # 3. 节点A有两个子节点
            # 这种情况需要找到节点A右边所有节点中key最小的子孙节点，并用该子孙节点替换节点A。这么一来，节点A这个位置还是符合左边的节点比A节点的key小，右边的节点比A节点的key大
            # 这里说一下后继节点succ的特点：succ不会有左子节点;succ本身只能是左节点
            succ = node.right.findSuccessor()    # 找到后继节点,后继节点succ是不会有左子节点的，原因很简单你自己想想吧
            succ.spliceOut()    # 将后继节点从原本的位置挖出来
            node.key = succ.key # 最后用后继节点替换要被删的节点，一旦替换那么原node就算被删除
            node.value = succ.value

    def __setitem__(self, key, value):
        self.put(key,value)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self.get(key):
            return True
        else:
            return False

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.root:
            return self.root.__iter__()