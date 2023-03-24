import json,datetime

class Article():
    all_j = None
    p = None
    n = None
    def __init__(self, article_j):
        self.article_j = article_j

    def getFileName(self):
        return self.article_j["file"]

    def getTitle(self):
        return self.article_j["title"]
        
    def getAbstract(self):
        return self.article_j["abstract"]
        
    def getPostTime(self):
        return self.article_j["time"]

    def setRelative(self, p, n):
        self.p = p
        self.n = n

    def getPrevious(self):
        return self.p

    def getNext(self):
        return self.n

    @staticmethod
    def load():
        if not Article.all_j:
            with open('json/Articles.json','r',encoding='utf8') as fp:
                Article.all_j = json.load(fp)
        
        if not Article.all_j:
            Article.all_j = []

        return True

    @staticmethod
    def getPageList(pageNo,perPage):
        Article.load()
        
        startIndex = pageNo*perPage
        maxIndex = len(Article.all_j) - 1
        if startIndex > maxIndex:
            return None
            
        pageList = []   
        for i in range(perPage):
            currentIndex = startIndex+i
            if currentIndex > maxIndex:
                break
            article = Article(Article.all_j[currentIndex])
            pageList.append(article)
            
        return pageList

    @staticmethod
    def save():
        with open('json/Articles.json','w',encoding='utf8') as fp:
            json.dump(Article.all_j,fp)
            
        return None

    @staticmethod
    def get(name):
        Article.load()

        previous = None
        current = None
        next = None
        for article_j in Article.all_j:
            if article_j['file'] == name:
                current = Article(article_j)
                continue
            if current and not next:
                next = article_j['file']
                break
            previous = article_j['file']

        current.setRelative(previous,next)
        return current

    @staticmethod
    def add(filename,title,abstract):
        Article.load()
        
        time_str = str(datetime.datetime.now())
        print(time_str)
        
        article = Article.get(filename)
        if article:
            article.article_j['title'] = title
            article.article_j['abstract'] = abstract
            article.article_j['time'] = time_str 
        else:
            article_j = {}
            article_j['file'] = filename
            article_j['title'] = title
            article_j['abstract'] = abstract
            article_j['time'] = time_str
            Article.all_j.append(article_j)
        
        return Article.save()
