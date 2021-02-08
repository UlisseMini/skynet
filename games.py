class Player:
    MAX = 1
    MIN = -1

# Two player, zero sum perfect information game.
class Game():
    @classmethod
    def startpos(cls):
        raise NotImplementedError

    def make_move(self, mv):
        """
        Make a move on the board, use copy if you want a backup
        """
        raise NotImplementedError

    def legal(self) -> iter:
        """
        Return an iterator of legal moves which can be passed to make_move
        """
        raise NotImplementedError

    def result(self) -> int:
        """
        Return the result of the game, if the game is over None otherwise.
        """
        raise NotImplementedError


    def copy(self):
        """
        Return a copy of the board
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Return a pretty ascii string representing the current state of the board
        """
        raise NotImplementedError


    def encode_list(self):
        """
        Encode the current board state to a list-vector for use in nerual networks.
        """

        raise NotImplementedError


class TicTacToe(Game):
    def __init__(self, board: list, turn: Player):
        assert len(board) == 9

        self.board = board
        self.turn = turn

    @classmethod
    def startpos(cls):
        return cls([0] * 9, turn=Player.MAX)

    def make_move(self, mv):
        self.board[mv] = self.turn
        self.turn = self.turn * -1

    def legal(self) -> list:
        return (i for i in range(9) if self.board[i] == 0)

    def result(self) -> int:
        board = self.board

        for turn in [1, -1]:
            for i in range(3):
                # horizontal
                if all(board[i*3 + j] == turn for j in range(3)):
                    return turn

            # virtical
            if all(board[j+i] == turn for j in (0,3,6)):
                return turn

            # diagonals
            if all(board[i] == turn for i in (0, 4, 8)):
                return turn

            if all(board[i] == turn for i in (2, 4, 6)):
                return turn

        return None

    def copy(self):
        return TicTacToe(self.board, self.turn)

    def __str__(self):
        def tile(x):
            return {0: '_', 1: 'X', -1: 'O'}[x]

        t = [tile(x) for x in self.board]
        s = '\n'.join([' '.join(t[i:j]) for i,j in [(0,3), (3,6), (6,9)]])

        return s


    def encode_list(self):
        return [*self.board, self.turn]


# TODO: Write generic test for any implementor of Game, ie.
# gen legal moves, encoding, etc...
def test_tic():
    tic = TicTacToe.startpos()
    tic.make_move(1)
    tic.make_move(2)
    tic.make_move(4)

    assert tic.encode_list() == [0, 1, -1, 0, 1, 0, 0, 0, 0, -1]


if __name__ == '__main__':
    # run tests
    test_tic()
