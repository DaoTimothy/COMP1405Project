import os

def get_outgoing_links(URL):
    file = openFile(URL)
    line = file.readline()
    closeFile(file)
    return stringToList(line)

def get_incoming_links(URL):
    file = openFile(URL)
    line = ""
    for i in range(3):
        line = file.readline()
    closeFile(file)
    return stringToList(line)

def get_page_rank(URL):
    return

def get_idf(word):
    return

def get_tf(URL, word):
    return

def get_tf_idf(URL, word):
    return

def openFile(URL):
    linkParts = URL.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    path = "PageResults/"+directory[0:len(directory)-5]+".txt"
    file = open(path, "r")
    return file

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

print("Out: ", get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html"))

print("In: ", get_incoming_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html"))