import heapq

class TopK():
    def __init__(self,k):
        self.k = k
        self.listContainer = list() #[]
        # heapify(self.listContainer)

    def count(self):
        '''return count of list container'''
        return self.listContainer.count()

    def update(self,pair):
        '''compare and update heap, pair is a two element tuple'''
        if len(self.listContainer) < self.k:
            heapq.heappush(self.listContainer,pair)
        elif pair[0] > self.listContainer[0][0]:
            heapq.heapreplace(self.listContainer,pair)
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
        
        
