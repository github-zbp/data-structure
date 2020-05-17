# coding=utf-8
import math

class Stack:
    def __init__(self):
        self.items=[]

    def pop(self):
        return self.items.pop()

    def push(self,item):
        self.items.append(item)

    # 查看栈顶的元素
    def peak(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items==[]

# 应用1：验证括号是否合法
def isValidBrackets(brackets):
    if len(brackets) % 2:
        return False

    left = ["[","(","{"]
    right = ["]",")","}"]
    stack = Stack()

    for bracket in brackets:
        # print(bracket)
        if bracket in left:
            stack.push(bracket)
        elif stack.size():        # 如果此时遍历到右括号，而且栈中还有左括号
            item = stack.pop()
            index = left.index(item)
            if right[index] != bracket:
                return False
        else:   # 如果此时遍历到右括号，而且栈中没有左括号，说明左右括号的数量不相等
            return False

    return True

# 应用2：十进制转2,8,16进制
def baseConverter(decNumber,base=2):
    stack = Stack()
    digits = "0123456789ABCDEF"

    while decNumber:
        stack.push(decNumber%base)
        decNumber = math.floor(decNumber/base)

    newString = ""

    while not stack.isEmpty():
        newString= newString + digits[stack.pop()]

    return newString

# 应用3：中缀表达式转为后缀表达式
def inFixToPostfix(expr):
    # 使用字典将操作符的优先级保存
    priority = {
        "+":2,
        "-":2,
        "*":3,
        "/":3,
        "(":1,
        ")":1
    }
    alpha = "QWERTYUIOPASDFGHJKLZXCVBNM"
    brackets = ["(",")"]

    stack = Stack()
    postfix_list = []

    for char in expr:
        print(char)
        if char in alpha:
            postfix_list.append(char)
        elif char == "(":
            stack.push(char)
        elif char == ")":
            sign = stack.pop()
            while sign!="(":
                postfix_list.append(sign)
                sign = stack.pop()
        else:
            while (not stack.isEmpty()) and priority[stack.peak()] > priority[char]:
                sign = stack.pop()
                postfix_list.append(sign)
            stack.push(char)

    # 遍历完之后，如果栈里面还有操作符则要一一弹出并放到列表中
    while not stack.isEmpty():
        postfix_list.append(stack.pop())

    newString=""
    for char in postfix_list:
        newString+=char

    return newString

def calcul(op,left,right):
    if op=="+":
        res = left+right
    elif op=="-":
        res = left-right
    elif op=="*":
        res = left*right
    elif op=="/":
        res = left/right
    else:
        res = False

    return res

# 应用4：计算后缀表达式
def calculPostfix(postfix,numDict):
    sign = ["+","-","*","/"]
    stack = Stack()

    for char in postfix:
        if char not in sign:
            stack.push(numDict[char])
        else:
            right = stack.pop()
            left = stack.pop()
            stack.push(calcul(char,left,right))


    return stack.pop()

