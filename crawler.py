import webdev
import os

titleindex = 0
wordsindex = 1
linkindex = 2

def crawl(seed):
    if not os.path.exists("PageResults"):
        os.mkdir("PageResults")
    totalPages = 0
    unreadPages = []
    unreadDict = {}
    readPages = {}
    linkRelations = {}
    unreadPages.append(seed)
    unreadDict[seed] = 0
    while len(unreadPages) > 0:
        currentPage = unreadPages.pop(0)
        del unreadDict[currentPage]
        addlink(readPages, currentPage)  
        contents = webdev.read_url(currentPage)
        words = contents.split("<")
        content = readhtml(words)
        print("At Page", content[titleindex])
        outgoinglinks = {}
        for link in content[linkindex]:
            absolutelink = buildlink(currentPage, link)
            outgoinglinks[absolutelink] = 0
            print(absolutelink)
            if absolutelink not in readPages and absolutelink not in unreadDict:
                unreadPages.append(absolutelink)
                unreadDict[absolutelink] = 0
        linkRelations[currentPage] = outgoinglinks
        totalPages += 1
        save(content)
    print(linkRelations)
    return totalPages

def readhtml(list):
    result = ["", "", ""]
    links = []
    for element in list:
        if len(element) == 0:
            continue
        elif element[0:6] == "title>":
            result[titleindex] = element[6:len(element)]
        elif element[0:2] == "p>":
            result[wordsindex] = element[2:len(element)]
        elif element[0:8] == "a href=\"":
            link = ""
            for letter in range(8,len(element)):
                if element[letter] == "\"":
                    break
                link += element[letter]
            links.append(link)
    result[linkindex] = links
    return result

#takes in a dictionary of links and a list representing a url that has been split at each.
def addlink(dict, string):
    if string not in dict:
        dict[string] = 0
    return

def buildlink(currenturl, string):
    if string[0] == ".":
        urlparts = currenturl.split("/")
        result = ""
        for part in range(0, len(urlparts)-1):
            result += urlparts[part]
            result += "/"
        result = result[0:len(result)-1]
        result += string[1:len(string)]
        return result
    return string

def save(content):
    file = open("PageResults/"+content[titleindex], "w")
    file.close()
temp = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))