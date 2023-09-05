import numpy as np
import numpy as np
import random
import copy

# future : can change number of straights and take note of winner_tallies


class Board():
    winner_tally = {}
    player_order = []
    current_player = ''
    registered_player = {}
    num_straight = 4
    ai_number_of_turns = 0
    EMPTY = '0'
    AI_SYMBOL = 'R'

    def __init__(self, rows: int = 6, cols: int = 7):
        self.num_row = rows
        self.num_col = cols
        # self.winner_tally = {player: 0 for player in self.registered_player}
        self.board = self.init_board()

    def __str__(self):
        str_board = ""
        for i, row in enumerate(self.board):
            str_board += str(i) + '\t' + '\t'.join(row) + '\n'
        str_board += ' ' + '\t' + '\t'.join(str(v)
                                            for v in range(self.num_col)) + '\n'

        str_board += str(self.registered_player) + '\n'
        return str_board

    def init_board(self):
        return np.array([[self.EMPTY]*self.num_col for i in range(self.num_row)])

    def start_game(self):
        print('Hi, we are about to play {} dots'.format(self.num_straight))
        self.withAI = self.ask_if_with_ai()
        if(self.withAI):
            self.register_player('AI', self.AI_SYMBOL)

        while(not self.check_if_enough_players()):
            name = input("Enter your name: ")
            # add validation not to enable 0 as symbol & AI Symbol
            sym = input("Enter your preferred symbol: ")[0]
            self.register_player(name, sym)

        if(not self.withAI):
            print("Shuffling order of players.")
            self.set_player_order()
        else:
            self.choose_turn_of_ai()

        print('This is the order of players: ', self.get_player_order())
        self.set_current_player(self.get_player_order()[0])

        print('Game start')
        print(self.__str__())

        while(True):
            if(self.check_if_board_full()):
                print('It\'s a tie. ')
                break

            if(self.withAI and self.current_player == 'AI'):
                minmax = MinMaxTree(5, self)
                recommendedCol, evalScore = minmax.madeTree
                print("The AI putted the piece on", recommendedCol)
                self.place_player(self.AI_SYMBOL, recommendedCol)
                self.ai_number_of_turns += 1
                print(self.__str__())
            else:
                print('Current Player: ' + self.current_player)
                self.set_turn_to(self.current_player)

            if(self.check_for_winner(self.registered_player[self.current_player])):
                print('Congrats,', self.current_player, '! You won!')
                if self.current_player == 'AI':
                    print('It beat you in {} turns.'.format(
                        self.ai_number_of_turns))
                break
            else:
                next_player_index = (self.player_order.index(
                    self.current_player) + 1) % len(self.player_order)
                self.set_current_player(self.player_order[next_player_index])

        print('Game has ended')

    def ask_if_with_ai(self):
        name = input("Play with AI? Y/N \n")[0].upper()
        if(name == 'Y'):
            return True
        else:
            return False

    def choose_turn_of_ai(self):
        turn_order = int(input("Should AI play 1st or 2nd? 1/2 \n"))
        self.player_order = list(self.registered_player.keys())
        if(turn_order == 2):
            self.player_order.reverse()

    def set_turn_to(self, player: str):
        selectedCol = input('Input the col: ')
        while(not self.check_valid_input(selectedCol)):
            selectedCol = input('Input the col: ')
        self.place_player(self.registered_player[player], int(selectedCol))
        print(self.__str__())

    def set_current_player(self, player: str):
        self.current_player = player

    def set_player_order(self):
        self.player_order = list(self.registered_player.keys()).copy()
        np.random.shuffle(self.player_order)

    def get_player_order(self):
        return self.player_order

    def register_player(self, name: str, symbol: str):
        if(self.check_if_enough_players()):
            pass
        else:
            self.registered_player[name] = str(symbol)

    def check_if_enough_players(self):
        if(len(self.registered_player.keys()) == 2):
            print("Maximum number of players have been reached!")
            return True
        else:
            return False

    def place_player(self, playerSym: str, selectedCol: int):
        self.board[self.get_lastest_row(selectedCol), selectedCol] = playerSym

    def check_valid_input(self, inputtedCol: str):
        try:
            inputtedCol = int(inputtedCol)
        except ValueError:
            print('Please enter an integer')
            return False

        if(inputtedCol > self.num_col-1 or inputtedCol < 0):
            print('Invalid col, please choose between 0 to ' + self.col-1)
            return False
        if(not self.is_valid_location(inputtedCol)):
            print('Invalid col, please choose another column')
            return False

        return True

    def get_lastest_row(self, col):
        for idx in reversed(range(self.num_row)):
            if(self.board[idx][col] == self.EMPTY):
                return idx
        return -1

    def get_valid_locations(self):
        valid_locations = []

        for col in range(self.num_col):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def is_valid_location(self, col):
        latestRow = self.get_lastest_row(col)
        if(latestRow == -1):
            return False
        return self.board[latestRow][col] == self.EMPTY

    def check_if_board_full(self):
        count = 0
        for piece in self.board[0, :]:
            if(piece != self.EMPTY):
                count += 1
        return count == self.num_col

    def check_for_winner(self, playerSym: str):
        return self.check_straight_row(playerSym) or self.check_straight_col(playerSym) or self.check_diag_right(playerSym) or self.check_diag_left(playerSym)

    def check_straight_row(self, player: str):
        winningRow = player * self.num_straight
        for row in self.board:
            if winningRow in ''.join(row):
                return True
        return False

    def check_straight_col(self, player: str):
        winningCol = player * self.num_straight
        for j in range(self.num_col):
            col = ''.join(self.board[:, j])
            if winningCol in col:
                return True
        return False

    def check_diag_right(self, player: str):
        winningPattern = player * self.num_straight
        for i in range(board.num_row-board.num_straight, board.num_row):
            for j in range(self.num_col-self.num_straight+1):
                diagional = self.board[i, j] + self.board[i-1, j +
                                                          1] + self.board[i-2, j+2] + self.board[i-3, j+3]
                if (diagional == winningPattern):
                    return True
        return False

    def check_diag_left(self, player: str):
        winningPattern = player * self.num_straight
        for i in range(self.num_row-self.num_straight+1):
            for j in range(self.num_col-self.num_straight+1):
                diagional = self.board[i, j] + self.board[i+1, j +
                                                          1] + self.board[i+2, j+2] + self.board[i+3, j+3]
                if (diagional == winningPattern):
                    return True
        return False

    def get_winner_tally(self):
        return self.winner_tally


class MinMaxTree():
    def __init__(self, max_depth: int, board: Board):
        self.max_depth = max_depth
        self.board = copy.deepcopy(board)
        self.madeTree = self.minimax(
            max_depth, board, True, float('-inf'), float('inf'))

    def is_terminal_node(self, board: Board):
        opponent = self.get_opponent_sym(board.AI_SYMBOL)
        return self.winning_move(board, board.AI_SYMBOL) or self.winning_move(board, opponent) or len(board.get_valid_locations()) == 0

    # make it flexible to any
    def minimax(self, depth, boardObj: Board, isMax, alpha, beta):
        valid_locations = boardObj.get_valid_locations()
        opponent = self.get_opponent_sym(boardObj.AI_SYMBOL)
        if(depth == 0) or self.is_terminal_node(boardObj):
            if(self.is_terminal_node(boardObj)):
                if(self.winning_move(boardObj, opponent)):
                    return (None, -10000000000000)
                elif(self.winning_move(boardObj, boardObj.AI_SYMBOL)):
                    return (None, 10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(boardObj, boardObj.AI_SYMBOL))

        if(isMax):
            maxScore = float('-inf')
            column = random.choice(valid_locations)
            random.shuffle(valid_locations)

            for loc in valid_locations:
                copy_board = copy.deepcopy(boardObj)
                copy_board.place_player(boardObj.AI_SYMBOL, loc)
                new_score = self.minimax(
                    depth-1, copy_board, False, alpha, beta)[1]
                if maxScore < new_score:
                    maxScore = new_score
                    column = loc
                alpha = max(alpha, maxScore)
                if beta <= alpha:
                    break
            return column, maxScore

        else:
            minScore = float('inf')
            column = random.choice(valid_locations)
            for loc in valid_locations:
                copy_board = copy.deepcopy(boardObj)
                boardObj.place_player(opponent, loc)
                new_score = self.minimax(
                    depth-1, copy_board, True, alpha, beta)[1]
                if minScore > new_score:
                    minScore = new_score
                    column = loc
                beta = min(beta, minScore)
                if beta <= alpha:
                    break
            return column, minScore

    def winning_move(self, boardObj, playerSym):
        ROW_COUNT = boardObj.num_row
        COL_COUNT = boardObj.num_col
        board = boardObj.board

        # Check horizontal locations for win
        for c in range(COL_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == playerSym and board[r][c+1] == playerSym and board[r][c+2] == playerSym and board[r][c+3] == playerSym:
                    return True

        # Check vertical locations for win
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == playerSym and board[r+1][c] == playerSym and board[r+2][c] == playerSym and board[r+3][c] == playerSym:
                    return True

        # Check negatively sloped diaganols
        for c in range(COL_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == playerSym and board[r+1][c+1] == playerSym and board[r+2][c+2] == playerSym and board[r+3][c+3] == playerSym:
                    return True

        # Check positively sloped diaganols
        for c in range(COL_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == playerSym and board[r-1][c+1] == playerSym and board[r-2][c+2] == playerSym and board[r-3][c+3] == playerSym:
                    return True

        return False

    def score_position(self, game: Board, playerSym):
        score = 0
        ROW_COUNT = game.num_row
        COL_COUNT = game.num_col
        WIN_LENGTH = game.num_straight
        state_board = game.board

        # Score center column
        center_array = state_board[:, COL_COUNT//2]
        score += (center_array == playerSym).sum() * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = state_board[r, :]
            for c in range(COL_COUNT-3):
                window = row_array[c:c+WIN_LENGTH]
                score += self.evaluate_window(window, playerSym)

        # Score Vertical
        for c in range(COL_COUNT):
            col_array = state_board[:, c]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WIN_LENGTH]
                score += self.evaluate_window(window, playerSym)

        # Score negative sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-3):
                window = state_board[r:r+WIN_LENGTH, c:c+WIN_LENGTH]
                score += self.evaluate_window(window, playerSym)

        # Score positive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-3):
                window = state_board[r: r+3-WIN_LENGTH, c:c+WIN_LENGTH]
                score += self.evaluate_window(window, playerSym)

        return score

    def get_opponent_sym(self, playerSym):
        list_sym = list(self.board.registered_player.values())
        opp_sym = (list_sym.index(playerSym) + 1) % 2
        return list_sym[opp_sym]

    def evaluate_window(self, window, playerSym):
        empty_sym = self.board.EMPTY
        score = 0
        opponent = self.get_opponent_sym(playerSym)
        if (window == playerSym).sum() == 4:
            score += 100
        elif (window == playerSym).sum() == 3 and (window == empty_sym).sum() == 1:
            score += 10
        elif (window == playerSym).sum() == 2 and (window == empty_sym).sum() == 2:
            score += 2

        if(window.ndim == 2):
            diagCount = (np.diag(window) == playerSym).sum()
            score += diagCount * 10
            diagCountFlip = (np.diag(np.fliplr(window)) == playerSym).sum()
            score += diagCountFlip * 10

        if (window == opponent).sum() == 3 and (window == empty_sym).sum() == 1:
            score -= 150
        if (window == opponent).sum() == 2 and (window == empty_sym).sum() == 2:
            score -= 50
        return score


board = Board()
board.start_game()
