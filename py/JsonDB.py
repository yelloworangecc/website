import json

class JsonDB():
    '''
    Json file read and write
    It's a list at top level
    '''
    def __init__(self,path):
        self.path = path
        self.data = None
        
    def load(self):
        if self.data:
            return self.data
        with open(self.path,'r',encoding='utf8') as fp:
            self.data = json.load(fp)
        return self.data
        
    def get(self,key,value):
        for item in self.data:
            if key in item:
                if item[key] == value:
                    return item
        return None

    def set(self,key,value,newItem):
        # update
        for item in self.data:
            if key in item:
                if item[key] == value:
                    item = newItem
                    return None
        # append
        self.data.append(newItem)
       
    def save(self):
        with open(self.path,'w',encoding='utf8') as fp:
            json.dump(self.data,fp)