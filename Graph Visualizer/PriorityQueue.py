# Priority Queue Class for Dijkstra and A*
# Current implementation is not efficient I think. Use a heap maybe ?

class PriorityQueue:
    def __init__(self):
        self.queue = {}

    def isEmpty(self):
        return len(self.queue) == 0

    def addItem(self, key, val):
        self.queue[tuple(key)] = val

    def get_removeMinCell(self):
        min_cell = sorted(self.queue.items(), key = lambda item: item[1])[0][0]
        self.queue.pop(min_cell)
        return list(min_cell)


if __name__ == "__main__":
    d = {}
    # d[tuple([1,1])] = 4
    # d[tuple([2,1])] = 2
    # d[tuple([1,2])] = 5
    # d[tuple([1,3])] = 1

    # d = sorted(d.items(), key = lambda item: item[1])

    # print(d)
    
    print(len(d) > 0)

    # if d:
    #     print("yes")
    # else:
    #     print("no")

    # p = PriorityQueue()
    # p.addItem([1,1], 4)
    # p.addItem([2,1], 2)
    # p.addItem([1,3], 1)
    # p.addItem([1,2], 5)

    # print(p.queue)

    # print(p.get_removeMinCell())
    # print(p.queue)