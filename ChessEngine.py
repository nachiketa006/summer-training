import numpy as np

class GameState():
    def __init__(self):
        # 8X8 2D MATRIX
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], #empty
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLoc = (7,4)
        self.blackKingLoc = (0,4)
        self.checkmate = False
        self.stalemate = False
        self.currentCastlingRights = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wqs,self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.bqs)]
        
    def makeMove(self,gameMove): # Not works for castling, en passant and pawn promotion
        self.board[gameMove.startRow][gameMove.startCol] = "--"
        self.board[gameMove.endRow][gameMove.endCol] = gameMove.pieceMoved
        self.moveLog.append(gameMove)
        #swap player turns
        self.whiteToMove = not self.whiteToMove
        if gameMove.pieceMoved == "wK":
            self.whiteKingLoc = (gameMove.endRow,gameMove.endCol)
        elif gameMove.pieceMoved == "bK":
            self.blackKingLoc = (gameMove.endRow,gameMove.endCol)
        # #updating castling rights
        # self.updateCastleRights(gameMove)
        # self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wqs,self.currentCastlingRights.wks,self.currentCastlingRights.bks,self.currentCastlingRights.bqs))
        # #castle move
        # if GameMove.isCastle:
        #     if gameMove.endCol-gameMove.startCol == 2:
        #         self.board[gameMove.endRow][gameMove.endCol-1] = self.board[gameMove.endRow][gameMove.endCol+1]
        #         self.board[gameMove.endRow][gameMove.endCol+1]=='--'
        #     else:
        #         self.board[gameMove.endRow][gameMove.endCol+1]= self.board[gameMove.endRow][gameMove.endCol-2]
        #         self.board[gameMove.endRow][gameMove.endCol-2] ='--'

        
    def undoMove(self):
        if len(self.moveLog)!=0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if lastMove.pieceMoved == "wK":
                self.whiteKingLoc = (lastMove.startRow, lastMove.startCol)
            elif lastMove.pieceMoved == "bK":
                self.blackKingLoc = (lastMove.startRow, lastMove.startCol)
            self.checkmate = False
            self.stalemate = False
            #undo castling rights
            # self.castleRightsLog.pop()
            # self.currentCastlingRights = self.castleRightsLog[-1]
            # if gameMove.isCastle:
            #     if gameMove.endCol - gameMove.startCol ==2:
            #         self.board[gameMove.endRow][gameMove.endCol+1] = self.board[gameMove.endRow][gameMove.endCol-1]
            #         self.board[gameMove.endRow][gameMove.endCol-1] = '--'
            #     else:
            #         self.board[gameMove.endRow][gameMove.endCol - 2] = self.board[gameMove.endRow][gameMove.endCol+1]
            #         self.board[gameMove.endRow][gameMove.endCol + 1] = '--'



    # def updateCastleRights(self,gameMove):
    #     if gameMove.pieceMoved == 'wK' :
    #         self.currentCastlingRights.wks = False
    #         self.currentCastlingRights.wqs = False
    #     elif gameMove.pieceMoved == 'bK':
    #         self.currentCastlingRights.bks = False
    #         self.currentCastlingRights.bqs = False
    #     elif gameMove.pieceMoved =='wR':
    #         if gameMove.startRow == 7:
    #             if gameMove.startCol == 0:
    #                 self.currentCastlingRights.wqs = False
    #             elif gameMove.startCol == 7:
    #                 self.currentCastlingRights.wks = False
    #     elif gameMove.pieceMoved =='bR':
    #         if gameMove.startRow == 0:
    #             if gameMove.startCol == 0:
    #                 self.currentCastlingRights.bqs = False
    #             elif gameMove.startCol == 7:
    #                 self.currentCastlingRights.bks = False






    def cellUnderAttack(self,row,col):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

    def inCheck(self):
        if self.whiteToMove:
            return self.cellUnderAttack(self.whiteKingLoc[0],self.whiteKingLoc[1])
        else:
            return self.cellUnderAttack(self.blackKingLoc[0],self.blackKingLoc[1])
        
    def getValidMoves(self): #All moves without checks subset of POSSIBLE MOVES
        # 1. Generate All Possible Moves
        moves  = self.getAllPossibleMoves()
        # 2. For each move make the move
        for i in range(len(moves)-1,-1,-1): #Removing from a list always try to traverse it backward
            self.makeMove(moves[i])
            # 3. Generate all the Opponent's Move
            # 4. For each of the Opponent's Move, see if check on your KING
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                # 5. Remove that move from Valid Moves
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if(len(moves) == 0):
            if self.inCheck():
                self.checkmate  = True
            else:
                self.stalemate  = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        return moves
    
    def getAllPossibleMoves(self): #All moves with checks
        moves = []
        for i in range(len(self.board)): #rows
            for j in range(len(self.board[0])): #cols
                pieceColor = self.board[i][j][0]
                if(self.whiteToMove and pieceColor == "w") or (not self.whiteToMove and pieceColor == "b"):
                    piece = self.board[i][j][1]
                    if piece == 'P':
                        self.getPawnMoves(i, j, moves)
                    elif piece == 'R':
                        self.getRookMoves(i, j, moves)
                    elif piece == 'N':
                        self.getKnightMoves(i, j ,moves)
                    elif piece == 'B':
                        self.getBishopMoves(i ,j ,moves)
                    elif piece == 'K':
                        self.getKingMoves(i, j, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(i, j, moves)
        return moves

    def getPawnMoves(self,row,col,moves):
        #WHITE - start on row 6
        if self.whiteToMove:
            # 1 square upward
            if self.board[row - 1][col]== "--":
                oneUp = GameMove(self.board,(row,col),(row - 1,col))
                moves.append(oneUp)
            # 2 square upward if on row 6
            if row == 6 and self.board[row - 1][col] == "--" and self.board[row - 2][col] == "--":
                twoUp = GameMove(self.board, (row, col), (row - 2, col))
                moves.append(twoUp)
            # Diagonal take
            if col-1>=0 and self.board[row - 1][col - 1][0] == "b":
                diagUpLeft = GameMove(self.board, (row, col), (row - 1, col - 1))
                moves.append(diagUpLeft)
            if col+1<=7 and self.board[row - 1][col + 1][0] == "b":
                diagUpRight = GameMove(self.board, (row, col), (row - 1, col + 1))
                moves.append(diagUpRight)
            
        #BLACK - start on row 1
        if not self.whiteToMove:
            # 1 square downward
            if ( self.board[row+1][col]=="--"):
                oneDown = GameMove(self.board,(row,col),(row + 1,col))
                moves.append(oneDown)
            # 2 square downward if on row 1
            if ( row == 1 and self.board[row + 1][col] == "--" and self.board[row + 2][col] == "--"):
                twoDown = GameMove(self.board, (row, col), (row + 2, col))
                moves.append(twoDown)
            # Diagonal take
            if col-1>=0 and self.board[row + 1][col - 1][0]== "w":
                diagUpLeft = GameMove(self.board, (row, col), (row + 1, col - 1))
                moves.append(diagUpLeft)
            if col+1<=7 and self.board[row + 1][col + 1][0] == "w":
                diagUpRight = GameMove(self.board, (row, col), (row + 1, col + 1))
                moves.append(diagUpRight)
        
    
    def getRookMoves(self,row,col,moves):
        target = "b" if self.whiteToMove else "w"
        direction = [(1, 0), (0, -1), (0, 1), (-1, 0)]
        for dirn in direction:
            for i in range(1, 8):
                endRow = row + dirn[0] * i
                endCol = col + dirn[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if self.board[endRow][endCol] == "--":
                        rookMove = GameMove(self.board, (row, col), (endRow, endCol))
                        moves.append(rookMove)
                    elif self.board[endRow][endCol][0] == target:
                        rookMove = GameMove(self.board, (row, col), (endRow, endCol))
                        moves.append(rookMove)
                        break
                    else:
                        break
                else:
                    break
 
    def getKnightMoves(self,row,col,moves):
        me = "w" if self.whiteToMove else "b"
        direction = [(1, 2),(2,1),(-1,2),(2,-1),(1,-2),(-2,1),(-1,-2),(-2,-1)]
        for dirn in direction:
            endRow = row + dirn[0]
            endCol = col + dirn[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if self.board[endRow][endCol][0] != me:
                    bishopMove = GameMove(self.board, (row, col), (endRow, endCol))
                    moves.append(bishopMove)

    
    def getBishopMoves(self,row,col,moves):
        target = "b" if self.whiteToMove else "w"
        direction = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dirn in direction:
            for i in range(1,8):
                endRow = row + dirn[0]*i
                endCol = col + dirn[1]*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    if self.board[endRow][endCol] == "--":
                        bishopMove = GameMove(self.board,(row,col),(endRow,endCol))
                        moves.append(bishopMove)
                    elif self.board[endRow][endCol][0] == target:
                        bishopMove = GameMove(self.board, (row, col), (endRow, endCol))
                        moves.append(bishopMove)
                        break
                    else:
                        break
                else:
                    break
    
    def getKingMoves(self,row,col,moves):
        me = "w" if self.whiteToMove else "b"
        direction = [(0,1),(1,0),(0,-1),(-1,0),(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for i in range(len(direction)):
            endRow = row + direction[i][0]
            endCol = col + direction[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if self.board[endRow][endCol][0] != me:
                    kingMove = GameMove(self.board, (row, col), (endRow, endCol))
                    moves.append(kingMove)
        # self.castleMove(row,col,moves,me)
    """
    get castle moves
    """
    # def castleMove(self,row,col,moves,me):
    #     if self.inCheck():
    #         return
    #     if self.whiteToMove and self.currentCastlingRights.wks or not self.whiteToMove and self.currentCastlingRights.bks:
    #         self.kingSideCastleMoves(row,col,moves,me)
    #     if self.whiteToMove and self.currentCastlingRights.wqs or not self.whiteToMove and self.currentCastlingRights.bqs:
    #         self.queenSideCastleMoves(row,col.col, moves, me)
    # def kingSideCastleMoves(self,row,col,moves,me):
    #     if self.board[row][col+1] =='--' and self.board[row][col+2]=='--':
    #         if not self.cellUnderAttack(row,col+1) and not self.cellUnderAttack(row,col+2):
    #             moves.append(GameMove((row,col),(row,col+2),self.board, isCastle = True))
    #
    # def queenSideCastleMoves(self,row,col,moves,me):
    #     if self.board[row][col-1] =='--' and self.board[row][col-2]=='--' and self.board[row][col-3]=='--':
    #         if not self.cellUnderAttack(row,col-1) and not self.cellUnderAttack(row,col-2) and not self.cellUnderAttack(row,col-3):
    #             moves.append(GameMove((row,col),(row,col-2),self.board, isCastle = True))
    #
    #
    def getQueenMoves(self,row,col,moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)
            
class GameMove():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRank = {v:k for k,v in ranksToRows.items()}
    filesToCol = {"a":7,"b":6,"c":5,"d":4,"e":3,"f":2,"g":1,"h":0}
    colToFiles = {v: k for k, v in filesToCol.items()}
    
    def __init__(self,board,startSquare,endSquare,isCastle = False):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        # print(self.moveID)
        self.isCastle = isCastle
        
    def toChessNotation(self):
        rankFileStart = self.colToFiles[self.startCol] + self.rowsToRank[self.startRow]
        rankFileEnd = self.colToFiles[self.endCol] + self.rowsToRank[self.endRow]
        return str(rankFileStart+rankFileEnd)
    
    #OPERATOR OVERLOADING "="
    def __eq__(self,other):
        if isinstance(other,GameMove): #if other is an instance of GameMove Class
            return ((self.moveID == other.moveID))
        return False
class CastleRights:
    def __init__(self,wqs,wks,bks,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
