
import numpy as np
from datetime import datetime

HORIZONTAL = -1
VERTICAL = -2


# a function that displays a message on the screen and then exits from the program. 
def exitProg(num):
    messege = ["********** The numbers in the layer are not consecutive !!!",
               "********** The input layer does not meet the requirements !!!"]
    print (messege[num])
    quit()

# a function that returns a Boolean value based on probability
def randomBoolPossibility(probability):
    return np.random.random_sample() < probability


#Generates a random input layer. With size column and row.
def generateRandomInput(column,row):
    seed = int(datetime.utcnow().timestamp())
    np.random.seed(seed)
    probability = 0
    # An empty matrix with the specified dimensions is created
    inputArray = np.full((row,column),0)  
    for y in range(0,row-1,2):
        try :
            # Random number of horizontal bricks are selected
            rand = np.random.choice(a=np.arange(1, int(column/2-1))) # Random number of horizontal bricks are selected
        except:
            rand = 1
        for x in range(column):
            # not divisible by zero
            if column-2-x >= 1:
                dev = column-2-x
            else :
                dev = 1
            # the coefficient must not be greater than 2    
            probability = (1.6*rand) / dev

            # Chooses how to lay the brick. And fills the fields with it
            if randomBoolPossibility(probability) :
                value = HORIZONTAL
            else:
                value = VERTICAL
            if inputArray[y][x] == 0:
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
    inputArray = assignNumber(inputArray)
    return inputArray

# User input interface
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

    print ("Do you want to generate a random layer")
    userInput = input("Yes or No ?")
    if userInput.lower() == "yes" or userInput.lower() == "y":
        inputArray = generateRandomInput(m,n)
        print ("\n*************************************\n - The layer solution is as follows:\n")
        return inputArray

    while True:
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
            # If all the fields are occupied, it exits the loоp
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
    print ("\n*************************************\n - The layer solution is as follows:\n")
    return inputArray

# Prints a layer graphically
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

# Transfers a layer with numbers in the mask of the layer with the orientation of the bricks
def makeMaskArray(mArray):
    maskArray = np.copy(mArray)
    columLen = mArray.shape[1]
    rowLen = mArray.shape[0]
    # Variables are used to keep out of range of the array
    lastColum = columLen-1
    lastRow = rowLen-1

    cells = columLen*rowLen
    sumCells = 0

    # Check the sequence of numbers in the layer
    for x in range (1,int(cells/2)+1):
        sumCells += x
    if np.sum(mArray) != sumCells*2:
        print ("np.sum(mArray) : {0} is not sumCells*2 : {1}".format(np.sum(mArray),sumCells*2))
        exitProg(0)
    
    # Assembling the layer mask
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

    # Check for the correct arrangement of the bricks
    if np.sum(maskArray) != sumCells:
        print ("np.sum(maskArray) : {0} is not sumCells : {1}".format(np.sum(maskArray),sumCells))
        exitProg(0)
    return maskArray

# The solution of the given layer
def solution(sArray):
    solutionArray = np.copy(sArray)
    columLen = sArray.shape[1]
    rowLen = sArray.shape[0]

    # Calculate how many areas 4x2 and 2x2 cover the layer
    segment = [0,0]
    segment[0] = columLen//4
    segment[1] = (columLen - segment[0]*4)//2

    # The layer is divided into areas 4x2 and 2x2
    for y in range(0,rowLen,2):
        for x in range(segment[0]):
            y_start = y
            y_stop = y+2
            x_start = x*4
            x_stop = (x+1)*4
            # The sum of each zone and sub-zone is calculated
            cell4 = solutionArray[y_start:y_stop,x_start:x_stop]
            cell2 = solutionArray[y_start:y_stop,x_start:x_stop-2]
            cellsum4 = np.sum(cell4)
            cellsum2 = np.sum(cell2)

            # Based on the calculations, a decision is made about the arrangement of the bricks
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
            if cellsum4 == -14 and cellsum2 == -6:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2,-1,-1],[-2,-2,-1,-1]]
            if cellsum4 == -16:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1,-1,-1],[-1,-1,-1,-1]]

        for x in range(segment[1]):
            y_start = y
            y_stop = y+2
            x_start = segment[0]*4 + x*2
            x_stop = segment[0]*4 + (x+1)*2
            # The sum of each zone and sub-zone is calculated
            cell2 = solutionArray[y_start:y_stop,x_start:x_stop]
            cell1 = solutionArray[y_start:y_stop,x_start:x_stop-1]
            cellsum2 = np.sum(cell2)
            cellsum1 = np.sum(cell1)
            # Based on the calculations, a decision is made about the arrangement of the bricks
            if cellsum2 == -4:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2],[-2,-2]]
            if cellsum2 == -6:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1],[-1,-1]]
            if cellsum2 == -6 and cellsum1 ==-3:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-2,-2],[-2,-2]]
            if cellsum2 == -8:
                solutionArray[y_start:y_stop,x_start:x_stop]=[[-1,-1],[-1,-1]]

    return solutionArray

# Add numbers to a mask layer
def assignNumber(nArray):
    numberArray = np.copy(nArray)
    position = 1

    for y in range(numberArray.shape[0]):
        for x in range(numberArray.shape[1]):
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

# Check if there are bricks with the same numbers on top of each other
# The parameters are:
# cArray- Array with the solution
# iArray - Array with the input layer
# mArray - Mask of the array with the solution
def numberCheck(cArray,iArray,mArray):
    # Variables are used to keep out of range of the array
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


# Launches the user interface
inputArray = userinput()

# Creates an input layer mask
maskInput = makeMaskArray(inputArray)
# Creates a solution mask
maskSolution = solution (maskInput)
# Add numbers to a mask layer
solutionArray = assignNumber(maskSolution)
# Checks if the solution is valid
numberCheck(solutionArray,inputArray,maskSolution)

# Prints the solution to the user
print ("Layer 1")
printArray(inputArray)
print ("Layer 2")
printArray(solutionArray)


