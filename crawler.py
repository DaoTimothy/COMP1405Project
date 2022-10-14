import webdev
import os

titleindex = 0
wordsindex = 1
linkindex = 2	

def crawl(seed):
    if os.path.exists("PageResults"):
        deleteFolder("PageResults")
    os.mkdir("PageResults")

    #variables required for crawl
    totalPages = 0
    unreadList = []
    unreadDict = {}
    readPages = {}
    addend(unreadList, unreadDict, seed)

    #extra information
    incomingLinks = {}

    while len(unreadList) > 0:
        currentLink = removestart(unreadList, unreadDict)
        readPages[currentLink] = 0

        contents = webdev.read_url(currentLink)
        htmlElements = contents.split("<")
        content = readHtml(htmlElements)

        print("At Page", content[titleindex])

        for link in content[linkindex]:
            absoluteLink = buildLink(currentLink, link)

            outgoingLinks = []
            outgoingLinks.append(absoluteLink)

            if absoluteLink not in incomingLinks:
                incomingLinks[absoluteLink] = []
            incomingLinks[absoluteLink].append(currentLink)
            
            #print(absolutelink)
            if absoluteLink not in readPages and not containshash(unreadDict, absoluteLink):
                addend(unreadList, unreadDict, absoluteLink)
        totalPages += 1
        savePage(currentLink, content, outgoingLinks)
    saveIncomingLinks(incomingLinks)
    return totalPages

def deleteFolder(string):
    if os.path.exists(string):
        files = os.listdir(string)
        for file in files:
            absolutePath = string+"/"+file
            if os.path.isdir(absolutePath):
                deleteFolder(absolutePath)
            elif os.path.isfile(absolutePath):
                os.remove(absolutePath)
    os.rmdir(string)
    return

def addend(list, dict, value):
	if value not in dict:
		dict[value] = 1
	else:
		dict[value] += 1
	list.append(value)
	
def removestart(list, dict):
	if len(list) == 0:
		return None
	dict[list[0]] -= 1
	if dict[list[0]] == 0:
		del dict[list[0]]
	return list.pop(0)
	
def containshash(dict, value):
	if value in dict:
		return True
	return False

def readHtml(list):
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

def buildLink(currenturl, string):
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

def savePage(currentLink, content, outgoingLinks):
    directory = buildDirectory(currentLink)
    file = open("PageResults/"+directory, "w")
    file.write(listtostring(outgoingLinks))
    file.write("\n"+dicttojson(rawtexttodict(content[wordsindex]))+"\n")
    file.close()

def buildDirectory(currentLink):
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

def saveIncomingLinks(incomingLinks):
    for page in incomingLinks:
        directory = buildDirectory(page)
        #print(directory)
        file = open("PageResults/"+directory, "a")
        file.write(listtostring(incomingLinks[page]))
    return

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

def dicttojson(jsonlist):
    result = "{"
    for key in jsonlist:
        result += "\""
        result += key
        result += "\":\""
        result += str(jsonlist[key])
        result += "\","
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