#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

from copy import copy, deepcopy
import random
import sys
# from test.test_bufio import lengths


class maxConnect4Game:
    
    depth = 0;
    actionValuesFirstMin = []
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    def checkPieceCountTempState(self, tempstate):
        self.pieceCount = sum(1 for row in tempstate for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'
        
    def printGameBoardNextState(self, tempstate):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % tempstate[i][j]),
            print '| '
        print ' -----------------'


    # Output current game status to file
    def printGameBoardToFile(self):
        
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
 
    def alphaBeta(self,userDepth):
#         utility will be the scores of each player...
#         for player1(comp)--> max and utility values  = +ve scores
#         for player1(human)--> min and utility values  = -ve scores
#         Returns Column number
        maxConnect4Game.actionValuesFirstMin = []
#         print "actionValuesFirstMin: ",maxConnect4Game.actionValuesFirstMin
        state = self.gameBoard
        alpha = -sys.maxint - 1
        beta = sys.maxint
        
        action, var = self.MaxValue(state,alpha,beta,userDepth)
        finalmax=max(maxConnect4Game.actionValuesFirstMin)
        indexaction = maxConnect4Game.actionValuesFirstMin.index(finalmax)
        return int(indexaction)
    
    def MaxValue(self,state,alpha,beta,userDepth):
        maxConnect4Game.depth += 1
        self.currentTurn = 1;

        if self.TerminalTest(state,userDepth):            
#             self.printGameBoardNextState(state)
            self.countScore(state)
            utility = 10*(self.player1Score - self.player2Score)
            maxConnect4Game.depth -= 1
            return 0, utility
        
        if (int(maxConnect4Game.depth) == int(userDepth)):
            utility = self.Eval(state)
            maxConnect4Game.depth -= 1
            return 0, utility
        
        var = -sys.maxint - 1
        
#         self.printGameBoardNextState(state)
        nextState = self.Succesor(state)
        for action, tempstate in nextState:
            if maxConnect4Game.depth == 1:
                i = len(maxConnect4Game.actionValuesFirstMin);
                for j in range(i,action):
                    maxConnect4Game.actionValuesFirstMin.append(-sys.maxint -1)
#                     print maxConnect4Game.actionValuesFirstMin
                    
#             self.printGameBoardNextState(tempstate)
            listOfActionAndValue = self.MinValue(tempstate,alpha,beta,userDepth)
            minVar = listOfActionAndValue[1]
            self.currentTurn = 1;
#             self.printGameBoardNextState(state)
#             self.printGameBoardNextState(tempstate)
            var = max(var, minVar)
            
            if var >= beta:
                maxConnect4Game.depth -= 1
                return [action, var]
            alpha = max(alpha, var)
               
        maxConnect4Game.depth -= 1
        return [action, var];    
    
    def MinValue(self,state,alpha,beta,userDepth):
        self.currentTurn = 2;
        maxConnect4Game.depth += 1
        
        if self.TerminalTest(state,userDepth):
            self.countScore(state)
            utility = 10*(self.player1Score - self.player2Score)
            maxConnect4Game.depth -= 1
            return 0, utility
        
        if (int(maxConnect4Game.depth) == int(userDepth)):
            utility = self.Eval(state)
            maxConnect4Game.depth -= 1
            return 0, utility
        
        
        var = sys.maxint
        nextState = self.Succesor(state)
        
        for action, tempstate in nextState:            
            listOfActionAndValue = self.MaxValue(tempstate,alpha,beta,userDepth)
            maxVar = listOfActionAndValue[1]
            self.currentTurn = 2;                                    
            var = min(var, maxVar)
            
            if var <= alpha:
                if maxConnect4Game.depth == 2:
                    maxConnect4Game.actionValuesFirstMin.append(var)
                maxConnect4Game.depth -= 1
                return [action, var]
            beta = min(alpha, var)
            
        # APPENDS THE VALUES OF THE POSSIBLE STATES OF DEPTH 2    
        if maxConnect4Game.depth == 2:            
            maxConnect4Game.actionValuesFirstMin.append(var)    
#             print  maxConnect4Game.actionValuesFirstMin
        maxConnect4Game.depth -= 1        
        return [action, var];
    
    def Succesor(self,state):
    # Returns a list of all 7 possible states and col in which number is inserted
        
        nextState = []        
        tempState = deepcopy(state)
        for col in range(0,7):
            flag = True
            for row in range(5,-1,-1):
                if not state[row][col]:
                    tempState[row][col] = self.currentTurn
                    # updation of piece count not needed
                    nextState.append([col,deepcopy(tempState)])
                    tempState[row][col] = 0
                    flag = False
                    break                        
                    
        self.pieceCount += 1
        return nextState    
        
    def TerminalTest(self, tempstate, depth):
    # Terminal test
        self.checkPieceCountTempState(tempstate)
        if self.pieceCount == 42:
            return True
        else: return False
        
    def Eval(self, tempState):
    # Calculates the scores Appropriately
        count1_2 = 0;count1_3 = 0; count1_4 = 0;
        count2_2 = 0; count2_3 = 0; count2_4 = 0;
        utility = 0
        
        
        for row in tempState:
            
            # check 3 together
            
            # Check player 1
            if (row[0:3] == [1]*3 and row[3] == 0) or (row[1:4] == [1]*3 and row[0] == 0):
                count1_3 += 1
            if ((row[1:4] == [1]*3 and row[4] == 0) or (row[2:5] == [1]*3 and row[1] == 0)):
                count1_3 += 1
            if ((row[2:5] == [1]*3 and row[5] == 0) or (row[3:6] == [1]*3 and row[2] == 0)):
                count1_3 += 1
            if ((row[3:6] == [1]*3 and row[6] == 0) or (row[4:7] == [1]*3 and row[3] == 0)):
                count1_3 += 1
            # Check player 2
            if (row[0:3] == [2]*3 and row[3] == 0) or (row[1:4] == [2]*3 and row[0] == 0):
                count2_3 += 1
            if ((row[1:4] == [2]*3 and row[4] == 0) or (row[2:5] == [2]*3 and row[1] == 0)):
                count2_3 += 1
            if ((row[2:5] == [2]*3 and row[5] == 0) or (row[3:6] == [2]*3 and row[2] == 0)):
                count2_3 += 1
            if ((row[3:6] == [2]*3 and row[6] == 0) or (row[4:7] == [2]*3 and row[3] == 0)):
                count2_3 += 1
        
            # check 2 together
            
            if (row[0:2] == [1]*2 and row[2:4] == 0) or (row[2:4] == [1]*2 and row[0:2] == 0):
                count1_3 += 1
            if ((row[1:3] == [1]*2 and row[3:5] == 0) or (row[3:5] == [1]*2 and row[1:3] == 0)):
                count1_3 += 1
            if ((row[2:4] == [1]*2 and row[4:6] == 0) or (row[4:6] == [1]*2 and row[2:4] == 0)):
                count1_3 += 1
            if ((row[3:5] == [1]*2 and row[5:7] == 0) or (row[5:7] == [1]*2 and row[3:5] == 0)):
                count1_3 += 1
            # Check player 2
            if (row[0:3] == [2]*2 and row[2:4] == 0) or (row[2:4] == [2]*2 and row[0:2] == 0):
                count2_3 += 1
            if ((row[1:4] == [2]*2 and row[3:5] == 0) or (row[3:5] == [2]*2 and row[1:3] == 0)):
                count2_3 += 1
            if ((row[2:5] == [2]*2 and row[4:6] == 0) or (row[4:6] == [2]*2 and row[2:4] == 0)):
                count2_3 += 1
            if ((row[3:6] == [2]*2 and row[5:7] == 0) or (row[5:7] == [2]*2 and row[3:5] == 0)):
                count2_3 += 1
        
                                
        for j in range(7):
            
            if (tempState[0][j] == 0 and tempState[1][j] == 1 and
                   tempState[2][j] == 1 and tempState[3][j] == 1):
                count1_3 += 1
            if (tempState[1][j] == 0 and tempState[2][j] == 1 and
                   tempState[3][j] == 1 and tempState[4][j] == 1):
                count1_3 += 1
            if (tempState[2][j] == 0 and tempState[3][j] == 1 and
                   tempState[4][j] == 1 and tempState[5][j] == 1):
                count1_3 += 1
            # Check player 2
            if (tempState[0][j] == 0 and tempState[1][j] == 2 and
                   tempState[2][j] == 2 and tempState[3][j] == 2):
                count2_3 += 1
            if (tempState[1][j] == 0 and tempState[2][j] == 2 and
                   tempState[3][j] == 2 and tempState[4][j] == 2):
                count2_3 += 1
            if (tempState[2][j] == 0 and tempState[3][j] == 2 and
                   tempState[4][j] == 2 and tempState[5][j] == 2):
                count2_3 += 1
            
            
            # check 2 filled together
            # Check player 1
            if (tempState[0][j] == 0 and tempState[1][j] == 0 and
                   tempState[2][j] == 1 and tempState[3][j] == 1):
                count1_2 += 1
            if (tempState[1][j] == 0 and tempState[2][j] == 0 and
                   tempState[3][j] == 1 and tempState[4][j] == 1):
                count1_2 += 1
            if (tempState[2][j] == 0 and tempState[3][j] == 0 and
                   tempState[4][j] == 1 and tempState[5][j] == 1):
                count1_2 += 1
            # Check player 2
            if (tempState[0][j] == 0 and tempState[1][j] == 0 and
                   tempState[2][j] == 2 and tempState[3][j] == 2):
                count2_2 += 1
            if (tempState[1][j] == 0 and tempState[2][j] == 0 and
                   tempState[3][j] == 2 and tempState[4][j] == 2):
                count2_2 += 1
            if (tempState[2][j] == 0 and tempState[3][j] == 0 and
                   tempState[4][j] == 2 and tempState[5][j] == 2):
                count2_2 += 1            
                        
            
            
        # Check diagonally
        # check for 3 together
        # Check player 1
        if (tempState[2][0] == 1 and tempState[3][1] == 1 and
               tempState[4][2] == 1 and tempState[5][3] == 0):
            count1_3 += 1
        if (tempState[1][0] == 1 and tempState[2][1] == 1 and
               tempState[3][2] == 1 and tempState[4][3] == 0):
            count1_3 += 1
        if (tempState[2][1] == 1 and tempState[3][2] == 1 and
               tempState[4][3] == 1 and tempState[5][4] == 0):
            count1_3 += 1
        if (tempState[0][0] == 1 and tempState[1][1] == 1 and
               tempState[2][2] == 1 and tempState[3][3] == 0):
            count1_3 += 1
        if (tempState[1][1] == 1 and tempState[2][2] == 1 and
               tempState[3][3] == 1 and tempState[4][4] == 0):
            count1_3 += 1
        if (tempState[2][2] == 1 and tempState[3][3] == 1 and
               tempState[4][4] == 1 and tempState[5][5] == 0):
            count1_3 += 1
        if (tempState[0][1] == 1 and tempState[1][2] == 1 and
               tempState[2][3] == 1 and tempState[3][4] == 0):
            count1_3 += 1
        if (tempState[1][2] == 1 and tempState[2][3] == 1 and
               tempState[3][4] == 1 and tempState[4][5] == 0):
            count1_3 += 1
        if (tempState[2][3] == 1 and tempState[3][4] == 1 and
               tempState[4][5] == 1 and tempState[5][6] == 0):
            count1_3 += 1
        if (tempState[0][2] == 1 and tempState[1][3] == 1 and
               tempState[2][4] == 1 and tempState[3][5] == 0):
            count1_3 += 1
        if (tempState[1][3] == 1 and tempState[2][4] == 1 and
               tempState[3][5] == 1 and tempState[4][6] == 0):
            count1_3 += 1
        if (tempState[0][3] == 1 and tempState[1][4] == 1 and
               tempState[2][5] == 1 and tempState[3][6] == 0):
            count1_3 += 1

        if (tempState[0][3] == 1 and tempState[1][2] == 1 and
               tempState[2][1] == 1 and tempState[3][0] == 0):
            count1_3 += 1
        if (tempState[0][4] == 1 and tempState[1][3] == 1 and
               tempState[2][2] == 1 and tempState[3][1] == 0):
            count1_3 += 1
        if (tempState[1][3] == 1 and tempState[2][2] == 1 and
               tempState[3][1] == 1 and tempState[4][0] == 0):
            count1_3 += 1
        if (tempState[0][5] == 1 and tempState[1][4] == 1 and
               tempState[2][3] == 1 and tempState[3][2] == 0):
            count1_3 += 1
        if (tempState[1][4] == 1 and tempState[2][3] == 1 and
               tempState[3][2] == 1 and tempState[4][1] == 0):
            count1_3 += 1
        if (tempState[2][3] == 1 and tempState[3][2] == 1 and
               tempState[4][1] == 1 and tempState[5][0] == 0):
            count1_3 += 1
        if (tempState[0][6] == 1 and tempState[1][5] == 1 and
               tempState[2][4] == 1 and tempState[3][3] == 0):
            count1_3 += 1
        if (tempState[1][5] == 1 and tempState[2][4] == 1 and
               tempState[3][3] == 1 and tempState[4][2] == 0):
            count1_3 += 1
        if (tempState[2][4] == 1 and tempState[3][3] == 1 and
               tempState[4][2] == 1 and tempState[5][1] == 0):
            count1_3 += 1
        if (tempState[1][6] == 1 and tempState[2][5] == 1 and
               tempState[3][4] == 1 and tempState[4][3] == 0):
            count1_3 += 1
        if (tempState[2][5] == 1 and tempState[3][4] == 1 and
               tempState[4][3] == 1 and tempState[5][2] == 0):
            count1_3 += 1
        if (tempState[2][6] == 1 and tempState[3][5] == 1 and
               tempState[4][4] == 1 and tempState[5][3] == 0):
            count1_3 += 1

        # Check player 2
        if (tempState[2][0] == 2 and tempState[3][1] == 2 and
               tempState[4][2] == 2 and tempState[5][3] == 0):
            count2_3 += 1
        if (tempState[1][0] == 2 and tempState[2][1] == 2 and
               tempState[3][2] == 2 and tempState[4][3] == 0):
            count2_3 += 1
        if (tempState[2][1] == 2 and tempState[3][2] == 2 and
               tempState[4][3] == 2 and tempState[5][4] == 0):
            count2_3 += 1
        if (tempState[0][0] == 2 and tempState[1][1] == 2 and
               tempState[2][2] == 2 and tempState[3][3] == 0):
            count2_3 += 1
        if (tempState[1][1] == 2 and tempState[2][2] == 2 and
               tempState[3][3] == 2 and tempState[4][4] == 0):
            count2_3 += 1
        if (tempState[2][2] == 2 and tempState[3][3] == 2 and
               tempState[4][4] == 2 and tempState[5][5] == 0):
            count2_3 += 1
        if (tempState[0][1] == 2 and tempState[1][2] == 2 and
               tempState[2][3] == 2 and tempState[3][4] == 0):
            count2_3 += 1
        if (tempState[1][2] == 2 and tempState[2][3] == 2 and
               tempState[3][4] == 2 and tempState[4][5] == 0):
            count2_3 += 1
        if (tempState[2][3] == 2 and tempState[3][4] == 2 and
               tempState[4][5] == 2 and tempState[5][6] == 0):
            count2_3 += 1
        if (tempState[0][2] == 2 and tempState[1][3] == 2 and
               tempState[2][4] == 2 and tempState[3][5] == 0):
            count2_3 += 1
        if (tempState[1][3] == 2 and tempState[2][4] == 2 and
               tempState[3][5] == 2 and tempState[4][6] == 0):
            count2_3 += 1
        if (tempState[0][3] == 2 and tempState[1][4] == 2 and
               tempState[2][5] == 2 and tempState[3][6] == 0):
            count2_3 += 1

        if (tempState[0][3] == 2 and tempState[1][2] == 2 and
               tempState[2][1] == 2 and tempState[3][0] == 0):
            count2_3 += 1
        if (tempState[0][4] == 2 and tempState[1][3] == 2 and
               tempState[2][2] == 2 and tempState[3][1] == 0):
            count2_3 += 1
        if (tempState[1][3] == 2 and tempState[2][2] == 2 and
               tempState[3][1] == 2 and tempState[4][0] == 0):
            count2_3 += 1
        if (tempState[0][5] == 2 and tempState[1][4] == 2 and
               tempState[2][3] == 2 and tempState[3][2] == 0):
            count2_3 += 1
        if (tempState[1][4] == 2 and tempState[2][3] == 2 and
               tempState[3][2] == 2 and tempState[4][1] == 0):
            count2_3 += 1
        if (tempState[2][3] == 2 and tempState[3][2] == 2 and
               tempState[4][1] == 2 and tempState[5][0] == 0):
            count2_3 += 1
        if (tempState[0][6] == 2 and tempState[1][5] == 2 and
               tempState[2][4] == 2 and tempState[3][3] == 0):
            count2_3 += 1
        if (tempState[1][5] == 2 and tempState[2][4] == 2 and
               tempState[3][3] == 2 and tempState[4][2] == 0):
            count2_3 += 1
        if (tempState[2][4] == 2 and tempState[3][3] == 2 and
               tempState[4][2] == 2 and tempState[5][1] == 0):
            count2_3 += 1
        if (tempState[1][6] == 2 and tempState[2][5] == 2 and
               tempState[3][4] == 2 and tempState[4][3] == 0):
            count2_3 += 1
        if (tempState[2][5] == 2 and tempState[3][4] == 2 and
               tempState[4][3] == 2 and tempState[5][2] == 0):
            count2_3 += 1
        if (tempState[2][6] == 2 and tempState[3][5] == 2 and
               tempState[4][4] == 2 and tempState[5][3] == 0):
            count2_3 += 1
    
            
                
        self.countScore(tempState)
        count1_4 = self.player1Score
        count2_4 = self.player2Score
        
        utility = (10*count1_4 + 6*count1_3 + 3*count1_2) - (10*count2_4 + 6*count2_3 + 3*count2_2)
        return utility
    # The AI section. Currently plays randomly.
    def aiPlay(self,userDepth):
#         randColumn = random.randrange(0,7)
#         result = self.playPiece(randColumn)

        #uses alpha beta and passes the action i.e the column number
        colAlphaBeta = self.alphaBeta(userDepth)
        result = self.playPiece(colAlphaBeta)
        if not result:
            self.aiPlay()
        else:
            self.checkPieceCount()
            print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, colAlphaBeta+1))
            if self.currentTurn == 1:
                self.currentTurn = 2
            elif self.currentTurn == 2:
                self.currentTurn = 1

    # Calculate the number of 4-in-a-row each player has
    def countScore(self,tempstate):
        # tempstate should be of similar to gameboard.
        
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in tempstate:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (tempstate[0][j] == 1 and tempstate[1][j] == 1 and
                   tempstate[2][j] == 1 and tempstate[3][j] == 1):
                self.player1Score += 1
            if (tempstate[1][j] == 1 and tempstate[2][j] == 1 and
                   tempstate[3][j] == 1 and tempstate[4][j] == 1):
                self.player1Score += 1
            if (tempstate[2][j] == 1 and tempstate[3][j] == 1 and
                   tempstate[4][j] == 1 and tempstate[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (tempstate[0][j] == 2 and tempstate[1][j] == 2 and
                   tempstate[2][j] == 2 and tempstate[3][j] == 2):
                self.player2Score += 1
            if (tempstate[1][j] == 2 and tempstate[2][j] == 2 and
                   tempstate[3][j] == 2 and tempstate[4][j] == 2):
                self.player2Score += 1
            if (tempstate[2][j] == 2 and tempstate[3][j] == 2 and
                   tempstate[4][j] == 2 and tempstate[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (tempstate[2][0] == 1 and tempstate[3][1] == 1 and
               tempstate[4][2] == 1 and tempstate[5][3] == 1):
            self.player1Score += 1
        if (tempstate[1][0] == 1 and tempstate[2][1] == 1 and
               tempstate[3][2] == 1 and tempstate[4][3] == 1):
            self.player1Score += 1
        if (tempstate[2][1] == 1 and tempstate[3][2] == 1 and
               tempstate[4][3] == 1 and tempstate[5][4] == 1):
            self.player1Score += 1
        if (tempstate[0][0] == 1 and tempstate[1][1] == 1 and
               tempstate[2][2] == 1 and tempstate[3][3] == 1):
            self.player1Score += 1
        if (tempstate[1][1] == 1 and tempstate[2][2] == 1 and
               tempstate[3][3] == 1 and tempstate[4][4] == 1):
            self.player1Score += 1
        if (tempstate[2][2] == 1 and tempstate[3][3] == 1 and
               tempstate[4][4] == 1 and tempstate[5][5] == 1):
            self.player1Score += 1
        if (tempstate[0][1] == 1 and tempstate[1][2] == 1 and
               tempstate[2][3] == 1 and tempstate[3][4] == 1):
            self.player1Score += 1
        if (tempstate[1][2] == 1 and tempstate[2][3] == 1 and
               tempstate[3][4] == 1 and tempstate[4][5] == 1):
            self.player1Score += 1
        if (tempstate[2][3] == 1 and tempstate[3][4] == 1 and
               tempstate[4][5] == 1 and tempstate[5][6] == 1):
            self.player1Score += 1
        if (tempstate[0][2] == 1 and tempstate[1][3] == 1 and
               tempstate[2][4] == 1 and tempstate[3][5] == 1):
            self.player1Score += 1
        if (tempstate[1][3] == 1 and tempstate[2][4] == 1 and
               tempstate[3][5] == 1 and tempstate[4][6] == 1):
            self.player1Score += 1
        if (tempstate[0][3] == 1 and tempstate[1][4] == 1 and
               tempstate[2][5] == 1 and tempstate[3][6] == 1):
            self.player1Score += 1

        if (tempstate[0][3] == 1 and tempstate[1][2] == 1 and
               tempstate[2][1] == 1 and tempstate[3][0] == 1):
            self.player1Score += 1
        if (tempstate[0][4] == 1 and tempstate[1][3] == 1 and
               tempstate[2][2] == 1 and tempstate[3][1] == 1):
            self.player1Score += 1
        if (tempstate[1][3] == 1 and tempstate[2][2] == 1 and
               tempstate[3][1] == 1 and tempstate[4][0] == 1):
            self.player1Score += 1
        if (tempstate[0][5] == 1 and tempstate[1][4] == 1 and
               tempstate[2][3] == 1 and tempstate[3][2] == 1):
            self.player1Score += 1
        if (tempstate[1][4] == 1 and tempstate[2][3] == 1 and
               tempstate[3][2] == 1 and tempstate[4][1] == 1):
            self.player1Score += 1
        if (tempstate[2][3] == 1 and tempstate[3][2] == 1 and
               tempstate[4][1] == 1 and tempstate[5][0] == 1):
            self.player1Score += 1
        if (tempstate[0][6] == 1 and tempstate[1][5] == 1 and
               tempstate[2][4] == 1 and tempstate[3][3] == 1):
            self.player1Score += 1
        if (tempstate[1][5] == 1 and tempstate[2][4] == 1 and
               tempstate[3][3] == 1 and tempstate[4][2] == 1):
            self.player1Score += 1
        if (tempstate[2][4] == 1 and tempstate[3][3] == 1 and
               tempstate[4][2] == 1 and tempstate[5][1] == 1):
            self.player1Score += 1
        if (tempstate[1][6] == 1 and tempstate[2][5] == 1 and
               tempstate[3][4] == 1 and tempstate[4][3] == 1):
            self.player1Score += 1
        if (tempstate[2][5] == 1 and tempstate[3][4] == 1 and
               tempstate[4][3] == 1 and tempstate[5][2] == 1):
            self.player1Score += 1
        if (tempstate[2][6] == 1 and tempstate[3][5] == 1 and
               tempstate[4][4] == 1 and tempstate[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (tempstate[2][0] == 2 and tempstate[3][1] == 2 and
               tempstate[4][2] == 2 and tempstate[5][3] == 2):
            self.player2Score += 1
        if (tempstate[1][0] == 2 and tempstate[2][1] == 2 and
               tempstate[3][2] == 2 and tempstate[4][3] == 2):
            self.player2Score += 1
        if (tempstate[2][1] == 2 and tempstate[3][2] == 2 and
               tempstate[4][3] == 2 and tempstate[5][4] == 2):
            self.player2Score += 1
        if (tempstate[0][0] == 2 and tempstate[1][1] == 2 and
               tempstate[2][2] == 2 and tempstate[3][3] == 2):
            self.player2Score += 1
        if (tempstate[1][1] == 2 and tempstate[2][2] == 2 and
               tempstate[3][3] == 2 and tempstate[4][4] == 2):
            self.player2Score += 1
        if (tempstate[2][2] == 2 and tempstate[3][3] == 2 and
               tempstate[4][4] == 2 and tempstate[5][5] == 2):
            self.player2Score += 1
        if (tempstate[0][1] == 2 and tempstate[1][2] == 2 and
               tempstate[2][3] == 2 and tempstate[3][4] == 2):
            self.player2Score += 1
        if (tempstate[1][2] == 2 and tempstate[2][3] == 2 and
               tempstate[3][4] == 2 and tempstate[4][5] == 2):
            self.player2Score += 1
        if (tempstate[2][3] == 2 and tempstate[3][4] == 2 and
               tempstate[4][5] == 2 and tempstate[5][6] == 2):
            self.player2Score += 1
        if (tempstate[0][2] == 2 and tempstate[1][3] == 2 and
               tempstate[2][4] == 2 and tempstate[3][5] == 2):
            self.player2Score += 1
        if (tempstate[1][3] == 2 and tempstate[2][4] == 2 and
               tempstate[3][5] == 2 and tempstate[4][6] == 2):
            self.player2Score += 1
        if (tempstate[0][3] == 2 and tempstate[1][4] == 2 and
               tempstate[2][5] == 2 and tempstate[3][6] == 2):
            self.player2Score += 1

        if (tempstate[0][3] == 2 and tempstate[1][2] == 2 and
               tempstate[2][1] == 2 and tempstate[3][0] == 2):
            self.player2Score += 1
        if (tempstate[0][4] == 2 and tempstate[1][3] == 2 and
               tempstate[2][2] == 2 and tempstate[3][1] == 2):
            self.player2Score += 1
        if (tempstate[1][3] == 2 and tempstate[2][2] == 2 and
               tempstate[3][1] == 2 and tempstate[4][0] == 2):
            self.player2Score += 1
        if (tempstate[0][5] == 2 and tempstate[1][4] == 2 and
               tempstate[2][3] == 2 and tempstate[3][2] == 2):
            self.player2Score += 1
        if (tempstate[1][4] == 2 and tempstate[2][3] == 2 and
               tempstate[3][2] == 2 and tempstate[4][1] == 2):
            self.player2Score += 1
        if (tempstate[2][3] == 2 and tempstate[3][2] == 2 and
               tempstate[4][1] == 2 and tempstate[5][0] == 2):
            self.player2Score += 1
        if (tempstate[0][6] == 2 and tempstate[1][5] == 2 and
               tempstate[2][4] == 2 and tempstate[3][3] == 2):
            self.player2Score += 1
        if (tempstate[1][5] == 2 and tempstate[2][4] == 2 and
               tempstate[3][3] == 2 and tempstate[4][2] == 2):
            self.player2Score += 1
        if (tempstate[2][4] == 2 and tempstate[3][3] == 2 and
               tempstate[4][2] == 2 and tempstate[5][1] == 2):
            self.player2Score += 1
        if (tempstate[1][6] == 2 and tempstate[2][5] == 2 and
               tempstate[3][4] == 2 and tempstate[4][3] == 2):
            self.player2Score += 1
        if (tempstate[2][5] == 2 and tempstate[3][4] == 2 and
               tempstate[4][3] == 2 and tempstate[5][2] == 2):
            self.player2Score += 1
        if (tempstate[2][6] == 2 and tempstate[3][5] == 2 and
               tempstate[4][4] == 2 and tempstate[5][3] == 2):
            self.player2Score += 1
