from .JsonDB import JsonDB

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
        if phone not None:
            self.data = Member.db.get("phone",phone)
        else:
            self.data = {}
        self.sum = None
        self.time = None

    def phone(self):
        '''
        phone is the primary key
        '''
        if self.data:
            return self.data["phone"]
        return None

    def setPhone(self,phone):
        self.data["phone"] = phone
        self.data["name"] = ""
        self.data["points"] = []
        self.data["times"] = []
        self.update()

    def name(self):
        if self.data:
            return self.data["name"]
        return None

    def setName(self,name):
        if self.data:
            self.data["name"] = name
            self.update()

    def points(self):
        if self.sum not None:
            return self.sum

        self.sum = 0
        if self.data:
            for item in self.data["points"]:
                self.sum = self.sum + item

        return self.sum

    def times(self):
        if self.time not None:
            return self.time

        self.time = ""
        if self.data:
            count = len(self.data["times"])
            if count > 0:
                self.time = self.data["times"][count]
   
        return self.time

    def lastTime(self):
        index = len(self.data["times"]) - 1
        if index < 0:
            return None
        return self.member["times"][index]

    def addPoint(self,point):
        if self.data:
            self.data["points"].append(point)
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data["times"].append(time)
            self.update()
        
    def updateDB(self):
        if self.data:
            Member.db.set(self, "phone", self.data["phone"], self.data)
            Member.db.save()

    @staticmethod
    def comparePoints(memberA,memberB):
        if memberA.points() > memberB.points():
            return 1
        elif memberA.points() == memberB.points():
            return 0
        else:
            return -1

    @staticmethod
    def compareTimes(memberA,memberB):
        if memberA.times() > memberB.times():
            return 1
        elif memberA.times() == memberB.times():
            return 0
        else:
            return -1
    
