import webdev

links = {}
titleindex = 0
wordsindex = 1
linkindex = 2

def crawl(seed):
    totalPages = 0
    unreadPages = []
    unreadDict = {}
    readPages = {}
    unreadPages.append(seed)
    unreadDict[seed] = 0
    while len(unreadPages) > 0:
        currentPage = unreadPages.pop(0)
        del unreadDict[currentPage]
        addlink(readPages, currentPage)  
        contents = webdev.read_url(currentPage)
        words = contents.split("<")
        content = readhtml(words)
        print(content[titleindex])
        for link in content[linkindex]:
            absolutelink = buildlink(currentPage, link)
            if absolutelink not in readPages and absolutelink not in unreadDict:
                unreadPages.append(absolutelink)
                unreadDict[absolutelink] = 0
        totalPages += 1
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
    
temp = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
addlink(links, temp)
print(links)
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))