import numpy as np

def randomBoolPossibility(probability):
    return np.random.random_sample() < probability

def generateRandomInput(row,comum,seed):

    if row % 2 == 1 or comum % 2 == 1:
        print ("Dimension (a or b) of generateRandomInput are not even numbers!")
        quit()

    np.random.seed(seed)
    probability = 0
    inputArray =  np.full ((comum,row),-1)
    for y in range(0,comum-1,2):
        try :
            rand = np.random.choice(a=np.arange(1, int(row/2-1)))
        except:
            rand = 1
        for x in range(row):

            if row-2-x >= 1:
                dev = row-2-x
            else :
                dev = 1
            probability = (1.6*rand) / dev

            value = randomBoolPossibility(probability)
            if inputArray[y][x] == -1:
                inputArray[y][x] = value
                if value == False:
                    inputArray[y+1][x] = value
                if value == True:
                   inputArray[y][x+1] = value
                   inputArray[y+1][x] = value
                   inputArray[y+1][x+1] = value
                   rand -= 1
                else:
                    pass
            else:
                pass
    return inputArray

def assignNumber(inputArray):
    position = 1
    enableTruePass = 0
    enableFalsePass = 0
    if inputArray [0][0] == True:
        enableTruePass = True
    if inputArray [0][0] == False:
        enableFalsePass = True


    for y in range(inputArray.shape[0]):
        for x in range(inputArray.shape[1]):
            if y == 0 and x == 1 and enableTruePass:
                enableTruePass == False
                continue
            if y == 1 and x == 0 and enableFalsePass:
                enableFalsePass == False
                continue
            if inputArray [y][x] == 1:
                inputArray [y][x] = position
                inputArray [y][x+1] = position
                position += 1
            if inputArray [y][x] == 0:
                inputArray [y][x] = position
                inputArray [y+1][x] = position
                position += 1
            else:
                continue
    return inputArray

def makeMask(inputArray):
    enableNextXPass = False
    enableNextYPass = False
    enableTruePass = False
    enableFalsePass = False
    if inputArray [0][0] == inputArray [0][1]:
        enableTruePass = True
    if inputArray [0][0] == inputArray [1][0]:
        inputArray [0][0] = 0
        inputArray [1][0] = 0
        enableFalsePass = True


    for y in range(inputArray.shape[0]):
        enableNextXPass = False
        for x in range(inputArray.shape[1]):

            if y == 0 and x == 1 and enableTruePass:
                enableTruePass == False
                continue
            if y == 1 and x == 0 and enableFalsePass:
                enableFalsePass == False
                continue

            if enableNextXPass:
                enableNextXPass = False
                continue

            if inputArray.shape[1] - 1 - x == 0:
                enableNextXPass = True
            else :
                enableNextXPass = False
            if inputArray.shape[0] - 1 - y == 0:
                enableNextYPass = True
            else :
                enableNextYPass = False


            if enableNextXPass == False and inputArray [y][x] > 1 and inputArray [y][x] == inputArray [y][x+1]:
                inputArray [y][x] = 1
                inputArray [y][x+1] = 1
                enableNextXPass = True

            if enableNextYPass == False and inputArray [y][x] > 1 and inputArray [y][x] == inputArray [y+1][x]:
                inputArray [y][x] = 0
                inputArray [y+1][x] = 0
                     
            # print ("{0} / {1}".format(x,y))
            # print (inputArray)
            
    return inputArray

def invertNumInputArr(inputArray):
    invInputArray =  np.full ((inputArray.shape[0],inputArray.shape[1]),0)
    for y in range(inputArray.shape[0]):
        for x in range(inputArray.shape[1]):
            inputArray [y][x] = np.negative(inputArray [y][x])
    return inputArray

def solution(inputArray):
    invNumInputArr = invertNumInputArr(inputArray)

    position = 1
    positions = []
    missingPositions = []

    for y in range(inputArray.shape[0]):
        for x in range(inputArray.shape[1]):

            if inputArray.shape[1] - 1 - x == 0:
                enableNextXPass = True
            else :
                enableNextXPass = False
            if inputArray.shape[0] - 1 - y == 0:
                enableNextYPass = True
            else :
                enableNextYPass = False


            if enableNextXPass == False and invNumInputArr [y][x] < 0 and invNumInputArr [y][x] == invNumInputArr [y][x+1]:
                if np.negative(invNumInputArr[y][x]) == position:
                    if len(missingPositions) > 0:
                        position=missingPositions.pop()
                    else :
                        position += 1
                inputArray [y][x] = position
                inputArray [y+1][x] = position
                positions.append(position)
                

            if enableNextYPass == False and invNumInputArr [y][x] < 0 and invNumInputArr [y][x] == invNumInputArr [y+1][x]:
                if np.negative(invNumInputArr[y][x]) == position:
                    if len(missingPositions) > 0:
                        position=missingPositions.pop()
                    else :
                        position += 1
                inputArray [y][x] = 0
                inputArray [y][x+1] = 0
                enableNextXPass = True
            
    return inputArray



x = 2
maskInputArr = generateRandomInput(x*4,x*2,int(x*6*np.random.random_sample()))
# print (maskInputArr)
numInputArr = assignNumber(maskInputArr)
print ("Input Array :")
print (numInputArr)
# invNumInputArr = invertNumInputArr(numInputArr)
# print(numInputArr)
# maskOutputArr = makeMask(numInputArr)
# print (maskOutputArr)
solutionArr = solution(numInputArr)
print ("solution Array :")
print (solutionArr)