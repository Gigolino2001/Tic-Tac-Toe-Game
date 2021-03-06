######################################################
#  Gigolino2001 -> https://github.com/Gigolino2001   #
######################################################
#               TIC TAC TOE GAME                     #
#                                                    #
#   -Player vs computer                              #
#   -2 modes of difficulty (Easy, Normal)            #
#   -Symbols "X" and "O"                             #
#   -Board 3x3                                       #
#                    Column                          #
#               |1|   |2|   |3                       #
#           |1|  1     2     3                       #
#     Line  |2|  4     5     6                       #
#           |3|  7     8     9                       #
#                                                    #
######################################################


def is_Board(board):

    """Verifies if the argument is a valid board."""

    if isinstance(board, tuple) and len(board) == 3:
        for subtuples in board:
            if isinstance(subtuples, tuple) and len(subtuples) == 3:
                for value in subtuples:
                    if (
                        isinstance(value, int)
                        and value != -1
                        and value != 0
                        and value != 1
                    ):
                        return False
            else:
                return False
        return True
    else:
        return False


def is_Position(value):

    """Verifies if the argument is a valid position."""

    return isinstance(value, int) and value in range(1, 10)


def is_Player(value):

    """Verifies if the argument is a valid player."""

    return value == -1 or value == 1


def get_Column(board, value):

    """Given board and a position returns the position's column."""

    if is_Board(board) and isinstance(value, int) and value in range(1, 4):
        column = ()
        for subtuples in board:
            column += (subtuples[value - 1],)
        return column
    else:
        raise ValueError("get_Column: argument is invalid")


def get_Line(board, value):

    """Given board and a position returns the position's line."""

    if is_Board(board) and isinstance(value, int) and value in range(1, 4):
        return board[value - 1]
    else:
        raise ValueError("get_Line: argument is invalid")


def get_Diagonal(board, value):

    """Given board and a position returns the position's diagonal."""

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


def number_ToCharacter(values):

    """Switches the code symbols to visual symbols."""

    switcher = {-1: " O ", 0: "   ", 1: " X "}
    return switcher.get(values)


def board_ToString(board):

    """Convert the code board to visual board."""

    if not is_Board(board):
        raise ValueError("board_ToString: argument is invalid")
    boardString = ""
    contline = 0
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

    """Checks if a given position is free or ocupated."""

    def value_ToBool(value):
        return value == 0

    if not is_Board(board) or not is_Position(value):
        raise ValueError("is_FreePosition: argument is invalid")
    if 0 < value < 4:
        return value_ToBool(board[0][value - 1])
    elif 3 < value < 7:
        return value_ToBool(board[1][value - 4])
    else:
        return value_ToBool(board[2][value - 7])


def get_FreePositions(board):

    """Gets all free positions from the board."""

    if not is_Board(board):
        raise ValueError("get_FreePositions: argument is invalid")
    free_positions = ()
    for values in range(1, 10):
        if is_FreePosition(board, values):
            free_positions += (values,)
    return free_positions


def get_Winner(board):

    """Gets the winner of the game."""

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


def set_ChangeinBoard(board, player, position):

    """Modifies the board after the player choose a position to play."""

    if (
        not is_Board(board)
        or not is_Player(player)
        or not is_FreePosition(board, position)
    ):
        raise ValueError("set_ChangeinBoard: argument is invalid")
    newboard = ()
    if 0 < position < 4:
        boardlst = list(board[0])
        boardlst[position - 1] = player
        newboard = (tuple(boardlst),) + (board[1],) + (board[2],)
        return newboard
    elif 3 < position < 7:
        boardlst = list(board[1])
        boardlst[position - 4] = player
        newboard = (board[0],) + (tuple(boardlst),) + (board[2],)
        return newboard
    else:
        boardlst = list(board[2])
        boardlst[position - 7] = player
        newboard = (board[0],) + (board[1],) + (tuple(boardlst),)
        return newboard


def set_PlayerChoice(board):

    """Gets the position that the player wants to play."""

    pos = int(input("Player turn. Choose a free position: "))
    if not is_Board(board) or not is_FreePosition(board, pos):
        raise ValueError("set_PlayerChoise: argument is invalid")
    return pos


def set_ComputerChoice(board, player, mode):

    """Gets the position that the Computer wants to play."""

    def get_CriterionCentre(board):

        """Criterion that plays in the middle position."""

        if is_FreePosition(board, 5):
            return 5
        else:
            return False

    def get_CriterionEmptyCorner(board):

        """Criterion that plays in a empty corner."""

        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if pos in (1, 3, 7, 9):
                return pos
        return False

    def get_CriterionEmptySide(board):

        """Criterion that plays in a empty side."""

        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if pos in (2, 4, 6, 8):
                return pos
        return False

    def get_CriterionVictory(board, player):

        """Criterion that plays to win the game."""

        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if 0 < pos < 4:
                line = get_Line(board, 1)
            elif 3 < pos < 7:
                line = get_Line(board, 2)
            else:
                line = get_Line(board, 3)
            cont = 0
            for value in line:
                if value == player:
                    cont += 1
            if cont == 2:
                return pos
        return False

    def get_CriterionBlockOpponent(board, player):

        """Criterion that block the opponent win."""

        free_positions = get_FreePositions(board)
        for pos in free_positions:
            if 0 < pos < 4:
                line = get_Line(board, 1)
            elif 3 < pos < 7:
                line = get_Line(board, 2)
            else:
                line = get_Line(board, 3)
            cont = 0
            for value in line:
                if value != player and value != 0:
                    cont += 1
            if cont == 2:
                return pos
        return False

    def get_CriterionOpponentCorner(board, player):

        """Criterion that blocks the opponent corner."""

        diagonal1 = get_Diagonal(board, 1)
        diagonal2 = get_Diagonal(board, 2)
        if diagonal1[0] == 0 and diagonal1[2] != player and diagonal1[2] != 0:
            return 1
        if diagonal2[0] == 0 and diagonal2[2] != player and diagonal2[2] != 0:
            return 7
        if diagonal1[2] == 0 and diagonal1[0] != player and diagonal1[0] != 0:
            return 9
        if diagonal2[2] == 0 and diagonal2[0] != player and diagonal2[0] != 0:
            return 3
        return False

    def set_EasyChoice(board):

        """Easy mode strategy."""

        pos = get_CriterionCentre(board)
        if not pos:
            pos = get_CriterionEmptyCorner(board)
            if not pos:
                return get_CriterionEmptySide(board)
            else:
                return pos
        else:
            return pos

    def set_NormalChoice(board, player):

        """Easy mode strategy."""

        pos = get_CriterionVictory(board, player)
        if not pos:
            pos = get_CriterionBlockOpponent(board, player)
            if not pos:
                pos = get_CriterionCentre(board)
                if not pos:
                    pos = get_CriterionOpponentCorner(board, player)
                    if not pos:
                        pos = get_CriterionEmptyCorner(board)
                        if not pos:
                            return get_CriterionEmptySide(board)
                        else:
                            return pos
                    else:
                        return pos
                else:
                    return pos
            else:
                return pos
        else:
            return pos

    if not is_Board(board) or not is_Player(player) or mode not in ("Easy", "Normal"):
        raise ValueError("set_ComputerChoise: argument is invalid")
    if mode == "Easy":
        return set_EasyChoice(board)
    if mode == "Normal":
        return set_NormalChoice(board, player)

    return 0


def set_restart():

    """Restarts the game if the player wants."""

    rr = input("Did you want to play again[yes/no]?:")
    if rr == "yes":
        symbol = input("Digit your symbol [X/O] : ")
        mode = input("Digit the mode [Easy/Normal]: ")
        if symbol not in ("X", "O") or mode not in ("Easy", "Normal"):
            raise ValueError("set_restart: argument is invalid")
        else:
            print("\n")
            game(symbol, mode)
    elif rr == "no":
        print("THANKS FOR PLAYING ;)")
        return "SUCESS"

    else:
        raise ValueError("set_restart: argument is invalid")


def game(symbol, mode):

    """Run the whole game."""

    def character_ToNumber(values):
        switcher = {"O": -1, "X": 1}
        return switcher.get(values)

    if symbol not in ("O", "X") or mode not in ("Easy", "Normal"):
        raise ValueError("game: argument is invalid")
    board = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    player = character_ToNumber(symbol)
    computer = -int(character_ToNumber(symbol))
    print("Welcome to Tic-Tac-Toe Game.\nYou play with '" + symbol + "'.")
    draw_flag = 1
    while get_FreePositions(board):
        print("Computer turn (" + mode + "):")
        board = set_ChangeinBoard(
            board, computer, set_ComputerChoice(board, computer, mode)
        )
        print(board_ToString(board))
        winner = get_Winner(board)
        if winner != 0:
            print("\nWinner:" + number_ToCharacter(winner))
            draw_flag = 0
            break
        if get_FreePositions(board):
            board = set_ChangeinBoard(board, player, set_PlayerChoice(board))
            print(board_ToString(board))
            winner = get_Winner(board)
            if winner != 0:
                print("\nWinner:" + number_ToCharacter(winner))
                draw_flag = 0
                break
        else:
            break
    if draw_flag == 1:
        print("\nDraw")
    set_restart()


# EXECUTE YOUR GAME HERE #
print(game("O", "Easy"))
