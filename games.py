class Player:
    MAX = 1
    MIN = -1

# Two player, zero sum perfect information game.
class Game():
    # The size of the vector returned from encode_list
    STATE_SIZE = None

    # How many moves there are, counting from zero
    MOVES_SIZE = None

    @classmethod
    def startpos(cls):
        raise NotImplementedError

    def make_move(self, mv: int):
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
        Return the winner of the game, 0 for TIE, None for in progress
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


    def encode_list(self) -> [float]:
        """
        Encode the current board state to a list-vector for use in nerual networks.
        """

        raise NotImplementedError


class TicTacToe(Game):
    # board + turn
    STATE_SIZE = 10
    MOVES_SIZE = 8

    def __init__(self, board: list, turn: Player):
        assert len(board) == 9

        self.board = board
        self.turn = turn

    @classmethod
    def startpos(cls):
        return cls([0] * 9, turn=Player.MAX)

    def make_move(self, mv: int):
        assert 0 <= mv <= self.MOVES_SIZE, f'move {mv} out of bounds'

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

        if all(board[i] != 0 for i in range(9)):
            return 0 # draw

        return None

    def copy(self):
        return TicTacToe(self.board.copy(), self.turn)

    def __str__(self):
        def tile(x):
            return {0: '_', 1: 'X', -1: 'O'}[x]

        t = [tile(x) for x in self.board]
        s = '\n'.join([' '.join(t[i:j]) for i,j in [(0,3), (3,6), (6,9)]])
        s += f'\nturn: {tile(self.turn)}'

        return s


    def encode_list(self):
        return [*[float(x) for x in self.board], float(self.turn)]



# generic game test method, useful for verifying the correctness
# of implemented games.
def test_game(game, n=100):
    import random
    random.seed(42)

    assert type(game.STATE_SIZE) == int

    # play random games, assert invariants
    for _ in range(n):
        g = game.startpos()
        while g.result() is None:
            enc = g.encode_list()
            assert len(enc) == game.STATE_SIZE, f'enclen {len(enc)} != want {game.STATE_SIZE}'
            assert all(type(e) == float for e in enc), f'enc {enc} contains non float'

            legal = list(g.legal())
            assert len(legal) > 0, 'game not over, we must have moves!'

            mv = random.choice(legal)

            copy = g.copy()
            g.make_move(mv)
            assert copy.encode_list() != g.encode_list(), 'copy equals board after move'



        # For movegen efficiency we want to avoid checking gameover.
        # assert len(list(g.legal())) == 0, 'game is over, but there are legal moves!'


def test_tic():
    tic = TicTacToe.startpos()
    tic.make_move(1)
    tic.make_move(2)
    tic.make_move(4)

    assert tic.encode_list() == [0, 1, -1, 0, 1, 0, 0, 0, 0, -1]


if __name__ == '__main__':
    print('running tests...')
    test_tic()
    test_game(TicTacToe)
    print('ok')
