import evolveyourchess as eyc
import chess
import collections

# see https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation#Definition
FEN = collections.namedtuple('FEN', [
    'board', 'color', 'castling_rights', 'en_passant', 'half_move', 'full_move'])

class Board(chess.Board):
    PIECES = {
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙'}

    def __init__(self, fen=None, chess960=False):
        if fen is None:
            fen = chess.STARTING_FEN
        elif type(fen) == FEN:
            fen = ' '.join(fen)
        elif type(fen) == eyc.BoardColor:
            fen = ' '.join(eyc.fake_position(fen))
        try:
            super().__init__(fen, chess960=chess960)
        except Exception:
            print(type(fen), fen)
            0/0

    def FEN(self):
        return FEN(*self.fen().split())

    def __str__(self):
        board = super().__str__()
        for char, piece in self.PIECES.items():
            board = board.replace(char, piece)
        return board

