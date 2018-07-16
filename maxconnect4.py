#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *

def oneMoveGame(currentGame, outFile, userDepth):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay(userDepth)
    
    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore(currentGame.gameBoard)
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    
    
#     currentGame.gameFile = outFile
#     currentGame.gameFile = open(outFile,'w')
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()



def interactiveGame(currentGame, turn, userDepth):
    # Fill me in
    
    if turn == 'computer-next':
        print turn
        currentGame.currentTurn = 1
    elif turn == 'human-next':
        print turn
        currentGame.currentTurn = 2
    while(True):
        if currentGame.currentTurn == 1:
            print "\n inside computer"     
            currentGame.gameFile = open('computer.txt','w')
            currentGame.printGameBoard()
            currentGame.countScore(currentGame.gameBoard)
            print "Player 1 Score =",currentGame.player1Score, "\tPlayer 2 Score =",currentGame.player2Score
            if currentGame.pieceCount == 42:
                print "No more moves left"
                break
            else:
                print "computer played"
                currentGame.aiPlay(userDepth)
                currentGame.printGameBoard()
                
                currentGame.countScore(currentGame.gameBoard)         
                currentGame.printGameBoardToFile()
                currentGame.currentTurn = 2
            currentGame.gameFile.close()
                
        elif currentGame.currentTurn == 2:
            flag = True
            print "\n inside human"
            currentGame.gameFile = open('human.txt','w')
            currentGame.printGameBoard()
            currentGame.countScore(currentGame.gameBoard)
            print "Player 1 Score =",currentGame.player1Score, "\tPlayer 2 Score =",currentGame.player2Score
            if currentGame.pieceCount == 42:
                print "No more moves left"
                break
            else:
                humanMove = int(raw_input("Make your move, Enter any column number from 0 to 6"))
                print "human move :",humanMove
                if humanMove not in range(0,7):
                    print "Invalid Move"
                    continue
                for row in range(5,-1,-1):
                    if not currentGame.gameBoard[row][humanMove]:
                        flag = False
                        pass
                if flag:
                    print "Column is Full, Invalid input"
                    continue
                print "Human played"
                currentGame.playPiece(humanMove)
                currentGame.printGameBoard()
                currentGame.countScore(currentGame.gameBoard)
                currentGame.printGameBoardToFile()
                currentGame.currentTurn = 1
            currentGame.gameFile.close()
                
    currentGame.countScore(currentGame.gameBoard)
    winner = currentGame.player1Score - currentGame.player2Score
    if(winner > 0):
        print "\nPlayer 1 Won!!!"
    elif(winner < 0):
        print "\nPlayer 2 Won!!!"
    elif(winner == 0):
        print "\nMatch Draw!!!"
    
    sys.exit()


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
 
    game_mode, inFile = argv[1:3]
 
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
 
    currentGame = maxConnect4Game() # Create a game
 
    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")
 
    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()
 
    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()
 
    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore(currentGame.gameBoard)
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
 
    if game_mode == 'interactive':
        turn = argv[3]
        userDepth = argv[4]
#         currentGame.gameFile = argv[2]
        if not turn == 'computer-next' and not turn == 'human-next':
            print "Unrecognized Player\nEnter either 'computer-next' or 'human-next'"
            sys.exit()
        interactiveGame(currentGame,turn,userDepth) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        inputFile = argv[2]
        userDepth = argv[4]
        try:
            currentGame.gameFile = open(outFile, 'w')
#             currentGame.gameFile = open(inputFile, 'r')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame,outFile, userDepth) # Be sure to pass any other arguments from the command line you might need.


 
if __name__ == '__main__':
    main(sys.argv)

# currentGame = maxConnect4Game() # Create a game
# # 
# #     # Try to open the input file
# try:
#     currentGame.gameFile = open('input4.txt', 'r')
# except IOError:
#     sys.exit("\nError opening input file.\nCheck file name.\n")
#     
# file_lines = currentGame.gameFile.readlines()
# currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
# currentGame.currentTurn = int(file_lines[-1][0])
# currentGame.gameFile.close()
# interactiveGame(currentGame, "computer-next", 5)


