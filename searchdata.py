import os
import math

def get_outgoing_links(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    outgoingLinks = os.listdir(directory+"/outgoing")
    for i in range(len(outgoingLinks)):
        outgoingLinks[i] = outgoingLinks[i].replace("-", "/").replace("http", "http:")
    return outgoingLinks

def get_incoming_links(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    incomingLinks = os.listdir(directory+"/incoming")
    for i in range(len(incomingLinks)):
        incomingLinks[i] = incomingLinks[i].replace("-", "/").replace("http", "http:")
    return incomingLinks

def get_page_rank(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    file = open(directory+"/PageRank", "r")
    return float(file.readline())

def get_idf(word):
    return

def get_tf(URL, word):
    directory = openPage(URL)
    if directory == None:
        return 0
    file = open(directory+"/tf/"+word, "r")
    return float(file.readline())

def get_tf_idf(URL, word):
    directory = openPage(URL)
    if directory == None:
        return 0
    file = open(directory+"/tf_idf/"+word, "r")
    return float(file.readline())

def openPage(URL):
    linkParts = URL.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    path = "PageResults/"+directory[0:len(directory)-5]
    if os.path.exists(path):
        return path
    return None

def closeFile(file):
    file.close()
    return

def stringToList(string):
    result = []
    item = ""
    readingItem = False
    for char in string:
        if char == "[" or char == "]":
            continue
        if char == "\"" and not readingItem:
            readingItem = True
        elif char == "\"" and readingItem:
            result.append(item)
            item = ""
            readingItem = False
        elif readingItem:
            item += char
    return result


print("Out:", get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html"))

print("In:", get_incoming_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html"))

print("TF:", get_tf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html", "coconut"))
print("IDF:", get_idf("coconut"))

print("TFIDF:", get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html", "coconut"))
