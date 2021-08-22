#######################        BOARD CLASS        ###########################
# The Board class is the data structure that holds the Connect 4 boards and the game operations

# The Connect 4 board is 7 cells wide and 6 cells tall

# The underlying data structure is a 2-d list
# The first dimension is the column; the second dimension is the row
# Note: each column ONLY contains pieces (no empty cell). Thus, the array is jagged.

# Every cell in the above list contains either a 0 or a 1. Player 1 is represented by 0 tiles, and Player
# 2 is represented by 1 tiles. Yes, this is confusing, but it helps with the efficiency of the code.
#
##############################################################################
class Board(object):

    # static class variables - shared across all instances
    HEIGHT = 6
    WIDTH = 7
    GENERATES_TRACE = False  # you may want to enable this for debugging purposes

    ########################   Constructor   ###############################
    #
    #
    #  No arguments --> Creates a brand new empty board
    #
    #  orig         --> If you pass an existing board as the orig argument,
    #                   this will create a copy of that board
    #
    #  trace        --> Constructs a board from a trace string;
    #                   to be used for debugging 
    #
    # *NOTE: orig overrides trace
    ########################################################################
    def __init__(self, orig=None, trace=None):
        if not orig is None: # copy original board
            self.board = [col.copy() for col in orig.board]
            self.numMoves = orig.numMoves
            self.prevMove = orig.prevMove
            self.state = orig.state
            if self.GENERATES_TRACE: self.trace = orig.trace
            self.turn = orig.turn
            # you may wish to copy any relevant variables here
            return

        self.board = [[] for i in range(self.WIDTH)]
        self.numMoves = 0
        self.prevMove = None
        self.state = 0
        self.turn = 0
        if self.GENERATES_TRACE: self.trace = ''
        
        if not trace is None:
            for move in trace:
                self.placeMove(int(move))

    ########################################################################
    #                           Mutations
    ########################################################################

    # Puts a piece in the appropriate column
    # Pieces are either 1 or 0 according to the current turn
    # NOTE: does NOT check if the move is valid
    def placeMove(self, column):
        piece = self.turn
        self.state += (piece + 1) * 3 ** (column*self.HEIGHT + len(self.board[column]))
        if self.GENERATES_TRACE: self.trace += str(column)
        self.board[column].append(piece)
        self.prevMove = (piece, column)
        self.numMoves += 1
        self.turn = (self.turn + 1) % 2
        
        # you may want to update any relevant variables here


    ########################################################################
    #                           Observations
    ########################################################################

    def getChild(self, col):
        ''' Returns the child board resulting from making a move in col. '''
        child = Board(self)
        child.placeMove(col)
        return child

    def getChildState(self, col):
        ''' Returns the state of the child resulting from making a move in col. '''
        piece = self.turn

        return self.state + (piece + 1) * 3 ** (col*self.HEIGHT + len(self.board[col]))
    
    def getChildTrace(self, col):
        if self.GENERATES_TRACE: return self.trace + str(col)
        else: raise RuntimeError('This Board is not tracking its move trace.')

    def getAllValidMoves(self, order=range(7)):
        ''' A generator yielding the columns for each valid possible move.
            Specify order to change the order in which columns are considered. '''
        for i in order:
            if len(self.board[i]) < self.HEIGHT:
                yield i

    ##################
    #      TODO      #
    ##################
    # Returns:
    #  None if game is not over
    #  -1 if the game is a draw
    #   0 if player 1 wins
    #   1 if player 2 wins

    # Win cases in horizontal, vertical, and two diagonals 
    # (in forms of 1-1-1-1 (total 4) , or 0-0-0-0 (total 0))
    # player 1 is zero, and player 2 is one.
    def isEnd(self):
        for x in range (0, Board.WIDTH):
            for y in range(0, Board.HEIGHT):
                # horizontal 
                try:
                    if self.board[x][y] == self.board[x+1][y] == self.board[x+2][y] == self.board[x+3][y] == 0:
                        return 0
                
                    if self.board[x][y] == self.board[x+1][y] == self.board[x+2][y] == self.board[x+3][y] == 1:
                        return 1
                except:
                    pass

                # vertical 
                try:
                    if self.board[x][y] == self.board[x][y+1] == self.board[x][y+2] == self.board[x][y+3] == 0:
                        return 0
                
                    if self.board[x][y] == self.board[x][y+1] == self.board[x][y+2] == self.board[x][y+3] == 1:
                        return 1
                except:
                    pass

                # diagonal from right to left
                try:
                    if y - 3 >= 0 and self.board[x][y] == self.board[x+1][y-1] == self.board[x+2][y-2] == self.board[x+3][y-3] == 0:
                        
                        return 0
                
                    if y - 3 >= 0 and self.board[x][y] == self.board[x+1][y-1] == self.board[x+2][y-2] == self.board[x+3][y-3] == 1:
                        return 1
                except:
                    pass

                # digonal from left to right                   
                try:
                    if self.board[x][y] == self.board[x+1][y+1] == self.board[x+2][y+2] == self.board[x+3][y+3] == 0:
                        return 0
                
                    if self.board[x][y] == self.board[x+1][y+1] == self.board[x+2][y+2] == self.board[x+3][y+3] == 1:
                        return 1
                except:
                    pass
        if self.isFull():
            return -1 # If the board is full, and no one wins, it is a draw
        else:
            return None # None if the board is not full


    ########################################################################
    #                           Utilities
    ########################################################################

    # Return true iff the board is full
    def isFull(self):
        return self.numMoves == 42

    # Prints out a visual representation of the board
    # X's are 1's and 0's are 0s
    def print(self):
        print("")
        print("+" + "---+" * self.WIDTH)
        for rowNum in range(self.HEIGHT - 1, -1, -1):
            row = "|"
            for colNum in range(self.WIDTH):
                if len(self.board[colNum]) > rowNum:
                    row += " " + ('X' if self.board[colNum][rowNum] else 'O') + " |"
                else:
                    row += "   |"
            print(row)
            print("+" + "---+" * self.WIDTH)