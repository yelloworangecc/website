import json
import datetime
from .TopK import TopK

class Member():
    allMembers_j = None
    top10Points = TopK(10)
    top10Times = TopK(10)
    def __init__(self, member):
        print("__init__")
        self.member = member

    def getPhone(self):
        return self.member["phone"]
        
    def getName(self):
        return self.member["name"]
        
    def sum(self):
        sum = 0.0
        for point in self.member["points"]:
            sum = sum + point
        return sum

    def count(self):
        return len(self.member["times"])
        
    def getLastTime(self):
        index = len(self.member["times"]) - 1
        return self.member["times"][index]

    def modifyPoints(self,point):
        self.member["points"].append(point)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.member["times"].append(time)
        return None

    @staticmethod
    def load():
        if Member.allMembers_j is not None:
            return True
        else:
            with open('json/Members.json','r',encoding='utf8') as fp:
                Member.allMembers_j = json.load(fp)
        
        if Member.allMembers_j is None:
            return False
        else:
            return True

    @staticmethod
    def get(phone):
        if Member.allMembers_j is None:
            return None
        
        for member in Member.allMembers_j:
            if member["phone"] == phone:
                return Member(member)
                
        return None

    @staticmethod
    def save():
        with open('json/Members.json','w',encoding='utf8') as fp:
            json.dump(Member.allMembers_j,fp)
            
        return None

    @staticmethod
    def comparePoints(memberA,memberB):
        if memberA.sum() > memberB.sum():
            return 1
        elif memberA.sum() == memberB.sum():
            return 0
        else:
            return -1

    @staticmethod
    def compareTimes(memberA,memberB):
        if memberA.count() > memberB.count():
            return 1
        elif memberA.count() == memberB.count():
            return 0
        else:
            return -1
            
    @staticmethod
    def genTop10():
        if Member.allMembers_j is None:
            return None

        Member.top10Points.clear()
        Member.top10Times.clear()
        for member_j in Member.allMembers_j:
            member=Member(member_j)
            Member.top10Points.update(member,Member.comparePoints)
            Member.top10Times.update(member,Member.compareTimes)

    @staticmethod
    def getTop10Points():
        return Member.top10Points.getList()

    @staticmethod
    def getTop10Times():
        return Member.top10Times.getList()

