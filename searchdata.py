import os

def get_outgoing_links(URL):
    directory = openPage(URL)
    if directory == None:
        return None
    outgoingLinks = os.listdir(os.path.join(directory, "outgoing"))
    for i in range(len(outgoingLinks)):
        outgoingLinks[i] = outgoingLinks[i].replace("}", "/").replace("http", "http:")
    return outgoingLinks

def get_incoming_links(URL):
    directory = openPage(URL)
    if directory == None:
        return None
    incomingLinks = os.listdir(os.path.join(directory, "incoming"))
    for i in range(len(incomingLinks)):
        incomingLinks[i] = incomingLinks[i].replace("}", "/").replace("http", "http:")
    return incomingLinks

def get_page_rank(URL):
    directory = openPage(URL)
    if directory == None:
        return -1
    file = open(os.path.join(directory,"PageRank"), "r")
    return float(file.readline())

def get_idf(word):
    if os.path.exists(os.path.join("idf", word)):
        file = open(os.path.join("idf", word), "r")
        return float(file.readline())
    return 0

def get_tf(URL, word):
    directory = openPage(URL)
    if directory == None or not os.path.exists(os.path.join(directory,"tf",word)):
        return 0
    file = open(os.path.join(directory,"tf",word),"r")
    return float(file.readline())

def get_tf_idf(URL, word):
    directory = openPage(URL)
    if directory == None:
        return 0
    if not os.path.exists(os.path.join(directory,"tf_idf",word)):
        return 0
    file = open(os.path.join(directory,"tf_idf",word),"r")
    return float(file.readline())


#This function's goal is to get the path of a page given it's URL. If the page was not visited during the crawl, the function returns None.
#Input:
# URL - a string representing the URL of a webpage.
#Output: a string representing the path to where that webpages' information is stored. Returns None if the page was not visited during the crawl.
def openPage(URL):
    linkParts = URL.replace(":", "").split("/")
    directory = ""
    for part in linkParts:
        directory = os.path.join(directory, part)
    path = os.path.join("PageResults", directory)

    if os.path.exists(path):
        return path
    return None