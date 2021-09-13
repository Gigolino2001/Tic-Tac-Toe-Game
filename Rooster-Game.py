# ROOSTER GAME

# Player vs computer 
# 3 modes of difficulty (Easy, Normal, Hard)
# Symbols "X" and "O"
# Board 3x3
#                Column
#           |1|   |2|   |3|
#       |1|  1     2     3
# Line  |2|  4     5     6
#       |3|  7     8     9


def is_Board(board):
    if isinstance(board, tuple) and len(board) == 3:
        for subtuples in board:
            if isinstance(subtuples, tuple) and len(subtuples) == 3:
                for value in subtuples:
                    if isinstance(value, int) and value != -1 and value != 0 and value != 1:
                        return False
            else:
                return False
        return True
    else:
        return False


def is_Position(value):
    return isinstance(value,int) and value in range(1, 10)

def is_Player(value):
    return value == -1 or value == 1

def get_Column(board, value):
    if is_Board(board) and isinstance(value,int) and value in range(1,4):
        column = ()
        for subtuples in board:
            column += (subtuples[value-1],)
        return column
    else:
        raise ValueError("get_Column: argument is invalid")

def get_Line(board, value):
    if is_Board(board) and isinstance(value, int) and value in range(1, 4):
        return board[value-1]
    else:
        raise ValueError("get_Line: argument is invalid")

def get_Diagonal(board, value):
    if is_Board(board) and isinstance(value, int) and value in range(1, 3):
        diagonal = ()
        aux_value = 0
        if value == 1:
            for subtuples in board:
                diagonal += (subtuples[aux_value],)
                aux_value += 1
            return diagonal
        elif value == 2:
            for subtuples in reversed(board):
                diagonal += (subtuples[aux_value],)
                aux_value += 1
            return diagonal
    else:
        raise ValueError("get_Diagonal: argument is invalid")


def board_ToString(board):
    
    def number_ToCharacter(values):
        switcher = {
            -1: " O ",
            0: "   ",
            1: " X "
        }
        return switcher.get(values)
    
    if not is_Board(board):
        raise ValueError("board_ToString: argument is invalid")
    boardString = ""
    contline =0
    for subtuples in board:
        contslash = 0
        for values in subtuples:
            boardString += number_ToCharacter(values)
            if contslash < 2:
                boardString += "|"
                contslash += 1
        if contline < 2:
            boardString += "\n-----------\n"
            contline += 1
    return boardString


def is_FreePosition(board, value):
    
    def value_ToBool(value):
        return value == 0

    if not is_Board(board) or not is_Position(value):
        raise ValueError("is_FreePosition: argument is invalid")
    if 0 < value < 4:
        return value_ToBool(board[0][value-1])
    elif 3 < value < 7:
        return value_ToBool(board[1][value - 4])
    else:
        return value_ToBool(board[2][value - 7])

def get_FreePositions(board):
    if not is_Board(board):
        raise ValueError("get_FreePositions: argument is invalid")
    free_positions = ()
    for values in range(1,10):
        if is_FreePosition(board, values):
            free_positions += (values,)
    return free_positions

def get_Winner(board):
    if not is_Board(board):
        raise ValueError("get_Winner: argument is invalid")

    for value in range(1, 4):

        line = get_Line(board, value)
        if all(ele == line[0] for ele in line) and line[0] != 0:
            return line[0]

        column = get_Column(board, value)
        if all(ele == column[0] for ele in column) and column[0] != 0:
            return column[0]

        if value < 3:
            diagonal = get_Diagonal(board, value)
            if all(ele == diagonal[0] for ele in diagonal) and diagonal[0] != 0:
                return diagonal[0]

    return 0

def set_ChangeinBoard(board,player,position):
    if not is_Board(board) or not is_Player(player) or not is_FreePosition(board,position):
        raise ValueError("set_ChangeinBoard: argument is invalid")
    newboard = ()
    if 0 < position < 4:
        boardlst = list(board[0])
        boardlst[position-1] = player
        newboard = (tuple(boardlst),) +(board[1],) + (board[2],)
        return newboard
    elif 3 < position < 7:
        boardlst = list(board[1])
        boardlst[position-4] = player
        newboard = (board[0],) + (tuple(boardlst),) + (board[2],)
        return newboard
    else:
        boardlst = list(board[2])
        boardlst[position - 7] = player
        newboard = (board[0],) + (board[1],) + (tuple(boardlst),)
        return newboard


def set_PlayerChoice(board):
    pos= int(input("Player turn. Choose a free position: "))
    if not is_Board(board) or not is_FreePosition(board,pos):
        raise ValueError("set_PlayerChoise: argument is invalid")
    return pos


def set_ComputerChoice(board,player,mode):
    def get_CriteriaCentre(board):
        if is_FreePosition(board, 5):
            return 5
        else:
            return False
    
    def get_CriteriaEmptyCorner(board):
        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if pos in (1,3,7,9):
                return pos
        return False
    
    def get_CriteriaEmptySide(board):
        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if pos in (2,4,6,8):
                return pos
        return False

    def set_EasyChoice(board):
        pos = get_CriteriaCentre(board)
        if not pos:
            pos = get_CriteriaEmptyCorner(board)
            if not pos:
                return get_CriteriaEmptySide(board)
            else:
                return pos
        else:
            return pos

    def set_NormalChoice(board,player):
        return 0

    def set_HardChoice(board,player):
        return 0

    if not is_Board(board) or not is_Player(player) or mode not in("Easy", "Normal", "Hard"):
        raise ValueError("set_ComputerChoise: argument is invalid")
    if mode == "Easy":
       return set_EasyChoice(board)
    if mode == "Normal":
       return set_NormalChoice(board,player)
    if mode == "Hard":
       return set_HardChoice(board,player)

    return 0




player = 1
pos = 7
tab = ((1,1,1),(1,0,1),(-1,1,1))
print(set_ComputerChoice(tab,player,"Easy"))
