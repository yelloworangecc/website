import json
import datetime

class Article():
    all_j = None
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

    @staticmethod
    def load():
        if Article.all_j:
            return True
        else:
            with open('json/Articles.json','r',encoding='utf8') as fp:
                Article.all_j = json.load(fp)
        
        if Article.all_j is None:
            return False

        Article.all_j.sort(key=lambda x:x["time"])
        return True

    @staticmethod
    def getPageList(pageNo,perPage):
        ''' pageNo start from 0 '''
        if Article.all_j is None:
            return None

        startIndex = pageNo*perPage
        maxIndex = len(Article.all_j) - 1
        print(startIndex,maxIndex)
        if startIndex > maxIndex:
            return None
            
        pageList = []   
        for i in range(perPage):
            currentIndex = startIndex+i
            print(currentIndex)
            if currentIndex > maxIndex:
                break
            article = Article(Article.all_j[currentIndex])
            pageList.append(article)
            
        print(len(pageList))
        return pageList

    @staticmethod
    def save():
        with open('json/Articles.json','w',encoding='utf8') as fp:
            json.dump(Article.all_j,fp)
            
        return None

    @staticmethod
    def get(name):
        if not Article.all_j:
            Article.load()
        for article_j in Article.all_j:
            if article_j["file"] == name:
                return Article(article_j)
        return None