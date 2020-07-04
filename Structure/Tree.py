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

