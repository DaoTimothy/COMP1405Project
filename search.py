import searchdata
import math

def search(phrase, boost):
    query = queryvector(phrase)
    print(query)
    return

def queryvector(phrase):
    dict = rawtexttodict(phrase)
    result = []
    words = phrase.split()
    print("Dict", dict)
    print("List", words)
    for word in words:
        tf = dict[word] / len(words)
        result.append(math.log(tf+1,2)*searchdata.get_idf(word))
    return result

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

search("coconut apple", False)