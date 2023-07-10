import json
from .Item import Item

class VideoSerial(Item):
    all_j = None
    def __init__(self, serial_j):
        self.j = serial_j
        self.file = serial_j["file"]
        self.title = serial_j["name"]
        self.abstract = serial_j["description"]
        self.addition = None

    def addEpisode(self,name):
        if name not in self.j["episode"]:
            self.j["episode"].append(name)
            VideoSerial.save()
            return True
        return False

    @staticmethod
    def load():
        if not VideoSerial.all_j:
            with open('json/VideoSerials.json','r',encoding='utf8') as fp:
                VideoSerial.all_j = json.load(fp)
        
        if not VideoSerial.all_j:
            VideoSerial.all_j = []

        return True

    @staticmethod
    def getPageList(pageNo,perPage):
        VideoSerial.load()
        
        startIndex = pageNo*perPage
        maxIndex = len(VideoSerial.all_j) - 1
        if startIndex > maxIndex:
            return None
            
        pageList = []   
        for i in range(perPage):
            currentIndex = startIndex+i
            if currentIndex > maxIndex:
                break
            serial = VideoSerial(VideoSerial.all_j[currentIndex])
            pageList.append(serial)
            
        return pageList

    @staticmethod
    def save():
        with open('json/VideoSerials.json','w',encoding='utf8') as fp:
            json.dump(VideoSerial.all_j,fp)
        return None

    @staticmethod
    def get(file):
        VideoSerial.load()
        
        current = None
        previous = None
        next = None
        for item_j in VideoSerial.all_j:
            if item_j['file'] == file:
                current = VideoSerial(item_j)
                continue
            if current and not next:
                next = item_j['file']
                break
            previous = item_j['file']

        current.previous = previous
        current.next = next
        return current

    # add a new serial
    @staticmethod
    def add(file,name,description):
        VideoSerial.load()
        
        serial = VideoSerial.get(file)
        if serial:
            serial.j['name'] = name
            serial.j['description'] = description
        else:
            serial_j = {}
            serial_j['file'] = file
            serial_j['name'] = name
            serial_j['description'] = description
            VideoSerial.all_j.append(serial_j)
        
        return VideoSerial.save()
    
