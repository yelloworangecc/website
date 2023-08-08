import json,datetime
from .Item import Item

class Article(Item):
    all_j = None
    def __init__(self, article_j):
        self.j = article_j
        self.file = article_j["file"]
        self.title = article_j["title"]
        self.abstract = article_j["abstract"]
        self.addition = article_j["time"]

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
        
        current = None
        previous = None
        next = None
        for article_j in Article.all_j:
            if article_j['file'] == name:
                current = Article(article_j)
                continue
            if current and not next:
                next = article_j['file']
                break
            previous = article_j['file']

        if current:
            current.previous = previous
            current.next = next

        return current

    @staticmethod
    def add(filename,title,abstract):
        Article.load()
        
        time_str = str(datetime.datetime.now())
        # print(time_str)
        
        article = Article.get(filename)
        if article:
            article.j['title'] = title
            article.j['abstract'] = abstract
            article.j['time'] = time_str 
        else:
            article_j = {}
            article_j['file'] = filename
            article_j['title'] = title
            article_j['abstract'] = abstract
            article_j['time'] = time_str
            Article.all_j.append(article_j)
        
        return Article.save()
