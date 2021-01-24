
import numpy as np
HORIZONTAL = -1
VERTICAL = -2

def exitProg(num):
    messege = ["********** The numbers in the layer are not consecutive !!!",
               "********** The input layer does not meet the requirements !!!"]
    print (messege[num])
    quit()

def randomBoolPossibility(probability):
    return np.random.random_sample() < probability


# Generates a random input mask matrix.
# Where 1 is a horizontal brick, 0 is a vertical brick
def generateRandomInput(row,comum,seed):

    np.random.seed(seed)
    probability = 0
    inputArray = np.full((comum,row),-1)  # An empty matrix with the specified dimensions is created
    for y in range(0,comum-1,2):
        try :
            rand = np.random.choice(a=np.arange(1, int(row/2-1))) # Random number of horizontal bricks are selected
        except:
            rand = 1
        for x in range(row):

            if row-2-x >= 1:
                dev = row-2-x
            else :
                dev = 1
            probability = (1.6*rand) / dev

            if randomBoolPossibility(probability) :
                value = HORIZONTAL
            else:
                value = VERTICAL
            if inputArray[y][x] == -1:
                inputArray[y][x] = value
                if value == VERTICAL:
                    inputArray[y+1][x] = value
                if value == HORIZONTAL:
                   inputArray[y][x+1] = value
                   inputArray[y+1][x] = value
                   inputArray[y+1][x+1] = value
                   rand -= 1
                else:
                    pass
            else:
                pass
    return inputArray

def userinput():
    print ("\nMENTORMATE\nBrickwork Assignment\nDaniel Dimitrov\n\n")
    while True:
        print ("Please enter input layer size M and N separated by commas.\nM and N must be even number. M must be greater than N.")
        try :
            userInput = input("Еxample \"6,4\" :").split(",")
            m, n = int(userInput[0]), int(userInput[1])
            if m>n and m%2==0 and n%2==0:
                break
            else :
                print ("********** M and N do not meet the requirements!\n")
        except:
            pass
    print ("\n")
    inputArray = np.full((n,m),-1)
    row = 0
    while True:

        print ("Do you want to generate a random layer")
        userInput = input("Yes or No ?")
        if userInput.lower() == "yes" or userInput.lower() == "y":
            inputArray = generateRandomInput(m,n,10)
            break


        print ("Please enter {0} numbers less than 100 separated by commas for {1} row.".format(m,row+1))
        try :
            userInput = input("Еxample \"1,1,2,3,3,4\", start from 1 :").split(",")
            if len(userInput) != m:
                print ("********** Input are not equal to M!\n")
                continue
            for num in range(0, len(userInput)):
                userInput[num] = int(userInput[num])
                if userInput[num] > 99:
                    userInput[num] = -1
            num = 0
            if not -1 in userInput:
                inputArray[row,:] = userInput
                printArray(inputArray)
                row += 1
            else :
                print ("********** Same Input numbers are more then 99.\n")
            if not -1 in inputArray:
                break
            else :
                pass
        except:
            print ("********** Input are not meet the requirements!\n")
    return inputArray

def printArray(pArray):
    columLen = pArray.shape[1]
    rowLen = pArray.shape[0]
    row = 0
    line = ""
    for row in range (rowLen):
        line = "+"
        for z in range (columLen):
            line += "------+"
        print (line)
        line = ""
        for z in range (columLen):
            if pArray[row][z] >= 0 and pArray[row][z] < 10:
                line += "|  {0}   ".format(pArray[row][z])
            else :
                line += "|  {0}  ".format(pArray[row][z])
        line += "|"
        print (line)
    line = "+"
    for z in range (columLen):
        line += "------+"
    print (line)

def makeMaskArray(mArray):
    maskArray = np.copy(mArray)
    columLen = mArray.shape[1]
    rowLen = mArray.shape[0]
    lastColum = columLen-1
    lastRow = rowLen-1
    cells = columLen*rowLen
    sumCells = 0
    for x in range (1,int(cells/2)+1):
        sumCells += x
    if np.sum(mArray) != sumCells*2:
        print ("np.sum(mArray) : {0} is not sumCells*2 : {1}".format(np.sum(mArray),sumCells*2))
        exitProg(0)
    sumCells=0
    for y in range(maskArray.shape[0]):
        for x in range(maskArray.shape[1]):
            if maskArray[y][x] > 0:
                if x != lastColum and maskArray[y][x] == maskArray[y][x+1]:
                    maskArray[y][x] = HORIZONTAL
                    maskArray[y][x+1] = HORIZONTAL
                    sumCells -= 2
                if y != lastRow and maskArray[y][x] == maskArray[y+1][x]:
                    maskArray[y][x] = VERTICAL
                    maskArray[y+1][x] = VERTICAL
                    sumCells -= 4
            else:
                pass
    # printArray(maskArray)
    if np.sum(maskArray) != sumCells:
        print ("np.sum(maskArray) : {0} is not sumCells : {1}".format(np.sum(maskArray),sumCells))
        exitProg(0)
    return maskArray

def solution(sArray):
    solutionArray = np.copy(sArray)
    columLen = sArray.shape[1]
    rowLen = sArray.shape[0]
    segment = [0,0]
    segment[0] = columLen//4
    segment[1] = (columLen - segment[0]*4)//2

    for y in range(0,rowLen,2):
        for x in range(segment[0]):
            y_start = y
            y_stop = y+2
            x_start = x*4
            x_stop = (x+1)*4
            cell4 = solutionArray[y_start:y_stop,x_start:x_stop]
            cell2 = solutionArray[y_start:y_stop,x_start:x_stop-2]
            cellsum4 = np.sum(cell4)
            cellsum2 = np.sum(cell2)
            if cellsum4 == -8:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2,-2,-2],[-2,-2,-2,-2]]
            if cellsum4 == -10 and cellsum2 == -6:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1,-2,-2],[-1,-1,-2,-2]]
            if cellsum4 == -10 and cellsum2 == -4:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2,-1,-1],[-2,-2,-1,-1]]
            if cellsum4 == -12 and cellsum2 == -8:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1,-2,-2],[-1,-1,-2,-2]]
            if cellsum4 == -12 and cellsum2 == -6:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1,-1,-1],[-1,-1,-1,-1]]
            if cellsum4 == -12 and cellsum2 == -4:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2,-1,-1],[-2,-2,-1,-1]]
            if cellsum4 == -14:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1,-1,-1],[-1,-1,-1,-1]]
            if cellsum4 == -16:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-1,-1,-2],[-2,-1,-1,-2]]

        for x in range(segment[1]):
            y_start = y
            y_stop = y+2
            x_start = segment[0]*4 + x*2
            x_stop = segment[0]*4 + (x+1)*2
            cell = sArray[y_start:y_stop,x_start:x_stop]
            cellsum = np.sum(cell)
            if cellsum == -4:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2],[-2,-2]]
            if cellsum == -6:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1],[-1,-1]]
            if cellsum == -8:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1],[-1,-1]]

    return solutionArray

def assignNumber(nArray):
    numberArray = np.copy(nArray)
    position = 1
    enableHorPass = False
    enableVerPass = False
    if numberArray [0][0] == HORIZONTAL:
        enableHorPass = True
    if numberArray [0][0] == VERTICAL:
        enableVerPass = True


    for y in range(numberArray.shape[0]):
        for x in range(numberArray.shape[1]):
            if y == 0 and x == 1 and enableHorPass:
                enableHorPass == False
                continue
            if y == 1 and x == 0 and enableVerPass:
                enableVerPass == False
                continue
            if numberArray [y][x] == HORIZONTAL:
                numberArray [y][x] = position
                numberArray [y][x+1] = position
                position += 1
            if numberArray [y][x] == VERTICAL:
                numberArray [y][x] = position
                numberArray [y+1][x] = position
                position += 1
            else:
                continue
    return numberArray

def numberCheck(cArray,iArray,mArray):
    lastColum = cArray.shape[1]-1
    lastRow = cArray.shape[0]-1
    for y in range(cArray.shape[0]):
        for x in range(cArray.shape[1]):
            if cArray [y][x] == iArray [y][x]:
                if x != lastColum and mArray[y][x] == HORIZONTAL:
                    if cArray [y][x] == cArray [y][x+1] and cArray [y][x+1] == iArray [y][x+1]:
                        print ("Same numbers : {0} on poition {1}/{2},{3}/{4} - {5}".format(cArray [y][x], x,y,x+1,y,mArray[y][x]))
                    if x > 0 and cArray [y][x] == cArray [y][x-1] and cArray [y][x-1] == iArray [y][x-1]:
                        print ("Same numbers : {0} on poition {1}/{2},{3}/{4} - {5}".format(cArray [y][x], x,y,x+1,y,mArray[y][x]))
                if y != lastRow and mArray[y][x] == VERTICAL:
                    if cArray [y][x] == cArray [y+1][x] and cArray [y+1][x] == iArray [y+1][x]:
                        print ("Same numbers : {0} on poition {1}/{2},{3}/{4} - {5}".format(cArray [y][x], x,y,x+1,y,mArray[y][x]))
                    if y > 0 and cArray [y][x] == cArray [y-1][x] and cArray [y-1][x] == iArray [y-1][x]:
                        print ("Same numbers : {0} on poition {1}/{2},{3}/{4} - {5}".format(cArray [y][x], x,y,x+1,y,mArray[y][x]))



# testYes1 = np.array([[1,1,2,3],[4,4,2,3],[5,6,7,7],[5,6,8,8]])
# testYes2 = np.array([[2,1,1,4],[2,3,3,4]])
# testYes3 = np.array([[1,1,2,3,4,4,5,6,7,7,8,9,10,10,11,12,13,13,14,15,16,16],
#                 [17,17,2,3,18,18,5,6,19,19,8,9,20,20,11,12,21,21,14,15,22,22],
# [23,24,24,25,27,28,28,30,30,32,33,33,36,37,35,35,39,40,40,42,42,44],
# [23,26,26,25,27,29,29,31,31,32,34,34,36,37,38,38,39,41,41,43,43,44]])
# testNo1 = np.array([[1,2,3,4],[4,3,2,1],[5,6,7,8],[8,7,6,5]])

# inputArray = generateRandomInput(10,4,10)
# printArray(inputArray)
# inputArray = assignNumber(inputArray)
# printArray(inputArray)


inputArray = userinput()

maskInput = makeMaskArray(inputArray)
maskSolution = solution (maskInput)
solutionArray = assignNumber(maskSolution)
numberCheck(solutionArray,inputArray,maskSolution)

print ("Layer 1")
printArray(inputArray)
print ("Layer 2")
printArray(solutionArray)


