from cgi import print_directory
import webdev
import math
import os
import pagerank
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
    allWords = {}
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
        outgoingLinks = []
        tfDict = {}

        for link in content[linkindex]:
            absoluteLink = buildLink(currentLink, link)
            
            outgoingLinks.append(absoluteLink)

            if absoluteLink not in incomingLinks:
                incomingLinks[absoluteLink] = []
            incomingLinks[absoluteLink].append(currentLink)
            
            #print(absolutelink)
            if absoluteLink not in readPages and not containshash(unreadDict, absoluteLink):
                addend(unreadList, unreadDict, absoluteLink)
        #print(content[wordsindex])
        wordDict = rawtexttodict(content[wordsindex])
        wordList = content[wordsindex].replace("\n", " ").split()
        for word in wordDict:
            if word not in allWords:
                allWords[word] = 1
            tfDict[word] = wordDict[word]/len(wordList)
        totalPages += 1
        savePage(currentLink, outgoingLinks, wordDict, tfDict)
    file = open("PageResults/master.txt", "w")
    file.write(str(totalPages)+"\n")
    idfDict = {}
    for word in allWords:
        idfDict[word] = calcIdf(word, totalPages)
    file.write(dicttojson(idfDict)+"\n")
    file.close()
    pageRankList = pagerank.pagerank(incomingLinks)[0]
    mappingDict = pagerank.idmapping(incomingLinks)
    print(mappingDict)
    saveInfoAfterCrawl(incomingLinks, idfDict, pageRankList, mappingDict)
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
    #print(list)
    for element in list:
        if len(element) == 0:
            continue
        elif element[0:6] == "title>" or element[0:6] == "title ":
            result[titleindex] = element[element.index(">")+1:len(element)]
        elif element[0:2] == "p " or element[0:2] == "p>":
            result[wordsindex] = element[element.index(">")+1:len(element)]
        elif "href=\"" in element:
            link = ""
            for letter in range(element.index("href=\"")+6,len(element)):
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

def savePage(currentLink, outgoingLinks, wordDict, tfDict):
    directory = "PageResults/"+buildDirectory(currentLink)
    tfDir = directory+"/tf"
    os.mkdir(tfDir)
    for word in wordDict:
        if word != "":
            file = open(tfDir+"/"+word, "w")
            file.write(str(tfDict[word]))
            file.close()
   
    outDir = directory+"/outgoing"
    os.mkdir(outDir)
    for link in outgoingLinks:
        temp = link.replace(":", "").replace("/", "-")
        file = open(outDir+"/"+temp, "w")
        file.close()
    return

def buildDirectory(currentLink):
    linkParts = currentLink.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    currentDirectory = "PageResults"
    folders = directory.split("/")
    for i in range(len(folders)):
        if folders[i] == "":
            continue
        elif not (os.path.exists(currentDirectory+"/"+folders[i]) or os.path.exists(currentDirectory+"/"+folders[i][0:len(folders[i])-5])):
            if folders[i][len(folders[i])-5:len(folders[i])] == ".html":
                os.mkdir(currentDirectory+"/"+folders[i][0:len(folders[i])-5])
            else:
                os.mkdir(currentDirectory+"/"+folders[i])
        currentDirectory += "/" + folders[i]
    return directory[0:len(directory)-5]

def saveInfoAfterCrawl(incomingLinks, idfDict, pageRankList, mappingDict):
    for page in incomingLinks:
        directory = "PageResults/"+buildDirectory(page)
        #print(directory)
        tf_idfDir = directory+"/tf_idf"
        #print(tf_idfDir)
        os.mkdir(tf_idfDir)
        
        tfDir = directory+"/tf"
        words = os.listdir(tfDir)
        #print(words)
        for word in words:
            file = open(tfDir+"/"+word, "r")
            tf = file.readline()
            file.close()
            file = open(tf_idfDir+"/"+word, "w")
            file.write(str(math.log(1+float(tf)) * idfDict[word]))
            file.close()
        
        inDir = directory+"/incoming"
        os.mkdir(inDir)
        for link in incomingLinks[page]:
            temp = link.replace(":", "").replace("/", "-")
            file = open(inDir+"/"+temp, "w")
            file.close()
    for key in mappingDict:
        directory = "PageResults/"+buildDirectory(mappingDict[key])
        file = open(directory+"/PageRank", "w")
        file.write(str(pageRankList[key]))
        file.close()
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


def calcIdf(word, totalDocs):
    #visit every page and see if this word is in that dictionary.
    numerator = totalDocs
    denominator = 1 + checkFiles("PageResults", word, 0)
    return math.log(int(numerator)/int(denominator), 2)

def checkFiles(base, word, total):
    if os.path.exists(base):
        files = os.listdir(base)
        for file in files:
            absolutePath = base+"/"+file
            if os.path.isdir(absolutePath):
                total += checkFiles(absolutePath, word, total)
            elif os.path.isfile(absolutePath):
                tempfile = open(absolutePath, "r")
                line = ""
                for i in range(2):
                    line = tempfile.readline()
                words = jsontodict(line)
                if word in words:
                    total += 1
    return total

def jsontodict(string):
    result = {}
    getkey = False
    getvalue = False
    passedColon = False
    key = ""
    value = ""
    
    for character in string:
        if character == ":":
            passedColon = True
        if character == '"':
            getkey = not getkey
            getvalue = not getvalue
        elif getkey == True and passedColon == False:
            key += character
        elif getvalue == True and passedColon == True:
            value += character
        elif character == ",":
            if key not in result:
                result[key] = value
            key = ""
            value = ""
            passedColon = False
    return result

def savepagerank(str):
    return

temp = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))