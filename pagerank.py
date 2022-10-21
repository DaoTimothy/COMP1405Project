
import matmult


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

def idmapping(incominglinksdict):
    fileid = {}
    count=0
    for key in incominglinksdict:
        fileid[count]=key
        count+=1
    return fileid

def creatematrix(idmap,incominglinksdict):
    alpha = 0.1
    matrix=[]
    notcount=0
    yescount=0
    totalpgs=len(idmap)

    #Creates Adjacency row with 1 and 0s ONLY
    for key in idmap:
        row=[]
        sidepage = idmap[key]

        for toprow in range(0,totalpgs):
            toppage= idmap[toprow]#onverts top row number to the page

            #Checks if the sidepage is contained in the incoming links of the top page
            if sidepage in  incominglinksdict[toppage]:
                row.append(1)
                yescount+=1
                notcount=0
            else:
                row.append(0)
                notcount+=1
                if notcount==totalpgs: #Checks if the page had no incoming links, row is all zeros
                    row=[]
                    for i in range(totalpgs):
                        row.append(1/totalpgs)#Can teleport to any page with 1/n probability

        #Initial transition probability matrix (dividing rows by # of 1s):
        for i in range(len(row)):
            if row[i]==1:

                row[i]=1/yescount

        #Scaled Adjacency Matrix (1-alpha * adjacency)
        for i in range(len(row)):
            row[i] = row[i]*(1-alpha)
                
        #Adjacency Matrix after adding alpha/N to each entry
        for i in range(len(row)):
            row[i]=row[i] + alpha/totalpgs

        yescount=0
        notcount=0
        matrix.append(row)
        
    return matrix
        
def dotproduct(matrix,vector):
    newvector=[]
    for column in range(len(vector[0])):
        sum=0
        index=0
        for row in matrix:
            sum+=row[column]*vector[0][index]
            index+=1
        newvector.append(sum)
        
    return newvector

def finalvector(matrix):
    threshhold = 0.0001
    dist=1
    oldvector=[[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
    newvector=[dotproduct(matrix,oldvector)]
    while dist>threshhold: 
        newvector=[dotproduct(matrix,newvector)]
        dist= matmult.euclidean_dist(newvector,oldvector)
        oldvector=newvector
    return newvector
        

def pagerank(incominglinksdict):
    idmap = idmapping(incominglinksdict)
    matrix= creatematrix(idmap,incominglinksdict)
    pageranking = finalvector(matrix)
    return pageranking






