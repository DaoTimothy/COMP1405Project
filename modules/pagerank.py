import modules.matmult as matmult

"""
0=PG3
1=PG4
2=PG5
3=PG6
4=PG8
5=PG1
6=PG2
7=PG7
8=PG0
9=PG9
"""

def pagerank(incomingLinksDict):
    idMap = idMapping(incomingLinksDict)
    matrix = createMatrix(idMap,incomingLinksDict)
    pageranking = finalVector(matrix)
    return pageranking


def idMapping(incomingLinksDict):
    fileID = {}
    count = 0
    for key in incomingLinksDict:
        fileID[count] = key
        count += 1
    return fileID

def createMatrix(idMap,incomingLinksDict):
    alpha = 0.1
    matrix = []
    notCount = 0
    yesCount = 0
    totalPages = len(idMap)

    #Creates Adjacency row with 1 and 0s ONLY
    for key in idMap:
        row = []
        sidePage = idMap[key]

        for toprow in range(0, totalPages):
            toppage = idMap[toprow]#onverts top row number to the page

            #Checks if the sidePage is contained in the incoming links of the top page
            if sidePage in incomingLinksDict[toppage]:
                row.append(1)
                yesCount += 1
                notCount = 0
            else:
                row.append(0)
                notCount += 1
                if notCount == totalPages: #Checks if the page had no incoming links, row is all zeros
                    row = []
                    for i in range(totalPages):
                        row.append(1 / totalPages)#Can teleport to any page with 1/n probability

        #Initial transition probability matrix (dividing rows by # of 1s):
        for i in range(len(row)):
            if row[i] == 1:
                row[i] = 1 / yesCount
            row[i] = row[i] * (1-alpha) + alpha / totalPages
         

        

        yesCount = 0
        notCount = 0
        matrix.append(row)
        
    return matrix

def finalVector(matrix):
    threshhold = 0.0001
    dist = 1
    oldVector = [[]]
    for i in range(len(matrix)):
        oldVector[0].append(0.1)
    newVector = [dotProduct(matrix,oldVector)]
    while dist > threshhold: 
        newVector = [dotProduct(matrix,newVector)]
        dist = matmult.euclidean_dist(newVector, oldVector)
        oldVector = newVector
    return newVector
        
def dotProduct(matrix, vector):
    newVector = []
    for column in range(len(vector[0])):
        sum = 0
        index = 0
        for row in matrix:
            sum += row[column] * vector[0][index]
            index += 1
        newVector.append(sum)
        
    return newVector






