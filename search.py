import os
from webbrowser import get
import searchdata
import math

def search(phrase, boost):
    phraseList = phrase.split()
    queryVector = queryvector(phrase, phraseList)
    print(topten("PageResults", queryVector, phraseList, [0,0,0,0,0,0,0,0,0,0]))
    if boost:
        return 
    return
    
    
    return

def queryvector(phrase, phraseList):
    dict = rawtexttodict(phrase)
    result = []
    words = phrase.split()
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


def topten(base, queryVector, phraseList, results):
    if os.path.exists(base):
        files = os.listdir(base)
        for file in files:
            absolutePath = os.path.join(base,file)
            #print(absolutePath)
            if os.path.exists(os.path.join(absolutePath, "PageRank")): #if the folder reperesents a page
                contentScore = cosineSimilarity(queryVector, documentvector(pathtolink(absolutePath), phraseList))
                for i in range(len(results)):
                    if results[i] < contentScore:
                        results.insert(i, contentScore)
                        del results[10]
            elif os.path.isdir(absolutePath):
                topten(absolutePath, queryVector, phraseList, results)
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

search("coconut apple", False)

