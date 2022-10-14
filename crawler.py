from distutils.command.build import build
import webdev
import os

titleindex = 0
wordsindex = 1
linkindex = 2

def crawl(seed):
    if not os.path.exists("PageResults"):
        os.mkdir("PageResults")

    #variables required for crawl
    totalPages = 0
    unreadLinks = []
    unreadDict = {}
    readPages = {}
    unreadLinks.append(seed)
    unreadDict[seed] = 0

    #extra information
    incomingLinks = {}

    while len(unreadLinks) > 0:
        currentLink = unreadLinks.pop(0)
        del unreadDict[currentLink]
        addlink(readPages, currentLink)  
        contents = webdev.read_url(currentLink)
        words = contents.split("<")
        content = readhtml(words)
        print("At Page", content[titleindex])

        for link in content[linkindex]:
            outgoinglinks = []
            absolutelink = buildlink(currentLink, link)
            if absolutelink not in incomingLinks:
                incomingLinks[absolutelink] = []
            incomingLinks[absolutelink].append(currentLink)
            outgoinglinks.append(absolutelink)
            #print(absolutelink)
            if absolutelink not in readPages and absolutelink not in unreadDict:
                unreadLinks.append(absolutelink)
                unreadDict[absolutelink] = 0
        totalPages += 1
        save(currentLink, content, outgoinglinks)
    save_incoming(incomingLinks)
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

def save(currentLink, content, outgoinglinks):
    directory = build_directory(currentLink)
    file = open("PageResults/"+directory, "w")
    file.write(str(len(outgoinglinks))+" Outgoing Links")
    for link in outgoinglinks:
        file.write("\n"+link)
    file.write(content[wordsindex])
    file.close()

def build_directory(currentLink):
    linkParts = currentLink.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    currentDirectory = "PageResults"
    folders = directory.split("/")
    for i in range(len(folders)-1):
        
        if folders[i] == "":
            continue
        elif not os.path.exists(currentDirectory+"/"+folders[i]):
            os.mkdir(currentDirectory+"/"+folders[i])
        currentDirectory += "/" + folders[i]
    return directory[0:len(directory)-5]+".txt"

def save_incoming(incomingLinks):
    for page in incomingLinks:
        directory = build_directory(page)
        #print(directory)
        file = open("PageResults/"+directory, "a")
        file.write(listtostring(incomingLinks[page]))
    return

def dicttojson(jsonlist):
    result = "{"
    for key in jsonlist:
        result += "\""
        result += key
        result += "\":\""
        result += jsonlist[key]
        result += ","
    result = result[0:len(result)-1]
    result += "}"
    return result

def listtostring(list):
    result = "["
    for item in list:
        result += "\"" + item + "\", "
    result = result[0:len(result)-2]
    result += "]"
    return result

temp = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))