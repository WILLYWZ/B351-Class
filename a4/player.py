# minimax got ideas from Abe Leite and worked with Mike
import math

class BasePlayer:
    def __init__(self, maxDepth):
        self.maxDepth = maxDepth

    ##################
    #      TODO #
    ##################
    # Assign integer scores to the three terminal states
    # P2_WIN_SCORE < TIE_SCORE < P1_WIN_SCORE
    # Access these with "self.TIE_SCORE", etc.
    P1_WIN_SCORE = 999999
    P2_WIN_SCORE = -999999
    TIE_SCORE = 0
    # Returns a heuristic for the board position
    # Good positions for 0 pieces should be positive and
    # good positions for 1 pieces should be negative
    # for all boards, P2_WIN_SCORE < heuristic(b) < P1_WIN_SCORE
    
    # player 1 is zero, and player 2 is one.
    def myHeuristic(self, board):
        h = 0
        for col in range(0, board.WIDTH):
            for row in range(0, board.HEIGHT):
                # horizontal
                # player 1
                try:
                    if (board.board[col][row] + board.board[col + 1][row]) == 0: 
                        h += 10
                    if (board.board[col][row] + board.board[col + 1][row] + board.board[col + 2][row]) == 0: 
                        h += 100
                    if (board[col][row] + board.board[col + 1][row] + board.board[col + 2][row] + board.board[col + 3][row]) == 0: 
                        h += 10000
                except:
                    pass

                # player 2
                try:
                    if (board.board[col][row] + board.board[col + 1][row]) == 2: 
                        h -= 10
                    if (board.board[col][row] + board.board[col + 1][row] + board.board[col + 2][row]) == 3: 
                        h -= 100
                    if (board.board[col][row] + board.board[col + 1][row] + board.board[col + 2][row] + board.board[col + 3][row]) == 4: 
                        h -= 10000
                except:
                    pass


                # vertical
                # player 1
                try:
                    if (board.board[col][row] + board.board[col][row + 1]) == 0: 
                        h += 10
                    if (board.board[col][row] + board.board[col][row + 1] + board.board[col][row + 2]) == 0: 
                        h += 100
                    if (board.board[col][row] + board.board[col][row + 1] + board.board[col][row + 2] + board.board[col][row + 3]) == 0: 
                        h += 10000
                except:
                    pass

                # player 2
                try:
                    if (board.board[col][row] + board.board[col][row + 1]) == 2: 
                        h -= 10
                    if (board.board[col][row] + board.board[col][row + 1] + board.board[col][row + 2]) == 3: 
                        h -= 100
                    if (board.board[col][row] + board.board[col][row + 1] + board.board[col][row + 2] + board.board[col][row + 3]) == 4: 
                        h -= 10000
                except:
                    pass


                # diagonal from right to left
                # player 1
                try:
                    if (board.board[col][row] + board.board[col + 1][row - 1]) == 0: 
                        h += 10
                    if (board.board[col][row] + board.board[col + 1][row - 1] + board.board[col + 2][row - 2]) == 0: 
                        h += 100
                    if (board.board[col][row] + board.board[col + 1][row - 1] + board.board[col + 2][row - 2] + board[col + 3][row - 3]) == 0:
                        h += 10000
                except:
                    pass
                # player 2
                try:
                    if (board.board[col][row] + board.board[col + 1][row - 1]) == 2: 
                        h -= 10
                    if (board.board[col][row] + board.board[col + 1][row - 1] + board.board[col + 2][row - 2]) == 3: 
                        h -= 100
                    if (board.board[col][row] + board.board[col + 1][row - 1] + board.board[col + 2][row - 2] + board.board[col + 3][row - 3]) == 4: 
                        h -= 10000
                except IndexError:
                    pass

                # digonal from left to right
                # player 1
                try:
                    if (board.board[col][row] + board.board[col + 1][row + 1]) == 0:
                        h += 10
                    if (board.board[col][row] + board.board[col + 1][row + 1] + board.board[col + 2][row + 2]) == 0:
                        h += 100
                    if (board.board[col][row] + board.board[col + 1][row + 1] + board.board[col + 2][row + 2] + board.board[col + 3][row + 3]) == 0:
                        h += 10000
                except:
                    pass
                # player 2
                try:
                    if (board.board[col][row] + board.board[col + 1][row + 1]) == 2:
                        h -= 10
                    if (board.board[col][row] + board.board[col + 1][row + 1] + board.board[col + 2][row + 2]) == 4:
                        h -= 100
                    if (board.board[col][row] + board.board[col + 1][row + 1] + board.board[col + 2][row + 2] + board.board[col + 3][row + 3]) == 4:
                        h -= 10000
                except:
                    pass
        return h

class ManualPlayer(BasePlayer):
    def __init__(self, maxDepth=None):
        BasePlayer.__init__(self, maxDepth)

    def findMove(self, board):
        opts = " "
        for c in range(board.WIDTH):
            opts += " " + (str(c + 1) if len(board.board[c]) < board.HEIGHT else ' ') + "  "
        print(opts)

        while True:
            col = input("Place a " + ('O' if board.turn == 0 else 'X') + " in column: ")
            try: col = int(col) - 1
            except ValueError: continue
            if col >= 0 and col < board.WIDTH and len(board.board[col]) < board.HEIGHT:
                return col


class PlayerMM(BasePlayer):
    ##################
    #      TODO #
    ##################
    # performs minimax on board with depth.
    # returns the best move and best score as a tuple

    def minimax(self, board, depth):
        if board.isEnd() == -1:
            return None, self.TIE_SCORE
        if board.isEnd() == 0:
            return None, self.P1_WIN_SCORE
        if (board.isEnd() == 1):
            return None, self.P2_WIN_SCORE
        if depth == 0:
            return None, self.myHeuristic(board)
        
        BestMove = None
        BestScore = None
        
        if depth > 0:
            for move in board.getAllValidMoves():
                score = self.minimax(board.getChild(move), depth - 1)[1]
                if board.turn == 0:
                    if BestScore == None:
                        BestScore = score
                    if score != None:
                        if score > BestScore:
                            BestScore = score
                            BestMove = move

                if board.turn == 1:
                    if BestScore == None:
                        BestScore = score
                    if score != None:
                        if score < BestScore:
                            BestScore = score
                            BestMove = move

        return BestMove, BestScore



    def findMove(self, board):
        move, score = self.minimax(board, self.maxDepth)
        return move

class PlayerAB(BasePlayer):
    ##################
    #      TODO #
    ##################
    # performs minimax with alpha-beta pruning on board with depth.
    # alpha represents the score of max's current strategy
    # beta represents the score of min's current strategy
    # in a cutoff situation, return the score that resulted in the cutoff
    # returns the best move and best score as a tuple
    def alphaBeta(self, alpha, beta, board, depth):
        if board.isEnd() == -1:
            return None, self.TIE_SCORE
        if board.isEnd() == 0:
            return None, self.P1_WIN_SCORE
        if (board.isEnd() == 1):
            return None, self.P2_WIN_SCORE
        if depth == 0:
            return None, self.myHeuristic(board)
        
        BestMove = None
        BestScore = None
        
        if board.turn == 0:
            BestScore = -math.inf
            for move in board.getAllValidMoves():
                score = self.alphaBeta(alpha, beta, board.getChild(move), depth - 1)[1]
                if BestScore == None:
                    BestScore = score
                if score != None:
                    if score > BestScore:
                        BestScore = score
                        BestMove = move
                    if score > alpha:
                        alpha = score
                    if alpha >= beta:
                        return None, score
            return BestMove, BestScore

        if board.turn == 1:
            BestScore = math.inf
            for move in board.getAllValidMoves():
                score = self.alphaBeta(alpha, beta, board.getChild(move), depth - 1)[1]
                if score != None:
                    if score < BestScore:
                        BestScore = score
                        BestMove = move

                    if score < beta:
                        beta = score
                    if alpha >= beta:
                        return None, score
            return BestMove, BestScore


    def findMove(self, board):
        move, score = self.alphaBeta(-math.inf, math.inf, board, self.maxDepth)
        return move

class PlayerDP(PlayerAB):
    ''' A version of PlayerAB that implements dynamic programming
        to cache values for its heuristic function, improving performance. '''
    def __init__(self, maxDepth):
        PlayerAB.__init__(self, maxDepth)

        self.resolved = {}

    ##################
    #      TODO #
    ##################
    # if a saved heuristic value exists in self.resolved for board.state,
    # returns that value
    # otherwise, uses BasePlayer.myHeuristic to get a heuristic value and saves
    # it under board.state
    def myHeuristic(self, board):
        if board.state in self.resolved:
            return self.resolved[board.state]
        else:
            self.resolved[board.state] = BasePlayer.myHeuristic(self, board)
            return self.resolved[board.state]
        


#######################################################
###########Example Subclass for Testing
#######################################################

# This will inherit your findMove from above, but will override the heuristic
# function with
# a new one; you can swap out the type of player by changing X in "class
# TestPlayer(X):"
class TestPlayer(BasePlayer):
    # define your new heuristic here
    def myHeurisitic(self):
        pass