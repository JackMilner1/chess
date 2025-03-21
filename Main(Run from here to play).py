####################################################################################
#################################### CHESS GAME ####################################
####################################################################################

#-------------------------------------- SETUP --------------------------------------
import Engine
import random
import File_handler as FileHandler
import UI_Handler as UI
import math
import Settings.PROJECT_SETTINGS as settings
#------------------------------------ FUNCTIONS ------------------------------------

CONSOLE_APPLICATION = settings.isConsoleApplication()

def startGame():
    # main loop of program

    Engine.precomputeSquaresToEdge()
    colour,playerTurn,newBoard,castlingData,enPassant = FileHandler.load(FileHandler.gameConfig()) # loads new game or previous game
    enemyColour = Engine.assignColours(colour)
    Engine.convertToBitBoard(newBoard,castlingData,enPassant)

    if not CONSOLE_APPLICATION:
        import MainMenuPage
    else:
        UI.clear()
        UI.mainMenuUI()
        UI.starterGameInfo(colour)
        UI.drawBoard(None)

        resigning = False

        while True:
            if Engine.Checkmate:
                UI.clear()
                if playerTurn:
                    UI.winLossUI(True)
                else:
                    UI.winLossUI(False)
                UI.sleep(10)
                print("\n\nReturning To Menu...")
                UI.load()
                startGame()
                break
            else:
                if resigning:
                    UI.clear()
                    print("thanks for playing!!")
                    break
                elif playerTurn:
                    resigning = playersTurn(colour)
                    playerTurn = False
                else:
                    AITurn(enemyColour)
                    playerTurn = True

            UI.clear()
            UI.drawBoard(None)


## all code below is only used in the console version of this application and isnt seen by the user

def playersTurn(colour):
    valid = False
    while not valid:
        square,isResigning = selectPiece(colour) 

        if not isResigning:
            legalMoves = Engine.filterMovesBySquare(int(math.log(square,2)),colour)
            valid = len(legalMoves) > 0
            if valid:
                chosenLegalMove = selectDestination(square,legalMoves,UI.createOverlay(legalMoves))
                Engine.makeMove(square,int(math.pow(2,chosenLegalMove)),colour,False,None)
                return False
            else:
                print("\nThis piece cant move, try again")
                UI.sleep(1.5)
        else:
            valid = True
            return True
    
def AITurn(colour):
    '''moves = Engine.generateAllMoves(colour,False)
    chosenMove,extraInfo,eval = Engine.search(moves,colour)
    UI.sleep(2)
    if chosenMove != None:
        Engine.makeMove(int(math.pow(2,chosenMove[0])),int(math.pow(2,chosenMove[1])),colour,False,extraInfo)'''
    
    moves = Engine.generateAllMoves(colour,False)
    #chosenMove,extraInfo,eval = Engine.search(moves,colour)
    #chosenMove,extraInfo,newEvaluation = Engine.search(moves,colour,1,1)
    #newEvaluation,chosenMove = Engine.searchv2(2,colour)
    #print(Engine.search(moves,colour,1,1))
    #chosenMove,extraInfo = Engine.searchWithDepth(2,colour,moves)
    bestOpponentEval,chosenMove,extraInfo = Engine.searchv3(colour,[],2)
    Engine.makeMove(int(math.pow(2,chosenMove[0])),int(math.pow(2,chosenMove[1])),colour,False,extraInfo)    
    UI.sleep(2)

def validCoordinates(coordinates):
    return len(coordinates) == 2 and coordinates[0].lower() in ['a','b','c','d','e','f','g','h'] and coordinates[1] in ['1','2','3','4','5','6','7','8']

def coordinatesToBinary(coordinates):
    file = ord(coordinates[0].lower()) - 97
    rank = 8 - int(coordinates[1])
    currentSquareIndex = (rank * 8) + file
    currentSquareInBinary = int(math.pow(2,currentSquareIndex))
    return currentSquareInBinary

def selectPiece(colour):
    chosenCoordinates = "XX"
    currentSquareInBinary = None
    while Engine.getColour(currentSquareInBinary) != colour:
        chosenCoordinates = "XX"
        while not validCoordinates(chosenCoordinates):
            UI.clear()
            UI.drawBoard(None)
            chosenCoordinates = input("\n\nEnter the coordinates on the chess board (such as A8,a8,b5 etc...) of the piece you would like to move or type 'resign' to resign\n\nInput: ")
            if chosenCoordinates == "resign":
                return None, True
        currentSquareInBinary = coordinatesToBinary(chosenCoordinates)
    return currentSquareInBinary,False

def selectDestination(square,legalMoves,overlay):
    chosenCoordinates = "XX"
    currentSquareInBinary = None
    legal = False
    while not legal:
        chosenCoordinates = "XX"
        UI.clear()
        UI.drawBoard(overlay)

        while not validCoordinates(chosenCoordinates):
            chosenCoordinates = input(f"\n\nEnter a legal location to move the {Engine.getPieceTypeFromSquare(square)} too\n\nInput: ")
            
        currentSquareInBinary = coordinatesToBinary(chosenCoordinates)
    
        for move in legalMoves:
            if move[1] == int(math.log(currentSquareInBinary,2)):
                legal = True

    return int(math.log(currentSquareInBinary,2))

startGame()

