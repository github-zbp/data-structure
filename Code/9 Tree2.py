# coding=utf-8

# 二叉查找树的节点
class TreeNode:
    def __init__(self,key,value,left=None,right=None,parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.balanceFactor = 0  # 平衡因子，用于AVL树，不用于普通的BST树

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


# AVL平衡树
# AVL树具有BST的基本功能，只是在插入key的时候要保持树两边的平衡，所以只需改写其__put方法即可
class AVL(BST):
    def __put(self,currentNode,key,value):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self.__put(currentNode.left, key, value)
            else:
                currentNode.left = TreeNode(key, value, parent=currentNode)

                # 添加完节点之后要更新插入的节点的所有祖先节点的平衡因子
                self.updateBalance(currentNode.left)
        else:
            if currentNode.hasRightChild():
                self.__put(currentNode.right, key, value)
            else:
                currentNode.right = TreeNode(key, value, parent=currentNode)

                # 添加完节点之后要更新插入的节点的所有祖先节点的平衡因子
                self.updateBalance(currentNode.right)

    # 更新某个节点的所有祖先节点的平衡因子
    def updateBalance(self,node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)    # 如果这个节点的平衡因子绝对值大于1则进行平衡调整
            return

        # 如果node的平衡因子绝对值没有大于1则只进行平衡因子+1和-1,平衡因子+1和-1是对其祖先节点的操作
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1      # 修改被插入节点的父节点的平衡因子
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:      # 意思是，如果被插入节点的父节点是从没有子节点到有子节点的话，就要对父节点的父节点修改平衡因子
                self.updateBalance(node.parent)

    # 调节某个节点的位置使得该位置的平衡因子在-1到1之间
    # 只有当node的balanceFactor的绝对值大于1才会走到这个方法
    def rebalance(self,node):
        if node.balanceFactore < 0: # 右重，要左旋
            if node.right.balanceFactor > 0:   # "之"型树情况,需要先对 node的右子节点进行右旋，再对node进行左旋
                self.rotateRight(node.right)
            self.rotateleft(node)
        elif node.balanceFactor > 0:    # 左重，要右旋
            if node.left.balanceFactor < 0: # 反"之"型树情况,需要先对 node的左子节点进行右旋，再对node进行右旋
                self.rotateLeft(node.left)
            self.rotateRight(node)

    # 左旋
    def rotateLeft(self,nowRoot):
        newRoot = nowRoot.right     # 找到要晋升的根节点
        nowRoot.right = newRoot.left
        if newRoot.left != None:
            newRoot.left.parent = nowRoot
        newRoot.parent = nowRoot.parent
        if nowRoot.isRoot():
            self.root = newRoot
        else:
            if nowRoot.isLeftChild():
                nowRoot.parent.left = newRoot
            else:
                nowRoot.parent.right = newRoot

        newRoot.left=nowRoot
        nowRoot.parent = newRoot
        nowRoot.balanceFactor = nowRoot.balanceFactor+1-min(newRoot.balanceFactor,0)    # 修改节点的平衡因子，修改成多少请自己画图和设未知数进行推算
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(nowRoot.balanceFactor,0)    # 修改晋升节点的平衡因子

    # 右旋
    def rotateRight(self,nowRoot):
        newRoot = nowRoot.left
        nowRoot.left = newRoot.right
        if newRoot.hasRightChild():
            newRoot.right.parent = nowRoot
        newRoot.parent = nowRoot.parent

        if nowRoot.isRoot():
            self.root = newRoot
        else:
            if nowRoot.isLeftChild():
                nowRoot.parent.left = newRoot
            else:
                nowRoot.parent.right = newRoot

        newRoot.right = nowRoot
        nowRoot.parent = newRoot
        nowRoot.balanceFactor = nowRoot.balanceFactor -  1 - min(newRoot.balanceFactor,0)  # 修改节点的平衡因子，修改成多少请自己画图和设未知数进行推算
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + max(nowRoot.balanceFactor, 0)  # 修改晋升节点的平衡因子

if __name__ == "__main__":
    # import random
    # dataKey = [i for i in range(1,50,3)]
    # random.shuffle(dataKey)
    dataKey = [34, 43, 49, 25, 46, 13, 1, 22, 40, 31, 7, 19, 37, 16, 4, 28, 10]
    print(dataKey)
    bst = BST()
    for i in dataKey:
        bst.put(i,i/2)

    for i in bst:
        print(i,bst[i])

    print(bst.get(40))
    print(bst.get(25))
    print(bst.get(22))
    print(bst.get(33))

    print("===================================")

    bst.remove(40)
    bst.remove(22)
    bst.remove(25)
    bst.remove(28)

    for i in bst:
        print(i,bst[i])


