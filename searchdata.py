import os

def get_outgoing_links(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    outgoingLinks = os.listdir(os.path.join(directory, "outgoing"))
    for i in range(len(outgoingLinks)):
        outgoingLinks[i] = outgoingLinks[i].replace("-", "/").replace("http", "http:")
    return outgoingLinks

def get_incoming_links(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    incomingLinks = os.listdir(os.path.join(directory, "incoming"))
    for i in range(len(incomingLinks)):
        incomingLinks[i] = incomingLinks[i].replace("-", "/").replace("http", "http:")
    return incomingLinks

def get_page_rank(URL):
    directory = openPage(URL)
    if directory == None:
        return 0
    file = open(os.path.join(directory,"PageRank"), "r")
    return float(file.readline())

def get_idf(word):
    file = open(os.path.join("idf", word), "r")
    return float(file.readline())

def get_tf(URL, word):
    directory = openPage(URL)
    if directory == None:
        return 0
    file = open(os.path.join(directory,"tf",word),"r")
    #file = open(directory+"/tf/"+word, "r")
    return float(file.readline())

def get_tf_idf(URL, word):
    directory = openPage(URL)
    if directory == None:
        return 0
    if not os.path.exists(os.path.join(directory,"tf_idf",word)):
        return 0
    file = open(os.path.join(directory,"tf_idf",word),"r")
    return float(file.readline())

def openPage(URL):
    linkParts = URL.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    #path = "PageResults/"+directory[0:len(directory)-5]
    path = os.path.join("PageResults",directory[0:len(directory)-5])
    if os.path.exists(path):
        return path
    return None

"""
print("Out:", get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/fruits/N-1.html"))

print("In:", get_incoming_links("http://people.scs.carleton.ca/~davidmckenney/fruits/N-1.html"))

print("TF:", get_tf("http://people.scs.carleton.ca/~davidmckenney/fruits/N-1.html", "coconut"))
print("IDF:", get_idf("coconut"))

print("TFIDF:", get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/fruits/N-1.html", "coconut"))
"""