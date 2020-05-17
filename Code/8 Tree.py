# coding=utf-8

import operator,os,sys

# 使用列表实现一个二叉树
class BinaryTree:
    def __init__(self,root):
        # 第二和第三个元素是左子树和右子树，如果要实现n叉树，则需要列表有n+1个元素
        self.tree = [root,[],[]]    # root是根节点，是一个普通类型的数据而不是列表

    # 添加一个新节点到树中作为其直接的左子节点
    def insertLeft(self,item,tree=[]):  # item是一个普通类型的数据
        tree = tree if tree else self.tree

        leftTree = tree.pop(1)
        if len(leftTree) > 0:
            tree.insert(1,[item,leftTree,[]])
        else:
            tree.insert(1,[item,[],[]])

    # 添加一个新节点到树中作为其直接的右子节点
    def insertRight(self,item,tree=[]):
        tree = tree if tree else self.tree

        rightTree = tree.pop(2)
        if len(rightTree) > 0:
            tree.insert(2, [item, [], rightTree])
        else:
            tree.insert(2, [item, [], []])

    # 获取根节点
    def getRootVal(self,tree=[]):
        tree = tree if tree else self.tree
        return tree[0]

    # 设置根节点
    def setRootVal(self,item,tree=[]):
        tree = tree if tree else self.tree
        tree[0] = item

    # 获取一个树的左子树
    def getLeftChild(self,tree=[]):
        tree = tree if tree else self.tree
        return tree[1]

    # 获取一个树的右子树
    def getRightChild(self,tree=[]):
        tree = tree if tree else self.tree
        return tree[2]

    def __str__(self):
        return str(self.tree)

# 使用链表实现二叉树
class Node:     # 链表节点类，这个节点类和之前单向链表或者双向链表中的节点类不同，不同在于它的有两个指针，因为二叉树的一个节点有两条边
    def __init__(self,value=""):
        self.value = value
        self.left = None    # 左指针
        self.right = None   # 右指针

    def __str__(self):
        return str({"value":self.value,"left":self.left,"right":self.right})

class LinkedListBinaryTree(Node):       # 二叉树本质是一个有两个指针的节点
    # 往一棵树的根节点下插入一个左子树
    def insertLeft(self,nodeValue=""):
        leftTree = LinkedListBinaryTree(nodeValue)  # 生成一棵左子树

        if self.left == None:
            self.left = leftTree
        else:
            leftTree.left = self.left
            self.left = leftTree

    # 往一棵树的根节点下插入一个右子树
    def insertRight(self, nodeValue=""):
        rightTree = LinkedListBinaryTree(nodeValue)  # 生成一棵右子树

        if self.right == None:
            self.right = rightTree
        else:
            rightTree.right = self.right
            self.right = rightTree

    def getRootVal(self):     # 获取根节点的值
        return self.value

    def setRootVal(self,value):
        self.value = value

    def getLeftChild(self):  # 获取左子树
        return self.left

    def getRightChild(self):
        return self.right

# 简单的数学表达式解析(用二叉树实现)
class MathExpression:
    num = list("0123456789")
    opDict = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

    def __init__(self,expression):
        self.expression = list(expression)      # 传入的表达式是一个全括号表达式，每一个操作都用()包住
        self.currentTree = None     # 记录当前子树是哪一棵
        self.topTree = None     # 记录最顶层的子树
        self.degree = []    # 将经过树的层用存入到栈内，栈用列表模拟

    # 构建一棵表达式解析树
    # 这棵树是由多个单层的二叉树构建而成的一棵大二叉树
    # 叶子节点只能是操作数，非叶子节点和根节点只能是操作符
    # 当遇到最后一个“)”的时候，当前子树 currentTree 会回到底层
    def build(self):
        for item in self.expression:
            if item == " ":
                continue

            if item == "(":     # 遇到左括号则创建一棵单层的二叉子树
                if self.currentTree == None:   # 如果没有创建过树，则该二叉子树作为顶层的树干
                    self.currentTree = LinkedListBinaryTree()
                    self.topTree = self.currentTree
                else:       # 如果已经有了顶层的树干，则创建的二叉子树添加为当前子树的左子树或者右子树
                    if self.currentTree.left == None:
                        self.currentTree.insertLeft("")
                        tree = self.currentTree.getLeftChild()
                    else:
                        self.currentTree.insertRight("")
                        tree = self.currentTree.getRightChild()

                    self.degree.append(self.currentTree)    # 进入下一层之前，先记录这一层是哪一个分支
                    self.currentTree = tree     # 进入下一层


            if item == ")": # 遇到右括号则返回到当前子树的上一层子树
                if len(self.degree) != 0:
                    lastDegree = self.degree.pop()
                    self.currentTree = lastDegree

            if item in self.opDict:     # 遇到操作符则为当前子树的根节点设置值
                self.currentTree.setRootVal(item)

            if item in self.num:        # 遇到操作数则将操作数记录到当前子树的左叶子节点或者右叶子节点
                if self.currentTree.left == None:
                    self.currentTree.left = item
                else:
                    self.currentTree.right = item

    # 计算表达式树中表达式的结果（使用递归 + 分治策略）
    def calculate(self):
        # 这个不是结束条件而是一种特殊情况的判断
        if self.currentTree.getRootVal() not in self.opDict:
            return self.currentTree.getRootVal()

        op = self.opDict[self.currentTree.getRootVal()]
        if not isinstance(self.currentTree.left, LinkedListBinaryTree):     # 结束条件
            left = self.currentTree.left
        else:
            self.degree.append(self.currentTree)
            self.currentTree = self.currentTree.left
            left = self.calculate()
            self.currentTree = self.degree.pop()


        if not isinstance(self.currentTree.right, LinkedListBinaryTree):    # 结束条件
            right = self.currentTree.right
        else:
            self.degree.append(self.currentTree)
            self.currentTree = self.currentTree.right
            right = self.calculate()
            self.currentTree = self.degree.pop()

        res = op(int(left),int(right))
        self.currentTree.setRootVal(res)    # 没有这一步也可以
        return res

# 树的遍历
# 前序遍历(以从上到下的顺序遍历)
def preorder(binaryTree):
    if isinstance(binaryTree,LinkedListBinaryTree):
        print(binaryTree.getRootVal())
        preorder(binaryTree.getLeftChild())
        preorder(binaryTree.getRightChild())
    elif binaryTree != None:
        print(binaryTree)

# 中序遍历(以从左到右的顺序遍历)
def inorder(binaryTree):
    if isinstance(binaryTree,LinkedListBinaryTree):
        inorder(binaryTree.getLeftChild())
        print(binaryTree.getRootVal())
        inorder(binaryTree.getRightChild())
    elif binaryTree != None:
        print(binaryTree)

# 后序遍历(以从下到上的顺序遍历)
def postorder(binaryTree):
    if isinstance(binaryTree,LinkedListBinaryTree):
        postorder(binaryTree.getLeftChild())
        postorder(binaryTree.getRightChild())
        print(binaryTree.getRootVal())
    elif binaryTree != None:
        print(binaryTree)


# 函数版的表达式树
def buildParseTree(fexp):
    fexp = list(fexp)

    # 一开始先创建一个顶层子树,根节点不赋值
    currentTree = None
    stack = []  # 用栈保存currentTree经过的哪几层子树，方便当前树currentTree的回溯

    for i in fexp:
        # print(stack)
        if fexp == " ":
            continue

        if i == "(":
            if currentTree == None:
                currentTree = LinkedListBinaryTree("")

            currentTree.insertLeft("")      # 创建一棵左子树
            currentTree.insertRight("")      # 创建一棵右子树
            stack.append(currentTree)  # 进入下一层的树前，先将本层的树放入stack中，记录currentTree经过的树
            currentTree = currentTree.getLeftChild()    # 进入下一层树

            # print(currentTree)

        elif i not in ["(","+","-","*","/",")"]:
            # print(currentTree)
            currentTree.setRootVal(i)
            currentTree = stack.pop()

        elif i in ["+","-","*","/"]:
            currentTree.setRootVal(i)
            stack.append(currentTree)
            currentTree = currentTree.getRightChild()

        elif i == ")":
            if len(stack):
                currentTree = stack.pop()

    return currentTree

# 使用中序遍历的方式计算
def calculateParseTree(tree):
    opDict = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

    if tree.getRootVal() not in ["+","-","*","/"]:  # 如果根节点的值是数值而不是符号，则满足结束条件
        return tree.getRootVal()

    left = calculateParseTree(tree.getLeftChild())
    op = opDict[tree.getRootVal()]
    right = calculateParseTree(tree.getRightChild())

    return op(int(left),int(right))


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

if __name__ == "__main__":
    bh = BinaryHeap()
    bh.insert(10)
    bh.insert(100)
    bh.insert(1)
    bh.insert(22)
    bh.insert(53)
    bh.insert(34)
    bh.insert(54)
    bh.insert(23)
    bh.insert(11)
    bh.insert(17)
    bh.insert(87)
    print(bh.heapList)
    while bh.currentSize>0:
        print(bh.pop())

    alist = [10,100,1,22,53,34,54,23,11,17,87]
    bh2 = BinaryHeap()
    bh2.buildHeap(alist)
    while bh2.currentSize>0:
        print(bh2.pop())
