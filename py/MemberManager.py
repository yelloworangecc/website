import json
import datetime

class Member():
    allMembers=None
    def __init__(self, member):
        print("__init__")
        self.member = member

    def getPhone(self):
        return self.member["phone"]
        
    def getName(self):
        return self.member["name"]
        
    def sumAllPoints(self):
        sum = 0.0
        for point in self.member["points"]:
            sum = sum + point
        return sum
        
    def getLastModifyTime(self):
        index = len(Member.allMembers) - 1
        return self.member["times"][index]

    def modifyPoints(self,point):
        self.member["points"].append(point)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.member["times"].append(time)
        return None

    @staticmethod
    def load():
        if Member.allMembers is not None:
            return True
        else:
            with open('json/Members.json','r',encoding='utf8') as fp:
                Member.allMembers = json.load(fp)
        
        if Member.allMembers is None:
            return False
        else:
            return True

    @staticmethod
    def get(phone):
        if Member.allMembers is None:
            return None
        
        for member in Member.allMembers:
            if member["phone"] == phone:
                return Member(member)
                
        return None

    @staticmethod
    def save():
        with open('json/Members.json','w',encoding='utf8') as fp:
            json.dump(Member.allMembers,fp)
            
        return None

    

