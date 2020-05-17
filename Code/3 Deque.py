# coding=utf-8

class Deque:
    def __init__(self):
        self.items=[]

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []

    def addRear(self,item):
        self.items.insert(0,item)

    def addFront(self,item):
        self.items.append(item)

    def removeRear(self):
        return self.items.pop(0)

    def removeFront(self):
        return self.items.pop()

# 改良的双端列表
class DequeImproved:
    def __init__(self):
        self.items = {"first":0,"last":0}
        self.size = 0

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def addFront(self,item):
        if self.size != 0:
            self.items['first'] -= 1
        self.items[self.items['first']] = item
        self.size += 1

    def addRear(self,item):
        if self.size != 0:
            self.items['last'] += 1

        self.item[self.items['last']] = item
        self.size += 1

    def removeRear(self):   # 就是pop
        if self.size == 0:
            return None

        item = self.items[self.items['last']]
        del self.items[self.items['last']]
        self.items['last'] -= 1
        self.size -= 1
        return item

    def removeFront(self):  # 就是shift
        if self.size == 0:
            return None

        item = self.items[self.items['first']]
        del self.items[self.items['first']]
        self.items['first'] += 1
        self.size -= 1
        return item

    def __str__(self):
        return str(self.items)

def isSymmetry(words):
    deque = DequeImproved()

    new_words = ""

    for word in words:
        deque.addFront(word)

    for word in words:
        new_words += deque.removeFront()

    if new_words == words:
        return True
    else:
        return False

def isSymmetry2(words):
    deque = DequeImproved()

    for word in words:
        deque.addFront(word)

    while deque.getSize()>1:
        front = deque.removeFront()
        rear = deque.removeRear()
        print(front,rear)

        if front != rear:
            return False

    return True

if __name__ == "__main__":
    words = "abcde"
    words2 = "上海自来水来自海上"
    print(isSymmetry(words))
    print(isSymmetry(words2))

    print(isSymmetry2(words))
    print(isSymmetry2(words2))