import modules.matmult as matmult

#This function pieces all the other functions of this module together .
#Input:
# incomingLinksDict - a dictionary containing each URL as keys and every incoming link of each URL as values of the dictionary.
#Returns the Page ranking of every URL.
def pagerank(incomingLinksDict):
    idMap = idMapping(incomingLinksDict)
    matrix = createMatrix(idMap,incomingLinksDict)
    pageranking = finalVector(matrix)
    return pageranking

#This function maps each page to an integer value, this makes it easier to create a matrix if every page is represented numerically.
#Input:
# incomingLinksDict - A dictionary containing each URL as keys and every incoming link of each URL as values of the dictionary.
#Returns a dictionary with integers from 0 to N-Pages as keys and the page's URL as values.
def idMapping(incomingLinksDict):
    fileID = {}
    count = 0
    for key in incomingLinksDict:
        fileID[count] = key
        count += 1
    return fileID

#This functions sets up a 2d matrix and calculates the likelihood of jumping to all other pages from a certain page.
#Input:
# idMap - mapping form idMapping.
# incomingLinksDict - same incomingLinksDict dictionary to determine if a page is contained within another.
#Returns a 2d matrix representing the likelihood of a random surfer jumping to a any page from each page.
def createMatrix(idMap, incomingLinksDict):
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

#This function repeats the dot product multiplication function until the euclidian distance between the vector is really small.
#Input:
# matrix - calculated in createMatrix.
#Returns a vector with the random probability of a random surfer ending up on each page (the index of the vector represents each link within the fileMAP).
def finalVector(matrix):
    threshhold = 0.0001
    dist = 1
    oldVector = [[]]
    for i in range(len(matrix)):
        oldVector[0].append(0)
    oldVector[0][1] = 1
    newVector = [dotProduct(matrix,oldVector)]
    while dist > threshhold: 
        newVector = [dotProduct(matrix,newVector)]
        dist = matmult.euclidean_dist(newVector, oldVector)
        oldVector = newVector
    return newVector
    
#Performs the matrix and vector dot product multiplication
#Input:
# matrix
# vector
#Returns the result of the dot product between the matrix and vector
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