import heapq

class TopK():
    def __init__(self,k):
        self.k = k
        self.listContainer = list() #[]
        # heapify(self.listContainer)

    def count(self):
        '''return count of list container'''
        return self.listContainer.count()

    def update(self,value,compareF):
        '''compare and update heap'''
        if len(self.listContainer) < self.k:
            heapq.heappush(self.listContainer,value)
        elif compareF(value,self.listContainer[0]) > 0:
            heapq.heapreplace(self.listContainer,value)
        else:
            pass

    def getList(self):
        '''copy result of heap and make a new sorted list'''
        newList = self.listContainer.copy() # shallow copy
        newList.sort()
        return newList

    def clear(self):
        '''clear list container '''
        self.listContainer.clear()
        
        
