import chess

class Board(chess.Board):
    PIECES = {
        'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟',
        'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def stateless_fen(self):
        (position, color, castling_rights, en_passant,
            half_move, full_move) = self.fen().split()
        # TODO handle castling rights and en-passant
        return '{} {}'.format(position, color)

    def __str__(self):
        board = super().__str__()
        for char, piece in self.PIECES.items():
            board = board.replace(char, piece)
        return board

