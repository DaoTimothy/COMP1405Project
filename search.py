import os
from webbrowser import get
import searchdata
import math

import time

scoreIndex = 0
titleIndex = 1
urlIndex = 2

def search(phrase, boost):
    phraseList = phrase.split()
    queryVector = queryvector(phrase, phraseList)
    temp = [{'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}, {'url' : '', 'title' : '', 'score' : 0}]
    return topten("PageResults", queryVector, phraseList, boost, temp)

def queryvector(phrase, phraseList):
    dict = rawtexttodict(phrase)
    result = []
    for word in phraseList:
        tf = dict[word] / len(phraseList)
        result.append(math.log(tf+1,2)*searchdata.get_idf(word))
    return result

def rawtexttodict(string):
    result = {}
    cleaned = string.replace("\n", " ")
    words = cleaned.split(" ")
    for word in words:
        if word not in result:
            result[word] = 1
        else:
            result[word] += 1
    return result

def topten(base, queryVector, phraseList, boost, results):
    if os.path.exists(base):
        files = os.listdir(base)
        for file in files:
            absolutePath = os.path.join(base,file)
            #print(absolutePath)
            if os.path.exists(os.path.join(absolutePath, "PageRank")): #if the folder reperesents a page
                pageInfo = {}
                pageInfo["url"] = pathtolink(absolutePath)
                pageInfo["score"] = cosineSimilarity(queryVector, documentvector(pageInfo["url"], phraseList))
                if boost:
                    pageInfo["score"] *= searchdata.get_page_rank(pageInfo["url"])
                pageInfo["title"] = getTitle(absolutePath)
                
                for i in range(len(results)):
                    if results[i]["score"] < pageInfo["score"]:
                        results.insert(i, pageInfo)
                        del results[10]
                        break
            elif os.path.isdir(absolutePath):
                topten(absolutePath, queryVector, phraseList, boost, results)
    return results

def dotproduct(a, b):
    sum = 0
    for i in range(len(a)):
        sum += a[i]*b[i]
    return sum

def cosineSimilarity(queryVector, docuVector):
    numerator = dotproduct(queryVector, docuVector)
    queryEuclidianNorm = euclidianNorm(queryVector)
    docuEuclidianNorm = euclidianNorm(docuVector)
    if docuEuclidianNorm == 0 or queryEuclidianNorm == 0:
        return 0
    return numerator/(queryEuclidianNorm*docuEuclidianNorm)

def euclidianNorm(vector):
    sum = 0
    for i in vector:
        sum += i**2
    return sum**0.5

def documentvector(URL, phraseList):
    result = []
    for word in phraseList:
        result.append(searchdata.get_tf_idf(URL, word))
    return result

def pathtolink(absolutePath):
    parts = absolutePath.split(os.sep)
    link = ""
    for i in range(1, len(parts)):
        if parts[i] == "http":
            link += parts[i]+"://"
        else:
            link += parts[i] + "/"
    return link[0:len(link)-1]+".html"

def getTitle(path):
    file = open(os.path.join(path, "title.txt"), "r")
    return file.readline()

startTime = time.time()
search("apple coconut", False)
print(time.time()-startTime, "Seconds")
