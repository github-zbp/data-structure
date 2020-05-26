# 链表

# 节点类
class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None    # 向后指针
        self.prev = None    # 向前指针

    def getValue(self):
        return self.value

    def getKey(self):
        return self.key

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def setValue(self,value):
        self.value = value

    def setNext(self,node):
        self.next = node

    def setPrev(self,node):
        self.prev = node

    def __str__(self):
        return str({'key':self.key,'value':self.value,'prev':self.prev.key if self.prev else None,'next':self.next.key if self.next else None})

# 单向链表(只能从头部添加，从尾部弹出)
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0       # 链表节点个数

    # 从头部添加
    def push(self,key,value):
        node = Node(key,value)

        if not self.isEmpty():
            node.setNext(self.head)
        self.head = node
        self.size += 1

    def pop(self):
        prev = None     # 当前节点的上一个节点
        current = self.head  #当前节点

        if self.isEmpty():
            return None

        if self.size == 1:
            self.head = None
        else:
            while current.getNext():
                prev = current
                current = current.getNext()

            prev.setNext(None)

        self.size -= 1

        return current

    # 根据key从链表中取出某节点
    def get(self,key):
        prev = None
        current = self.head

        while current:
            if current.getKey() == key:
                if prev:    # prev不为None说明链表节点大于1
                    prev.setNext(current.getNext())
                else:
                    self.head = None

                self.size -= 1
                return current
            else:
                prev = current
                current = current.getNext()

        return None

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.head == None

    def __str__(self):
        linkedList = {}
        current = self.head
        index = 0

        while current:
            linkedList[index] = {'key':current.key,'value':current.value,'prev':current.prev.key if current.prev else None,'next':current.next.key if current.next else None}
            current = current.getNext()
            index += 1
        
        return str(linkedList)

# 双向链表(可从头部添加或弹出，也可从尾部添加或弹出)
class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # 尾部添加
    def push(self,key,value):
        node = Node(key,value)
        if self.size == 0:
            self.head = node
        else:
            self.tail.setNext(node)
            node.setPrev(self.tail)

        self.tail = node
        self.size += 1

    # 头部添加
    def unshift(self,key,value):
        node = Node(key,value)
        if self.size == 0:
            self.tail = node
        else:
            self.head.setPrev(node)
            node.setNext(self.head)

        self.size += 1
        self.head = node

    # 尾部弹出
    def pop(self):
        tail = self.tail

        if self.size <= 1:      # 0和1两种情况
            self.head = None
            self.tail = None
        else:
            prev = tail.getPrev()
            tail.setPrev(None)
            prev.setNext(None)
            self.tail = prev

        self.size = self.size - 1 if self.size > 0 else 0

        return tail



    # 头部弹出
    def shift(self):
        head = self.head

        if self.size <= 1:  # 0和1两种情况
            self.head = None
            self.tail = None
        else:
            next = head.getNext()
            head.setNext(None)
            next.setPrev(None)
            self.head = next

        self.size = self.size - 1 if self.size > 0 else 0

        return head

    # 获取特定key的节点
    def get(self,key):
        if self.size == 0:
            return None
        
        current = self.head
        while current:
            prev = current.getPrev()
            next = current.getNext()
            if current.key == key:
                if self.head == current:
                    return self.shift()     # shift 和 pop中已经有 self.size - 1的操作，请勿重复-1
                
                if self.tail == current:
                    return self.pop()

                self.size -= 1
                prev.setNext(next)
                next.setPrev(prev)
                current.setNext(None)
                current.setPrev(None)
                return current
            else:
                current = next

        return None


    # 获取长度
    def getSize(self):
        return self.size

    # 是否为空
    def isEmpty(self):
        return self.size == 0

    def __str__(self):
        linkedList = {}
        current = self.head
        index = 0
        while current:
            linkedList[index] = {'key':current.key,'value':current.value,'prev':current.prev.key if current.prev else None,'next':current.next.key if current.next else None}
            current = current.getNext()
            index += 1
        
        return str(linkedList)


# 有序列表（使用双向链表实现）
# 有序列表可以从尾部添加元素，从头部弹出元素，不能从中间加入元素
# 有序列表添加元素的时候会将元素放到链表中合适的位置使得整个链表中的元素是从小到大排列的
# 有序链表在双向链表的基础上添加一个search方法，能够判断链表中是否含有这个元素
class OrderList(DoubleLinkedList):
    def pop(self):
        raise Exception("Method pop is forbidden in class OrderList ！")

    def unshift(self,item):
        raise Exception("Method unshift is forbidden in class OrderList ！")

    def push(self,item):
        node = Node(item,item)

        if self.size == 0:
            self.head = node
            self.tail = node
        else:
            current = self.tail     # 定义一个当前指针，用于记录节点要插入的位置
            isTail = True           # 如果新添加的item就是链表中的最大值，则要将self.tail指向node

            # 确定current，即确定要插入的位置
            while current != None and current.getValue() > item:
                current = current.getPrev()
                isTail = False

            # current有3种情况：current在首部（此时item是最小值）; current在中间; current在尾部(此时item是最大值)
            if current != None:     # 当item是最中间值或最大值
                afterNode = current.getNext()
                node.setNext(afterNode)
                node.setPrev(current)
                current.setNext(node)

                if not isTail:      # item是中间值
                    afterNode.setPrev(node)
                else:               # item是最大值
                    self.tail = node
            else:                   # item是最小值
                node.setNext(self.head)
                self.head.setPrev(node)
                self.head = node

        # 最后记得size加1
        self.size += 1

     # 判断链表是否有这个值
    def search(self,item):
        current = self.head

        # 遍历即可
        while current:
            if current.getValue() == item:
                return True
            else:
                current = current.getNext()

        return False

    # 从头部弹出时，不返回节点而直接返回元素值
    def shift(self):
        node = super(OrderList, self).shift()
        return node.getValue() if node else None

    def get(self,item):
        raise Exception("Method get is forbidden in class OrderList ！")

    def __str__(self):
        current = self.head
        valList = []

        while current:
            valList.append(current.getValue())
            current = current.getNext()

        return str(valList) 