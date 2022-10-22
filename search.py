from crawler import jsontodict
import searchdata
import math
import os

def search(phrase, boost):
    queryVec = queryvector(phrase)
    print(queryVec)
    return

def queryvector(phrase):
    dict = rawtexttodict(phrase)
    result = []
    words = phrase.split()
    print("Dict", dict)
    print("List", words)
    for word in words:
        tf = dict[word] / len(words)
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

def idklol(string):
    docDict = {}
    if os.path.exists(string):
        files = os.listdir(string)
        for file in files:
            absolutePath = string+"/"+file
            if os.path.isdir(absolutePath):
                
                docDict[absolutePath] = generateDocVector(absolutePath)
            elif os.path.isfile(absolutePath):
                os.remove(absolutePath)
    os.rmdir(string)
    return

def generateDocVector(absolutePath, queryList):
    file = open(absolutePath, "r")
    for i in range(6):
        line = file.readline()
    tf_idfDict = jsontodict(line)
    docVector = []
    for word in queryList:
        docVector.append(tf_idfDict[word])
    return docVector
search("coconut apple", False)