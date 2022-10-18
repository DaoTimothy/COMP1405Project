import os
import math

def get_outgoing_links(URL):
    file = openFile(URL)
    if file == None:
        return None
    line = file.readline()
    closeFile(file)
    return stringToList(line)

def get_incoming_links(URL):
    file = openFile(URL)
    if file == None:
        return None
    line = ""
    for i in range(4):
        line = file.readline()
    closeFile(file)
    return stringToList(line)

def get_page_rank(URL):
    return

def get_idf(word):
    file = open("master.txt", "r")
    totalDocs = file.readline()
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

def get_tf(URL, word):
    file = openFile(URL)
    if file == None:
        return 0
    line = ""
    for i in range(2):
        line = file.readline()
    words = jsontodict(line)
    if word not in words:
        return 0
    line = file.readline()
    numWords = len(stringToList(line))
    return int(words[word]) / numWords

def get_tf_idf(URL, word):
    return math.log(1+get_tf(URL, word) * get_idf(word))

def openFile(URL):
    linkParts = URL.split(":")
    directory = ""
    for part in linkParts:
        directory += part
    path = "PageResults/"+directory[0:len(directory)-5]+".txt"
    if os.path.exists(path):
        file = open(path, "r")
        return file
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

"""
print("Out:", get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))

print("In:", get_incoming_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))

print("TF:", get_tf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html", "coconut"))
print("IDF:", get_idf("coconut"))

print("TFIDF:", get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html", "coconut"))
"""