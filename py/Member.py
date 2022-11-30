from .JsonDB import JsonDB
import datetime

class Member():
    '''
    {
	"phone":"18112682607",
	"name":"黄程",
	"points": [1,98],
	"times": ["2022-02-05 14:44","2022-08-30 20:00"]
    }
    '''
    db = JsonDB('json/Members.json')
    
    def __init__(self, phone):
        if phone:
            self.data = Member.db.get("phone",phone)
            if self.data is None:
                self.data = {}
        else:
            self.data = {}
            
        self._point = 0
        self._time = 0
        self._lastTime = "1111-11-00 00:00"

    def __lt__(self, other):
        return self.name() < other.name()

    def __eq__(self, other):
        return self.name() == other.name()

    def phone(self):
        '''
        phone is the primary key
        '''
        if self.data:
            return self.data["phone"]
        return None

    def setPhone(self,phone):
        print(phone)
        self.data["phone"] = phone
        self.data["name"] = ""
        self.data["points"] = []
        self.data["times"] = []

    def name(self):
        if self.data:
            return self.data["name"]
        return None

    def setName(self,name):
        if self.data:
            self.data["name"] = name

    def point(self):
        if self._point == 0:
            self._calc();
        return self._point

    def time(self):
        if self._time == 0:
            self._calc()
        return self._time

    def lastTime(self):
        if self._lastTime == "1111-11-00 00:00":
            self._calc()
        return self._lastTime

    def addPoint(self,point):
        if self.data:
            self.data["points"].append(point)
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data["times"].append(time)
        
    def updateDB(self):
        if self.data:
            Member.db.set("phone", self.data["phone"], self.data)
            Member.db.save()

    def _calc(self):
        if self.data and "points" in self.data and "times" in self.data:
            index = 0
            for item in self.data["points"]:
                self._point = self._point + item
                if item > 0:
                    self._time = self._time + 1
                    self._lastTime = self.data["times"][index]
                index = index + 1

    @staticmethod
    def comparePoints(memberA,memberB):
        if memberA.point() > memberB.point():
            return 1
        elif memberA.point() == memberB.point():
            return 0
        else:
            return -1

    @staticmethod
    def compareTimes(memberA,memberB):
        if memberA.time() > memberB.time():
            return 1
        elif memberA.time() == memberB.time():
            return 0
        else:
            return -1
    
