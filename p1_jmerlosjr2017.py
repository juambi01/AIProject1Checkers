#!/usr/bin/env python3

from easyAI import TwoPlayerGame
from easyAI.Player import Human_Player
import time

class Checkers( TwoPlayerGame ):
    """ The board positions are numbered as follows:
            [0,0] - [0,7]
              ^   X   ^
            [7,0] - [7,7]
    """

    def __init__(self, players):
        #[x,y,occupier]
        #occupier = 0-empty 1-red 2-black 3-black king 4-red king
        self.players = players
        self.board = [[a,b,0] for a in range(8) for b in range(8)]
        #initialize pieces
        for space in self.board:
            if space[0] <= 2:
                if space[0]==0 and space[1] % 2 == 1:
                    space[2] = 1
                elif space[0]==1 and space[1] % 2 == 0:
                    space[2] = 1
                elif space[0]==2 and space[1] % 2 == 1:
                    space[2] = 1
                else:
                    space[2] = 0
            elif space[0] >= 5:
                if space[0]==5 and space[1] % 2 == 0:
                    space[2] = 2
                elif space[0]==6 and space[1] % 2 == 1:
                    space[2] = 2
                elif space[0]==7 and space[1] % 2 == 0:
                    space[2] = 2
                else:
                    space[2] = 0
            else:
                space[2] = 0
        self.current_player = 2 # player 2 (black) starts.

    def possible_moves(self):
        redpiecelocations = []
        blackpiecelocations = []
        redpiecepossiblemoves = []
        blackpiecepossiblemoves = []
        for space in self.board:
            if space[2] == 1 or space[2] == 4:
                redpiecelocations.append(space)
        for space in self.board:
            if space[2] == 2 or space[2] == 3:
                blackpiecelocations.append(space)
     
        #will check a series of possible moves by verifying they exist, if they are availible they get put into a possible moves list for each player
        for piece in redpiecelocations:
            try:#try taken northeast
                takennortheast = [piece[0] + 1, piece[1] + 1, 2]
                self.board.index(takennortheast)
                possibleeat = self.board.index([piece[0] + 2, piece[1] + 2, 0])
                redpiecepossiblemoves.append([[piece], [takennortheast, possibleeat]])
            except:#index fails pass
                try:#try empty northeast
                    emptynortheast = [piece[0] + 1, piece[1] + 1, 0]
                    self.board.index(emptynortheast)
                    redpiecepossiblemoves.append([[piece], [emptynortheast, -1]])
                except:#index fails pass
                    pass

            try:#try taken northwest
                takennorthwest = [piece[0] + 1, piece[1] - 1, 2]
                self.board.index(takennorthwest)
                possibleeat = self.board.index([piece[0] + 2, piece[1] - 2, 0])
                redpiecepossiblemoves.append([[piece], [takennorthwest, possibleeat]])
            except:#index fails pass
                try:#try empty northwest
                    emptynorthwest = [piece[0] + 1, piece[1] - 1, 0]
                    self.board.index(emptynorthwest)
                    redpiecepossiblemoves.append([[piece], [emptynorthwest, -1]])
                except:#index fails pass
                    pass



        for piece in blackpiecelocations:
            try:#try taken southeast
                takensoutheast = [piece[0] - 1, piece[1] + 1, 1]
                self.board.index(takensoutheast)
                possibleeat = self.board.index([piece[0] - 2, piece[1] + 2, 0])
                blackpiecepossiblemoves.append([[piece], [takensoutheast, possibleeat]])
            except:#index fails pass
                try:#try empty southeast
                    emptysoutheast = [piece[0] - 1, piece[1] + 1, 0]
                    self.board.index(emptysoutheast)
                    blackpiecepossiblemoves.append([[piece], [emptysoutheast, -1]])
                except:#index fails pass
                    pass
            try:#try taken southwest
                takensouthwest = [piece[0] - 1, piece[1] - 1, 1]
                self.board.index(takensouthwest)
                possibleeat = self.board.index([piece[0] - 2, piece[1] - 2, 0])
                blackpiecepossiblemoves.append([[piece], [takensouthwest, possibleeat]])
            except:#index fails pass
                try:#try empty southwest
                    emptysouthwest = [piece[0] - 1, piece[1] - 1, 0]
                    self.board.index(emptysouthwest)
                    blackpiecepossiblemoves.append([[piece], [emptysouthwest, -1]])
                except:#index fails pass
                    pass

                
        nextmoveeat = []
        nextmovemove = []
        if self.current_player == 1:
            for moves in redpiecepossiblemoves:#check to see if any of the moves are eat moves, if they are force the AI to choose an eat move (this is part of the rules of checkers)
                if moves[1][0][2] == 2:
                    nextmoveeat.append(moves)
                else:
                    nextmovemove.append(moves)#if no eat moves are available choose a normal move
            if len(nextmoveeat) > 0:
                return nextmoveeat
            else:
                return nextmovemove
        else:
            for moves in blackpiecepossiblemoves:
                if moves[1][0][2] == 1:
                    nextmoveeat.append(moves)
                else:
                    nextmovemove.append(moves)
            if len(nextmoveeat) > 0:
                return nextmoveeat
            else:
                return nextmovemove

    def make_move(self, move):
        oldspace = move[0][0]
        oldspaceindex = self.board.index(oldspace)
        oldspaceupdate = [oldspace[0], oldspace[1], 0]
        newspace = move[1][0]
        newspaceindex = self.board.index(newspace)
        eatspace = move[1][1]
        self.board[oldspaceindex] = oldspaceupdate
        if eatspace != -1:
            self.board[newspaceindex] = [newspace[0], newspace[1], 0]
            boardvaleatspot = self.board[eatspace]
            self.board[eatspace] = [boardvaleatspot[0], boardvaleatspot[1], oldspace[2]]
        else:
            self.board[newspaceindex] = [newspace[0], newspace[1], oldspace[2]]
        
        
    def lose(self):
        count1pieces = 0
        count2pieces = 0
        for i in self.board:
            if self.player == 1:
                if i[2]==2 and i[0]==0:
                    #player 1 looses, enemy piece in home teritory
                    return 1
            if self.player == 2:
                if i[2]==1 and i[0]==7:
                    #player 2 looses, enemy piece in home teritory
                    return 1
            if i[2] == 1:
                count1pieces = count1pieces + 1
            
            if i[2] == 2:
                count2pieces = count2pieces + 1
        if self.player == 1:
            if count1pieces == 0:
                return 1    
        if self.player == 2:
            if count2pieces == 0:
                return 1    
        return 0

    def is_over(self):
        return (self.possible_moves() == [] or self.lose())

    def show(self):
        showboard = ""
        rownum = 0
        for space in self.board:
            if rownum != space[0]:
                showboard = showboard + "\n"
            rownum = space[0]
            showboard = showboard + str(space[2])
        print(showboard)



    def scoring(self):
        return -100 if (self.lose()) else 0
    


if __name__ == "__main__":

    from easyAI import AI_Player, Negamax
    ai_algo = Negamax(6)
    Checkers([AI_Player(ai_algo),AI_Player(ai_algo)]).play()