#reads 'battlefield' named file
f=open('C:\\Users\\fırat\\Desktop\\battlefield.txt', 'r')
readLine= f.readlines()
f.close()

#creates 2 dictionaries, first holds the given configuration
#of the board, second holds the current board configuration
#that is modified during the game.
defaultDict = dict()
currentDict = dict()
count = 0

#dictionaries are created, each holds 64 keys and values, 1 for
#each location in the board.
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
for line in readLine:
    for i in range(len(line)):
        if i%2==0:
            defaultDict[letters[count] + str(int(i/2+1))] = line[i]
            currentDict[letters[count] + str(int(i/2+1))] = 'O'
    count+=1

#prints the board.
def printBoard(board):
    print('\n   1  2  3  4  5  6  7  8')
    for i in range(len(letters)):
        line = letters[i]
        for j in range(8):
            line+='  '+board[str(letters[i]+str(j+1))]
        print(line)

#a dictionary that holds the information about the ships. i.e.
#'B' is for battleship. 'T' is total amount of locations that
#contain a ship part. If 'T'=0, game is won.
ships = {'B' : 4, 'C' : 3, 'D' : 2, 'S' : 1, 'M' : 3, 'T' : 10}

#function to check the ships and print the log of the game.
def checkShips():
    if ships['B'] == 0:
        print('Battleship is sank.')
    elif ships['B'] != 4:
        print('Battleship is damaged.')

    if ships['C'] == 0:
        print('Cruise is sank.')
    elif ships['C'] != 3:
        print('Cruise is damaged.')

    if ships['D'] == 0:
        print('Destroyer is sank.')
    elif ships['D'] != 2:
        print('Destroyer is damaged.')

    if ships['S'] == 0:
        print('Submarine is sank.')
    elif ships['S'] != 1:
        print('Submarine is damaged.')

guesses = 25
print('Welcome to the Battleship game!\nHere is the board:')
printBoard(currentDict)
print('\nYou have ' + str(guesses) + ' remainning guesses.')

#main loop of the game. Keeps going the player has no guesses left or
#all the ships are sank.
while guesses!=0 and ships['T']!=0:

    #gets the input from the user, straightforward.
    inputA = input('\nPlease give a target location: ').upper()
    while ((inputA not in currentDict) or (currentDict[inputA] != 'O')) and inputA != 'GG':
        print('\nInvalid location!\n')
        inputA = input('Please give a VALID location that is NOT yet checked: ').upper()
        
    #if the user wants to terminate the game, we break out of the loop.
    if inputA == 'GG':
        break

    #checks the given board configuration and makes modifications
    #on the current board accordingly. all changes are made to the
    #current dictionary.
    if defaultDict[inputA] == 'O':
        currentDict[inputA] = 'X'
    elif defaultDict[inputA] == 'M':
        currentDict[inputA] = defaultDict[inputA]
        guesses -= 3
    else:
        currentDict[inputA] = defaultDict[inputA]
        ships[defaultDict[inputA]] -= 1
        ships['T'] -= 1
    guesses -= 1
    printBoard(currentDict)
    print('\nYou have ' + str(guesses) + ' remainning guesses.')
    checkShips()

#when the loop is over, all locations of ships and mines are made
#visible in the current dictionary.
for i in letters:
    for j in range(len(letters)):
        if defaultDict[i+str(j+1)] in ships:
            currentDict[i+str(j+1)] = defaultDict[i+str(j+1)]

#prints the board 1 final time. if 'T'=0 at this point, the game
#is won, else it is lost.
printBoard(currentDict)
if (ships['T'] == 0):
    print('\nYou won!')
else:
    print('\nYou lost!')

print('\nGame over, thanks for playing!')

