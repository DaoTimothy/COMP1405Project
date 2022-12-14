import os
import math

import searchdata

def search(phrase, boost):
    phraseDict = stringToDict(phrase)
    phraseList = phrase.split()
    queryVector = getQueryVector(phraseDict, phraseList)
    temp = [{'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}, {'url' : '', 'title' : '', 'score' : -1}]
    return topTen("PageResults", queryVector, phraseDict, boost, temp)

#This function's goal is to return a list representing the vector of the user's query.
#Input:
# phrase - string representing a search query from the user.
# phraseDict - a list representing the search query as well.
#Output: a vector of the tf_idf values of each word in the search query, in the order that they appeared within the query. 
def getQueryVector(phraseDict, phraseList):
    result = []
    for word in phraseDict:
        tf = phraseDict[word] / len(phraseList)
        idf = searchdata.get_idf(word)
        result.append(math.log(1 + tf,2)*idf)
    return result

#This function's goal is to represent a string as a dictionary, to reduce processing time for when we calculate the tf values for the query vector.
#Input: 
# string - a string of words, separated by spaces.
#Output: a dictionary representation of the string, with each key being a unique word in the string, and the value of each key being the number of times that word appears in the string.
def stringToDict(string):
    result = {}
    words = string.split(" ")
    for word in words:
        if word not in result:
            result[word] = 1
        else:
            result[word] += 1
    return result

#This function's goal is to return a list of dictionaries containing the top ten pages according to score.
#Input:
# base - a path representing where to look for files within. Included since the function will need to recursively look through all the directories within PageResults to find all the pages.
# queryVector - a list of tf_idf values representing the vector of the search query.
# phraseDict - a list of the words in the phrase in the order they were entered, so a document vector can be created to mirror the query vector. 
# boost - a boolean value to decide whether a page's cosine similarity should be boosted by its' pagerank.
# results - a list of dictionaries representing the top ten pages with the highest content scores. It's included in the parameters because the function is recursive.
#Output: a list of dictionaries representing the top ten pages with the highest content scores.
def topTen(base, queryVector, phraseDict, boost, results):
    if os.path.exists(base):
        files = os.listdir(base)
        for file in files:
            absolutePath = os.path.join(base,file)
            if os.path.exists(os.path.join(absolutePath, "PageRank")): #if the folder reperesents a page
                pageInfo = {}
                pageInfo["url"] = pathToLink(absolutePath)
                pageInfo["title"] = getTitle(absolutePath)
                pageInfo["score"] = cosineSimilarity(queryVector, getDocumentVector(pageInfo["url"], phraseDict))
                if boost:
                    pageInfo["score"] *= searchdata.get_page_rank(pageInfo["url"])
                
                for i in range(len(results)): #insert the page in the correct spot in the top ten ranking, then delete the lowest one
                    if results[i]["score"] < pageInfo["score"]:
                        results.insert(i, pageInfo)
                        del results[10]
                        break
            elif os.path.isdir(absolutePath):
                topTen(absolutePath, queryVector, phraseDict, boost, results)
    return results

#This function's goal is to produce a URL based off a path within the PageResults folder.
#Input: 
# absolutePath - the path to a directory that represents a page.
#Output: a string representing the URL of the page whose path was entered as a parameter.
def pathToLink(absolutePath):
    parts = absolutePath.split(os.sep)
    link = ""
    for i in range(1, len(parts)):
        if parts[i] == "http":
            link += parts[i] + "://"
        else:
            link += parts[i] + "/"
    return link[0:len(link)-1]

#This function's goal is to produce a list of tf_idf values that represents the document vector.
#Input: 
# URL - the url of the page that we want to get a document vector for.
# phraseDict - a list of the words in the search query in the order they were entered so the document vector can mirror the query vector.
#Output: a list of tf_idf values that represents the document vector.
def getDocumentVector(URL, phraseDict):
    result = []
    for word in phraseDict:
        result.append(searchdata.get_tf_idf(URL, word))
    return result

#This function's goal is to calculate the cosine similarity between the query vector a particular document vector.
#Input: 
# queryVector - a list of tf_idf values representing the query vector.
# documentVector - a list of tf_idf values representing the document vector.
#Output: a float representing the cosine similarity between the two vectors.
def cosineSimilarity(queryVector, documentVector):
    numerator = dotProduct(queryVector, documentVector)
    queryEuclideanNorm = euclideanNorm(queryVector)
    docuEuclideanNorm = euclideanNorm(documentVector)
    if docuEuclideanNorm == 0 or queryEuclideanNorm == 0:
        return 0
    return numerator / (queryEuclideanNorm * docuEuclideanNorm)

#This function's goal is to return the dot product of two vectors. 
#Input:
# a - a vector.
# b - another vector.
#Output: an integer representing the dot product of the two vectors.
def dotProduct(a, b):
    sum = 0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum

#This function's goal is to calculate the euclidian norm of a vector. 
#Input:
# vector - a vector.
#Output: a float representing the euclidian norm of the vector.
def euclideanNorm(vector):
    sum = 0
    for i in vector:
        sum += i**2
    return math.sqrt(sum)

#This function's goal is to retrieve the title of a page given the page's path.
#Input:
# path - a string representing the page's path.
#Output: a string representing the title of the page.
def getTitle(path):
    file = open(os.path.join(path, "title.txt"), "r")
    return file.readline()