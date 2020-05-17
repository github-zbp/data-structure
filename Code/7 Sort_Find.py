# coding=utf-8

from random import sample

# 顺序查找
def sequeSearch(items,value):
    i = 0
    while i<len(items):
        if items[i] == value:
            return True
        elif items[i] > value:
            return False
        i += 1

    return False

# 遍历版二分查找
# def binarySearch(items,value):
#     while len(items):
#         # 取list中中间的下标
#         midPos = (len(items) - 1) // 2    # // 是向下取整
#         mid = items[midPos]
#         if mid > value:
#             items = items[:midPos]
#         elif mid < value:
#             items = items[(midPos+1):]
#         else:
#             return True
#
#     return False

# 递归版二分查找
def binarySearch(items,value):
    if items == []:
        return False

    midPos = len(items) // 2
    mid = items[midPos]

    if mid > value:
        return binarySearch(items[:midPos],value)
    elif mid < value:
        return binarySearch(items[(midPos+1):], value)
    else:
        return True

# 冒泡排序
def bubbleSort(alist):
    for j in range(1,len(alist)):   # 外层遍历n-1次，表示n-1趟
        left = len(alist) - j
        for i in range(left):   # 内层遍历表示该趟要交换多少次
            if alist[i] > alist[i+1]:   # left最大也是n-1 所以i最大也是n-2 所以 i+1 最大也是n-1 所以 alist[i+1] 不会超出列表索引范围
                temp = alist[i+1]
                alist[i+1] = alist[i]   # 这三句可以写为语句 alist[i+1],alist[i] = alist[i],alist[i+1] 这是优雅的python独有的
                alist[i] = temp

    return alist

# 优化版冒泡排序
def shortbubleSort(alist):
    for j in range(1,len(alist)):
        left = len(alist) - j
        exchange = False
        for i in range(left):
            if alist[i] > alist[i+1]:
                alist[i+1],alist[i] = alist[i],alist[i+1]
                exchange = True     # 表示发生了交换

        if not exchange:    # 如果一趟下来没有元素发生交换就不用进行之后几趟的排序
            break

    return alist

# 选择排序
def selectionSort(alist):
    for j in range(1,len(alist)):
        left = len(alist) - j
        max_index = 0
        for i in range(left):   # 一趟下来就可以找到本趟中最大的数的下标
            if alist[max_index] < alist[i+1]:
                max_index = i+1

        alist[max_index],alist[left] = alist[left],alist[max_index]     # 每趟只做一次交换

    return alist

# 插入排序
def insertionSort(alist):
    sortedList = []

    for aitem in alist:
        if len(sortedList) == 0:
            sortedList.append(aitem)
            continue

        inserted = False
        for index in range(len(sortedList)):
            if sortedList[index] > aitem:
                sortedList.insert(index,aitem)
                inserted = True
                break

        if not inserted:
            sortedList.append(aitem)
    return sortedList

# 优化版插入排序
def newInsertionSort(alist):
    for index in range(1,len(alist)):
        currentValue = alist[index]
        insertedIndex = index   # 未排序的某元素要插入的位置
        while insertedIndex > 0 and currentValue < alist[insertedIndex-1]:
            # 当第 index 个元素（未排序的元素）比左边已排序的某元素小，将已排序的这个元素搬到后一位，并将要插入的位置设为前一位
            alist[insertedIndex] = alist[insertedIndex - 1]
            insertedIndex -= 1

        alist[insertedIndex] = currentValue  # 将未排序的元素插入到要插入的位置

    return alist

# 归并排序
def mergeSort(alist):
    if len(alist) <=1:
        return alist

    mid = len(alist) // 2
    left = mergeSort(alist[:mid])
    right = mergeSort(alist[mid:])

    newList = []
    while left and right:   # 当两个列表都不为空时，则将两个列表中的元素拉链式append进newList中
        if left[0] <= right[0]:
            newList.append(left.pop(0))
        else:
            newList.append(right.pop(0))

    newList.extend(left if left else right)     # 如果left还有剩余元素则将left的剩余元素压入newList;否则就是right还有剩余元素，此时将right剩余元素压入newList

    return newList


# 快速排序
def quickSort(alist):
    if len(alist) <= 1:
        return alist

    mid = alist.pop()
    left = []
    right = []

    while len(alist):
        item = alist.pop()
        if item>mid:
            right.append(item)
        else:
            left.append(item)

    left = quickSort(left)
    right = quickSort(right)

    return left+[mid]+right

# 使用简单求余为散列函数，线性探测加1作为解决冲突的方式实现ADT Map
class ADTMap:       # 映射表 key-value结构的表
    def __init__(self,size=11):
        self.size = size     # 将映射表的长度设为一个质数
        self.keys = [None] * self.size    # 用于存储映射表的key
        self.data = [None] * self.size     # 用于存储映射表的value

    # 简单求余
    def __hashfunction(self,key):
        return key % self.size      # 返回余数作为散列值（槽号）

    # 开放定址，线性探测加1
    def __rehash(self,oldhash):
        return (oldhash+1) % self.size  # 返回新槽号，可能是在原槽号的基础+1，可能变回为0

    # key是槽号
    def put(self,key,data):
        # 计算key的槽号（即key所在self.keys中的位置）
        slot = self.__hashfunction(key)
        # print(slot)
        # 如果key对应的槽号为空或者不为空但是为key本身，则key和data入驻该槽号对应的槽（新增和修改）
        if self.keys[slot] == None or self.keys[slot] == key:
            # print(111)
            self.keys[slot] = key
            self.data[slot] = data
        else:   # 到这里表示该槽已被其他节点占据，需要线性探测
            newSlot = self.__rehash(slot)

            # 如果新槽已经被占据，则往下找新的槽点，直到找到了空槽点就将key和value放到这个新槽点中
            while self.keys[newSlot] != None:
                if newSlot == slot:
                    raise Exception("ADTMap has been full！")

                newSlot = self.__rehash(newSlot)

            self.keys[newSlot] = key
            self.data[newSlot] = data

    def get(self,key):
        slot = self.__hashfunction(key)

        if self.keys[slot] == key:
            return self.data[slot]
        else:   # 如果对应槽点的key不是我要找的key则往下一个槽点找
            newSlot = self.__rehash(slot)

            # 三种情况：
            # 新槽点的key是要找的key，此时返回data
            # 新槽点的key是None，说明根本没有这个key
            # 新槽点的key不是要找的key或者不为None，也说明根本没这个key
            while self.keys[newSlot] != key and self.keys[newSlot] != None:
                print(111)
                newSlot = self.__rehash(newSlot)
                if newSlot == slot:
                    return None

            return self.data[newSlot]   # 可能是要找的key对应的值，可能是none

    # 使得ADTMap 可以通过[] 获取元素
    def __getitem__(self, key):
        return self.get(key)

    # 使得ADTMap 可以通过[] 设置元素
    def __setitem__(self, key, value):
        self.put(key,value)

    # 查看Map中的内容
    def __str__(self):
        mapStr = "{"
        for key in self.keys:
            mapStr += str(key)+":"+str(self[key])+", "
        mapStr = mapStr.strip(", ")

        mapStr = mapStr+"}"
        return mapStr


# 使用简单求余为散列函数，数据项链作为解决冲突的方式实现ADT Map
class ChainADTMap:       # 映射表 key-value结构的表
    def __init__(self,size=11):
        self.size = size     # 将映射表的长度设为一个质数
        self.keys = [None] * self.size    # 用于存储映射表的key
        self.data = [None] * self.size     # 用于存储映射表的value

    # 简单求余
    def __hashfunction(self,key):
        return key % self.size      # 返回余数作为散列值（槽号）

    @staticmethod
    def seque_search(alist,value):      # 返回值所在下表
        index = 0
        while index < len(alist):
            print(111)
            if alist[index] == value:
                return index
            index += 1

        return None

    def put(self,key,data):
        # 计算key的槽号（即key所在self.keys中的位置）
        slot = self.__hashfunction(key)

        # 如果key对应的槽号为空，则初始化2个空的子链表并将key和value放到子链表中
        if self.keys[slot] == None:
            self.keys[slot] = [key]
            self.data[slot] = [data]
        else:   # 如果槽号冲突，则把key和data添加到子链表中
            self.keys[slot].append(key)
            self.data[slot].append(data)

    def get(self,key):
        slot = self.__hashfunction(key)

        if self.keys[slot] == None:     # 说明该槽点不存在子列表，数据不存在
            return None
        else:
            # 说明这个key所在的槽点已经存过至少1一个值，即子列表存在；然后再使用顺序查找从子列表中查找数据
            index = self.__class__.seque_search(self.keys[slot],key)
            if index == None:   # 说明子列表中没有数据
                return None
            return self.data[slot][index]


    # 使得ADTMap 可以通过[] 获取元素
    def __getitem__(self, key):
        return self.get(key)

    # 使得ADTMap 可以通过[] 设置元素
    def __setitem__(self, key, value):
        self.put(key,value)

    # 查看Map中的内容
    def __str__(self):
        mapStr = "{"
        for key in self.keys:
            if key != None:
                for k in key:
                    mapStr += str(k)+":"+str(self[k])+", "
        mapStr = mapStr.strip(", ")

        mapStr = mapStr+"}"
        return mapStr

if __name__ == "__main__":
    adtMap = ChainADTMap()

    # 设置随机的key，key只能为数字不能为字符串；以key的平方作为value
    try:
        # 生成100个不重复的随机数
        dataDict = {i:i*i for i in sample(range(1,200),101)}
        for key,value in dataDict.items():
            adtMap[key] = value
    except BaseException as e:
        print(e)

    # print(adtMap)

    # 验证数据是否正确
    print(adtMap[10])
    print(adtMap[20])
    print(adtMap[30])
