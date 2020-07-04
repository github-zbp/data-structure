from Structure.Tree import BinaryTree
import operator

class MathTree:
    num = list("0123456789")
    op = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}

    def __init__(self,expression):
        self.ep = list(expression)
        self.currentTree = None
        self.topTree = None
        self.degree = []

        self.build()

    def build(self):
        for val in self.ep:
            if val == " ":
                continue

            if val == "(":
                if self.currentTree == None:
                    self.currentTree = BinaryTree()
                    self.topTree = self.currentTree
                else:
                    if self.currentTree.left == None:
                        self.currentTree.insertLeft("")
                        sonTree = self.currentTree.getLeft()
                    else:
                        self.currentTree.insertRight("")
                        sonTree = self.currentTree.getRight()

                    self.degree.append(self.currentTree)
                    self.currentTree = sonTree

            if val == ")":
                if len(self.degree) != 0:
                    self.currentTree = self.degree.pop()

            if val in self.num:
                if self.currentTree.left == None:
                    self.currentTree.left = val
                else:
                    self.currentTree.right = val

            if val in self.op:
                self.currentTree.setRootValue(val)

    def calculate(self):
        op = self.op[self.currentTree.getRootValue()]

        if isinstance(self.currentTree.left,BinaryTree):
            self.degree.append(self.currentTree)
            self.currentTree = self.currentTree.left
            left = self.calculate()
        else:
            left = self.currentTree.getLeft()

        if isinstance(self.currentTree.right,BinaryTree):
            self.degree.append(self.currentTree)
            self.currentTree = self.currentTree.right
            right = self.calculate()
        else:
            right = self.currentTree.getRight()

        res = op(int(left),int(right))

        if len(self.degree):
            self.currentTree = self.degree.pop()

        return res

if __name__ == "__main__":
    expression = "((1+(2*3))-4)"
    mp = MathTree(expression)
    
    print(mp.currentTree == mp.topTree)     # 当构建完表达式树的时候，当前节点变回根节点
    print(mp.currentTree)
    print(mp.calculate())
