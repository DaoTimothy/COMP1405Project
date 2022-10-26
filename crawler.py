import webdev
import math
import os

import modules.pagerank as pagerank
import modules.improvedqueue as improvedqueue

import searchdata

titleIndex = 0
wordsIndex = 1
linkIndex = 2	

def crawl(seed):
    #deleting old information
    if os.path.exists("PageResults"):
        deleteFolder("PageResults")
    if os.path.exists("idf"):
        deleteFolder("idf")
    os.mkdir("PageResults")

    #variables required for crawl
    totalPages = 0
    unreadList = []
    unreadDict = {}
    readPages = {}
    allWords = {}
    improvedqueue.addend(unreadList, unreadDict, seed)
    incomingLinks = {}

    while len(unreadList) > 0:
        currentLink = improvedqueue.removestart(unreadList, unreadDict)
        readPages[currentLink] = 0

        contents = webdev.read_url(currentLink)
        htmlElements = contents.split("<")
        content = readHtml(htmlElements)

        #print("At Page", content[titleIndex])
        outgoingLinks = []
        tfDict = {}

        for link in content[linkIndex]:
            absoluteLink = buildLink(currentLink, link)
            outgoingLinks.append(absoluteLink)
            if absoluteLink not in incomingLinks:
                incomingLinks[absoluteLink] = []
            incomingLinks[absoluteLink].append(currentLink)
            
            if absoluteLink not in readPages and not improvedqueue.containshash(unreadDict, absoluteLink):
                improvedqueue.addend(unreadList, unreadDict, absoluteLink)
        wordDict = stringToDict(content[wordsIndex])
        wordList = content[wordsIndex].replace("\n", " ").split()
        for word in wordDict:
            if word not in allWords:
                allWords[word] = 1
            tfDict[word] = wordDict[word]/len(wordList)
        totalPages += 1
        savePage(currentLink, outgoingLinks, wordDict, tfDict, content[titleIndex])
    pagerankList = pagerank.pagerank(incomingLinks)[0]
    mappingDict = pagerank.idMapping(incomingLinks)
    saveInfoAfterCrawl(incomingLinks, allWords, totalPages, pagerankList, mappingDict)
    return totalPages

#This function's goal is to delete a folder and all of it's contents
#Input:
# path - a string representing a file path of the folder to be deleted
#Output: None
def deleteFolder(path):
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            absolutePath = os.path.join(path, file)
            if os.path.isdir(absolutePath):
                deleteFolder(absolutePath)
            elif os.path.isfile(absolutePath):
                os.remove(absolutePath)
    os.rmdir(path)
    return

#This function's goal is to read through html and collect the needed information.
#Input: 
# htmlContents - a string of html contents that have been split at the "<" symbol.
#Output: a list containing the title, words and links found in the html contents.
def readHtml(htmlContents):
    result = ["", "", ""]
    links = []
    for element in htmlContents:
        if len(element) == 0:
            continue
        elif element[0:6] == "title>" or element[0:6] == "title ":
            result[titleIndex] = element[element.index(">")+1:len(element)]
        elif element[0:2] == "p " or element[0:2] == "p>":
            result[wordsIndex] += element[element.index(">")+1:len(element)] + " "
        elif "href=\"" in element:
            link = ""
            for letter in range(element.index("href=\"")+6,len(element)):
                if element[letter] == "\"":
                    break
                link += element[letter]
            links.append(link)
    result[linkIndex] = links
    return result

#This function's goal is to build an absolute given any (relative or absolute) link.
#Input: 
# currentURL - a string representing the current URL the crawler is at.
# string - a string representing the contents of an href attribute.
#Output: a string representing an absolute link.
def buildLink(currentURL, string):
    if string[0] == ".":
        urlParts = currentURL.split("/")
        result = ""
        for part in range(0, len(urlParts)-1):
            result = (result+"/"+urlParts[part])
        result = result[0:len(result)]
        result += string[1:len(string)]
        return result[1:len(result)]
    return string

#This function's goal is to parse through a string and add its contents to a dictionary.
#Input:
# string - a string of words, separated by newline characters or spaces.
#Output: a dictionary with each key being a unique word found in the string, and the value of each being the frequency of that word within the string.
def stringToDict(string):
    result = {}
    cleaned = string.replace("\n", " ")
    words = cleaned.split(" ")
    for word in words:
        if word not in result:
            result[word] = 1
        else:
            result[word] += 1
    return result

#This function's goal is to write information that can be saved right after reading one page to files.
#Input:
# currentLink - a string representing the current link of the page.
# outgoingLinks - a list of string representing all the outgoing links on a page.
# wordDict - a dictionary that represents the word contents of the page.
# title - a string representing the title of the page.
#Output: None
def savePage(currentLink, outgoingLinks, wordDict, tfDict, title):
    directory = os.path.join("PageResults", buildDirectory(currentLink))
    file = open(os.path.join(directory, "title.txt"), "w")
    file.write(title)
    file.close()
    tfDir = os.path.join(directory,"tf")
    os.mkdir(tfDir)
    for word in wordDict:
        if word != "":
            file = open(os.path.join(tfDir,word), "w")
            file.write(str(tfDict[word]))
            file.close()
    outDir = os.path.join(directory, "outgoing")
    os.mkdir(outDir)
    for link in outgoingLinks:
        temp = link.replace(":", "").replace("/", "}")
        file = open(os.path.join(outDir,temp), "w")
        file.close()
    return

#This function's goal is to create the necessary folders to save a page.
#Input: 
# currentLink - a string representing the URL of the page to be saved.
#Output: a string representing the path of the directories where that page is saved.
def buildDirectory(currentLink):
    linkParts = currentLink.replace(":", "").split("/")
    directory = ""
    for part in linkParts:
        directory = os.path.join(directory, part)
    currentDirectory = "PageResults"
    folders = directory.split(os.sep)
    for i in range(len(folders)):
        if folders[i] == "":
            continue
        elif not (os.path.exists(os.path.join(currentDirectory, folders[i])) or os.path.exists(os.path.join(currentDirectory, folders[i][0:len(folders[i])-5]))):
            os.mkdir(os.path.join(currentDirectory,folders[i]))
        currentDirectory= os.path.join(currentDirectory,folders[i])
        #currentDirectory += "/" + folders[i]
    return directory

#This function's goal is to save all of page information that is only available after the crawl has been completed.
#Input:
# incomingLinks - a dictionary where each key is a unique URL, and the value is a list of URLs representing the incoming links for that page.
# allWords - a dictionary containing every unique word found within the crawl.
# totalPages - an integer representing the total number of pages found during the crawl.
# pagerankList - a list of pagerank values for every page.
# mappingDict - dictionary which maps a particular page to an index within the pagerankList list.
#Output: None
def saveInfoAfterCrawl(incomingLinks, allWords, totalPages, pagerankList, mappingDict):
    idfDir = "idf"
    os.mkdir(idfDir)
    for word in allWords:
        if word != "":
            file = open(os.path.join(idfDir, word), "w")
            file.write(str(calcIdf(word, totalPages)))
            file.close()

    for page in incomingLinks:
        directory = os.path.join("PageResults", buildDirectory(page))

        tf_idfDir = os.path.join(directory,"tf_idf")
        os.mkdir(tf_idfDir)

        tfDir = os.path.join(directory,"tf")
        words = os.listdir(tfDir)
        for word in words:
            tf = searchdata.get_tf(page, word)
            idf = searchdata.get_idf(word)
            file = open(os.path.join(tf_idfDir,word), "w")
            file.write(str(math.log(1+tf, 2) * idf))
            file.close()
        
        inDir = os.path.join(directory, "incoming")
        os.mkdir(inDir)
        for link in incomingLinks[page]:
            temp = link.replace(":", "").replace("/", "}")
            file = open(os.path.join(inDir, temp),"w")
            file.close()

    for key in mappingDict:
        directory = os.path.join("PageResults",buildDirectory(mappingDict[key]))
        file = open(os.path.join(directory,"PageRank"),"w")
        file.write(str(pagerankList[key]))
        file.close()
    return

#This function's goal is to calculate the idf value for a word.
#Input:
# word - a string representing the word who's idf is to be calculated.
# totalDocs - an integer representing the total number of pages crawled.
#Output: a float representing the idf of the word.
def calcIdf(word, totalDocs):
    #visit every page and see if this word is in that dictionary.
    numerator = totalDocs
    denominator = 1 + (checkFiles("PageResults", word, 0))
    return math.log(int(numerator)/int(denominator), 2)

#This function's goal is to check all the files and return how many times a word has appeared within during the crawl.
#Input:
# base - a string representing the current directory for recursive purposes.
# word - a string representing the word to be checked.
# total - an integer representing the current total for the amount of times that word has been found.
#Output: an integer representing the total number of pages that word appeared in during the crawl.
def checkFiles(base, word, total):
    if os.path.exists(base):
        files = os.listdir(base)
        for file in files:
            absolutePath = os.path.join(base,file)
            if os.path.isfile(absolutePath) and file == word:
                total += 1
            elif os.path.isdir(absolutePath):
                total += checkFiles(absolutePath, word, 0)
    return total